#!/usr/bin/env python3
"""
Bounty Hunter Engine - Buscador de recompensas y vulnerabilidades
Encuentra bounties económicamente rentables en múltiples plataformas
"""

import json
from typing import List, Dict, Optional
from datetime import datetime
from pathlib import Path
import asyncio

class BountyAnalyzer:
    """Analizador de rentabilidad de bounties"""
    
    @staticmethod
    def calculate_roi(bounty: Dict) -> Dict:
        """Calcula ROI y rentabilidad de un bounty"""
        
        min_reward = bounty.get('min_reward', 0)
        max_reward = bounty.get('max_reward', 0)
        avg_reward = (min_reward + max_reward) / 2
        
        # Estimación de tiempo (en horas)
        estimated_time = bounty.get('estimated_time', 0)
        
        if estimated_time > 0:
            hourly_rate = avg_reward / estimated_time
        else:
            hourly_rate = 0
        
        return {
            'min_reward': min_reward,
            'max_reward': max_reward,
            'avg_reward': avg_reward,
            'hourly_rate': hourly_rate,
            'profitability_score': min(hourly_rate / 50, 100)  # Score 0-100
        }

class BountyHunter:
    """Motor de búsqueda y gestión de bounties"""
    
    def __init__(self):
        self.bounties = []
        self.load_bounty_database()
    
    def load_bounty_database(self):
        """Carga base de datos de bounties conocidos de alto valor"""
        
        self.bounties = [
            # HackerOne - Critical Vulnerabilities
            {
                'id': 'h1_001',
                'platform': 'HackerOne',
                'title': 'Remote Code Execution in Web Portal',
                'company': 'Fortune 500 Tech Corp',
                'description': 'Find RCE vulnerability in main web application',
                'min_reward': 5000,
                'max_reward': 25000,
                'avg_reward': 15000,
                'severity': 'Critical',
                'category': 'RCE',
                'estimated_time': 20,
                'approval_time': '24-48 hours',
                'status': 'active',
                'priority': 'High',
                'url': 'https://hackerone.com/...',
                'requirements': ['Proof of Concept', 'Impact Analysis'],
                'tags': ['rce', 'web', 'critical', 'fast_payout']
            },
            {
                'id': 'h1_002',
                'platform': 'HackerOne',
                'title': 'SQL Injection in API Endpoint',
                'company': 'SaaS Platform',
                'description': 'SQL injection in user management API',
                'min_reward': 3000,
                'max_reward': 10000,
                'avg_reward': 6500,
                'severity': 'High',
                'category': 'SQLI',
                'estimated_time': 15,
                'approval_time': '48 hours',
                'status': 'active',
                'priority': 'High',
                'url': 'https://hackerone.com/...',
                'requirements': ['Proof of Concept'],
                'tags': ['sqli', 'api', 'high', 'data_breach']
            },
            # Bugcrowd - Multiple Vulnerabilities
            {
                'id': 'bc_001',
                'platform': 'Bugcrowd',
                'title': 'Authentication Bypass',
                'company': 'Payment Processing Company',
                'description': 'Bypass 2FA in mobile application',
                'min_reward': 4000,
                'max_reward': 15000,
                'avg_reward': 9500,
                'severity': 'Critical',
                'category': 'Auth Bypass',
                'estimated_time': 25,
                'approval_time': '24-72 hours',
                'status': 'active',
                'priority': 'Critical',
                'url': 'https://bugcrowd.com/...',
                'requirements': ['Step by step reproduction', 'Video POC'],
                'tags': ['auth', 'mobile', 'critical', 'payment']
            },
            {
                'id': 'bc_002',
                'platform': 'Bugcrowd',
                'title': 'CORS Misconfiguration',
                'company': 'Financial Services',
                'description': 'CORS allowing unauthorized cross-origin requests',
                'min_reward': 2000,
                'max_reward': 8000,
                'avg_reward': 5000,
                'severity': 'Medium',
                'category': 'CORS',
                'estimated_time': 10,
                'approval_time': '48 hours',
                'status': 'active',
                'priority': 'Medium',
                'url': 'https://bugcrowd.com/...',
                'requirements': ['POC'],
                'tags': ['cors', 'web', 'medium', 'quick']
            },
            # Intigriti
            {
                'id': 'int_001',
                'platform': 'Intigriti',
                'title': 'XSS in Profile Settings',
                'company': 'European Tech Startup',
                'description': 'Reflected XSS allowing session hijacking',
                'min_reward': 2500,
                'max_reward': 7000,
                'avg_reward': 4750,
                'severity': 'High',
                'category': 'XSS',
                'estimated_time': 12,
                'approval_time': '24 hours',
                'status': 'active',
                'priority': 'High',
                'url': 'https://intigriti.com/...',
                'requirements': ['Working POC'],
                'tags': ['xss', 'session', 'high', 'european']
            },
            # Gitcoin Bounties
            {
                'id': 'gc_001',
                'platform': 'Gitcoin',
                'title': 'Smart Contract Audit Finding',
                'company': 'DeFi Protocol',
                'description': 'Find and document security issues in smart contracts',
                'min_reward': 3000,
                'max_reward': 20000,
                'avg_reward': 11500,
                'severity': 'Critical',
                'category': 'Blockchain',
                'estimated_time': 30,
                'approval_time': '72 hours',
                'status': 'active',
                'priority': 'High',
                'url': 'https://gitcoin.co/...',
                'requirements': ['Detailed Report', 'Remediation Advice'],
                'tags': ['blockchain', 'audit', 'critical', 'defi']
            },
            # Open source security
            {
                'id': 'os_001',
                'platform': 'GitHub Security Advisories',
                'title': 'Dependency Vulnerability Report',
                'company': 'Popular Open Source Project',
                'description': 'Identify and report vulnerable dependencies',
                'min_reward': 500,
                'max_reward': 5000,
                'avg_reward': 2500,
                'severity': 'Medium',
                'category': 'Dependencies',
                'estimated_time': 8,
                'approval_time': '48 hours',
                'status': 'active',
                'priority': 'Medium',
                'url': 'https://github.com/...',
                'requirements': ['Security Report'],
                'tags': ['opensource', 'dependencies', 'quick', 'automation']
            }
        ]
    
    def filter_bounties(self, min_reward: int = 0, max_time: int = 999, 
                       approval_time_max: str = None) -> List[Dict]:
        """Filtra bounties por criterios de rentabilidad"""
        
        filtered = []
        
        for bounty in self.bounties:
            avg_reward = bounty.get('avg_reward', 0)
            est_time = bounty.get('estimated_time', 0)
            
            # Rentabilidad: mínimo $1000 con máximo 40 horas
            if avg_reward >= min_reward and est_time <= max_time:
                if bounty.get('status') == 'active':
                    filtered.append(bounty)
        
        return filtered
    
    def rank_by_profitability(self, bounties: List[Dict]) -> List[Dict]:
        """Ordena bounties por rentabilidad ($/hora)"""
        
        ranked = []
        
        for bounty in bounties:
            analyzer = BountyAnalyzer()
            roi = analyzer.calculate_roi(bounty)
            bounty['roi'] = roi
            ranked.append(bounty)
        
        # Ordenar por hourly_rate descendente
        ranked.sort(key=lambda b: b['roi']['hourly_rate'], reverse=True)
        
        return ranked
    
    def get_quick_wins(self, max_time_hours: int = 10, min_reward: int = 2000) -> List[Dict]:
        """Encuentra bounties con rápida aprobación y alta rentabilidad"""
        
        quick_wins = []
        
        for bounty in self.bounties:
            if bounty.get('status') != 'active':
                continue
            
            est_time = bounty.get('estimated_time', 0)
            avg_reward = bounty.get('avg_reward', 0)
            
            # Criterios: < 10 horas, > $2000, aprobación rápida
            if est_time <= max_time_hours and avg_reward >= min_reward:
                if '24' in bounty.get('approval_time', '') or '48' in bounty.get('approval_time', ''):
                    quick_wins.append(bounty)
        
        return self.rank_by_profitability(quick_wins)
    
    def get_portfolio(self) -> Dict:
        """Genera portafolio de recomendaciones"""
        
        all_ranked = self.rank_by_profitability(
            [b for b in self.bounties if b.get('status') == 'active']
        )
        
        return {
            'total_bounties': len([b for b in self.bounties if b.get('status') == 'active']),
            'total_potential_reward': sum(b.get('avg_reward', 0) for b in self.bounties if b.get('status') == 'active'),
            'top_10_by_profitability': all_ranked[:10],
            'quick_wins': self.get_quick_wins(),
            'recommendation': 'Start with quick wins for fastest cash flow'
        }

class BountyOrganizer:
    """Organizador de carpetas por bounty"""
    
    @staticmethod
    def create_bounty_folder(bounty: Dict, base_path: Path) -> Path:
        """Crea estructura de carpeta para cada bounty"""
        
        # Crear ID seguro para carpeta
        folder_id = bounty['id'].replace('_', '-')
        folder_name = f"{folder_id}_{bounty['title'].replace(' ', '_')[:30]}"
        
        bounty_path = base_path / folder_name
        bounty_path.mkdir(parents=True, exist_ok=True)
        
        # Crear subcarpetas
        (bounty_path / 'poc').mkdir(exist_ok=True)
        (bounty_path / 'documentation').mkdir(exist_ok=True)
        (bounty_path / 'reports').mkdir(exist_ok=True)
        (bounty_path / 'code').mkdir(exist_ok=True)
        
        # Crear archivo README
        readme_content = f"""# {bounty['title']}

## Información del Bounty

- **Platform:** {bounty['platform']}
- **Company:** {bounty['company']}
- **ID:** {bounty['id']}
- **Severity:** {bounty['severity']}
- **Category:** {bounty['category']}

## Recompensa

- **Rango:** ${bounty['min_reward']:,} - ${bounty['max_reward']:,}
- **Promedio:** ${bounty['avg_reward']:,}
- **Tiempo Estimado:** {bounty['estimated_time']} horas
- **Aprobación:** {bounty['approval_time']}

## Descripción

{bounty['description']}

## Requisitos

"""
        
        for req in bounty.get('requirements', []):
            readme_content += f"- {req}\n"
        
        readme_content += f"""

## ROI Calculado

- Tasa Horaria: ${bounty['roi']['hourly_rate']:.0f}/hora
- Score de Rentabilidad: {bounty['roi']['profitability_score']:.1f}/100

## Estructura

- **poc/** - Proof of Concept files
- **documentation/** - Technical documentation
- **reports/** - Security reports and findings
- **code/** - Exploit code or scripts

## Estado

- Status: Pendiente
- Fecha Creada: {datetime.now().isoformat()}
- URL: {bounty.get('url', 'N/A')}

## Notas

Agrega tus hallazgos, PoCs y documentación aquí.
"""
        
        with open(bounty_path / 'README.md', 'w', encoding='utf-8') as f:
            f.write(readme_content)
        
        # Crear archivo de tracking
        tracking_data = {
            'bounty_id': bounty['id'],
            'title': bounty['title'],
            'platform': bounty['platform'],
            'created_at': datetime.now().isoformat(),
            'status': 'started',
            'progress': 0,
            'notes': [],
            'findings': [],
            'submission_ready': False
        }
        
        with open(bounty_path / 'tracking.json', 'w', encoding='utf-8') as f:
            json.dump(tracking_data, f, indent=2, ensure_ascii=False)
        
        return bounty_path

async def main():
    """Demo del bounty hunter"""
    
    print("\n" + "="*60)
    print("🎯 BOUNTY HUNTER ENGINE - Búsqueda de Recompensas")
    print("="*60 + "\n")
    
    # Inicializar hunter
    hunter = BountyHunter()
    
    # Obtener portafolio
    portfolio = hunter.get_portfolio()
    
    print(f"📊 PORTAFOLIO TOTAL:\n")
    print(f"  Bounties Activos: {portfolio['total_bounties']}")
    print(f"  Recompensa Total Potencial: ${portfolio['total_potential_reward']:,}\n")
    
    # Quick wins
    print(f"⚡ QUICK WINS (< 10 horas, aprobación rápida):\n")
    for i, bounty in enumerate(portfolio['quick_wins'][:3], 1):
        print(f"  {i}. {bounty['platform']} - {bounty['title']}")
        print(f"     Recompensa: ${bounty['roi']['avg_reward']:,}")
        print(f"     $/Hora: ${bounty['roi']['hourly_rate']:.0f}")
        print(f"     Tiempo: {bounty['estimated_time']}h\n")
    
    # Crear carpetas
    base_path = Path("/workspace/anais-workspace/shared/proyectos/bounty-hunter/bounties")
    base_path.mkdir(parents=True, exist_ok=True)
    
    print(f"📁 Creando carpetas para quick wins...\n")
    
    organizer = BountyOrganizer()
    for bounty in portfolio['quick_wins'][:3]:
        path = organizer.create_bounty_folder(bounty, base_path)
        print(f"✅ Carpeta creada: {path.name}")
    
    print(f"\n✨ Bounty Hunter listo para investigar!")

if __name__ == "__main__":
    asyncio.run(main())
