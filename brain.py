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
    Genera prompts ultracortos, estilo ráfaga de palabras clave, 
    sin introducciones ni explicaciones.
    """
    # 1. Instrucción agresiva de NO CHAT
    prompt_sistema_visual = (
        "TASK: You are a prompt generator for an image AI. "
        "STRICT RULE: Output ONLY the description. DO NOT use 'Here is...', 'Prompt:', or any conversational filler. "
        "STYLE: High-realism amateur photography, smartphone selfie, grainy, natural, candid. "
        "ABSOLUTELY NO: 3D, CGI, Animation, Studio Ghibli, 2D art, cinematic renders. "
        f"CHARACTER DNA: {jax_dna}. "
        f"SCENE: {user_input}. "
        "FORMAT: Raw keywords and short phrases only."
    )
    
    # 2. Mensaje limpio
    messages = [
        {"role": "system", "content": prompt_sistema_visual}, 
        {"role": "user", "content": f"Generate prompt for: {user_input}"}
    ]
    
    inputs = self.tokenizer.apply_chat_template(
        messages, 
        add_generation_prompt=True, 
        return_tensors="pt"
    ).to("cuda")

    # 3. Generación determinista para evitar verborrea
    with torch.no_grad():
        outputs = self.model.generate(
            **inputs, 
            max_new_tokens=60, # Reducimos para forzar la brevedad
            do_sample=False,    # Al apagar el sampling, el modelo es más directo
            pad_token_id=self.tokenizer.eos_token_id
        )
    
    # 4. Limpieza de tokens
    result = self.tokenizer.decode(
        outputs[0][len(inputs[0]):], 
        skip_special_tokens=True
    ).strip()
    
    # Limpieza final por si acaso se le escapa un "Prompt:"
    return result.replace("Prompt:", "").replace("Description:", "").strip()
