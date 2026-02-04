# brain.py v7.3 (Anti-Monólogo)
import re # <-- Necesitamos esto para limpiar el texto
from transformers import AutoModelForCausalLM, AutoTokenizer, BitsAndBytesConfig
import torch
from google.colab import userdata

class DvdBrain:
    def __init__(self, model_name="unsloth/DeepSeek-R1-Distill-Llama-8B-unsloth-bnb-4bit", api_token=None):
        print(f"[*] Inicializando núcleo cognitivo: {model_name}")
        self.hf_token = api_token or userdata.get('HF_TOKEN', None)

        bnb_config = BitsAndBytesConfig(
            load_in_4bit=True,
            bnb_4bit_compute_dtype=torch.float16,
            bnb_4bit_quant_type="nf4",
            bnb_4bit_use_double_quant=True
        )

        self.tokenizer = AutoTokenizer.from_pretrained(model_name, token=self.hf_token)
        self.model = AutoModelForCausalLM.from_pretrained(
            model_name, quantization_config=bnb_config, 
            device_map="auto", torch_dtype=torch.float16, token=self.hf_token
        )
        self.history = []

    def hablar(self, user_input, persona_prompt):
        # Reforzamos que NO queremos pensamientos
        full_prompt = f"{persona_prompt}\nIMPORTANT: Respond ONLY as the character. Do NOT show your internal reasoning or thinking process."
        
        messages = [{"role": "system", "content": full_prompt}] + self.history + [{"role": "user", "content": user_input}]
        inputs = self.tokenizer.apply_chat_template(messages, add_generation_prompt=True, return_tensors="pt", return_dict=True).to("cuda")

        with torch.no_grad():
            outputs = self.model.generate(**inputs, max_new_tokens=512, do_sample=True, temperature=0.6)

        respuesta = self.tokenizer.decode(outputs[0][len(inputs['input_ids'][0]):], skip_special_tokens=True)

        # --- LIMPIEZA DE PENSAMIENTO ---
        # Borra todo lo que esté dentro de tags <think> o que parezca razonamiento interno
        respuesta = re.sub(r'<think>.*?</think>', '', respuesta, flags=re.DOTALL)
        respuesta = respuesta.split("¡Hola!")[-1] if "Okay, the user just said" in respuesta else respuesta # Limpieza extra si no usa tags
        respuesta = respuesta.strip()

        self.history.append({"role": "user", "content": user_input})
        self.history.append({"role": "assistant", "content": respuesta})
        return respuesta
