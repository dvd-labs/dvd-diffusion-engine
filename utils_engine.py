# utils_engine.py
import base64
from io import BytesIO
from IPython.display import HTML, display
from personality import build_system_prompt, build_visual_dna
from ui_console import JaxInterface

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

def display_preview(img, p_size):
    """Genera el visor HTML con zoom para Colab."""
    buffered = BytesIO()
    img.save(buffered, format="PNG")
    b64 = base64.b64encode(buffered.getvalue()).decode()

    html_preview = f"""
    <script>
        function verFullPreview(b64) {{
            const byteCharacters = atob(b64);
            const byteNumbers = new Uint8Array(byteCharacters.length);
            for (let i = 0; i < byteCharacters.length; i++) byteNumbers[i] = byteCharacters.charCodeAt(i);
            const url = URL.createObjectURL(new Blob([byteNumbers], {{type: 'image/png'}}));
            window.open(url, '_blank');
        }}
    </script>
    <div style="margin: 10px 0;">
        <img src="data:image/png;base64,{{b64}}"
             style="width:{{p_size}}vw; border-radius:5px; cursor:zoom-in; border: 2px solid #333;"
             onclick="verFullPreview('{{b64}}')">
        <p style="color:#666; font-size:10px;">Clic para tamaño original</p>
    </div>
    """
    display(HTML(html_preview))

def boot_jax(config=None):
    """
    Inicializa la interfaz y genera los prompts. 
    Si no se pasa config, usa valores neutros por defecto.
    """
    ui = JaxInterface()
    
    # Si no hay config, forzamos el modo 'Asistente Aburrido'
    sexo = config.get("sexo", "Neutro") if config else "Neutro"
    edad = config.get("edad", 30) if config else 30
    pers = config.get("personalidad", "Asistente") if config else "Asistente"
    lang = config.get("slang", "Ninguno") if config else "Ninguno"
    estilo = config.get("estilo", "Básico") if config else "Básico"

    sys_prompt = build_system_prompt(sexo, edad, pers, lang)
    dna = build_visual_dna(sexo, estilo)
    
    return ui, sys_prompt, dna
