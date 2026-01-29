#!/usr/bin/env python3
"""
Bounty Hunter CLI - Interfaz de línea de comandos
Gestiona búsqueda y seguimiento de recompensas
"""

import sys
import json
from pathlib import Path
from bounty_engine import BountyHunter, BountyOrganizer, BountyAnalyzer

def print_header(text):
    """Imprime encabezado formateado"""
    print(f"\n{'='*60}")
    print(f"🎯 {text}")
    print(f"{'='*60}\n")

def cmd_list_bounties(hunter: BountyHunter):
    """Lista todos los bounties activos"""
    print_header("LISTA DE BOUNTIES ACTIVOS")
    
    for bounty in hunter.bounties:
        if bounty['status'] == 'active':
            print(f"ID: {bounty['id']}")
            print(f"Plataforma: {bounty['platform']}")
            print(f"Título: {bounty['title']}")
            print(f"Recompensa: ${bounty['avg_reward']:,}")
            print(f"Tiempo Est: {bounty['estimated_time']}h")
            print()

def cmd_quick_wins(hunter: BountyHunter):
    """Muestra rápidas ganancias"""
    print_header("QUICK WINS (Rápida aprobación y alta rentabilidad)")
    
    quick_wins = hunter.get_quick_wins()
    
    for i, bounty in enumerate(quick_wins, 1):
        roi = bounty['roi']
        print(f"{i}. {bounty['platform']} - {bounty['title']}")
        print(f"   Recompensa: ${roi['avg_reward']:,}")
        print(f"   $/Hora: ${roi['hourly_rate']:.0f}")
        print(f"   Tiempo: {bounty['estimated_time']}h")
        print(f"   Aprobación: {bounty['approval_time']}")
        print()

def cmd_top_profitable(hunter: BountyHunter):
    """Muestra top bounties por rentabilidad"""
    print_header("TOP 10 POR RENTABILIDAD ($/Hora)")
    
    portfolio = hunter.get_portfolio()
    
    for i, bounty in enumerate(portfolio['top_10_by_profitability'][:10], 1):
        roi = bounty['roi']
        print(f"{i}. {bounty['platform']} - {bounty['title']}")
        print(f"   $/Hora: ${roi['hourly_rate']:.0f}")
        print(f"   Recompensa: ${roi['avg_reward']:,}")
        print(f"   Tiempo: {bounty['estimated_time']}h")
        print(f"   Severidad: {bounty['severity']}")
        print()

def cmd_create_folders(hunter: BountyHunter):
    """Crea carpetas para top bounties"""
    print_header("CREANDO CARPETAS PARA BOUNTIES")
    
    base_path = Path("/workspace/anais-workspace/shared/proyectos/bounty-hunter/bounties")
    base_path.mkdir(parents=True, exist_ok=True)
    
    organizer = BountyOrganizer()
    quick_wins = hunter.get_quick_wins()
    
    print(f"Creando carpetas para {len(quick_wins[:5])} top quick wins...\n")
    
    for bounty in quick_wins[:5]:
        # Agregar ROI al bounty
        analyzer = BountyAnalyzer()
        bounty['roi'] = analyzer.calculate_roi(bounty)
        
        path = organizer.create_bounty_folder(bounty, base_path)
        print(f"✅ {path.name}")
    
    print(f"\n📁 Carpetas creadas en: {base_path}")

def cmd_filter_by_reward(hunter: BountyHunter, min_reward: int):
    """Filtra bounties por recompensa mínima"""
    print_header(f"BOUNTIES CON RECOMPENSA >= ${min_reward:,}")
    
    filtered = hunter.filter_bounties(min_reward=min_reward)
    ranked = hunter.rank_by_profitability(filtered)
    
    for i, bounty in enumerate(ranked[:10], 1):
        roi = bounty['roi']
        print(f"{i}. {bounty['platform']} - {bounty['title']}")
        print(f"   Recompensa: ${roi['avg_reward']:,}")
        print(f"   $/Hora: ${roi['hourly_rate']:.0f}")
        print()

def cmd_portfolio_summary(hunter: BountyHunter):
    """Muestra resumen del portafolio"""
    print_header("RESUMEN DE PORTAFOLIO")
    
    portfolio = hunter.get_portfolio()
    
    print(f"📊 ESTADÍSTICAS:")
    print(f"  Total de bounties activos: {portfolio['total_bounties']}")
    print(f"  Recompensa total potencial: ${portfolio['total_potential_reward']:,}")
    print(f"  Promedio por bounty: ${portfolio['total_potential_reward']/max(portfolio['total_bounties'], 1):,.0f}")
    
    print(f"\n💰 TOP 5 POR RENTABILIDAD:")
    for i, bounty in enumerate(portfolio['top_10_by_profitability'][:5], 1):
        roi = bounty['roi']
        print(f"  {i}. ${roi['hourly_rate']:.0f}/h - {bounty['title'][:50]}")
    
    print(f"\n⚡ TOP 3 QUICK WINS:")
    for i, bounty in enumerate(portfolio['quick_wins'][:3], 1):
        roi = bounty['roi']
        print(f"  {i}. ${roi['avg_reward']:,} in {bounty['estimated_time']}h - {bounty['title'][:40]}")
    
    print(f"\n✅ {portfolio['recommendation']}")

def cmd_help():
    """Muestra ayuda"""
    print_header("AYUDA - COMANDOS DISPONIBLES")
    
    commands = {
        'list': 'Listar todos los bounties activos',
        'quick': 'Mostrar quick wins (rápida aprobación)',
        'top': 'Top 10 bounties por rentabilidad ($/hora)',
        'create': 'Crear carpetas para top bounties',
        'filter [amount]': 'Filtrar bounties por recompensa mínima',
        'summary': 'Resumen del portafolio completo',
        'help': 'Mostrar esta ayuda'
    }
    
    for cmd, desc in commands.items():
        print(f"  {cmd:<20} - {desc}")
    
    print("\nEjemplos:")
    print("  python bounty_cli.py list")
    print("  python bounty_cli.py quick")
    print("  python bounty_cli.py filter 5000")
    print("  python bounty_cli.py create")

def main():
    """Punto de entrada"""
    
    hunter = BountyHunter()
    
    if len(sys.argv) < 2:
        cmd_help()
        return
    
    command = sys.argv[1].lower()
    
    if command == 'list':
        cmd_list_bounties(hunter)
    elif command == 'quick':
        cmd_quick_wins(hunter)
    elif command == 'top':
        cmd_top_profitable(hunter)
    elif command == 'create':
        cmd_create_folders(hunter)
    elif command == 'filter':
        amount = int(sys.argv[2]) if len(sys.argv) > 2 else 5000
        cmd_filter_by_reward(hunter, amount)
    elif command == 'summary':
        cmd_portfolio_summary(hunter)
    elif command == 'help' or command == '-h' or command == '--help':
        cmd_help()
    else:
        print(f"❌ Comando desconocido: {command}")
        cmd_help()

if __name__ == "__main__":
    main()
