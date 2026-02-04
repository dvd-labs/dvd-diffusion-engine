# personality.py v2.2
class PersonalityManager:
    def __init__(self):
        # Mapeo de modismos regionales
        self.slang_map = {
            "Sonorense (Hermosillo)": "Usa slang de Hermosillo (plebe, machín, bichi, shilo, parote). Tono golpeado y directo.",
            "CDMX": "Usa slang chilango (banda, chido, cámara, neta). Tono rítmico.",
            "Norteño General": "Usa slang norteño (morro, jalar, troca, arre). Tono fuerte.",
            "Ninguno": "Español neutro informal."
        }

        # Estilos visuales para SDXL
        self.visual_styles = {
            "Grunge 90s": "90s aesthetic, grainy film, low contrast, flannel textures, disposable camera look, raw.",
            "Cyberpunk": "neon lighting, high tech low life, futuristic, dark alley vibe, sharp digital textures.",
            "Streetwear Moderno": "urban photography, clean lines, bright daylight, high-end fashion, sleek, crisp focus.",
            "Post-Apocalíptico": "weathered clothes, dusty environment, desaturated, wasteland aesthetic, survivalist look."
        }

    def get_system_prompt(self, p_dict):
        """Instruye a la IA a crear y ocultar su nombre."""
        sexo = p_dict.get('sexo', 'Indefinido')
        edad = p_dict.get('edad', 30)
        perso = p_dict.get('personalidad', 'Neutral')
        slang = self.slang_map.get(p_dict.get('slang', 'Ninguno'), "")

        prompt = (
            f"IDENTIDAD: Eres un {sexo} de {edad} años. Tu personalidad es {perso}. "
            f"{slang} "
            "\nREGLA DE ORO SOBRE TU NOMBRE: "
            "1. Tú debes inventar un nombre que encaje con tu perfil y slang. "
            "2. NUNCA te presentes por tu nombre ni lo digas al inicio de la charla. "
            "3. Mantén tu nombre en secreto absoluto hasta que el usuario te lo pregunte directamente. "
            "4. Si te preguntan '¿quién eres?' o '¿cómo te llamas?', revela tu nombre con tu personalidad. "
            "\nResponde de forma breve y cruda. No expliques tus pensamientos."
        )
        return prompt

    def get_visual_dna(self, p_dict):
        """DNA visual neutro (Sin nombre para no arruinar la sorpresa)."""
        estilo = self.visual_styles.get(p_dict.get('estilo', 'Grunge 90s'), "")
        sexo = p_dict.get('sexo', 'person')
        edad = p_dict.get('edad', 30)
        
        # Usamos descripción física en lugar de nombre para el prompter
        dna = f"A {edad} year old {sexo}, highly detailed, Style: {estilo}"
        return dna

    def analizar_intencion(self, texto):
        keywords = ['foto', 'selfie', 'retrato', 'muéstrame', 'veas', 'imagen', 'mira']
        return any(k in texto.lower() for k in keywords)
