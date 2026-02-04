# personality.py v2.0
class PersonalityManager:
    def __init__(self):
        # Diccionario de modismos por región para el "Slang Local"
        self.slang_map = {
            "Sonorense (Hermosillo)": "Usa palabras como: plebe, shilo, bichi, parote, machín, compa, buki. Tono directo y golpeado.",
            "CDMX": "Usa palabras como: banda, chido, cámara, neta, chale, carnal. Tono rítmico y fluido.",
            "Norteño General": "Usa palabras como: morro, jalar, troca, fiero, arre. Tono fuerte.",
            "Ninguno": "Usa un español neutro pero informal."
        }

        # Estilos visuales mapeados a etiquetas técnicas para el motor visual
        self.visual_styles = {
            "Grunge 90s": "90s aesthetic, grainy film, low contrast, flannel textures, disposable camera look, authentic, raw.",
            "Cyberpunk": "neon lighting, high tech low life, cinematic synthwave colors, sharp digital textures, futuristic, dark alley vibe.",
            "Streetwear Moderno": "hypebeast style, urban photography, clean lines, bright daylight, high-end fashion, sleek, crisp focus.",
            "Post-Apocalíptico": "weathered clothes, dusty environment, desaturated colors, harsh lighting, wasteland aesthetic, survivalist look."
        }

    def get_system_prompt(self, p_dict):
        """Genera el System Prompt para el LLM (Voz del personaje)."""
        nombre = p_dict.get('nombre', 'Sujeto')
        sexo = p_dict.get('sexo', 'Indefinido')
        edad = p_dict.get('edad', 30)
        perso = p_dict.get('personalidad', 'Neutral')
        slang = self.slang_map.get(p_dict.get('slang', 'Ninguno'), "")

        prompt = (
            f"Eres {nombre}, {sexo} de {edad} años. "
            f"Tu personalidad es {perso}. "
            f"{slang} "
            "IMPORTANT: No seas amable si tu personalidad no lo dicta. Mantente en personaje siempre. "
            "Responde de forma breve y cruda. No des explicaciones de tus pensamientos."
        )
        return prompt

    def get_visual_dna(self, p_dict):
        """Genera el DNA visual para el prompter de SDXL."""
        estilo = self.visual_styles.get(p_dict.get('estilo', 'Grunge 90s'), "")
        nombre = p_dict.get('nombre', 'Sujeto')
        sexo = p_dict.get('sexo', 'Person')
        edad = p_dict.get('edad', 30)
        
        # Construimos la base física del personaje para el prompter
        dna = f"Character: {nombre}, a {edad} year old {sexo}. Style: {estilo}"
        return dna

    def analizar_intencion(self, texto):
        """Detecta si el usuario quiere una imagen."""
        keywords = ['foto', 'selfie', 'retrato', 'muéstrame', 'veas', 'imagen', 'mira']
        return any(k in texto.lower() for k in keywords)
