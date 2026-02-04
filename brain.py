# brain.py v7.2
from transformers import AutoModelForCausalLM, AutoTokenizer, BitsAndBytesConfig
import torch
from google.colab import userdata

class DvdBrain:
    def __init__(self, model_name="failspy/Llama-3-8B-Instruct-Abliterated", api_token=None):
        print(f"[*] Inicializando núcleo cognitivo: {model_name}")
        
        # Lógica de Token Inteligente: 
        # 1. Prioridad al token pegado manualmente.
        # 2. Si no hay, busca en Secretos.
        self.hf_token = api_token
        if not self.hf_token:
            try:
                self.hf_token = userdata.get('HF_TOKEN')
                print("[*] Usando HF_TOKEN desde los Secretos de Colab.")
            except:
                self.hf_token = None
                print("[!] Advertencia: No se detectó HF_TOKEN. Modelos protegidos podrían fallar.")

        bnb_config = BitsAndBytesConfig(
            load_in_4bit=True,
            bnb_4bit_compute_dtype=torch.float16,
            bnb_4bit_quant_type="nf4",
            bnb_4bit_use_double_quant=True
        )

        self.tokenizer = AutoTokenizer.from_pretrained(model_name, token=self.hf_token)
        self.tokenizer.pad_token = self.tokenizer.eos_token

        self.model = AutoModelForCausalLM.from_pretrained(
            model_name,
            quantization_config=bnb_config,
            device_map="auto",
            torch_dtype=torch.float16,
            token=self.hf_token
        )
        self.history = []

    def hablar(self, user_input, persona_prompt):
        # ... (el resto de la función hablar se mantiene igual)
        messages = [{"role": "system", "content": persona_prompt}] + self.history + [{"role": "user", "content": user_input}]
        inputs = self.tokenizer.apply_chat_template(messages, add_generation_prompt=True, return_tensors="pt", return_dict=True).to("cuda")
        with torch.no_grad():
            outputs = self.model.generate(**inputs, max_new_tokens=512, do_sample=True, temperature=0.8, top_p=0.9, repetition_penalty=1.2, pad_token_id=self.tokenizer.eos_token_id)
        respuesta = self.tokenizer.decode(outputs[0][len(inputs['input_ids'][0]):], skip_special_tokens=True)
        self.history.append({"role": "user", "content": user_input})
        self.history.append({"role": "assistant", "content": respuesta})
        return respuesta
