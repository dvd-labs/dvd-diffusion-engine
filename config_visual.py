# config_visual.py

# ADN Base: El look por defecto de Jax
JAX_DNA_BASE = (
    "A rugged latino survivalist DJ male, wearing a dusty tactical hoodie, "
    "large DJ headphones around neck, visible tattoos, scar on cheek, "
    "intense eyes, realistic skin texture, cinematic lighting, 8k"
)

# Diccionario de Presets: Configuraciones visuales rápidas
VISUAL_PRESETS = {
    "default": JAX_DNA_BASE,
    
    "dj_set": (
        "Jax performing behind a rusted DJ booth in a ruined club, "
        "turntables made of scrap metal, neon wires glowing in the dark, "
        "smoke and dust in the air, intense focus, nu-metal aesthetic"
    ),
    
    "hermosillo_sun": (
        "Jax standing in a scorched desert street of Hermosillo, "
        "ruined colonial buildings, extreme heat haze, orange sun, "
        "tactical sunglasses, wasteland nomad gear, high contrast"
    ),
    
    "sentra_garage": (
        "Jax repairing a 1994 Nissan Sentra B13 in a post-apocalyptic garage, "
        "grease on face, holding a wrench, glowing tools, dieselpunk style, "
        "detailed engine parts, gritty atmosphere"
    )
}

def get_visual_dna(preset_name="default"):
    """Devuelve el prompt visual basado en el preset seleccionado."""
    return VISUAL_PRESETS.get(preset_name, JAX_DNA_BASE)
