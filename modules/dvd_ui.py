import json, base64
from IPython.display import HTML, display
from io import BytesIO

# Agregué preview_percent a los argumentos para que jale el tamaño
def mostrar_tarjeta_galeria(img, meta, filename, steps, wd, ht, cfg, seed, prompt, neg, preview_percent):
    # 1. Convertir imagen a Base64
    buffered = BytesIO()
    img.save(buffered, format="PNG", pnginfo=meta)
    b64 = base64.b64encode(buffered.getvalue()).decode()
    
    # 2. String para copiar
    settings_str = f"steps={steps}, width={wd}, height={ht}, cfg={cfg}, seed={seed}"
    
    # 3. HTML del Visualizador
    html_code = f"""
    <style>
        .gallery-item {{ background: #000; padding: 15px; border-radius: 10px; display: inline-block; border: 1px solid #333; }}
        .controls {{ display: grid; grid-template-columns: 1fr 1fr; gap: 5px; margin-top: 10px; }}
        .btn-mini {{ border: none; padding: 6px; border-radius: 4px; font-size: 10px; cursor: pointer; color: white; font-weight: bold; text-transform: uppercase; }}
        .btn-copy-p {{ background: #27ae60; }} .btn-copy-n {{ background: #c0392b; }} .btn-copy-s {{ background: #2980b9; grid-column: span 2; }}
        .btn-dl {{ background: #f39c12; color: #000; grid-column: span 2; margin-top: 5px; font-size: 11px; }}
    </style>
    <script>
        function copyToClip(text) {{
            if (navigator.clipboard) {{ navigator.clipboard.writeText(text).then(() => alert('Copiado')).catch(err => alert('Error al copiar')); }}
            else {{
                var textarea = document.createElement('textarea');
                textarea.value = text;
                document.body.appendChild(textarea);
                textarea.select();
                document.execCommand('copy');
                document.body.removeChild(textarea);
                alert('Copiado (Fallback)');
            }}
        }}
        function openBlob(b64) {{
            const byteCharacters = atob(b64);
            const byteNumbers = new Array(byteCharacters.length);
            for (let i = 0; i < byteCharacters.length; i++) byteNumbers[i] = byteCharacters.charCodeAt(i);
            const blob = new Blob([new Uint8Array(byteNumbers)], {{type: 'image/png'}});
            const url = URL.createObjectURL(blob);
            window.open(url, '_blank');
        }}
        function downloadBlob(b64, fname) {{
            const link = document.createElement('a');
            link.href = 'data:image/png;base64,' + b64;
            link.download = fname;
            link.click();
        }}
    </script>
    <div class="gallery-item">
        <img src="data:image/png;base64,{b64}"
             style="width:{preview_percent}vw; border-radius:8px; cursor:zoom-in;"
             onclick="openBlob('{b64}')">
        <div class="controls">
            <button class="btn-mini btn-copy-p" onclick='copyToClip({json.dumps(prompt)})'>Copiar Prompt</button>
            <button class="btn-mini btn-copy-n" onclick='copyToClip({json.dumps(neg)})'>Copiar Negative</button>
            <button class="btn-mini btn-copy-s" onclick='copyToClip("{settings_str}")'>Copiar Settings</button>
            <button class="btn-mini btn-dl" onclick="downloadBlob('{b64}', '{filename}')">💾 DESCARGAR ORIGINAL</button>
        </div>
    </div>
    """
    display(HTML(html_code))
