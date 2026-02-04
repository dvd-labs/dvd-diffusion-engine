# ui_console.py v15.4 (Bridge to Notebook)
import ipywidgets as widgets
from IPython.display import display, HTML, Javascript
import time
import __main__ # <--- ESTE ES EL PARO: Conecta el archivo con el Notebook

def crear_interfaz(brain, motor, vram_logic, personality, jax_dna):
    chat_log = widgets.Output(layout={'height': '450px', 'overflow_y': 'scroll', 'border': '1px solid #30363d', 'padding': '10px'})
    gallery_output = widgets.Output()
    
    input_field = widgets.Text(placeholder='Habla con Jax...', layout=widgets.Layout(width='60%'))
    btn_send = widgets.Button(description='ENVIAR', button_style='success', layout=widgets.Layout(width='18%'))
    btn_gal = widgets.Button(description='🖼️ GALERÍA', layout=widgets.Layout(width='18%'))
    btn_gal.style.button_color = '#d35400'

    def imprimir(cont, tipo, es_img=False):
        with chat_log:
            mid = f"msg_{int(time.time()*1000)}"
            if tipo == "u": 
                display(HTML(f"<div id='{mid}' style='text-align:right; margin:5px;'><span style='background:#238636; color:white; padding:8px 12px; border-radius:12px; display:inline-block;'>{cont}</span></div>"))
            elif tipo == "ia":
                if es_img:
                    display(HTML(f"<div id='{mid}' style='margin:5px;'><b>📸 Jax envió una foto:</b></div>"))
                    display(cont)
                else:
                    display(HTML(f"<div id='{mid}' style='margin:5px;'><span style='background:#21262d; color:#c9d1d9; padding:8px 12px; border-radius:12px; border:1px solid #30363d; display:inline-block;'>{cont}</span></div>"))
            elif tipo == "sys":
                display(HTML(f"<div id='{mid}' style='text-align:center; font-size:11px; color:#f39c12; font-style:italic; margin:8px;'>{cont}</div>"))
            
            display(Javascript(f"var el=document.getElementById('{mid}'); if(el) el.scrollIntoView();"))

    def procesar(_=None):
        txt = input_field.value.strip()
        if not txt: return
        input_field.value = ""; imprimir(txt, "u")
        
        try:
            # --- ACCESO REAL AL NOTEBOOK ---
            # Buscamos en __main__ (el notebook) en lugar de globals() local
            raw_set = getattr(__main__, 'SETTINGS', "steps=15, cfg=5.5")
            neg_p = getattr(__main__, 'NEGATIVE_PROMPT', "low quality")
            ade = getattr(__main__, 'ADETAILER', False)
            
            if personality.analizar_intencion(txt):
                imprimir("📡 Jax está preparando la cámara...", "sys")
                
                # Reacción rápida de Jax
                reaccion = brain.hablar(f"Dime algo muy breve sobre: {txt}", personality.get_system_prompt('jax_dj'))
                imprimir(reaccion, "ia")
                
                imprimir(f"⚡ Generando con settings: {raw_set}", "sys")
                
                # Generar prompt técnico en inglés
                prompt_visual = brain.generar_prompt_visual(txt, jax_dna)
                
                # Disparo al motor
                img = vram_logic.generar_con_intercambio(
                    brain, motor, prompt_visual, 
                    raw_set, neg_p, ade, 
                    getattr(__main__, 'DETECTOR_STRENGTH', 0.35)
                )
                
                if img: imprimir(img, "ia", es_img=True)
                else: imprimir("⚠️ Falló el revelado.", "sys")
            else:
                imprimir("💬 Jax está escribiendo...", "sys")
                modo = getattr(__main__, 'MODO_JAX', 'jax_dj')
                sys_p = personality.get_system_prompt(modo, getattr(__main__, 'PROMPT_CUSTOM', ''))
                resp = brain.hablar(txt, sys_p)
                imprimir(resp, "ia")
                
        except Exception as e:
            imprimir(f"⚠️ ERROR: {str(e)}", "sys")

    btn_send.on_click(procesar)
    input_field.on_submit(procesar)
    
    display(widgets.VBox([chat_log, widgets.HBox([input_field, btn_send, btn_gal]), gallery_output]))
    with chat_log: imprimir("--- SISTEMA v15.4 ONLINE | BRIDGE ACTIVADO ---", "sys")
