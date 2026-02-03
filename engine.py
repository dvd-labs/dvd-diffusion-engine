import torch
import os
import requests
import re
import json
from datetime import datetime
from tqdm import tqdm
from PIL import Image, PngImagePlugin
from io import BytesIO
from diffusers import StableDiffusionXLPipeline, DPMSolverMultistepScheduler
from compel import Compel, ReturnedEmbeddingsType

class DvdEngine:
    def __init__(self, model_id="1759168", api_token=None):
        # 1. Configuración de rutas
        self.base_path = "/content/dvd-diffusion-engine"
        self.models_path = os.path.join(self.base_path, "models")
        self.outputs_path = os.path.join(self.base_path, "outputs")
        os.makedirs(self.models_path, exist_ok=True)
        os.makedirs(self.outputs_path, exist_ok=True)

        # 2. Construcción de la URL con Token
        self.model_url = f"https://civitai.com/api/download/models/{model_id}?type=Model&format=SafeTensor"
        if api_token:
            self.model_url += f"&token={api_token}"
        
        self.model_filename = self._get_remote_filename()
        self.model_local_path = os.path.join(self.models_path, self.model_filename)

        if not os.path.exists(self.model_local_path):
            self._download_model()

        # 3. Carga del Modelo
        print(f"[*] Cargando {self.model_filename} en GPU...")
        self.pipe = StableDiffusionXLPipeline.from_single_file(
            self.model_local_path,
            torch_dtype=torch.float16,
            use_safetensors=True,
            low_cpu_mem_usage=True
        ).to("cuda")

        self.pipe.scheduler = DPMSolverMultistepScheduler.from_config(
            self.pipe.scheduler.config,
            use_karras_sigmas=True,
            algorithm_type="sde-dpmsolver++"
        )
        
        self.pipe.enable_attention_slicing()
        self.pipe.enable_vae_tiling()
        self.pipe.enable_vae_slicing()

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
                    if len(fname) > 0:
                        return fname[0].strip('"; ')
        except Exception as e:
            print(f"[!] Error al identificar el nombre (revisa tu token): {e}")
        return "modelo_civitai.safetensors"

    def _download_model(self):
        print(f"[!] Iniciando descarga segura: {self.model_filename}")
        response = requests.get(self.model_url, stream=True)
        total_size = int(response.headers.get('content-length', 0))
        progress_bar = tqdm(total=total_size, unit='iB', unit_scale=True, desc="Descargando SDXL")
        with open(self.model_local_path, 'wb') as f:
            for data in response.iter_content(chunk_size=1024 * 1024):
                progress_bar.update(len(data))
                f.write(data)
        progress_bar.close()

    def generar(self, prompt, neg_prompt="low quality, blurry, distorted, canvas", steps=15, width=1024, height=1024, cfg=7.5, seed=None):
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        save_path = os.path.join(self.outputs_path, f"dvd_{timestamp}.png")
        
        if seed is None:
            seed = torch.randint(0, 2**32, (1,)).item()
        
        generator = torch.Generator(device="cuda").manual_seed(seed)
        
        print(f"[*] Renderizando: {width}x{height} | Seed: {seed} | CFG: {cfg}")
        
        conditioning, pooled = self.compel(prompt)
        neg_conditioning, neg_pooled = self.compel(neg_prompt)
        [conditioning, neg_conditioning] = self.compel.pad_conditioning_tensors_to_same_length([conditioning, neg_conditioning])

        with torch.inference_mode():
            image = self.pipe(
                prompt_embeds=conditioning,
                pooled_prompt_embeds=pooled,
                negative_prompt_embeds=neg_conditioning,
                negative_pooled_prompt_embeds=neg_pooled,
                num_inference_steps=steps,
                guidance_scale=cfg,
                width=width,
                height=height,
                generator=generator
            ).images[0]
            
        metadata = PngImagePlugin.PngInfo()
        metadata.add_text("Prompt", prompt)
        metadata.add_text("Negative Prompt", neg_prompt)
        metadata.add_text("Seed", str(seed))
        metadata.add_text("Model", self.model_filename)
        metadata.add_text("CFG scale", str(cfg))
        metadata.add_text("Steps", str(steps))
        
        image.save(save_path, pnginfo=metadata)
        print(f"[+] Guardado con metadatos: {save_path}")
        return image
