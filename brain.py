# brain.py v7.9 (FULL: Silencio + Visual Prompter + Slang)
import re
import warnings
from transformers import AutoModelForCausalLM, AutoTokenizer, BitsAndBytesConfig, logging as transformers_logging
import torch
from google.colab import userdata

# Apagamos la estática técnica
transformers_logging.set_verbosity_error()
warnings.filterwarnings("ignore")

class DvdBrain:
    def __init__(self, model_name="mlabonne/Llama-3.1-8B-Instruct-Abliterated", api_token=None):
        print(f"[*] Inicializando núcleo cognitivo: {model_name}")
        self.hf_token = api_token or (userdata.get('HF_TOKEN') if not api_token else None)
        
        bnb_config = BitsAndBytesConfig(
            load_in_4bit=True, bnb_4bit_compute_dtype=torch.float16,
            bnb_4bit_quant_type="nf4", bnb_4bit_use_double_quant=True
        )

        self.tokenizer = AutoTokenizer.from_pretrained(model_name, token=self.hf_token)
        self.tokenizer.pad_token = self.tokenizer.eos_token 
        
        self.model = AutoModelForCausalLM.from_pretrained(
            model_name, quantization_config=bnb_config, 
            device_map="auto", torch_dtype=torch.float16, token=self.hf_token
        )
        self.history = []

    def hablar(self, user_input, persona_prompt):
        """Voz ruda de Jax."""
        messages = [{"role": "system", "content": persona_prompt}] + self.history + [{"role": "user", "content": user_input}]
        inputs = self.tokenizer.apply_chat_template(messages, add_generation_prompt=True, return_tensors="pt", return_dict=True).to("cuda")
        
        with torch.no_grad():
            outputs = self.model.generate(
                **inputs, max_new_tokens=256, do_sample=True, temperature=0.8,
                pad_token_id=self.tokenizer.eos_token_id 
            )
        
        respuesta = self.tokenizer.decode(outputs[0][len(inputs['input_ids'][0]):], skip_special_tokens=True)
        self.history.append({"role": "user", "content": user_input})
        self.history.append({"role": "assistant", "content": respuesta.strip()})
        return respuesta.strip()

    # brain.py (Busca este método)

def generar_prompt_visual(self, user_input, jax_dna):
    """
    Fuerza el estilo de fotografía amateur y elimina la alucinación cinematográfica.
    """
    # 1. Definimos el "guion" de realismo sucio
    prompt_sistema_visual = (
        "TASK: Create a VERY SHORT image description. "
        "STYLE: Amateur smartphone selfie, high quality photo, realistic, grainy, "
        "natural lighting, direct flash, casual pose. "
        "ABSOLUTELY NO: 3D, 2D, Animation, Studio Ghibli, professional photography, "
        "cinematic, CGI, digital art. "
        f"SUBJECT: {jax_dna}. " 
        f"CONTEXT: {user_input} (make it look like a candid phone snap)."
    )
    
    # 2. Preparamos el mensaje para el motor de Llama
    messages = [
        {"role": "system", "content": prompt_sistema_visual}, 
        {"role": "user", "content": f"Describe the photo for: {user_input}"}
    ]
    
    # 3. Procesamiento en GPU (CUDA)
    inputs = self.tokenizer.apply_chat_template(
        messages, 
        add_generation_prompt=True, 
        return_tensors="pt", 
        return_dict=True
    ).to("cuda")

    # 4. Generación optimizada para no quemar tus 12GB de VRAM
    with torch.no_grad():
        outputs = self.model.generate(
            **inputs, 
            max_new_tokens=100, # No necesitamos más para un prompt visual
            do_sample=True,      
            temperature=0.7,      # Un poco de calor para que no sea repetitivo
            pad_token_id=self.tokenizer.eos_token_id
        )
    
    # 5. Entrega del resultado limpio
    return self.tokenizer.decode(
        outputs[0][len(inputs['input_ids'][0]):], 
        skip_special_tokens=True
    ).strip()
