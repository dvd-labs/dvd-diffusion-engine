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
        
        # Lógica de Intención (Desde personality.py)
        if personality.analizar_intencion(txt):
            imprimir("Jax está preparando la cámara...", "ia")
            # Usamos globals() para sacar los settings del notebook
            prompt_visual = brain.hablar(f"Describe: {txt}. Context: {jax_dna}", "System: Visual Prompter.")
            img = vram_logic.generar_con_intercambio(
                brain, motor, prompt_visual, 
                globals().get('SETTINGS', ""), globals().get('NEGATIVE_PROMPT', ""),
                globals().get('ADETAILER', False), globals().get('DETECTOR_STRENGTH', 0.35)
            )
            if img: imprimir(img, "ia", es_img=True)
        else:
            resp = brain.hablar(txt, personality.get_system_prompt(globals().get('MODO_JAX', 'jax_dj')))
            imprimir(resp, "ia")

    # --- CONEXIONES ---
    btn_send.on_click(procesar)
    input_field.on_submit(procesar)
    
    # Lanzar
    display(widgets.VBox([chat_log, widgets.HBox([input_field, btn_send, btn_gal]), gallery_output]))
