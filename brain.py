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
    Transforma el input en una cadena rígida de parámetros visuales.
    Fórmula: realistic photo of [jax_dna], [translation], [params].
    """
    # 1. Definimos los parámetros de realismo sucio (Amateur/Real)
    # 'skin pores', 'film grain' y 'f/1.8' matan el look de IA plástica.
    params = "highly detailed face, skin pores, natural lighting, raw photo, 8k, film grain, shot on 35mm lens, f/1.8"

    # 2. Instrucción de "Cero Tolerancia"
    system_instr = (
        f"FORMULA: realistic photo of {jax_dna}, [ENGLISH_TRANSLATION], {params}. "
        f"TRANSLATE THIS TO ENGLISH: {user_input}"
    )

    # 3. Procesamiento Determinista
    inputs = self.tokenizer.apply_chat_template(
        messages, 
        add_generation_prompt=True, 
        return_tensors="pt"
    ).to("cuda")

    with torch.no_grad():
        outputs = self.model.generate(
            **inputs, 
            max_new_tokens=80, 
            do_sample=False, # <-- Desactivado para evitar 'historias'
            pad_token_id=self.tokenizer.eos_token_id
        )

    # 4. Extracción y Limpieza Final
    res = self.tokenizer.decode(outputs[0][len(inputs[0]):], skip_special_tokens=True).strip()
    
    # Si Llama intenta ser amable a pesar de todo, aplicamos el decapado:
    if ":" in res: res = res.split(":")[-1].strip()
    return res.replace('"', '').replace("'", "").strip()
