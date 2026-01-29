#!/usr/bin/env python3
"""
Search API - Cliente Python
"""

import requests
import json
from typing import List, Dict

class SearchAPIClient:
    def __init__(self, base_url: str = "http://localhost:8000"):
        self.base_url = base_url
        self.session = requests.Session()
    
    def search(self, query: str, limit: int = 10) -> Dict:
        """Realiza una búsqueda"""
        response = self.session.get(
            f"{self.base_url}/search",
            params={"q": query, "limit": limit}
        )
        response.raise_for_status()
        return response.json()
    
    def get_documents(self, category: str = None, limit: int = 20) -> Dict:
        """Lista documentos"""
        params = {"limit": limit}
        if category:
            params["category"] = category
        
        response = self.session.get(
            f"{self.base_url}/documents",
            params=params
        )
        response.raise_for_status()
        return response.json()
    
    def get_document(self, doc_id: str) -> Dict:
        """Obtiene un documento"""
        response = self.session.get(f"{self.base_url}/documents/{doc_id}")
        response.raise_for_status()
        return response.json()
    
    def get_categories(self) -> Dict:
        """Lista categorías"""
        response = self.session.get(f"{self.base_url}/categories")
        response.raise_for_status()
        return response.json()
    
    def add_document(self, doc: Dict) -> Dict:
        """Agrega un documento"""
        response = self.session.post(
            f"{self.base_url}/documents",
            json=doc
        )
        response.raise_for_status()
        return response.json()
    
    def delete_document(self, doc_id: str) -> Dict:
        """Elimina un documento"""
        response = self.session.delete(f"{self.base_url}/documents/{doc_id}")
        response.raise_for_status()
        return response.json()
    
    def get_status(self) -> Dict:
        """Obtiene el estado de la API"""
        response = self.session.get(f"{self.base_url}/status")
        response.raise_for_status()
        return response.json()
    
    def health_check(self) -> bool:
        """Verifica si la API está disponible"""
        try:
            response = self.session.get(f"{self.base_url}/health")
            return response.status_code == 200
        except:
            return False

def main():
    """Ejemplos de uso"""
    client = SearchAPIClient()
    
    print("🔍 Search API - Cliente Python\n")
    
    # Verificar salud
    if not client.health_check():
        print("❌ API no está disponible")
        return
    
    print("✅ API disponible\n")
    
    # Obtener estado
    status = client.get_status()
    print(f"📊 Estado: {json.dumps(status, indent=2)}\n")
    
    # Listar categorías
    categories = client.get_categories()
    print(f"📂 Categorías: {categories['categories']}\n")
    
    # Búsquedas de ejemplo
    queries = ["python", "api", "docker", "web3"]
    
    for query in queries:
        print(f"🔎 Búsqueda: '{query}'")
        results = client.search(query, limit=3)
        print(f"   Resultados: {results['total']}")
        print(f"   Tiempo: {results['time_ms']}ms")
        for result in results['results']:
            print(f"   - {result['title']} (score: {result['score']})")
        print()
    
    # Obtener documento específico
    doc = client.get_document("1")
    print(f"📄 Documento #1: {doc['title']}\n")

if __name__ == "__main__":
    main()
