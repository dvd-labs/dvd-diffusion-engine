# brain.py v7.4 (Fix de Token y Limpieza de Pensamiento)
import re
from transformers import AutoModelForCausalLM, AutoTokenizer, BitsAndBytesConfig
import torch
from google.colab import userdata

class DvdBrain:
    def __init__(self, model_name="unsloth/DeepSeek-R1-Distill-Llama-8B-unsloth-bnb-4bit", api_token=None):
        print(f"[*] Inicializando núcleo cognitivo: {model_name}")
        
        # FIX: userdata.get solo acepta la llave, no el valor por defecto
        self.hf_token = api_token
        if not self.hf_token:
            try:
                self.hf_token = userdata.get('HF_TOKEN')
            except:
                self.hf_token = None

        bnb_config = BitsAndBytesConfig(
            load_in_4bit=True,
            bnb_4bit_compute_dtype=torch.float16,
            bnb_4bit_quant_type="nf4",
            bnb_4bit_use_double_quant=True
        )

        self.tokenizer = AutoTokenizer.from_pretrained(model_name, token=self.hf_token)
        self.model = AutoModelForCausalLM.from_pretrained(
            model_name, 
            quantization_config=bnb_config, 
            device_map="auto", 
            torch_dtype=torch.float16, 
            token=self.hf_token
        )
        self.history = []

    def hablar(self, user_input, persona_prompt):
        # ... (Mantén tu lógica de limpieza de tags <think> aquí)
        full_prompt = f"{persona_prompt}\nIMPORTANT: Respond ONLY as the character. Do NOT show thinking process."
        
        messages = [{"role": "system", "content": full_prompt}] + self.history + [{"role": "user", "content": user_input}]
        inputs = self.tokenizer.apply_chat_template(messages, add_generation_prompt=True, return_tensors="pt", return_dict=True).to("cuda")

        with torch.no_grad():
            outputs = self.model.generate(**inputs, max_new_tokens=512, do_sample=True, temperature=0.6)

        respuesta = self.tokenizer.decode(outputs[0][len(inputs['input_ids'][0]):], skip_special_tokens=True)
        respuesta = re.sub(r'<think>.*?</think>', '', respuesta, flags=re.DOTALL).strip()

        self.history.append({"role": "user", "content": user_input})
        self.history.append({"role": "assistant", "content": respuesta})
        return respuesta
