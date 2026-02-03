import torch
import os
import requests
import re
from datetime import datetime
from tqdm import tqdm
from diffusers import StableDiffusionXLPipeline, EulerAncestralDiscreteScheduler

class DvdEngine:
    def __init__(self, model_id="1759168"):
        # 1. Configuración de rutas
        self.base_path = "/content/dvd-diffusion-engine"
        self.models_path = os.path.join(self.base_path, "models")
        self.outputs_path = os.path.join(self.base_path, "outputs")
        os.makedirs(self.models_path, exist_ok=True)
        os.makedirs(self.outputs_path, exist_ok=True)

        # 2. Construcción de la URL dinámica
        self.model_url = f"https://civitai.com/api/download/models/{model_id}?type=Model&format=SafeTensor&size=full&fp=fp16"

        # 3. Obtener el nombre original del archivo desde el servidor
        self.model_filename = self._get_remote_filename()
        self.model_local_path = os.path.join(self.models_path, self.model_filename)

        # 4. Descarga si no existe
        if not os.path.exists(self.model_local_path):
            self._download_model()

        # 5. Carga del modelo
        print(f"[*] Cargando modelo: {self.model_filename}")
        self.pipe = StableDiffusionXLPipeline.from_single_file(
            self.model_local_path,
            torch_dtype=torch.float16,
            use_safetensors=True,
            low_cpu_mem_usage=True
        ).to("cuda")
        
        self.pipe.enable_attention_slicing()
        self.pipe.scheduler = EulerAncestralDiscreteScheduler.from_config(self.pipe.scheduler.config)

    def _get_remote_filename(self):
        # Hacemos una petición HEAD para no bajar el archivo, solo leer los encabezados
        response = requests.head(self.model_url, allow_redirects=True)
        cd = response.headers.get('content-disposition')
        if cd:
            # Extraemos el nombre que viene después de 'filename='
            fname = re.findall('filename=(.+)', cd)
            if len(fname) > 0:
                return fname[0].strip('"')
        return "model_desconocido.safetensors"

    def _download_model(self):
        print(f"[!] Identificado: {self.model_filename}. Iniciando descarga...")
        response = requests.get(self.model_url, stream=True)
        total_size = int(response.headers.get('content-length', 0))
        
        progress_bar = tqdm(total=total_size, unit='iB', unit_scale=True, desc="Descargando SDXL")
        
        with open(self.model_local_path, 'wb') as f:
            for data in response.iter_content(chunk_size=1024 * 1024):
                progress_bar.update(len(data))
                f.write(data)
        progress_bar.close()
        print(f"[+] Guardado correctamente como: {self.model_filename}")

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
        print(f"[+] Imagen guardada en: {save_path}")
        return image
