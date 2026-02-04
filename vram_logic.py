# vram_logic.py
import torch
import gc
from IPython.display import HTML, display

def parse_settings(settings_str):
    """Convierte el string de parámetros en un diccionario real."""
    kwargs = {}
    try:
        parts = [p.strip() for p in settings_str.split(',')]
        for part in parts:
            if '=' not in part: continue
            k, v = part.split('=')
            k, v = k.strip(), v.strip()
            if v.lower() == 'none': kwargs[k] = None
            elif '.' in v: kwargs[k] = float(v)
            else:
                num = int(v)
                kwargs[k] = None if (k == 'seed' and num == 0) else num
    except:
        pass
    return kwargs

def generar_con_intercambio(brain, motor, prompt, settings_str, neg_prompt, ade_on, ade_str):
    """
    Protocolo de Hot-Swap:
    1. Mueve Llama a CPU.
    2. Genera imagen en GPU.
    3. (Opcional) Aplica Adetailer.
    4. Regresa Llama a GPU.
    """
    # --- A. DESALOJO (LLM -> CPU) ---
    try:
        if hasattr(brain, 'model'): brain.model.to("cpu")
        elif hasattr(brain, 'pipeline'): brain.pipeline.model.to("cpu")
        torch.cuda.empty_cache(); gc.collect()
    except: pass

    # --- B. CONFIGURACIÓN ---
    kwargs = parse_settings(settings_str)
    img = None
    
    try:
        # --- C. GENERACIÓN ---
        img, meta, path = motor.generar(prompt=prompt, neg_prompt=neg_prompt, **kwargs)

        # --- D. ADETAILER (Tu lógica v6.0) ---
        if ade_on:
            display(HTML("<b style='color: #f39c12;'>[*] Aplicando Adetailer...</b>"))
            img = motor.aplicar_adetailer(img, prompt, neg_prompt, strength=ade_str)
            img.save(path.replace(".png", "_fixed.png"), pnginfo=meta)
            
    except Exception as e:
        print(f"¡ERROR DE MOTOR! {str(e)}")
    
    finally:
        # --- E. REPATRIACIÓN (LLM -> GPU) ---
        torch.cuda.empty_cache(); gc.collect()
        try:
            if hasattr(brain, 'model'): brain.model.to("cuda")
            elif hasattr(brain, 'pipeline'): brain.pipeline.model.to("cuda")
        except: pass
        
    return img
