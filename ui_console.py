# ui_console.py
import ipywidgets as widgets
from IPython.display import display, HTML, Javascript
import time

CSS_ESTILOS = """
<style>
    .msg-box { font-family: sans-serif; font-size: 14px; margin: 8px 0; line-height: 1.4; display: flex; flex-direction: column; }
    .u-bubble { background: #238636; color: white; padding: 8px 12px; border-radius: 12px; border-bottom-right-radius: 2px; align-self: flex-end; max-width: 80%; text-align: right; }
    .a-bubble { background: #21262d; color: #c9d1d9; padding: 8px 12px; border-radius: 12px; border-bottom-left-radius: 2px; align-self: flex-start; max-width: 80%; border: 1px solid #30363d; }
    .sys-msg { font-size: 11px; color: #8b949e; text-align: center; font-style: italic; margin: 5px 0; }
</style>
"""

class JaxInterface:
    def __init__(self):
        self.chat_log = widgets.Output(layout={'height': '500px', 'overflow_y': 'scroll', 'border': '1px solid #30363d', 'background_color': '#0d1117', 'padding': '10px'})
        self.input_field = widgets.Text(placeholder='Escribe algo...', layout=widgets.Layout(width='80%'))
        self.btn_send = widgets.Button(description='ENVIAR', button_style='success', layout=widgets.Layout(width='18%'))
        
    def imprimir(self, cont, tipo, es_img=False):
        with self.chat_log:
            mid = f"msg_{int(time.time()*1000)}"
            if tipo == "u": display(HTML(f"<div class='msg-box' id='{mid}'><div class='u-bubble'>{cont}</div></div>"))
            elif tipo == "sys": display(HTML(f"<div class='msg-box' id='{mid}'><div class='sys-msg'>{cont}</div></div>"))
            elif tipo == "ia":
                if es_img and cont:
                    display(HTML(f"<div class='msg-box' id='{mid}'><div class='a-bubble'>📸 <i>Jax adjuntó una imagen</i></div></div>"))
                    display(cont)
                else:
                    display(HTML(f"<div class='msg-box' id='{mid}'><div class='a-bubble'>{cont}</div></div>"))
            display(Javascript(f"var e=document.getElementById('{mid}');if(e)e.scrollIntoView({{behavior:'smooth',block:'nearest',inline:'start'}});"))

    def render(self):
        display(HTML(CSS_ESTILOS))
        display(widgets.VBox([self.chat_log, widgets.HBox([self.input_field, self.btn_send])]))
