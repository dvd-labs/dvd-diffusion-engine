# ui_console.py v15.8 (The Bulletproof Scroll)
import ipywidgets as widgets
from IPython.display import display, HTML, Javascript
import time
import __main__

def crear_interfaz(brain, motor, vram_logic, personality, p_dict):
    # El chat_log es nuestra zona de guerra
    chat_log = widgets.Output(layout={'height': '450px', 'overflow_y': 'scroll', 'border': '1px solid #30363d', 'padding': '10px'})
    input_field = widgets.Text(placeholder='Habla con el desconocido...', layout=widgets.Layout(width='60%'))
    btn_send = widgets.Button(description='ENVIAR', button_style='success')

    def imprimir(cont, tipo, es_img=False):
        with chat_log:
            # ID único para este mensaje
            mid = f"msg_{int(time.time()*1000)}"
            
            # Renderizado de burbujas
            if tipo == "u": 
                display(HTML(f"<div id='{mid}' style='text-align:right; margin:5px;'><span style='background:#238636; color:white; padding:8px 12px; border-radius:12px; display:inline-block;'>{cont}</span></div>"))
            elif tipo == "ia":
                style = "background:#21262d; color:#c9d1d9; padding:8px 12px; border-radius:12px; border:1px solid #30363d; display:inline-block;"
                if es_img:
                    display(HTML(f"<div id='{mid}' style='margin:5px;'><b>📸 Enviado:</b></div>"))
                    display(cont)
                else:
                    display(HTML(f"<div id='{mid}' style='margin:5px;'><span style='{style}'>{cont}</span></div>"))
            elif tipo == "sys":
                display(HTML(f"<div id='{mid}' style='text-align:center; font-size:11px; color:#f39c12; font-style:italic; margin:8px;'>{cont}</div>"))
            
            # --- EL PARO TÉCNICO DEL SCROLL v15.8 ---
            # 'block: "nearest"' evita que la ventana del navegador salte.
            # 'inline: "start"' asegura que se alinee al contenedor del widget.
            display(Javascript(f"""
                (function() {{
                    var el = document.getElementById('{mid}');
                    if (el) {{
                        el.scrollIntoView({{ behavior: "smooth", block: "nearest", inline: "start" }});
                    }}
                }})();
            """))

    def procesar(_=None):
        txt = input_field.value.strip()
        if not txt: return
        input_field.value = ""; imprimir(txt, "u")
        try:
            p_dict['custom_prompt'] = getattr(__main__, 'PROMPT_CUSTOM', '')
            if personality.analizar_intencion(txt):
                imprimir("📡 Preparando cámara...", "sys")
                sys_p = personality.get_system_prompt(p_dict)
                reaccion = brain.hablar(f"Dime algo breve sobre: {txt}", sys_p)
                imprimir(reaccion, "ia")
                jax_dna = personality.get_visual_dna(p_dict)
                prompt_visual = brain.generar_prompt_visual(txt, jax_dna)
                img = vram_logic.generar_con_intercambio(brain, motor, prompt_visual, getattr(__main__, 'SETTINGS', "steps=15, cfg=5.5"), getattr(__main__, 'NEGATIVE_PROMPT', "low quality"), getattr(__main__, 'ADETAILER', False), getattr(__main__, 'DETECTOR_STRENGTH', 0.35))
                if img: imprimir(img, "ia", es_img=True)
            else:
                imprimir("💬 Escribiendo...", "sys")
                sys_p = personality.get_system_prompt(p_dict)
                resp = brain.hablar(txt, sys_p)
                imprimir(resp, "ia")
        except Exception as e:
            imprimir(f"⚠️ ERROR: {str(e)}", "sys")

    btn_send.on_click(procesar)
    input_field.on_submit(procesar)
    display(widgets.VBox([chat_log, widgets.HBox([input_field, btn_send])]))
