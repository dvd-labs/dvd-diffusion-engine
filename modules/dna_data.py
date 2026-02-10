# dna_data.py - v42.0: Power Tokens & Conceptos Comprimidos

# 1. ETNIAS (Solo la raza, sin describir ojos ni pelo a menos que sea vital)
ETHNICITY_DNA = {
    "Nordico": "Scandinavian",
    "Latino": "Latina" if "Female" in globals().get('SEXO', '') else "Latino", # Ajuste dinámico simple
    "Afro": "African American",
    "Asiatico": "Japanese",
    "Mediterraneo": "Italian"
}

# 2. COMPLEXIÓN (Tipos de cuerpo visuales)
# Usamos términos de casting/moda que SDXL entiende perfecto
COMPLEXIONS = {
    "Curtido_Duro": "rugged",          # Piel áspera, texturas fuertes
    "Atletico": "athletic",            # Fibroso y en forma
    "Pesado": "heavyset",              # Robusto realista (sin ser ofensivo)
    "Delgado": "slender",              # Elegante, modelo, fino
    "Flaco": "skinny",                 # Delgado normal/callejero
    "Demacrado": "emaciated",          # Huesos salidos, look enfermo/extremo
    "Promedio": "average build"        # Cuerpo normal, sin definir
}

# 3. ESTEREOTIPOS (POWER TOKENS PUROS)
STEREOTYPES = {
    "Vaquero": "Cowboy",
    "Metalero": "Metalhead",               # Tu corrección: PERFECTA
    "Techie": "Nerd",                      # Tu corrección: PERFECTA
    "Gotico": "Goth",                      # Nuevo
    "Punk": "Punk",                        # Nuevo
    "Hipster": "Hipster",                  # Nuevo
    "Hippie": "Hippie",                    # Nuevo
    "Biker": "Biker",                      # Nuevo
    "Ejecutivo": "Corporate Business",     # Traje y corbata
    "Callejero": "Streetwear"              # Urbano moderno
}

# 4. ACCESORIOS (Modular: Se pueden combinar)
ACCESSORIES_DNA = {
    "Lentes": "glasses",                # Simple y efectivo
    "Aretes": "earrings",               # Detalle fino
    "Tatuajes": "tattoos",              # Textura en piel
    "Piercings": "facial piercings",    # Realismo
    "Maquillaje": "makeup",             # Estilo
    "Joyeria": "jewelry"                # Collares/Anillos genéricos
}

# 5. ACCIONES (Verbos directos)
ACTIONS = {
    "Estatico": "standing still",
    "Caminando": "walking",
    "Cubriendose_Arena": "shielding eyes from sandstorm",
    "Fumando": "smoking",
    "Gritando_Al_Cielo": "screaming at the sky"
}

# 6. ENCUADRE (Términos de cine)
FRAMING_SHOTS = {
    "Primer_Plano (Close-Up)": "close-up portrait",
    "Medio_Cuerpo (Mid-Shot)": "medium shot",
    "Plano_Americano (Knees-Up)": "cowboy shot",
    "Cuerpo_Completo (Full-Body)": "full body shot"
}

# 7. HÁBITAT (Lugares icónicos)
HABITATS = {
    "Favela_Gritty": "Favela slum",
    "Apartamento_Vivido": "messy bedroom",
    "Penthouse_Minimal": "luxury penthouse",
    "Workshop_Garage": "mechanic garage"
}

# 8. CLIMA (Atmósfera en 2 palabras)
CLIMATES = {
    "Soleado_Sonora": "harsh desert sun",
    "Nublado_Gris": "overcast day",
    "Lluvia_Cinematografica": "rainy night",
    "Tormenta_Arena": "sandstorm",
    "Atardecer_Dorado": "golden hour"
}

# 9. MODOS DE CÁMARA (Técnica Pura)
# Mantenemos esto técnico porque define el "look" de la foto, no el contenido.
CAMERA_MODES = {
    "Retrato": {
        "pos": "85mm lens, f/1.8, bokeh",
        "neg": "wide angle, distorted"
    },
    "Infinito": {
        "pos": "24mm lens, f/8, sharp focus",
        "neg": "bokeh, blur, macro"
    }
}

# 10. RESOLUCIONES
RESOLUTIONS = {
    "Square (1024x1024)": (1024, 1024),
    "Cinematic_Landscape (1216x832)": (1216, 832),
    "Cinematic_Portrait (832x1216)": (832, 1216),
    "Wide_16:9 (1344x768)": (1344, 768),
    "Tall_9:16 (768x1344)": (768, 1344)
}
