import torch
import os
import requests
import re
from datetime import datetime
from tqdm import tqdm
from diffusers import StableDiffusionXLPipeline, DPMSolverMultistepScheduler
from compel import Compel, ReturnedEmbeddingsType

class DvdEngine:
    def __init__(self, model_id="1759168"):
        # 1. Configuración de rutas
        self.base_path = "/content/dvd-diffusion-engine"
        self.models_path = os.path.join(self.base_path, "models")
        self.outputs_path = os.path.join(self.base_path, "outputs")
        os.makedirs(self.models_path, exist_ok=True)
        os.makedirs(self.outputs_path, exist_ok=True)

        # 2. Identificación y descarga
        self.model_url = f"https://civitai.com/api/download/models/{model_id}?type=Model&format=SafeTensor&size=full&fp=fp16"
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

        # --- AQUÍ VA EL SAMPLER DPM (Dentro del __init__) ---
        self.pipe.scheduler = DPMSolverMultistepScheduler.from_config(
            self.pipe.scheduler.config,
            use_karras_sigmas=True,
            algorithm_type="sde-dpmsolver++"
        )
        
        # Optimizaciones de memoria (Cruciales para evitar el crash)
        self.pipe.enable_attention_slicing()
        self.pipe.enable_vae_tiling()  # <--- ESTA SALVA TU SESIÓN
        self.pipe.enable_vae_slicing() # <--- ESTA REFUERZA LA SEGURIDAD

        # 4. Inicialización de Compel para SDXL
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
            print(f"[!] Error al identificar el nombre: {e}")
        return "model_desconocido.safetensors"

    def _download_model(self):
        print(f"[!] Iniciando descarga: {self.model_filename}")
        response = requests.get(self.model_url, stream=True)
        total_size = int(response.headers.get('content-length', 0))
        progress_bar = tqdm(total=total_size, unit='iB', unit_scale=True, desc="Descargando SDXL")
        
            with open(self.model_local_path, 'wb') as f:
            for data in response.iter_content(chunk_size=1024 * 1024):
                progress_bar.update(len(data))
                f.write(data)
        progress_bar.close()

    def generar(self, prompt, neg_prompt="low quality, blurry, distorted, canvas", steps=15, width=1024, height=1024, cfg=7.5):
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        save_path = os.path.join(self.outputs_path, f"dvd_{timestamp}.png")
        
        print(f"[*] Renderizando: {width}x{height} | Pasos: {steps} | CFG: {cfg}")
        
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
                guidance_scale=cfg, # Ahora es una variable
                width=width,
                height=height
            ).images[0]
            
        image.save(save_path)
        print(f"[+] Resultado guardado: {save_path}")
        return image
