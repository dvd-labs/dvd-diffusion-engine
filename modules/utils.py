import re

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

def parse_manual_string(settings_str, default_steps, default_cfg, default_seed):
    steps = default_steps
    cfg = default_cfg
    seed = default_seed
    
    if "steps=" in settings_str:
        try: steps = int(re.search(r'steps=(\d+)', settings_str).group(1))
        except: pass
        
    if "cfg=" in settings_str:
        try: cfg = float(re.search(r'cfg=([\d\.]+)', settings_str).group(1))
        except: pass
        
    if "seed=" in settings_str:
        try: seed = int(re.search(r'seed=(\d+)', settings_str).group(1))
        except: pass
        
    return steps, cfg, seed
