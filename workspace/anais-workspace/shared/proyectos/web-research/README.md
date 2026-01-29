# 🔬 Web Research Engine

**Motor de investigación web inteligente - Busca, extrae y analiza información automáticamente.**

---

## ⚡ Features

✅ **Búsqueda en Google** - Top resultados automáticos  
✅ **Extracción de Contenido** - Parse HTML + metadata  
✅ **Análisis Profundo** - Keywords + relevancia  
✅ **Investigación Multi-stage** - Búsqueda → Extracción → Análisis  
✅ **CLI Interactivo** - Usa desde terminal  
✅ **Subagente Support** - Spawn para investigaciones paralelas  
✅ **Reportes JSON** - Resultados estructurados  
✅ **No requiere Chrome** - Funciona con requests + BeautifulSoup  

---

## 🚀 Instalación

```bash
cd web-research

# Instalar dependencias
pip install --break-system-packages beautifulsoup4 requests lxml

# Crear directorio de resultados
mkdir -p results
```

---

## 📖 Uso

### 1. CLI Interactivo

```bash
python research_cli.py
```

Menú:
```
1. Búsqueda simple
2. Investigación profunda
3. Investigación con subtópicos
4. Salir
```

### 2. CLI Directo

```bash
# Búsqueda simple
python research_cli.py "AI 2026"

# Con profundidad
python research_cli.py "FastAPI" --depth 5

# Con subtópicos
python research_cli.py "Web3" --subs "blockchain,crypto,NFTs"
```

### 3. Como Python Module

```python
from research_engine import WebResearchEngine
import asyncio

async def research():
    engine = WebResearchEngine()
    
    # Búsqueda simple
    results = await engine.google_search("Python FastAPI")
    
    # Investigación completa
    research = await engine.search_and_analyze("AI trends", depth=5)
    
    # Con subtópicos
    research = await engine.research_topic(
        "Machine Learning",
        subtopics=["neural networks", "deep learning"]
    )
    
    # Guardar
    engine.save_research(research)
    engine.print_report(research)

asyncio.run(research())
```

### 4. Como Subagente

```python
from sessions_spawn import sessions_spawn

# Spawn investigación en paralelo
await sessions_spawn(
    task="Investiga las tendencias de IA en 2026",
    agentId="research-bot",
    runTimeoutSeconds=300
)

# El subagente automáticamente:
# 1. Busca en Google
# 2. Extrae contenido
# 3. Analiza resultados
# 4. Retorna reporte
# 5. Se elimina
```

---

## 📊 Ejemplo de Salida

```json
{
  "query": "AI 2026",
  "timestamp": "2026-01-29T20:30:00",
  "summary": {
    "total_sources": 10,
    "total_extracted": 8,
    "total_analyzed": 8,
    "avg_relevance": 78.5
  },
  "stages": {
    "search": {
      "total_results": 10,
      "results": [
        {
          "title": "The Future of AI in 2026",
          "url": "https://...",
          "snippet": "AI is transforming...",
          "source": "google"
        }
      ]
    },
    "extraction": {
      "content": [
        {
          "url": "https://...",
          "title": "The Future of AI in 2026",
          "content": "AI is transforming industries..."
        }
      ]
    },
    "analysis": {
      "analyses": [
        {
          "keywords_found": {"AI": 15, "2026": 8},
          "relevance_score": 85,
          "word_count": 1250
        }
      ]
    }
  }
}
```

---

## 🔍 Métodos Principales

### google_search()
```python
results = await engine.google_search("query", num_results=10)
# Retorna: List[Dict] con title, url, snippet
```

### fetch_page()
```python
content = await engine.fetch_page("https://example.com")
# Retorna: Dict con title, h1, meta_description, content
```

### analyze_content()
```python
analysis = await engine.analyze_content(text, query)
# Retorna: Dict con keywords_found, relevance_score
```

### search_and_analyze()
```python
investigation = await engine.search_and_analyze("query", depth=5)
# Retorna: Investigación completa multi-stage
```

### research_topic()
```python
research = await engine.research_topic("main", subtopics=[...])
# Retorna: Investigación del tema + subtópicos
```

### save_research()
```python
path = engine.save_research(research)
# Guarda a JSON en results/
```

---

## 🎯 Casos de Uso

### 1. Investigación Competitiva
```python
research = await engine.research_topic(
    "FastAPI vs Django vs Express",
    subtopics=["performance", "features", "community"]
)
```

### 2. Market Research
```python
research = await engine.research_topic(
    "AI Startups 2026",
    subtopics=["funding", "applications", "trends"]
)
```

### 3. Fact Checking
```python
query = "Is AI superintelligence possible in 2026?"
research = await engine.search_and_analyze(query, depth=10)
```

### 4. Content Research
```python
research = await engine.research_topic(
    "Web Development Best Practices",
    subtopics=["performance", "accessibility", "security"]
)
```

---

## 🛠️ Configuración

### Timeout
```python
response = self.session.get(url, timeout=15)  # 15 segundos
```

### Rate Limiting
```python
await asyncio.sleep(1)  # Entre requests
await asyncio.sleep(2)  # Entre investigaciones
```

### User Agent
```python
'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) ...'
```

### Results Directory
```
web-research/
├── results/
│   ├── research_20260129_203000.json
│   └── research_20260129_203500.json
└── ...
```

---

## ⚠️ Limitaciones (v1)

- ❌ Sin JavaScript execution (SPA limitadas)
- ❌ Sin proxy rotation (puede ser bloqueado)
- ❌ Rate limiting puede afectar
- ❌ Google puede bloquear después de muchas requests
- ❌ No extrae contenido dinámico (solo HTML estático)

---

## 🔮 Roadmap

### v1.1
- [ ] Retry con backoff exponencial
- [ ] Caching de resultados
- [ ] Better error handling

### v2.0
- [ ] Playwright/Selenium integration (si disponible)
- [ ] JavaScript rendering
- [ ] Proxy rotation

### v3.0
- [ ] Real-time alerts
- [ ] Trend monitoring
- [ ] NLP summaries
- [ ] PDF extraction

---

## 📁 Estructura

```
web-research/
├── research_engine.py       (Motor principal)
├── research_cli.py          (CLI)
├── research_agent.md        (Documentación subagente)
├── README.md               (Este archivo)
├── requirements.txt
└── results/
    └── research_*.json     (Reportes)
```

---

## 🚀 Deploy

### Local
```bash
python research_cli.py "tu_query"
```

### Como Task Cron
```
@hourly python research_cli.py "market trends"
```

### Como Subagente
```python
await sessions_spawn(
    task="Investiga: [query]",
    agentId="research"
)
```

---

## 📝 Ejemplos

### Ejemplo 1: Búsqueda Simple
```bash
$ python research_cli.py "FastAPI tutorial"

🔍 Buscando en Google: FastAPI tutorial
✅ Encontrados: 10 resultados

1. FastAPI - The Modern Web Framework
   FastAPI is a modern web framework for building APIs...
   
2. FastAPI Tutorial - Full Course
   Learn FastAPI from scratch with this...
```

### Ejemplo 2: Investigación Profunda
```bash
$ python research_cli.py "AI 2026" --depth 5

🔬 INVESTIGACIÓN WEB: AI 2026
📍 STAGE 1: BÚSQUEDA
✅ Encontrados: 10 resultados

📍 STAGE 2: EXTRACCIÓN
✅ Extraídos: 5 contenidos

📍 STAGE 3: ANÁLISIS
✅ Analizados: 5 documentos

📊 REPORTE DE INVESTIGACIÓN
🔍 TÓPICO: AI 2026
   Fuentes encontradas: 10
   Contenido extraído: 5
   Relevancia promedio: 78.5%
```

### Ejemplo 3: Investigación con Subtópicos
```bash
$ python research_cli.py "Web3" --subs "blockchain,crypto,NFTs"

🔬 INVESTIGACIÓN WEB: Web3
(investigación principal + 3 subtópicos)

Resultados guardados en: results/research_*.json
```

---

## 🐛 Troubleshooting

### "No se encontraron resultados"
```
✓ Intenta con una query más específica
✓ Verifica conexión a internet
✓ Google puede estar bloqueando (retry en 5 min)
```

### "Connection timeout"
```
✓ Aumenta timeout: timeout=30
✓ Aumenta delays: asyncio.sleep(5)
✓ Usa VPN o proxy
```

### "BeautifulSoup error"
```bash
pip install --break-system-packages lxml
```

---

## 💡 Tips

1. **Queries específicas** funcionan mejor
   ```
   ❌ "AI"
   ✅ "AI applications in healthcare 2026"
   ```

2. **Profundidad moderada** es más rápido
   ```python
   depth=3   # Rápido, suficiente
   depth=10  # Lento, exhaustivo
   ```

3. **Subtópicos ayudan** a investigaciones
   ```python
   research_topic(
       "Python",
       subtopics=["async", "web frameworks", "data science"]
   )
   ```

4. **Guarda resultados** para reutilizar
   ```python
   engine.save_research(research)  # JSON reutilizable
   ```

---

## 📄 Licencia

Open Source - Libre para usar y modificar

---

## 👨‍💻 Autor

**Anais** 🐎  
Web Research Engine v1.0  
Enero 2026

---

**¡Listo para investigar!** 🔬🚀
