import torch
import os
import requests
from datetime import datetime
from tqdm import tqdm # Importamos la barra de progreso
from diffusers import StableDiffusionXLPipeline, EulerAncestralDiscreteScheduler

class DvdEngine:
    def __init__(self):
        self.base_path = "/content/dvd-diffusion-engine"
        self.models_path = os.path.join(self.base_path, "models")
        self.outputs_path = os.path.join(self.base_path, "outputs")
        self.model_local_path = os.path.join(self.models_path, "dvd_default_model.safetensors")
        self.model_url = "https://civitai.com/api/download/models/1759168?type=Model&format=SafeTensor&size=full&fp=fp16"

        os.makedirs(self.models_path, exist_ok=True)
        os.makedirs(self.outputs_path, exist_ok=True)

        if not os.path.exists(self.model_local_path):
            self._download_model()

        print(f"[*] Cargando modelo en GPU...")
        self.pipe = StableDiffusionXLPipeline.from_single_file(
            self.model_local_path,
            torch_dtype=torch.float16,
            use_safetensors=True,
            low_cpu_mem_usage=True
        ).to("cuda")
        
        self.pipe.enable_attention_slicing()
        self.pipe.scheduler = EulerAncestralDiscreteScheduler.from_config(self.pipe.scheduler.config)

    def _download_model(self):
        print(f"[!] Iniciando descarga del modelo de Civitai...")
        response = requests.get(self.model_url, stream=True)
        total_size = int(response.headers.get('content-length', 0))
        
        # Configuración de la barra estilo "dvd-labs"
        progress_bar = tqdm(total=total_size, unit='iB', unit_scale=True, desc="Descargando SDXL")
        
        with open(self.model_local_path, 'wb') as f:
            for data in response.iter_content(chunk_size=1024 * 1024): # Bloques de 1MB
                progress_bar.update(len(data))
                f.write(data)
        progress_bar.close()
        
        if total_size != 0 and progress_bar.n != total_size:
            print("ERROR: La descarga no se completó correctamente.")
        else:
            print(f"[+] Modelo guardado en: {self.model_local_path}")

    def generar(self, prompt, neg_prompt="low quality, blurry, distorted", steps=25):
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        save_path = os.path.join(self.outputs_path, f"dvd_{timestamp}.png")
        
        print(f"[*] Generando: {prompt}")
        with torch.inference_mode():
            image = self.pipe(
                prompt=prompt,
                negative_prompt=neg_prompt,
                num_inference_steps=steps,
                guidance_scale=7.0
            ).images[0]
            
        image.save(save_path)
        print(f"[+] Guardada en: {save_path}")
        return image
