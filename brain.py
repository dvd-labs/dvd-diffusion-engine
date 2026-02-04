# brain.py v7.8 (Silencio de Logs)
import re
import warnings
import logging
from transformers import AutoModelForCausalLM, AutoTokenizer, BitsAndBytesConfig, logging as transformers_logging
import torch
from google.colab import userdata

# --- EL FILTRO DE SILENCIO ---
# Esto apaga los avisos de "pad_token_id" de raíz
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
        self.tokenizer.pad_token = self.tokenizer.eos_token # Aseguramos que el token exista
        
        self.model = AutoModelForCausalLM.from_pretrained(
            model_name, quantization_config=bnb_config, 
            device_map="auto", torch_dtype=torch.float16, token=self.hf_token
        )
        self.history = []

    def hablar(self, user_input, persona_prompt):
        messages = [{"role": "system", "content": persona_prompt}] + self.history + [{"role": "user", "content": user_input}]
        inputs = self.tokenizer.apply_chat_template(messages, add_generation_prompt=True, return_tensors="pt", return_dict=True).to("cuda")
        
        with torch.no_grad():
            outputs = self.model.generate(
                **inputs, 
                max_new_tokens=256, 
                do_sample=True, 
                temperature=0.8,
                pad_token_id=self.tokenizer.eos_token_id # <-- FIX: Se lo pasamos aquí para que no se queje
            )
        
        respuesta = self.tokenizer.decode(outputs[0][len(inputs['input_ids'][0]):], skip_special_tokens=True)
        self.history.append({"role": "user", "content": user_input})
        self.history.append({"role": "assistant", "content": respuesta.strip()})
        return respuesta.strip()

    def generar_prompt_visual(self, user_input, jax_dna):
        # ... (aplica lo mismo de pad_token_id aquí si usas el método v7.7)
        # Asegúrate de añadir pad_token_id=self.tokenizer.eos_token_id en el .generate
        pass
