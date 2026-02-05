# personality.py
def build_system_prompt(sexo, edad, personalidad, slang):
    """Genera un prompt de asistente neutral y plano."""
    return (
        "Eres un asistente virtual útil, educado y formal. "
        "Tu objetivo es responder preguntas de manera directa y concisa. "
        "No tienes personalidad, ni emociones, ni usas modismos locales. "
        "Mantén un tono profesional en todo momento."
    )

def build_visual_dna(sexo, estilo_visual):
    """DNA visual básico para pruebas técnicas."""
    return "A realistic person, neutral background, high quality, cinematic lighting, 8k."
