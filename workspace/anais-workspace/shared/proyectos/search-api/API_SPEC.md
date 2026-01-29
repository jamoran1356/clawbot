# 📋 Search API - Especificación Completa

## 🏗️ Arquitectura

```
┌─────────────────────────────────────────────────────────┐
│                    Cliente (Browser/App)                 │
└────────────────────┬────────────────────────────────────┘
                     │ HTTP/REST
┌────────────────────▼────────────────────────────────────┐
│                   FastAPI Server                         │
│  ┌──────────────────────────────────────────────────┐  │
│  │         CORS Middleware                          │  │
│  └──────────────────────────────────────────────────┘  │
│  ┌──────────────────────────────────────────────────┐  │
│  │    Routes (Search, Documents, Categories)        │  │
│  └────────────────┬─────────────────────────────────┘  │
│                   │                                     │
│  ┌────────────────▼─────────────────────────────────┐  │
│  │         SearchIndex (In-Memory)                  │  │
│  │  ├── documents: Dict[id, Document]              │  │
│  │  └── inverted_index: Dict[word, List[id]]       │  │
│  └──────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────┘
```

---

## 🔗 Endpoints

### Base URL
```
http://localhost:8000
```

### 1. GET /

**Info de la API**

```
GET /
```

**Response (200):**
```json
{
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
```

---

### 2. GET /search

**Búsqueda Principal**

```
GET /search?q={query}&limit={limit}
```

**Query Parameters:**
| Parámetro | Tipo | Requerido | Default | Rango |
|-----------|------|-----------|---------|-------|
| q | string | ✅ Sí | - | min: 1 char |
| limit | integer | ❌ No | 10 | 1-100 |

**Response (200):**
```json
{
  "query": "string",
  "results": [
    {
      "id": "string",
      "title": "string",
      "description": "string",
      "url": "string",
      "category": "string",
      "score": 0.0,
      "tags": ["string"],
      "date": "string"
    }
  ],
  "total": 0,
  "time_ms": 0.0
}
```

**Response (400):**
```json
{
  "detail": [
    {
      "loc": ["query", "q"],
      "msg": "ensure this value has at least 1 characters",
      "type": "value_error.string.too_short"
    }
  ]
}
```

**Ejemplos:**
```
GET /search?q=python
GET /search?q=docker&limit=5
GET /search?q=api%20rest&limit=20
```

---

### 3. GET /documents

**Listar Documentos**

```
GET /documents?category={category}&limit={limit}
```

**Query Parameters:**
| Parámetro | Tipo | Default |
|-----------|------|---------|
| category | string | (none) |
| limit | integer | 20 |

**Response (200):**
```json
{
  "total": 0,
  "documents": [
    {
      "id": "string",
      "title": "string",
      "description": "string",
      "url": "string",
      "category": "string",
      "tags": ["string"],
      "date": "string",
      "content": "string"
    }
  ]
}
```

**Ejemplos:**
```
GET /documents
GET /documents?category=Backend
GET /documents?category=Frontend&limit=50
```

---

### 4. GET /documents/{id}

**Obtener Documento Específico**

```
GET /documents/{id}
```

**Path Parameters:**
| Parámetro | Tipo | Descripción |
|-----------|------|-------------|
| id | string | Document ID |

**Response (200):**
```json
{
  "id": "string",
  "title": "string",
  "description": "string",
  "url": "string",
  "category": "string",
  "tags": ["string"],
  "date": "string",
  "content": "string"
}
```

**Response (404):**
```json
{
  "detail": "Documento no encontrado"
}
```

**Ejemplo:**
```
GET /documents/1
```

---

### 5. GET /categories

**Listar Categorías**

```
GET /categories
```

**Response (200):**
```json
{
  "categories": [
    "Backend",
    "Blockchain",
    "Desarrollo",
    "DevOps",
    "Educación",
    "Frontend",
    "IA",
    "Seguridad"
  ],
  "total": 8
}
```

---

### 6. GET /status

**Estado de la API**

```
GET /status
```

**Response (200):**
```json
{
  "status": "healthy",
  "timestamp": "2026-01-29T20:15:00.000000",
  "documents": 10,
  "indexed_words": 250,
  "version": "1.0.0"
}
```

---

### 7. POST /documents

**Agregar Documento**

```
POST /documents
Content-Type: application/json

{
  "id": "string",
  "title": "string",
  "description": "string",
  "url": "string",
  "category": "string",
  "tags": ["string"],
  "date": "string",
  "content": "string"
}
```

**Request Body:**
```json
{
  "id": "11",
  "title": "Mi Nuevo Artículo",
  "description": "Una descripción interesante",
  "url": "https://example.com/articulo",
  "category": "Backend",
  "tags": ["python", "fastapi", "api"],
  "date": "2026-01-29",
  "content": "Contenido del artículo..."
}
```

**Response (200):**
```json
{
  "status": "created",
  "id": "11",
  "message": "Documento agregado exitosamente"
}
```

**Response (400):**
```json
{
  "detail": "Documento ya existe"
}
```

---

### 8. DELETE /documents/{id}

**Eliminar Documento**

```
DELETE /documents/{id}
```

**Path Parameters:**
| Parámetro | Tipo | Descripción |
|-----------|------|-------------|
| id | string | Document ID |

**Response (200):**
```json
{
  "status": "deleted",
  "id": "1"
}
```

**Response (404):**
```json
{
  "detail": "Documento no encontrado"
}
```

---

### 9. GET /health

**Health Check**

```
GET /health
```

**Response (200):**
```json
{
  "status": "ok"
}
```

---

## 📊 Data Models

### SearchResult
```typescript
{
  id: string                  // Identificador único
  title: string               // Título del documento
  description: string         // Descripción corta
  url: string                 // URL del documento
  category: string            // Categoría
  score: float                // Score de relevancia (0-100)
  tags: string[]              // Etiquetas
  date: string                // Fecha (ISO 8601)
}
```

### SearchResponse
```typescript
{
  query: string               // Query de búsqueda
  results: SearchResult[]      // Array de resultados
  total: number               // Total de resultados encontrados
  time_ms: float              // Tiempo de búsqueda en ms
}
```

### Document
```typescript
{
  id: string                  // Identificador único
  title: string               // Título
  description: string         // Descripción
  url: string                 // URL
  category: string            // Categoría
  tags: string[]              // Etiquetas
  date: string                // Fecha (ISO 8601)
  content: string             // Contenido completo
}
```

---

## 🎯 HTTP Status Codes

| Code | Meaning | Uso |
|------|---------|-----|
| 200 | OK | Solicitud exitosa |
| 400 | Bad Request | Parámetros inválidos |
| 404 | Not Found | Recurso no encontrado |
| 422 | Unprocessable Entity | Validación fallida |
| 500 | Server Error | Error interno |

---

## 🔒 Security

### CORS
```
Access-Control-Allow-Origin: *
Access-Control-Allow-Methods: GET, POST, DELETE
Access-Control-Allow-Headers: Content-Type
```

### Input Validation
- `q` (query): min 1 char, max 1000 chars
- `limit`: 1-100
- `id`: alphanumeric + hyphens

### Rate Limiting
- TODO: Implementar (6 req/min por IP)

---

## 📈 Performance Targets

| Operación | Target | Actual |
|-----------|--------|--------|
| GET /search (10 results) | <50ms | ~2-10ms |
| GET /documents (20 docs) | <50ms | ~2-3ms |
| POST /documents | <50ms | <1ms |
| DELETE /documents | <50ms | <1ms |

---

## 🧪 cURL Examples

### Búsqueda
```bash
curl "http://localhost:8000/search?q=python&limit=5"
```

### Listar documentos
```bash
curl "http://localhost:8000/documents?category=Backend&limit=10"
```

### Obtener documento
```bash
curl "http://localhost:8000/documents/1"
```

### Agregar documento
```bash
curl -X POST "http://localhost:8000/documents" \
  -H "Content-Type: application/json" \
  -d '{
    "id": "11",
    "title": "Nuevo",
    "description": "Desc",
    "url": "https://example.com",
    "category": "Backend",
    "tags": ["tag"],
    "date": "2026-01-29",
    "content": "Content"
  }'
```

### Eliminar documento
```bash
curl -X DELETE "http://localhost:8000/documents/1"
```

### Estado
```bash
curl "http://localhost:8000/status"
```

---

## 📝 Changelog

### v1.0.0 (2026-01-29)
- ✅ Búsqueda básica
- ✅ CRUD de documentos
- ✅ Filtros y categorías
- ✅ API REST completa
- ✅ Documentación automática

### v1.1.0 (Próximo)
- 🔄 Autenticación JWT
- 🔄 Rate limiting
- 🔄 Caching con Redis
- 🔄 Fuzzy matching
- 🔄 Autocomplete

---

**Especificación v1.0**  
Generada: 2026-01-29  
Por: Anais 🐎
