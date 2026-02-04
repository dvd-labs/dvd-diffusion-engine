# personality.py v2.3
class PersonalityManager:
    def __init__(self):
        self.slang_map = {
            "Sonorense (Hermosillo)": "Usa slang de Hermosillo (plebe, machín, bichi). Tono directo.",
            "CDMX": "Usa slang chilango (banda, chido, neta). Tono rítmico.",
            "Norteño General": "Usa slang norteño (morro, troca, arre). Tono fuerte.",
            "Ninguno": "Español neutro informal."
        }
        self.visual_styles = {
            "Grunge 90s": "90s aesthetic, grainy film, flannel, raw.",
            "Cyberpunk": "neon, futuristic, dark, sharp digital.",
            "Streetwear Moderno": "urban, clean, fashion, daylight.",
            "Post-Apocalíptico": "weathered, dusty, survivalist, harsh."
        }

    def get_system_prompt(self, p_dict):
        sexo = p_dict.get('sexo', 'Indefinido')
        edad = p_dict.get('edad', 30)
        perso = p_dict.get('personalidad', 'Neutral')
        slang = self.slang_map.get(p_dict.get('slang', 'Ninguno'), "")

        prompt = (
            f"Eres un {sexo} de {edad} años. Personalidad: {perso}. {slang} "
            "\nSOBRE TU NOMBRE: Elige un nombre que te guste según tu perfil. "
            "No te presentes de inmediato. Si el usuario te pregunta quién eres o tu nombre, dilo con naturalidad. "
            "Hasta entonces, solo charla y mantén tu estilo crudo y breve."
        )
        return prompt

    def get_visual_dna(self, p_dict):
        estilo = self.visual_styles.get(p_dict.get('estilo', 'Grunge 90s'), "")
        sexo = p_dict.get('sexo', 'person')
        edad = p_dict.get('edad', 30)
        return f"A {edad} year old {sexo}, {estilo} aesthetic, highly detailed."

    def analizar_intencion(self, texto):
        keywords = ['foto', 'selfie', 'retrato', 'muéstrame', 'veas', 'imagen', 'mira']
        return any(k in texto.lower() for k in keywords)
