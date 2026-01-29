#!/usr/bin/env python3
"""
Crypto Bounty Finder - Buscador de recompensas en USDT/USDC
Bounties gestionables desde GitHub con rápida aprobación
"""

import json
from typing import List, Dict
from datetime import datetime
from pathlib import Path

class CryptoBountyFinder:
    """Finder especializado en bounties crypto/GitHub"""
    
    def __init__(self):
        self.bounties = []
        self.load_crypto_bounties()
    
    def load_crypto_bounties(self):
        """Carga bounties en USDT/USDC"""
        
        self.bounties = [
            # GITCOIN - Smart Contracts & Code Audits
            {
                'id': 'git_001',
                'platform': 'Gitcoin',
                'type': 'GitHub Issue',
                'title': 'Fix Critical Bug in Uniswap V3 Integration',
                'description': 'Fix vulnerability in Uniswap V3 router integration',
                'currency': 'USDT',
                'amount': 2000,
                'repo': 'github.com/protocol/contracts',
                'difficulty': 'Medium',
                'estimated_time': 8,
                'approval_time': '24-48 hours',
                'category': 'Bug Fix',
                'tags': ['github', 'solidity', 'defi', 'uniswap'],
                'status': 'open',
                'priority': 'High',
                'pr_required': True,
                'quick_payout': True,
                'payment_method': 'Direct to Wallet'
            },
            {
                'id': 'git_002',
                'platform': 'Gitcoin',
                'type': 'GitHub Issue',
                'title': 'Implement Gas Optimization for Token Transfer',
                'description': 'Optimize token transfer function to reduce gas costs by 30%',
                'currency': 'USDC',
                'amount': 1500,
                'repo': 'github.com/opensea/contracts',
                'difficulty': 'Medium',
                'estimated_time': 6,
                'approval_time': '24 hours',
                'category': 'Optimization',
                'tags': ['github', 'solidity', 'gas', 'optimization'],
                'status': 'open',
                'priority': 'High',
                'pr_required': True,
                'quick_payout': True,
                'payment_method': 'Direct to Wallet'
            },
            {
                'id': 'git_003',
                'platform': 'Gitcoin',
                'type': 'GitHub Issue',
                'title': 'Add Multi-Sig Support to Treasury',
                'description': 'Implement multi-signature wallet support in treasury contract',
                'currency': 'USDT',
                'amount': 3000,
                'repo': 'github.com/lido/dao',
                'difficulty': 'High',
                'estimated_time': 20,
                'approval_time': '24-48 hours',
                'category': 'Feature',
                'tags': ['github', 'solidity', 'multisig', 'governance'],
                'status': 'open',
                'priority': 'Critical',
                'pr_required': True,
                'quick_payout': True,
                'payment_method': 'Direct to Wallet'
            },
            
            # GITHUB SPONSORS & BOUNTIES
            {
                'id': 'gh_001',
                'platform': 'GitHub Sponsors',
                'type': 'GitHub Issue',
                'title': 'Write Security Audit Report for Smart Contract',
                'description': 'Complete security audit and report for new smart contract',
                'currency': 'USDC',
                'amount': 2500,
                'repo': 'github.com/makerdao/governance',
                'difficulty': 'High',
                'estimated_time': 16,
                'approval_time': '48-72 hours',
                'category': 'Audit',
                'tags': ['github', 'audit', 'security', 'solidity'],
                'status': 'open',
                'priority': 'High',
                'pr_required': False,
                'quick_payout': True,
                'payment_method': 'GitHub Sponsors'
            },
            {
                'id': 'gh_002',
                'platform': 'GitHub',
                'type': 'GitHub Issue',
                'title': 'Fix Arithmetic Overflow in Pool Calculator',
                'description': 'Fix potential overflow vulnerability in math calculations',
                'currency': 'USDT',
                'amount': 1200,
                'repo': 'github.com/curve/protocol',
                'difficulty': 'Medium',
                'estimated_time': 5,
                'approval_time': '24 hours',
                'category': 'Bug Fix',
                'tags': ['github', 'math', 'security', 'quick'],
                'status': 'open',
                'priority': 'Critical',
                'pr_required': True,
                'quick_payout': True,
                'payment_method': 'Direct to Wallet'
            },
            
            # OPEN ZEP - Bug Bounty Program
            {
                'id': 'openzep_001',
                'platform': 'OpenZeppelin',
                'type': 'GitHub Issue',
                'title': 'Document Gas-Safe Array Transfer Pattern',
                'description': 'Create documentation and example for gas-safe array transfers',
                'currency': 'USDC',
                'amount': 800,
                'repo': 'github.com/openzeppelin/contracts',
                'difficulty': 'Easy',
                'estimated_time': 4,
                'approval_time': '24 hours',
                'category': 'Documentation',
                'tags': ['github', 'documentation', 'easy', 'quick'],
                'status': 'open',
                'priority': 'Medium',
                'pr_required': True,
                'quick_payout': True,
                'payment_method': 'Direct to Wallet'
            },
            
            # AAVE PROTOCOL
            {
                'id': 'aave_001',
                'platform': 'Gitcoin',
                'type': 'GitHub Issue',
                'title': 'Implement Flash Loan Risk Assessment',
                'description': 'Create risk assessment framework for flash loans',
                'currency': 'USDT',
                'amount': 4000,
                'repo': 'github.com/aave/protocol',
                'difficulty': 'High',
                'estimated_time': 25,
                'approval_time': '48 hours',
                'category': 'Feature',
                'tags': ['github', 'aave', 'flashloan', 'risk'],
                'status': 'open',
                'priority': 'High',
                'pr_required': True,
                'quick_payout': True,
                'payment_method': 'Direct to Wallet'
            },
            
            # BALANCER LABS
            {
                'id': 'balancer_001',
                'platform': 'Gitcoin',
                'type': 'GitHub Issue',
                'title': 'Optimize Swap Route Calculation',
                'description': 'Improve swap route calculation algorithm for better prices',
                'currency': 'USDC',
                'amount': 2800,
                'repo': 'github.com/balancer-labs/balancer',
                'difficulty': 'High',
                'estimated_time': 15,
                'approval_time': '24-48 hours',
                'category': 'Optimization',
                'tags': ['github', 'balancer', 'routing', 'optimization'],
                'status': 'open',
                'priority': 'High',
                'pr_required': True,
                'quick_payout': True,
                'payment_method': 'Direct to Wallet'
            },
            
            # YEARN FINANCE
            {
                'id': 'yearn_001',
                'platform': 'Gitcoin',
                'type': 'GitHub Issue',
                'title': 'Create Vault Strategy for LST Tokens',
                'description': 'Develop new vault strategy for liquid staking tokens',
                'currency': 'USDT',
                'amount': 5000,
                'repo': 'github.com/yearn/yearn-vaults',
                'difficulty': 'High',
                'estimated_time': 30,
                'approval_time': '48-72 hours',
                'category': 'Strategy',
                'tags': ['github', 'yearn', 'strategy', 'lst'],
                'status': 'open',
                'priority': 'Critical',
                'pr_required': True,
                'quick_payout': True,
                'payment_method': 'Direct to Wallet'
            },
            
            # QUICK WINS - < 5 HORAS
            {
                'id': 'quick_001',
                'platform': 'GitHub',
                'type': 'GitHub Issue',
                'title': 'Fix Typo in Contract Comments',
                'description': 'Fix documentation and comment typos in main contract',
                'currency': 'USDC',
                'amount': 100,
                'repo': 'github.com/compound/compound-protocol',
                'difficulty': 'Easy',
                'estimated_time': 0.5,
                'approval_time': '1 hour',
                'category': 'Documentation',
                'tags': ['github', 'easy', 'quick', 'typo'],
                'status': 'open',
                'priority': 'Low',
                'pr_required': True,
                'quick_payout': True,
                'payment_method': 'Direct to Wallet'
            },
            {
                'id': 'quick_002',
                'platform': 'Gitcoin',
                'type': 'GitHub Issue',
                'title': 'Add Unit Tests for Transfer Function',
                'description': 'Write comprehensive unit tests for token transfer function',
                'currency': 'USDT',
                'amount': 300,
                'repo': 'github.com/0x/protocol',
                'difficulty': 'Easy',
                'estimated_time': 3,
                'approval_time': '2-4 hours',
                'category': 'Testing',
                'tags': ['github', 'testing', 'quick', 'easy'],
                'status': 'open',
                'priority': 'Medium',
                'pr_required': True,
                'quick_payout': True,
                'payment_method': 'Direct to Wallet'
            },
            {
                'id': 'quick_003',
                'platform': 'GitHub',
                'type': 'GitHub Issue',
                'title': 'Update README with New API Endpoint',
                'description': 'Document new API endpoint in README with examples',
                'currency': 'USDC',
                'amount': 150,
                'repo': 'github.com/traderjoe/traderjoe',
                'difficulty': 'Easy',
                'estimated_time': 1,
                'approval_time': '1-2 hours',
                'category': 'Documentation',
                'tags': ['github', 'documentation', 'quick', 'easy'],
                'status': 'open',
                'priority': 'Low',
                'pr_required': True,
                'quick_payout': True,
                'payment_method': 'Direct to Wallet'
            }
        ]
    
    def get_quick_wins(self, max_time: float = 5, min_payout: int = 100) -> List[Dict]:
        """Encuentra quick wins (< 5 horas, rápida aprobación)"""
        
        quick_wins = []
        
        for bounty in self.bounties:
            if (bounty.get('estimated_time', 0) <= max_time and
                bounty.get('amount', 0) >= min_payout and
                bounty.get('quick_payout') and
                bounty.get('status') == 'open'):
                quick_wins.append(bounty)
        
        # Ordenar por $/hora
        quick_wins.sort(key=lambda b: b.get('amount', 0) / max(b.get('estimated_time', 1), 1), reverse=True)
        return quick_wins
    
    def get_manageable_from_github(self) -> List[Dict]:
        """Obtiene bounties que se pueden manejar desde GitHub"""
        
        github_manageable = [b for b in self.bounties 
                             if b.get('pr_required') and 
                             b.get('status') == 'open']
        
        github_manageable.sort(key=lambda b: b.get('amount', 0) / max(b.get('estimated_time', 1), 1), reverse=True)
        return github_manageable
    
    def get_instant_approval(self, max_hours: int = 4) -> List[Dict]:
        """Bounties con aprobación casi instantánea"""
        
        instant = []
        
        for bounty in self.bounties:
            approval = bounty.get('approval_time', '')
            if (('1 hour' in approval or '2' in approval or '4' in approval) and
                bounty.get('estimated_time', 0) <= max_hours and
                bounty.get('status') == 'open'):
                instant.append(bounty)
        
        instant.sort(key=lambda b: b.get('amount', 0) / max(b.get('estimated_time', 1), 1), reverse=True)
        return instant
    
    def get_by_difficulty(self, difficulty: str) -> List[Dict]:
        """Filtra por dificultad"""
        
        filtered = [b for b in self.bounties 
                   if b.get('difficulty') == difficulty and
                   b.get('status') == 'open']
        
        filtered.sort(key=lambda b: b.get('amount', 0) / max(b.get('estimated_time', 1), 1), reverse=True)
        return filtered
    
    def get_portfolio_analysis(self) -> Dict:
        """Análisis completo del portafolio"""
        
        total_bounties = len([b for b in self.bounties if b.get('status') == 'open'])
        total_reward = sum(b.get('amount', 0) for b in self.bounties if b.get('status') == 'open')
        
        quick_wins = self.get_quick_wins()
        quick_wins_reward = sum(b.get('amount', 0) for b in quick_wins)
        quick_wins_time = sum(b.get('estimated_time', 0) for b in quick_wins)
        
        return {
            'total_open': total_bounties,
            'total_potential_reward': total_reward,
            'total_potential_usdt': sum(b.get('amount', 0) for b in self.bounties 
                                        if b.get('currency') == 'USDT' and b.get('status') == 'open'),
            'total_potential_usdc': sum(b.get('amount', 0) for b in self.bounties 
                                        if b.get('currency') == 'USDC' and b.get('status') == 'open'),
            'quick_wins': {
                'count': len(quick_wins),
                'total_reward': quick_wins_reward,
                'total_time': quick_wins_time,
                'rate_per_hour': quick_wins_reward / max(quick_wins_time, 1),
                'items': quick_wins
            },
            'platforms': list(set(b.get('platform') for b in self.bounties if b.get('status') == 'open')),
            'all_github_manageable': self.get_manageable_from_github(),
            'instant_approval': self.get_instant_approval()
        }

def main():
    """Demo"""
    
    print("\n" + "="*70)
    print("🎯 CRYPTO BOUNTY FINDER - GitHub + USDT/USDC")
    print("="*70 + "\n")
    
    finder = CryptoBountyFinder()
    analysis = finder.get_portfolio_analysis()
    
    print(f"📊 PORTAFOLIO TOTAL:\n")
    print(f"  Bounties Abiertos: {analysis['total_open']}")
    print(f"  Recompensa Total: ${analysis['total_potential_reward']:,}")
    print(f"  En USDT: ${analysis['total_potential_usdt']:,}")
    print(f"  En USDC: ${analysis['total_potential_usdc']:,}\n")
    
    # Quick Wins
    print(f"⚡ QUICK WINS (< 5 horas):\n")
    quick_wins = analysis['quick_wins']
    print(f"  Total: {quick_wins['count']} bounties")
    print(f"  Dinero: ${quick_wins['total_reward']:,}")
    print(f"  Tiempo: {quick_wins['total_time']:.1f} horas")
    print(f"  $/Hora: ${quick_wins['rate_per_hour']:.0f}\n")
    
    for i, bounty in enumerate(quick_wins['items'][:5], 1):
        hourly = bounty['amount'] / max(bounty['estimated_time'], 0.5)
        print(f"  {i}. {bounty['currency']} {bounty['amount']} - {bounty['title']}")
        print(f"     {bounty['estimated_time']}h | ${hourly:.0f}/h | {bounty['approval_time']}\n")
    
    # Instant Approval
    print(f"🔥 APROBACIÓN INSTANTÁNEA (<= 4 horas):\n")
    instant = analysis['instant_approval']
    for i, bounty in enumerate(instant[:3], 1):
        hourly = bounty['amount'] / max(bounty['estimated_time'], 1)
        print(f"  {i}. {bounty['currency']} {bounty['amount']} - {bounty['title']}")
        print(f"     {bounty['estimated_time']}h | {bounty['approval_time']}\n")
    
    # GitHub Manageable
    print(f"🐙 MANEJABLES DESDE GITHUB (PR-based):\n")
    github = analysis['all_github_manageable'][:5]
    for i, bounty in enumerate(github, 1):
        hourly = bounty['amount'] / max(bounty['estimated_time'], 1)
        print(f"  {i}. {bounty['platform']} - {bounty['title'][:50]}")
        print(f"     {bounty['repo'].split('/')[-1]} | {bounty['currency']} ${hourly:.0f}/h\n")

if __name__ == "__main__":
    main()
