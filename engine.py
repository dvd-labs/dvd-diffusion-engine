import torch
import os
import requests
from datetime import datetime
from diffusers import StableDiffusionXLPipeline, EulerAncestralDiscreteScheduler

class DvdEngine:
    def __init__(self):
        # 1. Rutas y Configuración del Modelo
        self.base_path = "/content/dvd-diffusion-engine"
        self.models_path = os.path.join(self.base_path, "models")
        self.outputs_path = os.path.join(self.base_path, "outputs")
        
        # Nombre que le daremos al archivo local
        self.model_filename = "dvd_default_model.safetensors"
        self.model_local_path = os.path.join(self.models_path, self.model_filename)
        
        # Tu enlace de Civitai
        self.model_url = "https://civitai.com/api/download/models/1759168?type=Model&format=SafeTensor&size=full&fp=fp16"

        # 2. Crear carpetas
        os.makedirs(self.models_path, exist_ok=True)
        os.makedirs(self.outputs_path, exist_ok=True)

        # 3. Descarga Automática (Solo la primera vez)
        if not os.path.exists(self.model_local_path):
            self._download_model()

        # 4. Carga del Modelo (Modo High VRAM para Colab)
        print(f"[*] Cargando modelo desde archivo local: {self.model_filename}")
        self.pipe = StableDiffusionXLPipeline.from_single_file(
            self.model_local_path,
            torch_dtype=torch.float16,
            variant="fp16",
            use_safetensors=True,
            low_cpu_mem_usage=True
        ).to("cuda")
        
        self.pipe.enable_attention_slicing()
        self.pipe.scheduler = EulerAncestralDiscreteScheduler.from_config(self.pipe.scheduler.config)

    def _download_model(self):
        print(f"[!] Modelo no encontrado. Descargando desde Civitai... (Esto puede tardar unos minutos)")
        response = requests.get(self.model_url, stream=True)
        response.raise_for_status()
        
        with open(self.model_local_path, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)
        print(f"[+] Descarga completada: {self.model_local_path}")

    def generar(self, prompt, neg_prompt="low quality, blurry, distorted", steps=25):
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"dvd_{timestamp}.png"
        save_path = os.path.join(self.outputs_path, filename)
        
        print(f"[*] Generando: {prompt}")
        with torch.inference_mode():
            image = self.pipe(
                prompt=prompt,
                negative_prompt=neg_prompt,
                num_inference_steps=steps,
                guidance_scale=7.0
            ).images[0]
            
        image.save(save_path)
        print(f"[+] Imagen guardada en: {save_path}")
        return image
