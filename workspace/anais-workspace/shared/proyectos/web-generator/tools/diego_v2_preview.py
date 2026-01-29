#!/usr/bin/env python3
"""
Previsualizaciones visuales del sitio Diego Urquijo v2
"""

from PIL import Image, ImageDraw, ImageFont
from pathlib import Path

def create_preview_image(title, content, emoji, output_path):
    """Crea una imagen de preview"""
    img = Image.new('RGB', (1920, 1080), color=(15, 24, 42))
    draw = ImageDraw.Draw(img)
    
    try:
        header_font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 72)
        normal_font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 32)
        small_font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 24)
    except:
        header_font = normal_font = small_font = ImageFont.load_default()
    
    red = (255, 107, 107)
    white = (255, 255, 255)
    gray = (156, 163, 175)
    
    # Emoji grande
    draw.text((1800, 100), emoji, font=header_font, fill=red)
    
    # Título
    draw.text((100, 150), title, font=header_font, fill=white)
    
    # Contenido
    y = 350
    for line in content:
        draw.text((100, y), line, font=normal_font, fill=gray)
        y += 80
    
    img.save(output_path)
    return output_path

def create_diego_v2_previews():
    """Crea previsualizaciones del sitio v2"""
    
    output_dir = Path("/workspace/anais-workspace/shared/proyectos/web-generator/generated")
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # Preview 1: Hero & About
    preview1 = create_preview_image(
        "HERO & ABOUT",
        [
            "✨ Bienvenido a Soydiegoup",
            "Diego Urquijo",
            "Creator, Developer & Digital Strategist",
            "5+ Años de Experiencia | 100+ Proyectos | 50K+ Seguidores"
        ],
        "🚀",
        output_dir / "diego_v2_01_hero_about.png"
    )
    
    # Preview 2: Producto & Servicios
    preview2 = create_preview_image(
        "MI PRODUCTO",
        [
            "🌐 Desarrollo Web",
            "📱 Desarrollo Mobile",
            "🚀 Consultoría Digital",
            "✓ Personalizado | ✓ 1-a-1 Support | ✓ Garantizado"
        ],
        "💼",
        output_dir / "diego_v2_02_producto.png"
    )
    
    # Preview 3: Testimonios & Garantía
    preview3 = create_preview_image(
        "TESTIMONIOS & GARANTÍA",
        [
            "⭐⭐⭐⭐⭐ Testimonios Verificados",
            "🛡️ Garantía 30 Días",
            "💰 100% Reembolso si no estás satisfecho",
            "✓ Soporte de Por Vida | ✓ Actualizaciones Gratis"
        ],
        "⭐",
        output_dir / "diego_v2_03_testimonios_garantia.png"
    )
    
    # Preview 4: CTA & Footer
    preview4 = create_preview_image(
        "LLAMADAS A LA ACCIÓN",
        [
            "1️⃣ Agendar Llamada Gratuita",
            "2️⃣ Acceso a Comunidad",
            "3️⃣ Empezar Sin Riesgo",
            "50,000+ Personas Aprendiendo y Creciendo"
        ],
        "📞",
        output_dir / "diego_v2_04_cta_footer.png"
    )
    
    return [preview1, preview2, preview3, preview4]

if __name__ == "__main__":
    files = create_diego_v2_previews()
    print(f"\n✅ {len(files)} previsualizaciones v2 creadas:\n")
    for f in files:
        print(f"  📸 {f.name}")
