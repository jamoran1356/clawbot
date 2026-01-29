#!/usr/bin/env python3
"""
Research CLI - Interfaz de línea de comandos para investigación web
"""

import asyncio
import json
import sys
from pathlib import Path
from research_engine import WebResearchEngine

async def interactive_research():
    """Modo interactivo"""
    
    print("\n" + "="*60)
    print("🔬 WEB RESEARCH ENGINE - Modo Interactivo")
    print("="*60)
    
    engine = WebResearchEngine()
    
    while True:
        print("\n📋 Opciones:")
        print("  1. Búsqueda simple")
        print("  2. Investigación profunda")
        print("  3. Investigación con subtópicos")
        print("  4. Salir")
        
        choice = input("\n👉 Elige una opción (1-4): ").strip()
        
        if choice == "1":
            query = input("🔍 ¿Qué deseas buscar?: ").strip()
            if query:
                results = await engine.google_search(query, num_results=5)
                print(f"\n✅ Encontrados {len(results)} resultados")
                for i, r in enumerate(results, 1):
                    print(f"\n{i}. {r['title']}")
                    print(f"   {r['snippet'][:150]}...")
        
        elif choice == "2":
            query = input("🔍 ¿Qué deseas investigar?: ").strip()
            if query:
                research = await engine.search_and_analyze(query, depth=3)
                engine.save_research(research)
                engine.print_report(research)
        
        elif choice == "3":
            topic = input("📌 Tópico principal: ").strip()
            subs = input("📌 Subtópicos (separados por coma): ").strip()
            if topic:
                subtopics = [s.strip() for s in subs.split(",") if s.strip()]
                research = await engine.research_topic(topic, subtopics)
                engine.save_research(research)
                engine.print_report(research)
        
        elif choice == "4":
            print("👋 ¡Hasta luego!")
            break
        
        else:
            print("❌ Opción inválida")

async def cli_research(query: str, depth: int = 3, subtopics: str = None):
    """Investigación desde CLI"""
    
    engine = WebResearchEngine()
    
    if subtopics:
        subs = [s.strip() for s in subtopics.split(",")]
        research = await engine.research_topic(query, subs)
    else:
        research = await engine.search_and_analyze(query, depth)
    
    engine.save_research(research)
    engine.print_report(research)
    
    return research

def main():
    """Punto de entrada"""
    
    if len(sys.argv) < 2:
        # Modo interactivo
        asyncio.run(interactive_research())
    else:
        # Modo CLI
        if sys.argv[1] == "--help" or sys.argv[1] == "-h":
            print("""
Web Research Engine - CLI

Uso:
  python research_cli.py                    # Modo interactivo
  python research_cli.py "query"            # Búsqueda simple
  python research_cli.py "query" --depth 5  # Con profundidad
  python research_cli.py "query" --subs "sub1,sub2"  # Con subtópicos

Ejemplos:
  python research_cli.py "AI 2026"
  python research_cli.py "FastAPI" --depth 5
  python research_cli.py "Web3" --subs "blockchain,crypto,NFTs"
            """)
        else:
            query = sys.argv[1]
            depth = 3
            subtopics = None
            
            # Parse arguments
            for i, arg in enumerate(sys.argv[2:]):
                if arg == "--depth" and i+2 < len(sys.argv):
                    depth = int(sys.argv[i+3])
                elif arg == "--subs" and i+2 < len(sys.argv):
                    subtopics = sys.argv[i+3]
            
            asyncio.run(cli_research(query, depth, subtopics))

if __name__ == "__main__":
    main()
