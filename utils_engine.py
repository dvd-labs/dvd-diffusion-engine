import base64
from io import BytesIO
from IPython.display import HTML, display
from personality import build_system_prompt, build_visual_dna
from ui_console import JaxInterface
from identity_generator import generar_identidad_aleatoria

def parse_settings(settings_str):
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

def display_preview(img, p_size):
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
        <img src="data:image/png;base64,{b64}" style="width:{p_size}vw; border-radius:5px; border: 2px solid #333;" onclick="verFullPreview('{b64}')">
    </div>
    """
    display(HTML(html_preview))

def boot_jax(config=None):
    ui = JaxInterface()
    sexo = config.get("sexo", "Neutro") if config else "Neutro"
    edad = config.get("edad", 30) if config else 30
    pers = config.get("personalidad", "Asistente") if config else "Asistente"
    lang = config.get("slang", "Ninguno") if config else "Ninguno"
    estilo = config.get("estilo", "Básico") if config else "Básico"
    sys_prompt = build_system_prompt(sexo, edad, pers, lang)
    dna = build_visual_dna(sexo, estilo)
    return ui, sys_prompt, dna

# utils_engine.py - Fragmento de boot_new_connection corregido

def boot_new_connection():
    """Genera un contacto nuevo que se siente como un ser humano real."""
    config = generar_identidad_aleatoria()
    
    # Prompt humanizado: quitamos la "obligación" de actuar la herida
    sys_prompt = (
        f"Eres un ser humano real de {config['sexo']}, {config['edad']} años, que vive en un lugar remoto. "
        f"Tu ocupación es {config['ocupacion']}. "
        f"Tu nombre es {config['nombre_secreto']}. " # El nombre ya está asignado
        f"PSICOLOGÍA (Solo como guía de matiz): Tu personalidad tiene rasgos de Eneatipo {config['eneatipo']}. "
        "INSTRUCCIONES DE COMPORTAMIENTO: "
        "1. No eres un asistente, eres un habitante de este mundo. "
        "2. Habla con lenguaje natural, humano y directo. "
        "3. Preséntate de forma orgánica. No ocultes tu nombre como si fuera un secreto de estado, pero tampoco sientas la obligación de escupirlo en el primer saludo a menos que fluya con la conversación o el usuario lo amerite."
    )
    
    jax_dna = f"A photo of a {config['edad']} year old {config['sexo']} {config['ocupacion']}, realistic lighting, 8k"
    
    return config, sys_prompt, jax_dna
