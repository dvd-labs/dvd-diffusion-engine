import torch
import os
from datetime import datetime
from diffusers import StableDiffusionXLPipeline, EulerAncestralDiscreteScheduler

class DvdEngine:
    def __init__(self, model_id="stabilityai/stable-diffusion-xl-base-1.0"):
        # 1. Definir rutas
        self.base_path = "/content/dvd-diffusion-engine"
        self.models_path = os.path.join(self.base_path, "models")
        self.outputs_path = os.path.join(self.base_path, "outputs")
        
        # 2. Crear carpetas si no existen
        os.makedirs(self.models_path, exist_ok=True)
        os.makedirs(self.outputs_path, exist_ok=True)
        
        print(f"[*] Carpetas listas en: {self.base_path}")
        print(f"[*] Cargando modelo: {model_id}")

        # 3. Carga de modelo (Redirigiendo la descarga a nuestra carpeta de modelos)
        self.pipe = StableDiffusionXLPipeline.from_pretrained(
            model_id,
            torch_dtype=torch.float16,
            variant="fp16",
            use_safetensors=True,
            low_cpu_mem_usage=True,
            cache_dir=self.models_path # <--- AQUÍ se guardará el modelo ahora
        ).to("cuda")
        
        self.pipe.enable_attention_slicing()
        self.pipe.scheduler = EulerAncestralDiscreteScheduler.from_config(self.pipe.scheduler.config)

    def generar(self, prompt, neg_prompt="low quality, blurry, distorted", steps=25):
        # Generar nombre de archivo único con timestamp
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
            
        # Guardado automático estilo Fooocus
        image.save(save_path)
        print(f"[+] Imagen guardada en: {save_path}")
        
        return image
