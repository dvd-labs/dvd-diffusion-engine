import torch
from diffusers import StableDiffusionXLPipeline, EulerAncestralDiscreteScheduler
from diffusers.utils import is_xformers_available

class DvdEngine:
    def __init__(self, model_id="stabilityai/stable-diffusion-xl-base-1.0"):
        print(f"[*] Iniciando DvdEngine con {model_id}...")
        self.pipe = StableDiffusionXLPipeline.from_pretrained(
            model_id,
            torch_dtype=torch.float16,
            variant="fp16",
            use_safetensors=True
        ).to("cuda")
        
        # Gestión de memoria estilo Forge
        self.pipe.enable_model_cpu_offload()
        
        # Verificación inteligente de xformers
        if is_xformers_available():
            print("[+] Optimizando con xformers...")
            self.pipe.enable_xformers_memory_efficient_attention()
        else:
            print("[-] xformers no detectado, usando optimización nativa de PyTorch...")
        
        self.pipe.scheduler = EulerAncestralDiscreteScheduler.from_config(self.pipe.scheduler.config)

    def generar(self, prompt, neg_prompt="low quality, blurry, distorted", steps=25):
        print(f"[*] Generando: {prompt}")
        return self.pipe(
            prompt=prompt,
            negative_prompt=neg_prompt,
            num_inference_steps=steps,
            guidance_scale=7.0
        ).images[0]
