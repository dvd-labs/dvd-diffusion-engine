import torch
import os
import requests
import re
from datetime import datetime
from tqdm import tqdm
from diffusers import StableDiffusionXLPipeline, EulerAncestralDiscreteScheduler

class DvdEngine:
    def __init__(self, model_id="1759168"):
        # 1. Rutas Operativas
        self.base_path = "/content/dvd-diffusion-engine"
        self.models_path = os.path.join(self.base_path, "models")
        self.outputs_path = os.path.join(self.base_path, "outputs")
        os.makedirs(self.models_path, exist_ok=True)
        os.makedirs(self.outputs_path, exist_ok=True)

        # 2. Configuración Dinámica de URL
        self.model_url = f"https://civitai.com/api/download/models/{model_id}?type=Model&format=SafeTensor&size=full&fp=fp16"

        # 3. Identificación del Modelo (Tu nueva lógica)
        print(f"[*] Identificando modelo para ID: {model_id}...")
        self.model_filename = self._get_remote_filename()
        self.model_local_path = os.path.join(self.models_path, self.model_filename)

        # 4. Gestión de Descarga
        if not os.path.exists(self.model_local_path):
            self._download_model()
        else:
            print(f"[+] Modelo ya existe en disco: {self.model_filename}")

        # 5. Carga en VRAM (Modo High VRAM para T4)
        print(f"[*] Cargando {self.model_filename} en GPU...")
        self.pipe = StableDiffusionXLPipeline.from_single_file(
            self.model_local_path,
            torch_dtype=torch.float16,
            use_safetensors=True,
            low_cpu_mem_usage=True
        ).to("cuda")
        
        self.pipe.enable_attention_slicing()
        self.pipe.scheduler = EulerAncestralDiscreteScheduler.from_config(self.pipe.scheduler.config)

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
        print(f"[+] Descarga completada: {self.model_local_path}")

    def generar(self, prompt, neg_prompt="low quality, blurry, distorted, canvas", steps=30):
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        save_path = os.path.join(self.outputs_path, f"dvd_{timestamp}.png")
        
        print(f"[*] Renderizando: {prompt}")
        with torch.inference_mode():
            image = self.pipe(
                prompt=prompt,
                negative_prompt=neg_prompt,
                num_inference_steps=steps,
                guidance_scale=7.5
            ).images[0]
            
        image.save(save_path)
        print(f"[+] Resultado guardado: {save_path}")
        return image
