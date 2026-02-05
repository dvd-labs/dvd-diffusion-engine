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
    Fuerza a Llama a comportarse como un generador de metadatos técnico, 
    eliminando introducciones y narrativas largas.
    """
    # 1. Instrucción agresiva de NO CHAT
    prompt_sistema_visual = (
        "TASK: You are a TECHNICAL metadata generator for Stable Diffusion. "
        "STRICT RULES: "
        "1. Output ONLY the visual description. "
        "2. NO introductions (e.g., 'Here is...', 'Prompt:'). "
        "3. NO narrative instructions (e.g., 'Imagine a story'). "
        "4. NO conversational filler. "
        f"CHARACTER DNA: {jax_dna}. "
        f"SCENE: {user_input}. "
        "FORMAT: Raw keywords and short phrases only."
    )
    
    messages = [
        {"role": "system", "content": prompt_sistema_visual}, 
        {"role": "user", "content": f"Visual description for: {user_input}"}
    ]
    
    # 2. Tokenización y envío a CUDA
    inputs = self.tokenizer.apply_chat_template(
        messages, 
        add_generation_prompt=True, 
        return_tensors="pt"
    ).to("cuda")

    # 3. Generación DETERMINISTA (do_sample=False corta la creatividad excesiva)
    with torch.no_grad():
        outputs = self.model.generate(
            inputs, 
            max_new_tokens=60, 
            do_sample=False, # <-- ESTO mata la amabilidad y las introducciones
            pad_token_id=self.tokenizer.eos_token_id
        )
    
# 4. Decodificación de la salida de Llama
    raw_output = self.tokenizer.decode(
        outputs[0][inputs.shape[1]:], 
        skip_special_tokens=True
    ).strip()
    
    # 5. EL CORTA-CORRIENTES (Split Agresivo)
    # Si detecta dos puntos, asumimos que lo de antes es basura (ej: "Here is your prompt: ...")
    if ":" in raw_output:
        # Tomamos solo lo que está después del ÚLTIMO ":" por seguridad
        raw_output = raw_output.split(":")[-1].strip()
    
    # 6. FILTRO DE COMILLAS Y BASURA RESIDUAL
    # Quitamos comillas si el modelo intentó encerrar el prompt
    raw_output = raw_output.replace('"', '').replace("'", "")
    
    # Lista negra de frases que Llama suele escupir
    trash_phrases = ["here is", "detailed prompt", "description of", "imagine"]
    for phrase in trash_phrases:
        if raw_output.lower().startswith(phrase):
            raw_output = raw_output.lower().replace(phrase, "", 1).strip()

    return raw_output.capitalize() # Lo entregamos limpio y con la primera en mayúscula
