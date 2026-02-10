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

def get_gender_term(sex, age_str):
    try:
        age = int(re.search(r'\d+', age_str).group())
    except:
        age = 19
    if sex == "Male":
        if age < 13: return "little boy"
        if age < 30: return "young man"
        return "man, adult male"
    else:
        if age < 13: return "little girl"
        if age < 30: return "girl"
        return "woman, adult female"
