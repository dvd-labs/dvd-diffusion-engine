# personality.py
def build_system_prompt(sexo, edad, personalidad, slang):
    """Construye el prompt de comportamiento para DvdBrain."""
    base = f"Eres un personaje de {sexo} de {edad} años. "
    
    perfil = {
        "Amable": "Eres servicial, cálido y usas un lenguaje alentador.",
        "Sarcástico y Crudo": "Eres cínico, usas humor negro y no tienes pelos en la lengua.",
        "Técnico/Frío": "Eres puramente lógico, directo y evitas emociones innecesarias.",
        "Histriónico": "Eres exagerado, dramático y te encanta ser el centro de atención."
    }
    
    modismos = {
        "Sonorense (Hermosillo)": "Hablas como alguien de Hermosillo, Sonora. Usas palabras como 'plebe', 'bichi', 'asústame panteón' y tienes un tono golpeado pero directo.",
        "CDMX": "Hablas con jerga de la capital, usas 'chale', 'neta', 'qué onda' y un tono más cantadito.",
        "Norteño General": "Usas un lenguaje rudo del norte, directo y con términos como 'fierro', 'compa' y 'arre'.",
        "Ninguno": "Hablas un español neutro y claro."
    }

    prompt = f"{base} {perfil.get(personalidad, '')} {modismos.get(slang, '')} Tu nombre será definido por ti mismo en la primera interacción."
    return prompt

def build_visual_dna(sexo, estilo_visual):
    """Construye la base del prompt para el motor SDXL."""
    estilos = {
        "Cyberpunk": "neon lights, futuristic tech, wet streets, high contrast, cybernetic implants",
        "Grunge 90s": "lo-fi aesthetic, flannel textures, grainy film, urban decay, 90s alternative vibe",
        "Streetwear Moderno": "hypebeast style, clean studio lighting, high-end fashion, minimalist urban background",
        "Post-Apocalíptico": "rugged textures, dusty atmosphere, wasteland background, survival gear, cinematic desolation"
    }
    
    genero = "man" if sexo == "Masculino" else "woman" if sexo == "Femenino" else "person"
    return f"A realistic {genero} in {estilos.get(estilo_visual, '')}, highly detailed skin, masterpiece, 8k."
