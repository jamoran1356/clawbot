#!/usr/bin/env python3
"""
GitHub Bounty Manager - Gestor de bounties desde GitHub
Crea issues, PRs y carpetas organizadas automáticamente
"""

import json
from pathlib import Path
from datetime import datetime
from typing import Dict, List

class GitHubBountyManager:
    """Gestor automático de bounties en GitHub"""
    
    @staticmethod
    def create_bounty_folder_structure(bounty: Dict, base_path: Path) -> Path:
        """Crea estructura de carpeta para bounty"""
        
        # Nombre seguro
        folder_name = f"{bounty['id']}_{bounty['title'].replace(' ', '_')[:40]}"
        bounty_path = base_path / folder_name
        bounty_path.mkdir(parents=True, exist_ok=True)
        
        # Subdirectorios
        (bounty_path / 'code').mkdir(exist_ok=True)
        (bounty_path / 'tests').mkdir(exist_ok=True)
        (bounty_path / 'docs').mkdir(exist_ok=True)
        (bounty_path / '.github' / 'workflows').mkdir(parents=True, exist_ok=True)
        
        # Archivo principal
        main_content = f"""# {bounty['title']}

## 💰 Información de Recompensa

- **Plataforma:** {bounty['platform']}
- **Cantidad:** {bounty['currency']} {bounty['amount']}
- **Repositorio:** [{bounty['repo']}](https://{bounty['repo']})
- **Dificultad:** {bounty['difficulty']}
- **Tiempo Estimado:** {bounty['estimated_time']} horas
- **Aprobación:** {bounty['approval_time']}

## 📝 Descripción

{bounty['description']}

## 🎯 Requisitos

- [ ] Fork del repositorio
- [ ] Rama de feature creada
- [ ] Código implementado
- [ ] Tests pasando
- [ ] PR creado
- [ ] Revisión completada
- [ ] Merge aprobado

## 💵 Pago

- **Monto:** {bounty['currency']} ${bounty['amount']}
- **Método:** {bounty['payment_method']}
- **Wallet:** (Agregarás durante el PR)
- **Status:** Pendiente

## 📊 ROI

- Tasa Horaria: ${bounty['amount'] / max(bounty['estimated_time'], 1):.0f}/h
- Tiempo Total: {bounty['estimated_time']}h
- Recompensa Total: ${bounty['amount']}

## 🔗 Links

- **Issue:** {bounty.get('issue_url', 'Por determinar')}
- **PR:** (Será agregado cuando se cree)
- **Repo:** https://{bounty['repo']}

## 📅 Timeline

- **Creado:** {datetime.now().isoformat()}
- **Comenzado:** (Por determinar)
- **Completado:** (Por determinar)
- **Pagado:** (Por determinar)

## 📝 Notas

Agrega tus notas de progreso aquí.

---

**Status:** 🔄 En Progreso
**Progreso:** 0%
"""
        
        with open(bounty_path / 'README.md', 'w', encoding='utf-8') as f:
            f.write(main_content)
        
        # Archivo de tracking
        tracking = {
            'bounty_id': bounty['id'],
            'title': bounty['title'],
            'platform': bounty['platform'],
            'currency': bounty['currency'],
            'amount': bounty['amount'],
            'repo': bounty['repo'],
            'created_at': datetime.now().isoformat(),
            'status': 'started',
            'progress': 0,
            'pr_url': None,
            'payment_wallet': None,
            'completed_at': None,
            'paid_at': None,
            'notes': []
        }
        
        with open(bounty_path / 'tracking.json', 'w') as f:
            json.dump(tracking, f, indent=2)
        
        # Archivo de configuración de CI/CD
        github_workflow = """name: Bounty Tests

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Run tests
        run: |
          npm install
          npm test
      - name: Check coverage
        run: npm run coverage
"""
        
        with open(bounty_path / '.github' / 'workflows' / 'test.yml', 'w') as f:
            f.write(github_workflow)
        
        return bounty_path
    
    @staticmethod
    def generate_pr_template(bounty: Dict) -> str:
        """Genera template de PR para GitHub"""
        
        template = f"""## 💰 Bounty Submission - {bounty['currency']} ${bounty['amount']}

**Bounty ID:** {bounty['id']}
**Platform:** {bounty['platform']}
**Title:** {bounty['title']}

### 📝 Description

Fixes #{bounty.get('issue_number', 'TBD')}

Implements: {bounty['description']}

### ✅ Checklist

- [ ] Changes follow the style guidelines
- [ ] Tests passing locally
- [ ] New tests added/updated
- [ ] Documentation updated
- [ ] No breaking changes
- [ ] Ready for review

### 🧪 Testing

```bash
# Command to reproduce issue (if bug fix)
# Command to test implementation
```

### 💵 Payment Information

**Bounty:** {bounty['currency']} ${bounty['amount']}
**Wallet Address:** 0x...

### 📊 Stats

- **Estimated Time:** {bounty['estimated_time']}h
- **Actual Time:** (To be filled)
- **Hourly Rate:** ${bounty['amount'] / max(bounty['estimated_time'], 1):.0f}/h

---

**Related:** Bounty #{bounty['id']} on {bounty['platform']}
"""
        
        return template
    
    @staticmethod
    def generate_issue_template(bounty: Dict) -> str:
        """Genera template de issue para GitHub"""
        
        template = f"""# {bounty['title']}

## 💰 Bounty Information

- **Reward:** {bounty['currency']} ${bounty['amount']}
- **Difficulty:** {bounty['difficulty']}
- **Estimated Time:** {bounty['estimated_time']} hours
- **Approval Time:** {bounty['approval_time']}
- **Platform:** {bounty['platform']}
- **ID:** {bounty['id']}

## 📝 Description

{bounty['description']}

## 🎯 Requirements

- [ ] Requirement 1
- [ ] Requirement 2
- [ ] Requirement 3

## 🚀 Getting Started

1. Fork the repository
2. Create a feature branch
3. Implement the solution
4. Add tests
5. Submit a PR

## 💡 Notes

- Include your wallet address in the PR
- Follow the code style guide
- All tests must pass

## 🏆 Reward

Successful completion and merge will result in {bounty['currency']} ${bounty['amount']} payout.
"""
        
        return template

def create_github_bounty_setup(bounties: List[Dict], base_path: Path):
    """Crea setup completo para github bounties"""
    
    base_path.mkdir(parents=True, exist_ok=True)
    manager = GitHubBountyManager()
    
    print("\n📁 Creando estructura para GitHub bounties...\n")
    
    for bounty in bounties:
        path = manager.create_bounty_folder_structure(bounty, base_path)
        
        # Generar PR template
        pr_template = manager.generate_pr_template(bounty)
        with open(path / 'PR_TEMPLATE.md', 'w') as f:
            f.write(pr_template)
        
        # Generar Issue template
        issue_template = manager.generate_issue_template(bounty)
        with open(path / 'ISSUE_TEMPLATE.md', 'w') as f:
            f.write(issue_template)
        
        hourly_rate = bounty['amount'] / max(bounty['estimated_time'], 1)
        print(f"✅ {path.name}")
        print(f"   💰 {bounty['currency']} ${bounty['amount']} | ⏱️ {bounty['estimated_time']}h | 💵 ${hourly_rate:.0f}/h\n")

# Main execution
if __name__ == "__main__":
    from crypto_bounty_finder import CryptoBountyFinder
    
    finder = CryptoBountyFinder()
    
    # Quick wins
    quick_wins = finder.get_quick_wins()
    
    # Crear estructura
    base_path = Path("/workspace/anais-workspace/shared/proyectos/bounty-hunter/github-bounties")
    create_github_bounty_setup(quick_wins[:5], base_path)
    
    print(f"\n✨ Estructura GitHub lista en: {base_path}\n")
