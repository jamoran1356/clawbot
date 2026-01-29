# 🔗 Web Research Integration Guide

## Cómo Integrar el Motor de Investigación

---

## Opción 1: Motor Independiente (Recomendado)

### Uso Directo
```bash
# Instalación
pip install --break-system-packages beautifulsoup4 requests lxml

# Uso
python research_cli.py "AI 2026"
```

**Ventajas:**
✅ No requiere Chrome  
✅ Funciona en cualquier servidor  
✅ Rápido y ligero  
✅ No depende de Clawdbot  

**Desventajas:**
⚠️ No ejecuta JavaScript  
⚠️ Google puede bloquear después de muchas requests  

---

## Opción 2: Integración con Clawdbot APIs

### Usar web_search() y web_fetch()

```python
from web_search import web_search
from web_fetch import web_fetch

# 1. Buscar
results = await web_search(
    query="AI trends 2026",
    count=10,
    country="US"
)

# 2. Extraer contenido
for result in results:
    content = await web_fetch(result['url'])
    print(content)
```

**Ventajas:**
✅ Acceso a APIs de Clawdbot  
✅ Mejor rate limiting  
✅ Resultados más confiables  

**Implementación:**
```python
# research_with_api.py
class WebResearchEngineWithAPI:
    async def search(self, query: str):
        return await web_search(query=query, count=10)
    
    async def fetch(self, url: str):
        return await web_fetch(url=url)
```

---

## Opción 3: Subagente (Más Poderoso)

### Spawn investigación paralela

```python
from sessions_spawn import sessions_spawn

# Spawn subagente
response = await sessions_spawn(
    task="Investiga: AI trends en 2026 con subtópicos: ML, Neural Networks",
    agentId="research-bot",
    model="openrouter/anthropic/claude-haiku-4.5",
    runTimeoutSeconds=300,
    cleanup="delete"
)

# El subagente ejecuta:
# 1. research_engine.py
# 2. Busca + extrae + analiza
# 3. Retorna reporte JSON
```

**Workflow:**
```
Usuario (sesión principal)
    ↓
    └─→ Spawn Subagente (aislado)
            ├─ Busca en Google
            ├─ Extrae contenido
            ├─ Analiza resultados
            └─ Retorna reporte
    ↓
Usuario recibe resultado
```

**Ventajas:**
✅ No bloquea sesión principal  
✅ Investigaciones paralelas  
✅ Timeout automático  
✅ Aislado y seguro  

---

## Opción 4: Integración con Search API

### Combinar con el motor de búsqueda local

```python
# search-api/app/main.py
@app.post("/research")
async def research_endpoint(query: str):
    """Endpoint para investigación"""
    
    engine = WebResearchEngine()
    
    # 1. Buscar
    results = await engine.google_search(query)
    
    # 2. Guardar en Search API
    for result in results:
        document = {
            "id": result['url'],
            "title": result['title'],
            "description": result['snippet'],
            "url": result['url'],
            "category": "Research",
            "tags": query.split(),
            "date": datetime.now().isoformat(),
            "content": result['snippet']
        }
        await search_api.add_document(document)
    
    return {"added": len(results)}
```

**Flujo:**
```
Búsqueda → Motor de Investigación → Search API → BD Local
```

---

## Integración con Sitio Diego

### Agregar buscador al sitio

```html
<!-- soydiegoup_v2.html -->
<form action="/api/research" method="POST">
    <input type="text" name="query" placeholder="Buscar...">
    <button type="submit">Investigar</button>
</form>
```

**Backend:**
```python
@app.post("/api/research")
async def website_research(query: str):
    engine = WebResearchEngine()
    research = await engine.search_and_analyze(query, depth=3)
    return research
```

---

## Configuraciones por Caso

### Caso 1: Búsqueda Rápida
```python
depth = 3
rate_limit = 1  # segundo entre requests
timeout = 10    # segundos
```

### Caso 2: Investigación Profunda
```python
depth = 10
rate_limit = 2
timeout = 30
```

### Caso 3: Monitoreo Continuo
```python
# Cron job
@scheduled("@hourly")
async def monitor_topic():
    query = "AI trends 2026"
    engine = WebResearchEngine()
    research = await engine.search_and_analyze(query)
    engine.save_research(research)
```

---

## Deployment

### Local
```bash
python research_cli.py "query"
```

### Docker
```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["python", "research_cli.py"]
```

### Vercel (con Playwright si necesario)
```bash
# vercel.json
{
  "buildCommand": "pip install -r requirements.txt",
  "outputDirectory": "results"
}
```

### Como Cron Job
```bash
0 * * * * cd /path/to/web-research && python research_cli.py "daily-query" >> logs.txt
```

---

## Supervisión y Alertas

### Monitorear investigaciones
```python
async def monitor_research(query: str, keywords: List[str]):
    research = await engine.search_and_analyze(query)
    
    for result in research['results']:
        for keyword in keywords:
            if keyword.lower() in result['snippet'].lower():
                await send_alert(f"Found: {keyword} in {result['title']}")
```

### Logs
```json
{
  "timestamp": "2026-01-29T20:30:00",
  "query": "AI 2026",
  "status": "success",
  "results": 10,
  "duration_ms": 5234
}
```

---

## Mejoras Futuras

### v1.1
- [ ] Caching de resultados
- [ ] Proxy rotation
- [ ] Retry automático

### v2.0
- [ ] Playwright integration
- [ ] JavaScript rendering
- [ ] PDF extraction

### v3.0
- [ ] Real-time alerts
- [ ] Trend analysis
- [ ] Competitive monitoring

---

## Troubleshooting

### "Google blocked my requests"
```python
# Aumentar delays
await asyncio.sleep(5)  # Entre requests

# Usar proxy (futura feature)
proxies = {"http": "http://proxy:8080"}
```

### "Rate limit exceeded"
```python
# Implementar backoff exponencial
max_retries = 3
delay = 2
for retry in range(max_retries):
    try:
        result = await engine.search(query)
        break
    except:
        delay *= 2
        await asyncio.sleep(delay)
```

### "No results found"
```python
# Queries más específicas
query = "AI machine learning neural networks 2026"  # Better
query = "AI"  # Too vague
```

---

## Checklist de Integración

- [ ] Instalar dependencias
- [ ] Crear directorio results/
- [ ] Probar CLI: `python research_cli.py "test"`
- [ ] Integrar con APIs de Clawdbot
- [ ] Agregar a Search API
- [ ] Deployar a producción
- [ ] Configurar monitoreo
- [ ] Documentar para equipo

---

## Support

Para problemas o dudas:
1. Revisa README.md
2. Verifica troubleshooting
3. Revisa logs en results/
4. Contacta a Anais 🐎

---

**Ready to integrate!** 🚀
