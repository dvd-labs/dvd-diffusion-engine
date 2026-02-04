# ui_console.py
import ipywidgets as widgets
from IPython.display import display, HTML, Javascript
import time

def crear_interfaz(brain, motor, vram_logic, personality, jax_dna):
    # --- ELEMENTOS VISUALES ---
    chat_log = widgets.Output(layout={'height': '450px', 'overflow_y': 'scroll', 'border': '1px solid #30363d', 'background_color': '#0d1117'})
    gallery_output = widgets.Output()
    
    input_field = widgets.Text(placeholder='Habla con Jax...', layout=widgets.Layout(width='60%'))
    btn_send = widgets.Button(description='ENVIAR', button_style='success', layout=widgets.Layout(width='18%'))
    btn_gal = widgets.Button(description='🖼️ GALERÍA', layout=widgets.Layout(width='18%'))
    btn_gal.style.button_color = '#d35400'

    # --- FUNCIONES INTERNAS ---
    def imprimir(cont, tipo, es_img=False):
        with chat_log:
            mid = f"msg_{int(time.time()*1000)}"
            if tipo == "u": display(HTML(f"<div class='u-bubble' style='background:#238636; color:white; padding:8px; margin:5px; border-radius:10px; align-self:flex-end;'>{cont}</div>"))
            elif tipo == "ia":
                if es_img: 
                    display(HTML("<b>📸 Jax envió una foto</b>"))
                    display(cont)
                else: display(HTML(f"<div class='a-bubble' style='background:#21262d; color:#c9d1d9; padding:8px; margin:5px; border-radius:10px; border:1px solid #30363d;'>{cont}</div>"))

    def procesar(_=None):
        txt = input_field.value.strip()
        if not txt: return
        input_field.value = ""; imprimir(txt, "u")
        
        try:
            # 1. ¿El usuario quiere ver algo?
            if personality.analizar_intencion(txt):
                # A. Jax reacciona con su voz (Conversación rápida)
                # Le pedimos algo breve para que no se suelte un discurso
                reaccion = brain.hablar(f"Dime algo muy breve sobre que vas a tomar la foto de: {txt}", personality.get_system_prompt('jax_dj'))
                imprimir(reaccion, "ia")
                
                imprimir("📸 *Jax ajustando el lente...*", "sys")
                
                # B. Generamos el prompt TÉCNICO (Sin que Jax hable)
                # Aquí usamos el método nuevo que solo escupe inglés para el SDXL
                prompt_visual = brain.generar_prompt_visual(txt, jax_dna)
                
                # C. Mandamos a la cámara
                img = vram_logic.generar_con_intercambio(
                    brain, motor, prompt_visual, 
                    globals().get('SETTINGS', ""), globals().get('NEGATIVE_PROMPT', ""),
                    globals().get('ADETAILER', False), globals().get('DETECTOR_STRENGTH', 0.35)
                )
                
                if img: 
                    imprimir(img, "ia", es_img=True)
                else:
                    imprimir("⚠️ Falló el flash, intenta de nuevo.", "sys")
            
            # 2. Es solo plática normal
            else:
                imprimir("Jax está escribiendo...", "sys")
                modo = globals().get('MODO_JAX', 'jax_dj')
                sys_p = personality.get_system_prompt(modo, globals().get('PROMPT_CUSTOM', ''))
                resp = brain.hablar(txt, sys_p)
                imprimir(resp, "ia")
                
        except Exception as e:
            imprimir(f"⚠️ Error en el set: {str(e)}", "sys")

    # --- CONEXIONES ---
    btn_send.on_click(procesar)
    input_field.on_submit(procesar)
    
    # Lanzar
    display(widgets.VBox([chat_log, widgets.HBox([input_field, btn_send, btn_gal]), gallery_output]))
