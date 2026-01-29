#!/usr/bin/env python3
"""
Search API - Demo de uso
"""

from app.main import app, search_index
from fastapi.testclient import TestClient

# Client para testing
client = TestClient(app)

def print_section(title):
    print(f"\n{'='*60}")
    print(f"🔍 {title}")
    print(f"{'='*60}\n")

def main():
    print("\n" + "🚀" * 30)
    print("SEARCH API - DEMO")
    print("🚀" * 30)
    
    # 1. Status
    print_section("1. Estado de la API")
    response = client.get("/status")
    print(f"Status: {response.json()['status']}")
    print(f"Documentos: {response.json()['documents']}")
    print(f"Palabras indexadas: {response.json()['indexed_words']}")
    
    # 2. Categorías
    print_section("2. Categorías Disponibles")
    response = client.get("/categories")
    cats = response.json()['categories']
    print(f"Total: {len(cats)}")
    for cat in cats:
        print(f"  • {cat}")
    
    # 3. Búsquedas
    print_section("3. Búsquedas de Ejemplo")
    queries = ["python", "api", "docker", "web3", "typescript"]
    
    for query in queries:
        response = client.get(f"/search?q={query}&limit=3")
        data = response.json()
        print(f"\n📌 Búsqueda: '{query}'")
        print(f"   Resultados: {data['total']}")
        print(f"   Tiempo: {data['time_ms']}ms")
        
        for i, result in enumerate(data['results'], 1):
            print(f"   {i}. {result['title']}")
            print(f"      Score: {result['score']} | Categoría: {result['category']}")
    
    # 4. Búsqueda específica
    print_section("4. Búsqueda Específica: 'kubernetes'")
    response = client.get("/search?q=kubernetes&limit=5")
    data = response.json()
    
    if data['results']:
        for result in data['results']:
            print(f"\n📄 {result['title']}")
            print(f"   URL: {result['url']}")
            print(f"   Descripción: {result['description']}")
            print(f"   Tags: {', '.join(result['tags'])}")
            print(f"   Score: {result['score']}")
    else:
        print("No se encontraron resultados")
    
    # 5. Listar documentos por categoría
    print_section("5. Documentos por Categoría")
    response = client.get("/documents?category=Backend&limit=3")
    docs = response.json()['documents']
    print(f"Backend ({len(docs)} documentos):")
    for doc in docs:
        print(f"  • {doc['title']}")
    
    # 6. Obtener documento específico
    print_section("6. Documento Específico (ID: 1)")
    response = client.get("/documents/1")
    doc = response.json()
    print(f"Título: {doc['title']}")
    print(f"Categoría: {doc['category']}")
    print(f"Descripción: {doc['description']}")
    print(f"Tags: {', '.join(doc['tags'])}")
    print(f"URL: {doc['url']}")
    print(f"Fecha: {doc['date']}")
    
    # 7. Agregar documento
    print_section("7. Agregar Nuevo Documento")
    new_doc = {
        "id": "11",
        "title": "AI Safety - Asegurando el Futuro",
        "description": "Cómo garantizar que la IA sea segura y beneficiosa",
        "url": "https://example.com/ai-safety",
        "category": "IA",
        "tags": ["ai", "safety", "ethics", "future"],
        "date": "2026-01-29",
        "content": "AI Safety es crítico para el futuro. Necesitamos regulaciones..."
    }
    
    response = client.post("/documents", json=new_doc)
    result = response.json()
    print(f"Status: {result['status']}")
    print(f"ID: {result['id']}")
    print(f"Mensaje: {result['message']}")
    
    # 8. Verificar que fue agregado
    print_section("8. Verificar Documento Agregado")
    response = client.get("/documents/11")
    doc = response.json()
    print(f"✅ Documento agregado correctamente: {doc['title']}")
    
    # 9. Búsqueda del nuevo documento
    print_section("9. Búsqueda del Nuevo Documento")
    response = client.get("/search?q=safety&limit=10")
    data = response.json()
    print(f"Búsqueda 'safety': {data['total']} resultados")
    for result in data['results']:
        print(f"  • {result['title']} (Score: {result['score']})")
    
    # 10. Eliminar documento
    print_section("10. Eliminar Documento")
    response = client.delete("/documents/11")
    result = response.json()
    print(f"Status: {result['status']}")
    print(f"ID eliminado: {result['id']}")
    
    # 11. Verificar que fue eliminado
    print_section("11. Verificar Que Fue Eliminado")
    response = client.get("/search?q=safety&limit=10")
    data = response.json()
    print(f"Búsqueda 'safety' después de eliminar: {data['total']} resultados")
    if data['total'] == 0:
        print("✅ Documento eliminado correctamente")
    
    # 12. Performance test
    print_section("12. Test de Performance")
    import time
    
    queries_perf = ["python", "api", "docker", "web3", "fastapi", "kubernetes"]
    times = []
    
    for query in queries_perf:
        start = time.time()
        response = client.get(f"/search?q={query}&limit=10")
        elapsed = (time.time() - start) * 1000
        api_time = response.json()['time_ms']
        times.append(api_time)
        print(f"Query '{query}': {api_time:.2f}ms")
    
    avg_time = sum(times) / len(times)
    print(f"\n⚡ Tiempo promedio: {avg_time:.2f}ms")
    print(f"📊 Min: {min(times):.2f}ms | Max: {max(times):.2f}ms")
    
    # Resumen final
    print("\n" + "=" * 60)
    print("✅ DEMO COMPLETADA")
    print("=" * 60)
    print(f"\n📚 Total de documentos: {len(search_index.documents)}")
    print(f"🔍 Palabras indexadas: {len(search_index.inverted_index)}")
    print(f"⚡ Tiempo promedio de búsqueda: {avg_time:.2f}ms")
    print("\n🚀 Accede a http://localhost:8000/docs para ver la documentación\n")

if __name__ == "__main__":
    main()
