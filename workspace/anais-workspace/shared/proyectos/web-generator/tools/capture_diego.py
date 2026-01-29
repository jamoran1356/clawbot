#!/usr/bin/env python3
"""
Captura screenshot del sitio Diego Urquijo
"""

from html2image import Html2Image
from pathlib import Path

def capture_diego_site():
    """Captura screenshot del HTML de Diego"""
    
    try:
        # Crear instancia
        hti = Html2Image(size=(1920, 2400))
        
        # Leer archivo HTML
        html_path = "/workspace/anais-workspace/shared/proyectos/web-generator/generated/soydiegoup.html"
        output_path = "/workspace/anais-workspace/shared/proyectos/web-generator/generated/soydiegoup_preview.png"
        
        with open(html_path, 'r', encoding='utf-8') as f:
            html_content = f.read()
        
        # Crear directorio si no existe
        Path(output_path).parent.mkdir(parents=True, exist_ok=True)
        
        # Capturar
        hti.screenshot(html_string=html_content, save_as=output_path)
        
        print(f"✅ Screenshot capturado: {output_path}")
        return output_path
    except Exception as e:
        print(f"⚠️ Error con Html2Image: {e}")
        print("💡 Solución: Usa Firefox headless o exporta a PDF")
        return None

if __name__ == "__main__":
    capture_diego_site()
