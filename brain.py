# brain.py
from transformers import AutoModelForCausalLM, AutoTokenizer, BitsAndBytesConfig
import torch

class DvdBrain:
    def __init__(self, model_name="failspy/Llama-3-8B-Instruct-Abliterated"):
        print(f"[*] Inicializando núcleo cognitivo: {model_name}")

        # Configuración de 4-bits para optimización de VRAM
        bnb_config = BitsAndBytesConfig(
            load_in_4bit=True,
            bnb_4bit_compute_dtype=torch.float16,
            bnb_4bit_quant_type="nf4",
            bnb_4bit_use_double_quant=True
        )

        self.tokenizer = AutoTokenizer.from_pretrained(model_name)
        self.tokenizer.pad_token = self.tokenizer.eos_token

        self.model = AutoModelForCausalLM.from_pretrained(
            model_name,
            quantization_config=bnb_config,
            device_map="auto",
            torch_dtype=torch.float16
        )
        self.history = []

    def hablar(self, user_input, persona_prompt):
        # Mantenemos la lógica de historial y template de chat
        messages = [{"role": "system", "content": persona_prompt}] + self.history + [{"role": "user", "content": user_input}]

        inputs = self.tokenizer.apply_chat_template(
            messages,
            add_generation_prompt=True,
            return_tensors="pt",
            return_dict=True
        ).to("cuda")

        with torch.no_grad():
            outputs = self.model.generate(
                **inputs,
                max_new_tokens=512,
                do_sample=True,
                temperature=0.8,
                top_p=0.9,
                repetition_penalty=1.2,
                pad_token_id=self.tokenizer.eos_token_id
            )

        respuesta = self.tokenizer.decode(outputs[0][len(inputs['input_ids'][0]):], skip_special_tokens=True)

        self.history.append({"role": "user", "content": user_input})
        self.history.append({"role": "assistant", "content": respuesta})

        return respuesta
