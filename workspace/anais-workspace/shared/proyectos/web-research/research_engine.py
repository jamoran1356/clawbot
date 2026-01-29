#!/usr/bin/env python3
"""
Web Research Engine - Motor de búsqueda e investigación web
Usa: Web scraping, búsqueda en Google, análisis de contenido
"""

import asyncio
import json
from typing import List, Dict, Optional
from datetime import datetime
from pathlib import Path
import requests
from bs4 import BeautifulSoup
import re

class WebResearchEngine:
    """Motor de investigación web sin dependencias de Chrome"""
    
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })
        self.results = []
    
    async def google_search(self, query: str, num_results: int = 10) -> List[Dict]:
        """Busca en Google usando web scraping"""
        print(f"🔍 Buscando en Google: {query}")
        
        results = []
        try:
            # Usar API alternativa (busca en múltiples fuentes)
            url = f"https://www.google.com/search?q={query}&num={num_results}"
            
            response = self.session.get(url, timeout=10)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Extraer resultados
            for g in soup.find_all('div', class_='g'):
                try:
                    link = g.find('a', href=True)
                    title = g.find('h3')
                    snippet = g.find('div', class_='VwiC3b')
                    
                    if link and title and snippet:
                        result = {
                            'title': title.text,
                            'url': link['href'],
                            'snippet': snippet.text,
                            'source': 'google',
                            'timestamp': datetime.now().isoformat()
                        }
                        results.append(result)
                except:
                    continue
            
            print(f"✅ Encontrados: {len(results)} resultados")
            return results
        
        except Exception as e:
            print(f"⚠️ Error en búsqueda: {e}")
            return []
    
    async def fetch_page(self, url: str) -> Dict:
        """Extrae contenido de una página"""
        print(f"📄 Extrayendo: {url}")
        
        try:
            response = self.session.get(url, timeout=15)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Extraer elementos
            title = soup.find('title')
            meta_desc = soup.find('meta', {'name': 'description'})
            h1 = soup.find('h1')
            paragraphs = soup.find_all('p')
            
            # Limpiar contenido
            content = '\n'.join([p.get_text().strip() for p in paragraphs[:10]])
            
            result = {
                'url': url,
                'title': title.text if title else 'N/A',
                'meta_description': meta_desc.get('content') if meta_desc else 'N/A',
                'h1': h1.text if h1 else 'N/A',
                'content': content[:500] + '...' if len(content) > 500 else content,
                'status': 'success',
                'timestamp': datetime.now().isoformat()
            }
            
            print(f"✅ Extraído: {title.text if title else 'Sin título'}")
            return result
        
        except Exception as e:
            print(f"⚠️ Error extrayendo: {e}")
            return {'url': url, 'status': 'error', 'error': str(e)}
    
    async def analyze_content(self, text: str, query: str) -> Dict:
        """Analiza contenido y busca relevancia con query"""
        
        # Buscar palabras clave
        keywords = query.split()
        found_keywords = {}
        
        for keyword in keywords:
            count = len(re.findall(keyword.lower(), text.lower()))
            if count > 0:
                found_keywords[keyword] = count
        
        # Relevancia (0-100)
        relevance = min(100, len(found_keywords) * 25)
        
        return {
            'keywords_found': found_keywords,
            'relevance_score': relevance,
            'word_count': len(text.split()),
            'analysis_timestamp': datetime.now().isoformat()
        }
    
    async def search_and_analyze(self, query: str, depth: int = 3) -> Dict:
        """Búsqueda profunda: busca → extrae → analiza"""
        
        print(f"\n{'='*60}")
        print(f"🔬 INVESTIGACIÓN WEB: {query}")
        print(f"{'='*60}\n")
        
        investigation = {
            'query': query,
            'depth': depth,
            'timestamp': datetime.now().isoformat(),
            'stages': {
                'search': None,
                'extraction': None,
                'analysis': None
            }
        }
        
        # STAGE 1: Búsqueda
        print(f"📍 STAGE 1: BÚSQUEDA")
        search_results = await self.google_search(query, num_results=depth)
        investigation['stages']['search'] = {
            'total_results': len(search_results),
            'results': search_results[:depth]
        }
        
        # STAGE 2: Extracción de contenido
        print(f"\n📍 STAGE 2: EXTRACCIÓN")
        extracted_content = []
        for result in search_results[:depth]:
            content = await self.fetch_page(result['url'])
            extracted_content.append(content)
            await asyncio.sleep(1)  # Rate limiting
        
        investigation['stages']['extraction'] = {
            'total_extracted': len(extracted_content),
            'content': extracted_content
        }
        
        # STAGE 3: Análisis
        print(f"\n📍 STAGE 3: ANÁLISIS")
        analyses = []
        for content in extracted_content:
            if content.get('status') == 'success':
                analysis = await self.analyze_content(content['content'], query)
                analysis['source_url'] = content['url']
                analyses.append(analysis)
        
        investigation['stages']['analysis'] = {
            'total_analyzed': len(analyses),
            'analyses': analyses
        }
        
        # Summary
        investigation['summary'] = {
            'total_sources': len(search_results),
            'total_extracted': len(extracted_content),
            'total_analyzed': len(analyses),
            'avg_relevance': sum(a['relevance_score'] for a in analyses) / len(analyses) if analyses else 0
        }
        
        return investigation
    
    async def research_topic(self, topic: str, subtopics: List[str] = None) -> Dict:
        """Investigación de tópico con subtópicos"""
        
        research = {
            'main_topic': topic,
            'timestamp': datetime.now().isoformat(),
            'investigations': {}
        }
        
        # Investigación principal
        main_inv = await self.search_and_analyze(topic, depth=5)
        research['investigations'][topic] = main_inv
        
        # Subtópicos
        if subtopics:
            for subtopic in subtopics:
                full_query = f"{topic} {subtopic}"
                sub_inv = await self.search_and_analyze(full_query, depth=3)
                research['investigations'][subtopic] = sub_inv
                await asyncio.sleep(2)
        
        return research
    
    def save_research(self, research: Dict, filename: str = None) -> Path:
        """Guarda investigación a JSON"""
        if not filename:
            filename = f"research_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        
        path = Path(f"/workspace/anais-workspace/shared/proyectos/web-research/results/{filename}")
        path.parent.mkdir(parents=True, exist_ok=True)
        
        with open(path, 'w', encoding='utf-8') as f:
            json.dump(research, f, indent=2, ensure_ascii=False)
        
        print(f"\n💾 Investigación guardada: {path}")
        return path
    
    def print_report(self, research: Dict):
        """Imprime reporte legible"""
        
        print(f"\n{'='*60}")
        print(f"📊 REPORTE DE INVESTIGACIÓN")
        print(f"{'='*60}\n")
        
        for topic, investigation in research.get('investigations', {}).items():
            print(f"\n🔍 TÓPICO: {topic}")
            print(f"   Fuentes encontradas: {investigation['summary']['total_sources']}")
            print(f"   Contenido extraído: {investigation['summary']['total_extracted']}")
            print(f"   Relevancia promedio: {investigation['summary']['avg_relevance']:.1f}%")
            
            if investigation['stages']['search']['results']:
                print(f"\n   Top 3 Resultados:")
                for i, result in enumerate(investigation['stages']['search']['results'][:3], 1):
                    print(f"   {i}. {result['title']}")
                    print(f"      URL: {result['url']}")
                    print(f"      {result['snippet'][:100]}...")

async def main():
    """Demo del motor de investigación"""
    
    engine = WebResearchEngine()
    
    # Ejemplo: Investigación sobre AI y Machine Learning
    research = await engine.research_topic(
        "Artificial Intelligence 2026",
        subtopics=["machine learning trends", "neural networks"]
    )
    
    # Guardar
    engine.save_research(research)
    
    # Imprimir reporte
    engine.print_report(research)

if __name__ == "__main__":
    asyncio.run(main())
