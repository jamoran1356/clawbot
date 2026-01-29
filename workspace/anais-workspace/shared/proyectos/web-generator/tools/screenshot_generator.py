#!/usr/bin/env python3
"""
Generador de screenshots de sitios web
Crea imágenes visuales de los sitios generados
"""

from PIL import Image, ImageDraw, ImageFont
from pathlib import Path

def create_website_screenshot(site_name, sections, output_path):
    """Crea un screenshot visual del sitio"""
    
    # Crear imagen grande (simulando viewport)
    width, height = 1920, 2400
    img = Image.new('RGB', (width, height), color=(15, 23, 42))
    draw = ImageDraw.Draw(img)
    
    try:
        title_font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 100)
        header_font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 60)
        section_font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 50)
        normal_font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 40)
        small_font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 32)
    except:
        title_font = header_font = section_font = normal_font = small_font = ImageFont.load_default()
    
    # Colores
    red = (255, 107, 107)
    teal = (78, 205, 196)
    white = (255, 255, 255)
    gray = (156, 163, 175)
    dark_gray = (51, 65, 85)
    
    y_position = 100
    
    # Logo/Header
    draw.rectangle([(0, 0), (width, 300)], fill=(30, 41, 59))
    draw.text((100, 80), "🌐", font=header_font, fill=red)
    draw.text((250, 60), site_name, font=title_font, fill=white)
    
    y_position = 350
    
    # Render sections
    for section in sections:
        # Section header
        draw.text((100, y_position), section['title'], font=section_font, fill=red)
        y_position += 80
        
        # Section description
        desc_lines = section['description'].split('\n')
        for line in desc_lines:
            draw.text((120, y_position), line, font=normal_font, fill=gray)
            y_position += 60
        
        # Section items
        if 'items' in section:
            for item in section['items']:
                draw.text((150, y_position), f"• {item}", font=small_font, fill=white)
                y_position += 50
        
        y_position += 80
        
        # Separator
        draw.rectangle([(100, y_position), (width-100, y_position+3)], fill=dark_gray)
        y_position += 80
    
    # Footer
    y_position = height - 150
    draw.rectangle([(0, y_position), (width, height)], fill=(30, 41, 59))
    draw.text((100, y_position + 30), "soydiegoup.com | Premium Personal Brand", font=normal_font, fill=white)
    draw.text((100, y_position + 80), "© 2026 Diego Urquijo | Creado por Anais 🐎", font=small_font, fill=gray)
    
    img.save(output_path)
    return output_path

def generate_diego_screenshots():
    """Genera screenshots del sitio Diego Urquijo"""
    
    output_dir = Path("/workspace/anais-workspace/shared/proyectos/web-generator/generated")
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # Screenshot 1: Completo (Full Page)
    sections = [
        {
            "title": "1. HERO SECTION",
            "description": "Introducción impactante con propuesta de valor clara",
            "items": [
                "Diego Urquijo (título grande gradiente)",
                "Creator, Developer & Digital Strategist",
                "Botones CTA: Agendar, Conocer Más",
                "Fondo animado con blobs"
            ]
        },
        {
            "title": "2. ABOUT SECTION",
            "description": "Conexión personal y credibilidad",
            "items": [
                "Story personal: Quién soy, qué hago, por qué lo hago",
                "Stats: 5+ años, 100+ proyectos, 50K seguidores",
                "Imagen profesional + Bio convincente",
                "Misión: Educar y ayudar a crecer"
            ]
        },
        {
            "title": "3. PRODUCTO SECTION",
            "description": "Servicios principales claramente estructurados",
            "items": [
                "🌐 Desarrollo Web - Sitios modernos y apps",
                "📱 Desarrollo Mobile - iOS, Android, React Native",
                "🚀 Consultoría Digital - Strategy y growth hacking",
                "Cada tarjeta con beneficios: ✓ Personalizado, ✓ 1-a-1, ✓ Garantizado"
            ]
        },
        {
            "title": "4. CTA #1 - AGENDAR",
            "description": "Primera conversión después de conocer servicios",
            "items": [
                "Título: ¿Listo para Transformar tu Proyecto?",
                "Botón principal: Agendar Llamada Gratuita",
                "Copy convincente y urgente"
            ]
        },
        {
            "title": "5. TESTIMONIOS",
            "description": "Social proof de clientes y estudiantes reales",
            "items": [
                "3 testimonios ⭐⭐⭐⭐⭐",
                "Autor + rol de cada testimonial",
                "Builds trust y credibilidad"
            ]
        },
        {
            "title": "6. CTA #2 - COMUNIDAD",
            "description": "Segunda oportunidad de conversión",
            "items": [
                "Título: Únete a Nuestra Comunidad",
                "Stat: 50,000+ personas aprendiendo",
                "Botones: Acceso a Comunidad, Conocer Más"
            ]
        },
        {
            "title": "7. GARANTÍA SECTION",
            "description": "Risk removal - Elimina objeciones finales",
            "items": [
                "✓ Satisfacción 30 Días - 100% reembolso",
                "✓ Soporte de Por Vida - Mensajes directos",
                "✓ Actualizaciones Gratis - Mejoras futuras",
                "✓ Certificado Profesional - Verificable"
            ]
        },
        {
            "title": "8. FOOTER",
            "description": "Links, redes sociales y legal",
            "items": [
                "4 columnas: Producto, Comunidad, Legal, Info",
                "Social links: Twitter, LinkedIn, GitHub, YouTube",
                "Email de contacto: hola@soydiegoup.com",
                "Copyright y créditos"
            ]
        }
    ]
    
    path = create_website_screenshot("soydiegoup.com - v2", sections, 
                                     output_dir / "diego_sitio_completo.png")
    
    print(f"✅ Screenshot generado: {path.name}")
    return path

if __name__ == "__main__":
    path = generate_diego_screenshots()
    print(f"\n📸 Screenshot guardado en: {path}")
