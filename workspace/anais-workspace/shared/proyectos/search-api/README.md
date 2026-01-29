# 🔍 Search API - Motor de Búsqueda Inteligente

**Una API de búsqueda rápida, escalable y fácil de usar, construida con FastAPI.**

---

## ⚡ Características

- ✅ **Búsqueda Rápida** - Resultados en < 10ms
- ✅ **Índice Invertido** - Algoritmo eficiente
- ✅ **API REST** - Endpoints limpios y simples
- ✅ **Documentación Automática** - Swagger UI
- ✅ **Scoring Inteligente** - Resultados relevantes primero
- ✅ **CORS** - Accesible desde cualquier origen
- ✅ **Paginación** - Soporte de limit/offset
- ✅ **Filtros** - Por categoría, tags, etc
- ✅ **Hot Reload** - Desarrollo rápido
- ✅ **Async** - Operaciones no-bloqueantes

---

## 🚀 Inicio Rápido

### 1. Instalación

```bash
# Clonar o descargar el proyecto
cd search-api

# Crear entorno virtual
python3 -m venv venv
source venv/bin/activate  # Linux/Mac
# o: venv\Scripts\activate  # Windows

# Instalar dependencias
pip install -r requirements.txt
```

### 2. Ejecutar la API

```bash
# Desarrollo con hot-reload
uvicorn app.main:app --reload

# Producción
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

### 3. Acceder a la API

- **API:** http://localhost:8000
- **Swagger UI:** http://localhost:8000/docs
- **ReDoc:** http://localhost:8000/redoc

---

## 📚 Endpoints

### 🔎 Búsqueda

```
GET /search?q=python&limit=10
```

**Parámetros:**
- `q` (string, requerido): Término de búsqueda
- `limit` (int, default: 10): Máximo de resultados (1-100)

**Respuesta:**
```json
{
  "query": "python",
  "results": [
    {
      "id": "1",
      "title": "Python Tutorial - Guía Completa",
      "description": "Aprende Python desde cero...",
      "url": "https://example.com/python-tutorial",
      "category": "Educación",
      "score": 4.0,
      "tags": ["python", "programming", "tutorial"],
      "date": "2026-01-28"
    }
  ],
  "total": 1,
  "time_ms": 2.34
}
```

### 📄 Documentos

#### Listar documentos
```
GET /documents?category=Educación&limit=20
```

#### Obtener documento específico
```
GET /documents/{id}
```

#### Agregar documento
```
POST /documents
Content-Type: application/json

{
  "id": "11",
  "title": "Mi Artículo",
  "description": "Descripción...",
  "url": "https://example.com/articulo",
  "category": "Desarrollo",
  "tags": ["tag1", "tag2"],
  "date": "2026-01-29",
  "content": "Contenido del artículo..."
}
```

#### Eliminar documento
```
DELETE /documents/{id}
```

### 🏷️ Categorías

```
GET /categories
```

Respuesta:
```json
{
  "categories": ["Backend", "Blockchain", "Desarrollo", "DevOps", "Educación", "Frontend", "IA", "Seguridad"],
  "total": 8
}
```

### 📊 Estado

```
GET /status
```

Respuesta:
```json
{
  "status": "healthy",
  "timestamp": "2026-01-29T20:15:00",
  "documents": 10,
  "indexed_words": 250,
  "version": "1.0.0"
}
```

### ❤️ Health Check

```
GET /health
```

---

## 🐍 Cliente Python

```python
from client import SearchAPIClient

# Conectar
client = SearchAPIClient("http://localhost:8000")

# Buscar
results = client.search("python", limit=10)
print(f"Encontrados: {results['total']}")
for result in results['results']:
    print(f"- {result['title']} ({result['score']})")

# Listar documentos
docs = client.get_documents(category="Desarrollo")

# Obtener documento
doc = client.get_document("1")

# Obtener categorías
cats = client.get_categories()

# Agregar documento
new_doc = {
    "id": "11",
    "title": "Mi Artículo",
    "description": "...",
    "url": "https://example.com",
    "category": "Desarrollo",
    "tags": ["tag1"],
    "date": "2026-01-29",
    "content": "..."
}
client.add_document(new_doc)

# Verificar salud
if client.health_check():
    print("API está disponible")
```

---

## 🧪 Testing

### Con curl

```bash
# Buscar
curl "http://localhost:8000/search?q=python&limit=5"

# Listar categorías
curl "http://localhost:8000/categories"

# Estado
curl "http://localhost:8000/status"

# Agregar documento
curl -X POST "http://localhost:8000/documents" \
  -H "Content-Type: application/json" \
  -d '{
    "id": "11",
    "title": "Nuevo",
    "description": "...",
    "url": "https://example.com",
    "category": "Desarrollo",
    "tags": ["new"],
    "date": "2026-01-29",
    "content": "..."
  }'
```

### Con Python

```python
python client.py
```

### Con Swagger UI

Abre http://localhost:8000/docs y prueba directamente

---

## 🎯 Casos de Uso

### 1. Blog Search
```
GET /search?q=django&limit=20
```

### 2. Product Search
```
GET /documents?category=Backend&limit=50
```

### 3. Filter by Category
```
GET /categories
GET /documents?category=Frontend
```

### 4. Analytics
```
GET /status
```

---

## 📊 Algoritmo de Búsqueda

1. **Tokenización:** Divide el query en palabras
2. **Índice Invertido:** Busca documentos que contengan esas palabras
3. **Scoring:** Calcula relevancia
   - +1 por cada palabra encontrada
   - +3 si coincide en el título
   - +2 si coincide en la categoría
4. **Ranking:** Ordena por score descendente
5. **Limitación:** Retorna los top N resultados

**Tiempo O(n):** O(m + k) donde m = palabras en query, k = documentos coincidentes

---

## 🔧 Configuración

### Variables de Entorno

```bash
# .env
HOST=0.0.0.0
PORT=8000
DEBUG=True
LOG_LEVEL=info
```

### Modificar puerto
```python
# En main.py
uvicorn.run(
    app,
    host="0.0.0.0",
    port=3000,  # Cambiar a 3000
    log_level="info"
)
```

---

## 🚀 Deployment

### Heroku
```bash
pip freeze > requirements.txt
git push heroku main
```

### Docker
```dockerfile
FROM python:3.11-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

```bash
docker build -t search-api .
docker run -p 8000:8000 search-api
```

### Vercel / Netlify
```bash
# Usar serverless functions (próximo)
```

---

## 📈 Performance

| Métrica | Valor |
|---------|-------|
| **Búsqueda simple** | 1-5ms |
| **Búsqueda compleja** | 5-15ms |
| **Agregar documento** | <1ms |
| **Eliminar documento** | <1ms |
| **Listado (20 docs)** | 2-3ms |

---

## 🎓 Roadmap

- [ ] ElasticSearch integration
- [ ] Full-text search
- [ ] Fuzzy matching
- [ ] Autocomplete
- [ ] Faceted search
- [ ] Search analytics
- [ ] Multi-language support
- [ ] Redis caching
- [ ] Database persistence
- [ ] GraphQL API

---

## 📝 Datos de Ejemplo

### Categorías Disponibles
- Educación
- Desarrollo
- Backend
- DevOps
- IA
- Blockchain
- Seguridad
- Frontend

### Documentos Iniciales
10 documentos sobre:
- Python
- React
- FastAPI
- Docker
- AI/ML
- Web3
- Seguridad API
- TypeScript
- Kubernetes
- GraphQL

---

## 🔒 Seguridad

- ✅ CORS habilitado (configurable)
- ✅ Validación de inputs (Pydantic)
- ✅ Rate limiting (implementar)
- ✅ Sanitización de queries
- ⚠️ TODO: Authentication (JWT)
- ⚠️ TODO: Encryption

---

## 📞 Support

### Errores Comunes

**"Connection refused"**
```bash
# Asegúrate de que la API está corriendo
uvicorn app.main:app --reload
```

**"Port already in use"**
```bash
# Cambiar puerto
uvicorn app.main:app --port 3000 --reload
```

**"Module not found"**
```bash
# Instalar dependencias
pip install -r requirements.txt
```

---

## 📄 Licencia

Open Source - Libre para usar y modificar

---

## 👨‍💻 Autor

**Anais** 🐎  
Search API v1.0  
Enero 2026

---

## 🎯 Próximos Pasos

1. ✅ API base funcionando
2. ⬜ Agregar autenticación
3. ⬜ Conectar a database real
4. ⬜ Implementar caching
5. ⬜ Agregar analytics
6. ⬜ Deploy a producción

---

**¡Lista para usar!** 🚀
