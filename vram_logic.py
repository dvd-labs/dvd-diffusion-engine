%%writefile vram_logic.py
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
    except: pass
    return kwargs

def generar_con_intercambio(brain, motor, prompt, settings_str, neg_prompt, ade_on, ade_str):
    # --- A. DESALOJO RÁPIDO (LLM -> CPU Float16) ---
    # El truco: dtype=torch.float16 evita que se infle en RAM.
    try:
        if hasattr(brain, 'model'): 
            brain.model.to("cpu", dtype=torch.float16)
        elif hasattr(brain, 'pipeline'): 
            brain.pipeline.model.to("cpu", dtype=torch.float16)
        
        # Vaciamos solo caché de GPU, evitamos gc.collect() excesivo
        torch.cuda.empty_cache()
    except: pass

    # --- B. CONFIGURACIÓN ---
    kwargs = parse_settings(settings_str)
    img = None
    
    try:
        # --- C. GENERACIÓN ---
        # Aseguramos que el motor sepa que tiene vía libre
        if hasattr(motor, 'pipe'):
            # Si el motor estaba dormido, esto lo despierta rápido si tienes .to() implementado
            # Si no, confiamos en que StableDiffusionPipeline maneja su device map
            pass

        img, meta, path = motor.generar(prompt=prompt, neg_prompt=neg_prompt, **kwargs)

        # --- D. ADETAILER ---
        if ade_on:
            display(HTML("<b style='color: #f39c12;'>[*] Aplicando Adetailer...</b>"))
            img = motor.aplicar_adetailer(img, prompt, neg_prompt, strength=ade_str)
            img.save(path.replace(".png", "_fixed.png"), pnginfo=meta)
            
    except Exception as e:
        print(f"¡ERROR DE MOTOR! {str(e)}")
    
    finally:
        # --- E. REPATRIACIÓN RÁPIDA (LLM -> GPU) ---
        torch.cuda.empty_cache() # Limpieza rápida de VRAM visual
        try:
            if hasattr(brain, 'model'): 
                brain.model.to("cuda")
            elif hasattr(brain, 'pipeline'): 
                brain.pipeline.model.to("cuda")
        except: pass
        
    return img
