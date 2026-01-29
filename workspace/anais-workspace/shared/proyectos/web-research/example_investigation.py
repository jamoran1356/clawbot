#!/usr/bin/env python3
"""
Ejemplo: Investigación web completa sobre "AI en 2026"
"""

import asyncio
import json
from research_engine import WebResearchEngine

async def main():
    """Ejecuta investigación de ejemplo"""
    
    engine = WebResearchEngine()
    
    print("\n" + "="*70)
    print("🔬 EJEMPLO: Investigación sobre 'Artificial Intelligence 2026'")
    print("="*70)
    
    # Investigación con subtópicos
    research = await engine.research_topic(
        "Artificial Intelligence 2026",
        subtopics=[
            "machine learning trends",
            "neural networks",
            "AI applications"
        ]
    )
    
    # Guardar resultados
    path = engine.save_research(research, "ai_2026_investigation.json")
    
    # Imprimir reporte
    engine.print_report(research)
    
    # Mostrar estadísticas
    print("\n" + "="*70)
    print("📊 ESTADÍSTICAS")
    print("="*70)
    
    print(f"\n📍 Investigaciones Ejecutadas: {len(research['investigations'])}")
    
    for topic, investigation in research['investigations'].items():
        summary = investigation['summary']
        print(f"\n  🔍 {topic}")
        print(f"     - Fuentes encontradas: {summary['total_sources']}")
        print(f"     - Contenido extraído: {summary['total_extracted']}")
        print(f"     - Contenido analizado: {summary['total_analyzed']}")
        print(f"     - Relevancia promedio: {summary['avg_relevance']:.1f}%")
    
    # Mostrar archivos
    print(f"\n📁 Archivo guardado: {path}")
    print(f"   Tamaño: {path.stat().st_size / 1024:.1f} KB")
    
    print("\n✅ Investigación completada\n")

if __name__ == "__main__":
    asyncio.run(main())
