#!/usr/bin/env python3
"""
Search API - Motor de búsqueda inteligente
FastAPI + Elasticsearch-like performance con datos en memoria
"""

from fastapi import FastAPI, Query, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime
import asyncio
import json
from pathlib import Path

# Modelos
class SearchResult(BaseModel):
    id: str
    title: str
    description: str
    url: str
    category: str
    score: float
    tags: List[str]
    date: str

class SearchResponse(BaseModel):
    query: str
    results: List[SearchResult]
    total: int
    time_ms: float

class Document(BaseModel):
    id: str
    title: str
    description: str
    url: str
    category: str
    tags: List[str]
    date: str
    content: str

# Inicializar FastAPI
app = FastAPI(
    title="Search API",
    description="Motor de búsqueda inteligente y escalable",
    version="1.0.0"
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Base de datos en memoria (índice)
class SearchIndex:
    def __init__(self):
        self.documents: dict = {}
        self.inverted_index: dict = {}
        self.load_sample_data()
    
    def load_sample_data(self):
        """Carga datos de ejemplo"""
        sample_docs = [
            {
                "id": "1",
                "title": "Python Tutorial - Guía Completa",
                "description": "Aprende Python desde cero con este tutorial interactivo",
                "url": "https://example.com/python-tutorial",
                "category": "Educación",
                "tags": ["python", "programming", "tutorial", "education"],
                "date": "2026-01-28",
                "content": "Python es un lenguaje de programación versátil. Aprende sintaxis, funciones, clases..."
            },
            {
                "id": "2",
                "title": "React 19 - Nuevas Features",
                "description": "Descubre las nuevas características de React 19",
                "url": "https://example.com/react-19",
                "category": "Desarrollo",
                "tags": ["react", "javascript", "frontend", "web"],
                "date": "2026-01-27",
                "content": "React 19 trae mejoras significativas en performance. Server Components, Actions..."
            },
            {
                "id": "3",
                "title": "FastAPI - Construir APIs Rápidamente",
                "description": "Crea APIs modernas con FastAPI en Python",
                "url": "https://example.com/fastapi-guide",
                "category": "Backend",
                "tags": ["fastapi", "api", "python", "backend"],
                "date": "2026-01-26",
                "content": "FastAPI es un framework web moderno para construir APIs. Async by default..."
            },
            {
                "id": "4",
                "title": "Docker para Desarrolladores",
                "description": "Aprende Docker y containerización",
                "url": "https://example.com/docker-guide",
                "category": "DevOps",
                "tags": ["docker", "containers", "devops", "deployment"],
                "date": "2026-01-25",
                "content": "Docker permite empacar aplicaciones en contenedores. Aprende Dockerfile, Docker Compose..."
            },
            {
                "id": "5",
                "title": "AI y Machine Learning 2026",
                "description": "El futuro de la IA: tendencias y predicciones",
                "url": "https://example.com/ai-trends",
                "category": "IA",
                "tags": ["ai", "machine-learning", "neural-networks", "future"],
                "date": "2026-01-24",
                "content": "La IA está transformando todos los sectores. GPT-5, AGI, quantum computing..."
            },
            {
                "id": "6",
                "title": "Web3 y Blockchain Explicado",
                "description": "Entender Web3, Smart Contracts y DeFi",
                "url": "https://example.com/web3-guide",
                "category": "Blockchain",
                "tags": ["web3", "blockchain", "crypto", "defi"],
                "date": "2026-01-23",
                "content": "Web3 representa la próxima generación de internet. Descentralización, tokens..."
            },
            {
                "id": "7",
                "title": "Seguridad en APIs REST",
                "description": "Best practices para proteger tus APIs",
                "url": "https://example.com/api-security",
                "category": "Seguridad",
                "tags": ["security", "api", "authentication", "encryption"],
                "date": "2026-01-22",
                "content": "Protege tus APIs: JWT, OAuth2, rate limiting, HTTPS..."
            },
            {
                "id": "8",
                "title": "Typescript - Tipado Estático para JavaScript",
                "description": "Aprende TypeScript y escribe código más seguro",
                "url": "https://example.com/typescript",
                "category": "Frontend",
                "tags": ["typescript", "javascript", "types", "frontend"],
                "date": "2026-01-21",
                "content": "TypeScript agrega tipado estático a JavaScript. Interfaces, generics, decorators..."
            },
            {
                "id": "9",
                "title": "Kubernetes en Producción",
                "description": "Orquestar contenedores con K8s",
                "url": "https://example.com/kubernetes",
                "category": "DevOps",
                "tags": ["kubernetes", "k8s", "orchestration", "devops"],
                "date": "2026-01-20",
                "content": "Kubernetes es el estándar de orquestación. Pods, Services, Deployments..."
            },
            {
                "id": "10",
                "title": "GraphQL vs REST",
                "description": "Comparación entre GraphQL y REST APIs",
                "url": "https://example.com/graphql-vs-rest",
                "category": "Backend",
                "tags": ["graphql", "rest", "api", "backend"],
                "date": "2026-01-19",
                "content": "GraphQL ofrece más flexibilidad que REST. Query lenguaje, sin over-fetching..."
            }
        ]
        
        for doc in sample_docs:
            self.add_document(doc)
    
    def add_document(self, doc: dict):
        """Agrega un documento al índice"""
        self.documents[doc["id"]] = doc
        
        # Crear índice invertido
        text = (doc["title"] + " " + doc["description"] + " " + " ".join(doc["tags"])).lower()
        words = set(text.split())
        
        for word in words:
            if word not in self.inverted_index:
                self.inverted_index[word] = []
            self.inverted_index[word].append(doc["id"])
    
    def search(self, query: str, limit: int = 10) -> List[tuple]:
        """Busca documentos y retorna con score"""
        if not query:
            return []
        
        query_words = set(query.lower().split())
        results = {}
        
        # Buscar documentos que coincidan
        for word in query_words:
            matching_docs = self.inverted_index.get(word, [])
            for doc_id in matching_docs:
                if doc_id not in results:
                    results[doc_id] = 0
                results[doc_id] += 1
        
        # Calcular scores
        scored_results = []
        for doc_id, count in results.items():
            doc = self.documents[doc_id]
            
            # Score = frecuencia de palabras + match en título (bonus)
            score = count
            
            # Bonus si coincide en título
            if any(word in doc["title"].lower() for word in query_words):
                score += 3
            
            # Bonus si coincide en categoría
            if any(word in doc["category"].lower() for word in query_words):
                score += 2
            
            scored_results.append((doc_id, score))
        
        # Ordenar por score descendente
        scored_results.sort(key=lambda x: x[1], reverse=True)
        
        return scored_results[:limit]

# Instanciar índice
search_index = SearchIndex()

# Endpoints

@app.get("/", tags=["Info"])
async def root():
    """Información de la API"""
    return {
        "name": "Search API",
        "version": "1.0.0",
        "description": "Motor de búsqueda inteligente",
        "endpoints": {
            "search": "/search?q=query&limit=10",
            "documents": "/documents",
            "document": "/documents/{id}",
            "status": "/status"
        }
    }

@app.get("/search", response_model=SearchResponse, tags=["Search"])
async def search(
    q: str = Query(..., description="Término de búsqueda", min_length=1),
    limit: int = Query(10, description="Número de resultados", ge=1, le=100)
):
    """
    Busca en la base de datos
    
    Query params:
    - q: Término de búsqueda (requerido)
    - limit: Máximo 100 resultados (default: 10)
    """
    start_time = datetime.now()
    
    # Realizar búsqueda
    results_scored = search_index.search(q, limit)
    
    # Construir respuesta
    results = []
    for doc_id, score in results_scored:
        doc = search_index.documents[doc_id]
        results.append(SearchResult(
            id=doc["id"],
            title=doc["title"],
            description=doc["description"],
            url=doc["url"],
            category=doc["category"],
            score=round(score, 2),
            tags=doc["tags"],
            date=doc["date"]
        ))
    
    # Tiempo de búsqueda
    elapsed = (datetime.now() - start_time).total_seconds() * 1000
    
    return SearchResponse(
        query=q,
        results=results,
        total=len(results),
        time_ms=round(elapsed, 2)
    )

@app.get("/documents", tags=["Documents"])
async def list_documents(
    category: Optional[str] = Query(None, description="Filtrar por categoría"),
    limit: int = Query(20, ge=1, le=100)
):
    """Lista todos los documentos (con paginación)"""
    docs = list(search_index.documents.values())
    
    if category:
        docs = [d for d in docs if d["category"].lower() == category.lower()]
    
    return {
        "total": len(docs),
        "documents": docs[:limit]
    }

@app.get("/documents/{doc_id}", tags=["Documents"])
async def get_document(doc_id: str):
    """Obtiene un documento específico"""
    if doc_id not in search_index.documents:
        raise HTTPException(status_code=404, detail="Documento no encontrado")
    
    return search_index.documents[doc_id]

@app.get("/categories", tags=["Info"])
async def get_categories():
    """Lista todas las categorías"""
    categories = set(doc["category"] for doc in search_index.documents.values())
    return {
        "categories": sorted(list(categories)),
        "total": len(categories)
    }

@app.get("/status", tags=["Info"])
async def status():
    """Estado de la API"""
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "documents": len(search_index.documents),
        "indexed_words": len(search_index.inverted_index),
        "version": "1.0.0"
    }

@app.post("/documents", tags=["Documents"])
async def add_document(doc: Document):
    """Agrega un nuevo documento al índice"""
    if doc.id in search_index.documents:
        raise HTTPException(status_code=400, detail="Documento ya existe")
    
    doc_dict = doc.dict()
    search_index.add_document(doc_dict)
    
    return {
        "status": "created",
        "id": doc.id,
        "message": "Documento agregado exitosamente"
    }

@app.delete("/documents/{doc_id}", tags=["Documents"])
async def delete_document(doc_id: str):
    """Elimina un documento"""
    if doc_id not in search_index.documents:
        raise HTTPException(status_code=404, detail="Documento no encontrado")
    
    del search_index.documents[doc_id]
    
    return {
        "status": "deleted",
        "id": doc_id
    }

# Health check para uptime monitoring
@app.get("/health", tags=["Info"])
async def health():
    """Health check para load balancers"""
    return {"status": "ok"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8000,
        log_level="info"
    )
