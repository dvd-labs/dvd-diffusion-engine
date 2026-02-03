import torch
from diffusers import StableDiffusionXLPipeline, EulerAncestralDiscreteScheduler

class DvdEngine:
    def __init__(self, model_id="stabilityai/stable-diffusion-xl-base-1.0"):
        print(f"[*] Iniciando DvdEngine en modo High VRAM...")
        
        # 1. Cargamos directo a GPU. low_cpu_mem_usage es el secreto para no tronar la RAM al inicio.
        self.pipe = StableDiffusionXLPipeline.from_pretrained(
            model_id,
            torch_dtype=torch.float16,
            variant="fp16",
            use_safetensors=True,
            low_cpu_mem_usage=True 
        ).to("cuda")
        
        # 2. Optimizaciones de atención nativas (reemplazan a xformers sin errores)
        self.pipe.enable_attention_slicing()
        
        # 3. Configuración del Scheduler
        self.pipe.scheduler = EulerAncestralDiscreteScheduler.from_config(self.pipe.scheduler.config)

    def generar(self, prompt, neg_prompt="low quality, blurry, distorted", steps=25):
        print(f"[*] Generando: {prompt}")
        
        # Usamos inference_mode para que PyTorch no gaste memoria rastreando gradientes
        with torch.inference_mode():
            return self.pipe(
                prompt=prompt,
                negative_prompt=neg_prompt,
                num_inference_steps=steps,
                guidance_scale=7.0
            ).images[0]
