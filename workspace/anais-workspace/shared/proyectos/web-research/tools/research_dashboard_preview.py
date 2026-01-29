#!/usr/bin/env python3
"""
Previsualizaciones visuales del Dashboard de Investigación
"""

from PIL import Image, ImageDraw, ImageFont
from pathlib import Path

def create_preview(title, sections, emoji, output_path):
    """Crea una preview del dashboard"""
    img = Image.new('RGB', (1920, 1080), color=(15, 23, 42))
    draw = ImageDraw.Draw(img)
    
    try:
        title_font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 80)
        header_font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 48)
        normal_font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 32)
    except:
        title_font = header_font = normal_font = ImageFont.load_default()
    
    # Colores
    indigo = (99, 102, 241)
    white = (255, 255, 255)
    gray = (156, 163, 175)
    
    # Fondo degradado simple
    draw.rectangle([(0, 0), (1920, 200)], fill=(30, 41, 59))
    
    # Header
    draw.text((100, 50), emoji, font=title_font, fill=indigo)
    draw.text((250, 60), title, font=header_font, fill=white)
    
    # Contenido
    y = 300
    for section in sections:
        draw.rectangle([(100, y), (1820, y+120)], outline=indigo, width=2)
        draw.text((130, y+30), section, font=normal_font, fill=white)
        y += 160
    
    img.save(output_path)
    return output_path

def create_previews():
    """Crea todas las previsualizaciones"""
    
    output_dir = Path("/workspace/anais-workspace/shared/proyectos/web-research/generated")
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # Preview 1: Hero
    create_preview(
        "Research Dashboard - Hero Section",
        [
            "🔍 Search Box: 'Investiga la Web'",
            "⚡ Depth Selector: Normal, Profunda, Exhaustiva",
            "📊 Features: Búsqueda Global, Análisis Profundo, Resultados Rápidos"
        ],
        "🔬",
        output_dir / "research_01_hero.png"
    )
    
    # Preview 2: Results
    create_preview(
        "Research Dashboard - Results Section",
        [
            "📈 Stats: 15 Resultados, 12 Extraídos, 12 Analizados, 82% Relevancia",
            "🔗 Result Cards: Título, Snippet, Score, Fuente",
            "💾 Download: JSON Export Button"
        ],
        "📊",
        output_dir / "research_02_results.png"
    )
    
    # Preview 3: Examples
    create_preview(
        "Research Dashboard - Examples Section",
        [
            "🤖 AI 2026: Machine Learning, Neural Networks, Aplicaciones",
            "⚡ FastAPI: Performance, Async, Tutoriales",
            "🔗 Web3: Blockchain, Crypto, Smart Contracts"
        ],
        "💡",
        output_dir / "research_03_examples.png"
    )
    
    # Preview 4: Features
    create_preview(
        "Research Dashboard - Technical Features",
        [
            "🔍 Búsqueda Avanzada: Multi-source, Filtering, Keywords, Metadata",
            "📊 Análisis: HTML Extraction, Scoring, Multi-stage, Reports",
            "⚡ Performance: Async, Rate Limiting, Caching, Real-time"
        ],
        "✨",
        output_dir / "research_04_features.png"
    )
    
    print("\n✅ Previsualizaciones del Dashboard creadas:\n")
    for f in output_dir.glob("research_*.png"):
        print(f"  📸 {f.name}")

if __name__ == "__main__":
    create_previews()
