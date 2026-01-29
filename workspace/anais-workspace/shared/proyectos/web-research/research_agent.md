# 🔬 Web Research Agent - Subagente de Investigación

## Propósito

Subagente especializado en investigación web profunda que:
- ✅ Busca información en Google
- ✅ Extrae contenido de páginas
- ✅ Analiza relevancia de resultados
- ✅ Organiza hallazgos
- ✅ Genera reportes

## Modo de Uso

```
Usuario: "Investiga sobre AI y machine learning en 2026"

Subagente ejecuta:
1. Búsqueda en Google (query: "AI machine learning 2026")
2. Extrae contenido de top 5 resultados
3. Analiza relevancia (palabras clave, contexto)
4. Genera reporte JSON
5. Retorna resumen a usuario
```

## Flujo

```
┌─────────────────────────────────┐
│  Usuario: "Investiga X"         │
└────────────┬────────────────────┘
             │
             ▼
┌─────────────────────────────────┐
│  Subagente creado (aislado)     │
└────────────┬────────────────────┘
             │
             ▼
┌─────────────────────────────────┐
│  1. google_search(query)        │
│     └─ Encuentra 10+ resultados │
└────────────┬────────────────────┘
             │
             ▼
┌─────────────────────────────────┐
│  2. fetch_page() x N URLs       │
│     └─ Extrae contenido HTML    │
└────────────┬────────────────────┘
             │
             ▼
┌─────────────────────────────────┐
│  3. analyze_content()           │
│     └─ Busca palabras clave     │
└────────────┬────────────────────┘
             │
             ▼
┌─────────────────────────────────┐
│  4. Genera reporte JSON         │
└────────────┬────────────────────┘
             │
             ▼
┌─────────────────────────────────┐
│  Retorna a usuario              │
│  + Resumen + Links + Análisis   │
└─────────────────────────────────┘
```

## Casos de Uso

### 1. Investigación Simple
```
"Investiga qué es Web3"
→ Busca + extrae + analiza
→ Retorna: Definición, casos de uso, ejemplos
```

### 2. Investigación Profunda
```
"Investiga AI 2026 con subtópicos: ML trends, neural networks"
→ Búsqueda principal + búsquedas secundarias
→ Retorna: Análisis exhaustivo por subtópico
```

### 3. Investigación Competitiva
```
"Investiga: FastAPI vs Express vs Django"
→ Busca cada framework
→ Compara características
→ Retorna: Matriz de comparación
```

### 4. Investigación de Mercado
```
"Investiga: Tendencias en startups 2026"
→ Busca noticias + artículos + datos
→ Analiza patrones
→ Retorna: Insights de mercado
```

## Resultados

### Salida Típica

```json
{
  "query": "AI 2026",
  "timestamp": "2026-01-29T20:30:00",
  "summary": {
    "total_sources": 10,
    "total_extracted": 8,
    "avg_relevance": 78.5
  },
  "investigations": {
    "AI 2026": {
      "stages": {
        "search": {
          "total_results": 10,
          "results": [...]
        },
        "extraction": {
          "total_extracted": 8,
          "content": [...]
        },
        "analysis": {
          "analyses": [...]
        }
      }
    }
  }
}
```

## Spawn del Subagente

```
sessions_spawn(
  task="Investiga: [QUERY] con subtópicos: [LIST]",
  model="openrouter/anthropic/claude-haiku-4.5",
  agentId="research-bot",
  runTimeoutSeconds=300
)
```

## Ejemplo de Uso

```python
# Como subagente separado:
await sessions_spawn(
  task="Investiga las tendencias de AI en 2026",
  agentId="research"
)

# El subagente:
# 1. Ejecuta research_engine.py
# 2. Busca en Google
# 3. Extrae contenido
# 4. Analiza resultados
# 5. Retorna reporte
```

## Ventajas

✅ **Aislado** - No afecta sesión principal  
✅ **Async** - No bloquea espera  
✅ **Profundo** - Análisis multi-stage  
✅ **Organizado** - JSON estructurado  
✅ **Escalable** - Múltiples investigaciones paralelas  

## Limitaciones (v1)

- ⚠️ Sin JavaScript execution (páginas dinámicas limitadas)
- ⚠️ Sin proxy rotation (puede ser bloqueado)
- ⚠️ Sin caching (requests duplicadas lentas)
- ⚠️ Rate limiting básico

## Roadmap

### v1.1
- [ ] Caching de resultados
- [ ] Proxy rotation
- [ ] Retry logic
- [ ] Better error handling

### v2.0
- [ ] Playwright integration (si disponible)
- [ ] JavaScript rendering
- [ ] PDF extraction
- [ ] Image analysis
- [ ] NLP summary

### v3.0
- [ ] Real-time alerts
- [ ] Competitive monitoring
- [ ] Market trend analysis
- [ ] Automated reports

## Configuración

### Timeout
```python
runTimeoutSeconds=300  # 5 minutos máximo
```

### Modelo
```python
model="openrouter/anthropic/claude-haiku-4.5"  # Rápido
# o
model="openrouter/auto"  # Auto-select
```

### Limpieza
```python
cleanup="delete"  # Borrar después de terminar
# o
cleanup="keep"    # Mantener sesión
```

---

**Ready to research!** 🔬🐎
