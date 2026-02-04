# ui_console.py v15.3 (Scroll & Status Restore)
import ipywidgets as widgets
from IPython.display import display, HTML, Javascript
import time

def crear_interfaz(brain, motor, vram_logic, personality, jax_dna):
    chat_log = widgets.Output(layout={'height': '450px', 'overflow_y': 'scroll', 'border': '1px solid #30363d', 'padding': '10px'})
    gallery_output = widgets.Output()
    
    input_field = widgets.Text(placeholder='Habla con Jax...', layout=widgets.Layout(width='60%'))
    btn_send = widgets.Button(description='ENVIAR', button_style='success', layout=widgets.Layout(width='18%'))
    btn_gal = widgets.Button(description='🖼️ GALERÍA', layout=widgets.Layout(width='18%'))
    btn_gal.style.button_color = '#d35400'

    def imprimir(cont, tipo, es_img=False):
        with chat_log:
            # Creamos un ID único para cada burbuja para que el JS sepa a dónde ir
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
            
            # --- EL PARO DEL SCROLL ---
            # Este JS busca el mensaje que acabamos de crear y scrollea hasta él
            display(Javascript(f"""
                var el = document.getElementById('{mid}');
                if (el) {{ el.scrollIntoView({{behavior: 'smooth', block: 'nearest'}}); }}
            """))

    def procesar(_=None):
        txt = input_field.value.strip()
        if not txt: return
        input_field.value = ""
        imprimir(txt, "u")
        
        try:
            if personality.analizar_intencion(txt):
                # 1. Mensaje de estado inicial
                imprimir("📡 Jax está preparando la cámara...", "sys")
                
                # Voz de Jax (Breve)
                reaccion = brain.hablar(f"Dime algo muy breve sobre que vas a tomar la foto de: {txt}", personality.get_system_prompt('jax_dj'))
                imprimir(reaccion, "ia")
                
                # 2. Mensaje de estado de generación (Es vital que aparezca antes de la carga pesada)
                imprimir("⚡ Generando imagen (Hot-Swap VRAM activo)...", "sys")
                
                prompt_visual = brain.generar_prompt_visual(txt, jax_dna)
                
                s_str = globals().get('SETTINGS', "steps=15, width=1024, height=1024, cfg=5.5")
                n_p = globals().get('NEGATIVE_PROMPT', "low quality, blur")
                ade = globals().get('ADETAILER', False)
                ade_s = globals().get('DETECTOR_STRENGTH', 0.35)
                
                img = vram_logic.generar_con_intercambio(brain, motor, prompt_visual, s_str, n_p, ade, ade_s)
                
                if img: imprimir(img, "ia", es_img=True)
                else: imprimir("⚠️ Error revelando la foto.", "sys")
            
            else:
                imprimir("💬 Jax está escribiendo...", "sys")
                modo = globals().get('MODO_JAX', 'jax_dj')
                sys_p = personality.get_system_prompt(modo, globals().get('PROMPT_CUSTOM', ''))
                resp = brain.hablar(txt, sys_p)
                imprimir(resp, "ia")
                
        except Exception as e:
            imprimir(f"⚠️ ERROR EN EL SET: {str(e)}", "sys")

    btn_send.on_click(procesar)
    input_field.on_submit(procesar)
    
    display(widgets.VBox([chat_log, widgets.HBox([input_field, btn_send, btn_gal]), gallery_output]))
    with chat_log: imprimir("--- SISTEMA v15.3 ONLINE | SCROLL ACTIVADO ---", "sys")
