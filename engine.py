import torch
from diffusers import StableDiffusionXLPipeline, EulerAncestralDiscreteScheduler

class DvdEngine:
    def __init__(self, model_id="stabilityai/stable-diffusion-xl-base-1.0"):
        print(f"[*] Iniciando DvdEngine con {model_id}...")
        self.pipe = StableDiffusionXLPipeline.from_pretrained(
            model_id,
            torch_dtype=torch.float16,
            variant="fp16",
            use_safetensors=True
        ).to("cuda")
        
        # Optimizaciones de memoria nivel experto
        self.pipe.enable_model_cpu_offload()
        self.pipe.enable_xformers_memory_efficient_attention()
        
        # Sampler rápido para no perder tiempo
        self.pipe.scheduler = EulerAncestralDiscreteScheduler.from_config(self.pipe.scheduler.config)

    def generar(self, prompt, neg_prompt="low quality, blurry, distorted", steps=25):
        print(f"[*] Generando: {prompt}")
        return self.pipe(
            prompt=prompt,
            negative_prompt=neg_prompt,
            num_inference_steps=steps,
            guidance_scale=7.0
        ).images[0]
