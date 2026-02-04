import torch, os, requests, re, json, cv2
import numpy as np
from datetime import datetime
from tqdm import tqdm
from PIL import Image, PngImagePlugin
from io import BytesIO
from diffusers import StableDiffusionXLPipeline, DPMSolverMultistepScheduler, StableDiffusionXLImg2ImgPipeline # <-- Añade este último
from compel import Compel, ReturnedEmbeddingsType
from ultralytics import YOLO

class DvdEngine:
    def __init__(self, model_id="1759168", api_token=None):
        self.base_path = "/content/dvd-diffusion-engine"
        self.models_path = os.path.join(self.base_path, "models")
        self.outputs_path = os.path.join(self.base_path, "outputs")
        os.makedirs(self.models_path, exist_ok=True)
        os.makedirs(self.outputs_path, exist_ok=True)

        # 1. Gestión de Pesos de SDXL
        self.model_url = f"https://civitai.com/api/download/models/{model_id}?type=Model&format=SafeTensor"
        if api_token: self.model_url += f"&token={api_token}"
        self.model_filename = self._get_remote_filename()
        self.model_local_path = os.path.join(self.models_path, self.model_filename)
        if not os.path.exists(self.model_local_path): self._download_file(self.model_url, self.model_local_path, "Modelo SDXL")

        # 2. Gestión de Pesos del Adetailer (FIX: Descarga Manual)
        face_model_url = "https://huggingface.co/Bingsu/adetailer/resolve/main/face_yolov8n.pt"
        self.face_model_path = os.path.join(self.models_path, "face_yolov8n.pt")
        if not os.path.exists(self.face_model_path):
            self._download_file(face_model_url, self.face_model_path, "Detector de Rostros")

        # 3. Carga de Detectores e IA
        print(f"[*] Inicializando DvdEngine con {self.model_filename}...")
        self.face_detector = YOLO(self.face_model_path) # Cargamos desde ruta local garantizada
        
        self.pipe = StableDiffusionXLPipeline.from_single_file(
            self.model_local_path, torch_dtype=torch.float16, use_safetensors=True
        ).to("cuda")

        # Optimizaciones Fooocus
        self.pipe.enable_freeu(s1=0.99, s2=0.95, b1=1.01, b2=1.02) 
        self.pipe.vae.enable_tiling()
        self.pipe.vae.enable_slicing()
        self.pipe.scheduler = DPMSolverMultistepScheduler.from_config(
            self.pipe.scheduler.config, use_karras_sigmas=True, algorithm_type="dpmsolver++"
        )
        self.pipe.enable_attention_slicing()

        # 4. Procesador de Prompts
        self.compel = Compel(
            tokenizer=[self.pipe.tokenizer, self.pipe.tokenizer_2],
            text_encoder=[self.pipe.text_encoder, self.pipe.text_encoder_2],
            returned_embeddings_type=ReturnedEmbeddingsType.PENULTIMATE_HIDDEN_STATES_NON_NORMALIZED,
            requires_pooled=[False, True]
        )

    def _get_remote_filename(self):
        try:
            with requests.get(self.model_url, stream=True, allow_redirects=True) as r:
                cd = r.headers.get('content-disposition')
                if cd:
                    fname = re.findall(r'filename\*?=(?:utf-8\'\')?(.+)', cd)
                    if len(fname) > 0: return fname[0].strip('"; ')
        except: pass
        return "modelo_dvd_labs.safetensors"

    def _download_file(self, url, path, desc):
        response = requests.get(url, stream=True)
        total_size = int(response.headers.get('content-length', 0))
        pbar = tqdm(total=total_size, unit='iB', unit_scale=True, desc=f"Descargando {desc}")
        with open(path, 'wb') as f:
            for data in response.iter_content(chunk_size=1024 * 1024):
                pbar.update(len(data)); f.write(data)
        pbar.close()

    def slerp(self, v0, v1, t):
        v0_norm, v1_norm = v0 / torch.norm(v0), v1 / torch.norm(v1)
        dot = torch.sum(v0_norm * v1_norm)
        if dot > 0.9995: return (1.0 - t) * v0 + t * v1
        omega = torch.acos(dot); so = torch.sin(omega)
        return (torch.sin((1.0 - t) * omega) / so) * v0 + (torch.sin(t * omega) / so) * v1

    def aplicar_adetailer(self, image, prompt, neg_prompt, strength=0.35):
        from PIL import ImageFilter, ImageOps
        
        cv_img = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)
        results = self.face_detector(cv_img, conf=0.3)
        if not results[0].boxes: return image

        # Cargamos el motor de cirugía
        img2img = StableDiffusionXLImg2ImgPipeline(
            vae=self.pipe.vae, text_encoder=self.pipe.text_encoder, 
            text_encoder_2=self.pipe.text_encoder_2, tokenizer=self.pipe.tokenizer, 
            tokenizer_2=self.pipe.tokenizer_2, unet=self.pipe.unet, scheduler=self.pipe.scheduler
        )

        final_image = image.copy()
        for box in results[0].boxes.xyxy:
            x1, y1, x2, y2 = map(int, box)
            w, h = x2 - x1, y2 - y1
            cx, cy = x1 + w//2, y1 + h//2
            side = int(max(w, h) * 1.5)
            nx1, ny1 = max(0, cx - side//2), max(0, cy - side//2)
            nx2, ny2 = min(image.width, nx1 + side), min(image.height, ny1 + side)
            
            face_crop = image.crop((nx1, ny1, nx2, ny2)).resize((768, 768))
            
            # Procesamiento con Compel (v6.5)
            c_ade, p_ade = self.compel(prompt)
            nc_ade, np_ade = self.compel(neg_prompt)
            [c_ade, nc_ade] = self.compel.pad_conditioning_tensors_to_same_length([c_ade, nc_ade])
            
            with torch.inference_mode():
                refined_face = img2img(
                    prompt_embeds=c_ade, pooled_prompt_embeds=p_ade,
                    negative_prompt_embeds=nc_ade, negative_pooled_prompt_embeds=np_ade,
                    image=face_crop, strength=strength, guidance_scale=5.0, num_inference_steps=20
                ).images[0]
            
            refined_face = refined_face.resize((nx2 - nx1, ny2 - ny1))

            # --- CORRECCIÓN DE MÁSCARA (FEATHERING REAL) ---
            # 1. Crear máscara negra (transparente)
            mask = Image.new("L", refined_face.size, 0)
            # 2. Crear un área blanca central más pequeña que el recorte
            # Dejamos un margen de 20px para que el desenfoque tenga espacio
            border = 20
            inner_w, inner_h = refined_face.size[0] - (border * 2), refined_face.size[1] - (border * 2)
            draw_mask = Image.new("L", (inner_w, inner_h), 255)
            # 3. Pegamos el centro blanco sobre el fondo negro
            mask.paste(draw_mask, (border, border))
            # 4. Aplicamos un desenfoque pesado para crear el degradado
            mask = mask.filter(ImageFilter.GaussianBlur(radius=15))
            
            # 5. Pegado final usando la máscara de degradado
            final_image.paste(refined_face, (nx1, ny1), mask)
            
        return final_image
        
    def generar(self, prompt, neg_prompt="low quality", steps=15, width=1024, height=1024, cfg=7.5, seed=None, var_seed=None, var_strength=0.0):
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        save_path = os.path.join(self.outputs_path, f"dvd_{timestamp}.png")
        if seed is None: seed = torch.randint(0, 2**32, (1,)).item()
        generator = torch.Generator(device="cuda").manual_seed(seed)
        shape = (1, self.pipe.unet.config.in_channels, height // 8, width // 8)
        latents = torch.randn(shape, generator=generator, device="cuda", dtype=torch.float16)
        if var_strength > 0 and var_seed is not None:
            var_generator = torch.Generator(device="cuda").manual_seed(var_seed)
            var_latents = torch.randn(shape, generator=var_generator, device="cuda", dtype=torch.float16)
            latents = self.slerp(latents, var_latents, var_strength)
        c, p = self.compel(prompt)
        nc, np_ = self.compel(neg_prompt)
        [c, nc] = self.compel.pad_conditioning_tensors_to_same_length([c, nc])
        with torch.inference_mode():
            image = self.pipe(
                prompt_embeds=c, pooled_prompt_embeds=p,
                negative_prompt_embeds=nc, negative_pooled_prompt_embeds=np_,
                num_inference_steps=steps, guidance_scale=cfg,
                width=width, height=height, latents=latents, clip_skip=2 
            ).images[0]
        meta = PngImagePlugin.PngInfo()
        meta.add_text("Prompt", prompt); meta.add_text("Negative Prompt", neg_prompt)
        meta.add_text("Seed", str(seed)); meta.add_text("CFG scale", str(cfg)); meta.add_text("Steps", str(steps))
        image.save(save_path, pnginfo=meta)
        return image, meta, save_path
