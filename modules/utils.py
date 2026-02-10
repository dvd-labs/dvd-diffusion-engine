import re
# --- 2. FUNCIONES DE SOPORTE ---
def parse_manual_string(s_str, default_steps, default_cfg, default_seed):
    p_steps, p_cfg, p_seed = default_steps, default_cfg, default_seed
    if not s_str: return p_steps, p_cfg, p_seed
    try:
        steps_match = re.search(r'(?:Steps|steps)[:=]\s*(\d+)', s_str)
        if steps_match: p_steps = int(steps_match.group(1))
        cfg_match = re.search(r'(?:CFG scale|cfg)[:=]\s*([\d\.]+)', s_str)
        if cfg_match: p_cfg = float(cfg_match.group(1))
        seed_match = re.search(r'(?:Seed|seed)[:=]\s*(\d+)', s_str)
        if seed_match: p_seed = int(seed_match.group(1))
    except: pass
    return p_steps, p_cfg, p_seed

def get_gender_term(sex, age):
    # Aseguramos que sea entero por si acaso
    age = int(age)

    # --- LÓGICA MASCULINA ---
    if sex == "Male":
        if age < 4:  return "toddler boy"       # 0-3: Proporciones de bebé (cabeza grande)
        if age < 10: return "little boy"        # 4-9: Infancia clásica (Child/Kid)
        if age < 13: return "preteen boy"       # 10-12: La etapa "incómoda" antes de la pubertad
        if age < 20: return "teenage boy"       # 13-19: Adolescencia
        if age < 30: return "young man"         # 20-29: Juventud plena
        if age < 60: return "middle-aged man"   # 30-59: Madurez y texturas
        return "elderly man"                    # 60+: Vejez

    # --- LÓGICA FEMENINA ---
    else:
        if age < 4:  return "toddler girl"
        if age < 10: return "little girl"
        if age < 13: return "preteen girl"
        if age < 20: return "teenage girl"
        if age < 30: return "young woman"
        if age < 60: return "middle-aged woman"
        return "elderly woman"
