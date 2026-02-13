# dna_data.py - v44.0: Sincronizado con Checkboxes

# 1. ETNIAS (Estructura Ósea + Tono de Piel)
ETHNICITY_DNA = {
    # PÁLIDO / BLANCO
    "Nordico": "pale skin Scandinavian",       # Piel muy blanca, pelo claro
    "Blanco_USA": "fair skin American",        # Blanco genérico occidental
    
    # MEDIO / TRIGUEÑO
    "Mediterraneo": "olive skin Italian",      # Piel aceitunada (ni muy blanco ni moreno)
    "Asiatico": "fair skin Japanese",          # Piel clara asiática
    
    # MORENO / LATINO
    "Latino": "tan skin Hispanic",             # Moreno clásico (lo que buscas)
    "Arabe": "brown skin Middle Eastern",      # Moreno tipo medio oriente
    
    # NEGRO / OSCURO
    "Afro": "dark skin African American",      # Piel oscura, rasgos afro
    "Ebano": "very dark skin Sudanese"         # Piel negra profunda (muy estético)
}

# 2. COMPLEXIÓN (Español)
COMPLEXIONS = {
    "Curtido_Duro": "rugged",
    "Atletico": "athletic",
    "Pesado": "heavyset",
    "Delgado": "slender",
    "Flaco": "skinny",
    "Demacrado": "emaciated",
    "Promedio": "average build"
}

# 3. ESTEREOTIPOS
STEREOTYPES = {
    "Vaquero": "Cowboy",
    "Metalero": "Metalhead",
    "Techie": "Nerd",
    "Gotico": "Goth",
    "Punk": "Punk",
    "Hipster": "Hipster",
    "Hippie": "Hippie",
    "Biker": "Biker",
    "Ejecutivo": "Corporate Business",
    "Callejero": "Streetwear"
}

# 4. ACCESORIOS (Aquí estaba el error - Ahora sí coinciden)
ACCESSORIES_DNA = {
    "Lentes": "glasses",
    "Aretes": "earrings",
    "Tatuajes": "tattoos",
    "Piercings": "facial piercings",
    "Maquillaje": "makeup",
    "Joyeria": "jewelry"
}

# 5. ACCIONES
ACTIONS = {
    "Estatico": "standing still",
    "Caminando": "walking",
    "Posando": "posing",
    "Fumando": "smoking",
    "Gritando": "screaming"
}

# 6. ENCUADRE (Versión Descontaminada)
FRAMING_SHOTS = {
    "Primer_Plano (Close-Up)": "close-up portrait, head and shoulders",
    "Medio_Cuerpo (Mid-Shot)": "medium shot, waist up",
    # CAMBIO AQUÍ: Agregamos 'cut off at knees' y 'thigh-up'
    "Plano_Americano (Knees-Up)": "medium-full shot, thigh-up framing, cut off at knees, shot from thighs up",
    "Cuerpo_Completo (Full-Body)": "full body shot, showing shoes"
}

# 7. HÁBITAT
HABITATS = {
    "Callejon": "dark alley",
    "Apartamento": "messy bedroom",
    "Penthouse": "luxury penthouse",
    "Taller": "garage workshop",
    "Bosque": "forest",
    "Desierto": "desert",
    "Neon_City": "cyberpunk city street"
}

# 8. CLIMA
CLIMATES = {
    "Soleado": "golden hour sunlight, warm lighting, clear sky",
    "Nublado": "overcast sky, flat diffused lighting",
    "Lluvia": "rainy day, wet surfaces, reflections, dramatic sky",
    
    # --- CAMBIO AQUÍ: Dividimos la noche ---
    "Noche_Luna": "night time, moonlight, clear dark sky",  # Noche visible (la que tienes ahora)
    "Noche_Profunda": "deep pitch black night, low key lighting, dimly lit, heavy shadows, intense atmosphere", # Noche oscura real
    
    "Atardecer": "sunset lighting, orange and purple sky, silhouettes"
}

# 9. MODOS DE CÁMARA
CAMERA_MODES = {
    "Retrato": {
        "pos": "85mm lens, f/1.8, bokeh",
        "neg": "wide angle, distorted"
    },
    # --- NUEVO MODO: EL EQUILIBRADO ---
    "Cine_Estandar": {
        "pos": "50mm lens, f/2.8, depth of field",
        "neg": "fisheye, extreme close-up"
    },
    # ----------------------------------
    "Infinito": {
        "pos": "24mm lens, f/8, sharp focus",
        "neg": "bokeh, blur, macro"
    }
}

# 10. RESOLUCIONES
RESOLUTIONS = {
    "Square (1024x1024)": (1024, 1024),
    "Cinematic_Landscape (1216x832)": (1216, 832),
    "Cinematic_Landscape 1.5 MP (1482x1014)": (1482, 1014),
    "Cinematic_Portrait (832x1216)": (832, 1216),
    "Wide_16:9 (1344x768)": (1344, 768),
    "Tall_9:16 (768x1344)": (768, 1344)
}
