#!/usr/bin/env python3
"""
Crea previsualizaciones visuales del sitio Diego Urquijo
"""

from PIL import Image, ImageDraw, ImageFont
from pathlib import Path

def create_diego_preview():
    """Crea previsualizaciones del sitio"""
    
    # Crear directorio
    output_dir = Path("/workspace/anais-workspace/shared/proyectos/web-generator/generated")
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # 1. Hero Section Preview
    img = Image.new('RGB', (1920, 1080), color=(15, 24, 42))
    draw = ImageDraw.Draw(img)
    
    try:
        title_font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 120)
        header_font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 48)
        normal_font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 32)
    except:
        title_font = header_font = normal_font = ImageFont.load_default()
    
    # Gradiente rojo
    red = (255, 107, 107)
    white = (255, 255, 255)
    gray = (156, 163, 175)
    
    # Contenido
    draw.text((100, 150), "Diego Urquijo", font=title_font, fill=red)
    draw.text((100, 300), "Creator, Developer & Digital Strategist", font=header_font, fill=white)
    draw.text((100, 400), "Construyo experiencias digitales innovadoras", font=normal_font, fill=gray)
    
    # Botones
    draw.rectangle([(100, 550), (400, 650)], fill=red)
    draw.text((130, 575), "Explorar Mi Trabajo", font=header_font, fill=white)
    
    draw.rectangle([(450, 550), (750, 650)], outline=red, width=3)
    draw.text((480, 575), "Contactarme", font=header_font, fill=red)
    
    # Stats
    y = 800
    stats = [
        ("5+", "Años de Experiencia"),
        ("100+", "Proyectos Completados"),
        ("50K+", "Seguidores"),
        ("5K+", "Estudiantes")
    ]
    
    x_start = 100
    for val, label in stats:
        draw.text((x_start, y), val, font=title_font, fill=red)
        draw.text((x_start, y+100), label, font=normal_font, fill=gray)
        x_start += 420
    
    hero_path = output_dir / "diego_01_hero.png"
    img.save(hero_path)
    print(f"✅ Preview 1 guardado: {hero_path}")
    
    # 2. Portfolio Section
    img2 = Image.new('RGB', (1920, 1440), color=(15, 24, 42))
    draw2 = ImageDraw.Draw(img2)
    
    draw2.text((100, 100), "Portafolio Destacado", font=title_font, fill=red)
    
    projects = [
        ("🎓", "SoyDiegoUp - Comunidad Tech", "Plataforma educativa con miles de estudiantes"),
        ("⚙️", "Portfolio API Generator", "Herramienta Open Source para desarrolladores"),
        ("📊", "Digital Strategy Consulting", "Consultoría a empresas en transformación digital")
    ]
    
    y = 300
    for i, (emoji, title, desc) in enumerate(projects):
        # Card
        x = 100 + (i % 3) * 590
        if i == 2:
            x = 100
            y += 350
        
        draw2.rectangle([(x, y), (x+550, y+300)], outline=(100, 116, 139), width=2)
        draw2.text((x+30, y+30), emoji, font=title_font, fill=red)
        draw2.text((x+30, y+100), title, font=header_font, fill=white)
        draw2.text((x+30, y+200), desc, font=normal_font, fill=gray)
    
    portfolio_path = output_dir / "diego_02_portfolio.png"
    img2.save(portfolio_path)
    print(f"✅ Preview 2 guardado: {portfolio_path}")
    
    # 3. Services Section
    img3 = Image.new('RGB', (1920, 1080), color=(15, 24, 42))
    draw3 = ImageDraw.Draw(img3)
    
    draw3.text((100, 100), "Servicios", font=title_font, fill=red)
    
    services = [
        ("🌐", "Desarrollo Web"),
        ("📱", "Desarrollo Mobile"),
        ("🚀", "Consultoría Digital"),
        ("👨‍🏫", "Educación & Mentoría")
    ]
    
    x_pos = 100
    for emoji, service in services:
        draw3.text((x_pos, 400), emoji, font=title_font, fill=red)
        draw3.text((x_pos, 550), service, font=header_font, fill=white)
        x_pos += 420
    
    services_path = output_dir / "diego_03_services.png"
    img3.save(services_path)
    print(f"✅ Preview 3 guardado: {services_path}")
    
    return [hero_path, portfolio_path, services_path]

if __name__ == "__main__":
    files = create_diego_preview()
    print(f"\n✅ {len(files)} previsualizaciones creadas")
    for f in files:
        print(f"  - {f.name}")
