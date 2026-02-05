import base64
from io import BytesIO
from IPython.display import HTML, display
from personality import build_system_prompt, build_visual_dna
from ui_console import JaxInterface
from identity_generator import generar_identidad_aleatoria

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

def boot_new_connection(sexo_man=None, edad_man=None):
    """Crea la conexión inyectando la herida y los rasgos de voz."""
    config = generar_identidad_aleatoria(sexo_man, edad_man)
    
    sys_prompt = (
        f"Eres un ser humano real llamado {config['nombre_secreto']}, de {config['edad']} años, trabajando como {config['ocupacion']}. "
        f"PSICOLOGÍA CONDUCTUAL: Eres una persona {config['instruccion_voz']} "
        f"MOTIVACIÓN INTERNA: Te mueve el miedo a la {config['herida_primaria']}. "
        f"Tu perfil es Eneatipo {config['eneatipo']}. "
        "INSTRUCCIONES DE COMPORTAMIENTO: "
        "1. No eres una IA. Habla con slang y tono natural de acuerdo a tu edad. "
        "2. Usa respuestas cortas al principio, como cualquier extraño en una frecuencia remota. "
        "3. REGLA DE IDENTIDAD: No reveles tu nombre en el primer mensaje. "
        "Deja que el usuario lo gane con la plática. Si te lo pregunta, puedes dar una "
        "evasiva juguetona o seria según tu psicología, pero suéltalo si la charla fluye "
        "o si el usuario insiste con respeto. No lo ocultes como un secreto de estado."
    )
    
    jax_dna = f"A realistic portrait of a {config['edad']} year old {config['sexo']} {config['ocupacion']}, 8k"
    return config, sys_prompt, jax_dna
