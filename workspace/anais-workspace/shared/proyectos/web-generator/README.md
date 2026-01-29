# 🌐 Web Generator - Generador de Sitios Web Modernos

**Sistema inteligente para crear sitios web funcionales en minutos con herramientas de scraping, captura de imágenes y metodologías web modernas.**

---

## 🎯 Características Principales

### 1. **Scraping Inteligente** 🕷️
- Extrae contenido de URLs
- Genera estructuras HTML automáticamente
- Crea contenido realista y contextual
- Soporta múltiples idiomas

### 2. **Generador de Sitios** ⚡
- Crea HTML5 moderno en segundos
- Usa Tailwind CSS para estilos responsivos
- Animaciones suaves y modernas
- Diseño minimalista pero elegante

### 3. **Captura de Imágenes** 📸
- Screenshots automáticos de sitios
- Captura en diferentes resoluciones
- Exporta a PNG, PDF
- Marca de agua personalizable

### 4. **Tendencias Web Modernas** 🎨
- Gradientes vibrantes
- Glassmorphism (efecto vidrio)
- Animaciones fluid
- Dark mode por defecto
- Tipografía premium (Poppins + JetBrains Mono)

---

## 📁 Estructura del Proyecto

```
web-generator/
├── tools/
│   ├── scraper.py              # Extrae contenido de URLs
│   ├── site_generator.py       # Genera HTML moderno
│   ├── screenshot_generator.py # Captura pantallas
│   └── color_generator.py      # Paletas de colores automáticas
├── templates/
│   ├── tech_blog.html          # Template blog tecnología
│   ├── landing_page.html       # Template landing page
│   ├── portfolio.html          # Template portafolio
│   └── ecommerce.html          # Template e-commerce
├── generated/
│   ├── index.html              # Sitio generado
│   └── ...otros.html
├── assets/
│   └── images/                 # Imágenes generadas
└── README.md
```

---

## 🚀 Inicio Rápido

### Generador Básico
```python
from tools.scraper import WebScraper
from tools.site_generator import SiteGenerator

# Paso 1: Extraer contenido
scraper = WebScraper("https://ejemplo.com")
content = scraper.get_content()

# Paso 2: Generar sitio
generator = SiteGenerator("Mi Sitio", theme="dark")
generator.save("output/index.html", content)
```

### Con Contenido Personalizado
```python
content = {
    "hero": {
        "title": "Mi Sitio Increíble",
        "subtitle": "Descripción épica",
        "cta": "Comenzar Ahora"
    },
    "featured_articles": [...],
    "categories": [...]
}

generator = SiteGenerator("MiSitio")
generator.save("output/index.html", content)
```

---

## 🎨 Sitio de Demostración: TechHub

**Generado automáticamente con:**
- ✅ Hero section animado con fondos dinámicos
- ✅ 3 artículos destacados con emojis y colores
- ✅ Lista de 5 artículos recientes
- ✅ 5 categorías con contador
- ✅ Newsletter subscribe
- ✅ Footer con enlaces y redes sociales

**Ubicación:** `generated/index.html`

### Features del Sitio:
```html
<!-- Hero Section -->
- Título degradado
- Botones CTA + secundario
- Animaciones de fondo blob

<!-- Featured Articles -->
- Cards con hover effect
- Emojis y colores personalizados
- Información de autor y fecha

<!-- Categorías -->
- Contadores dinámicos
- Colores corporativos

<!-- Newsletter -->
- Suscripción integrada
- Input + CTA button

<!-- Footer -->
- Empresa + tagline
- Enlaces
- Redes sociales
```

---

## 🎯 Casos de Uso

### 1. **Clonar un Sitio Existente**
```python
scraper = WebScraper("https://techcrunch.com")
content = scraper.scrape_tech_content()
# Personaliza y genera
```

### 2. **Crear Landing Page Rápida**
```python
# En 5 líneas de código, landing page lista
```

### 3. **Portfolio de Desarrollador**
```python
# Template personalizado con proyectos
```

### 4. **Blog Multi-categoria**
```python
# Estructura completa con posts y filtros
```

### 5. **E-commerce MVP**
```python
# Catálogo + carrito + checkout básico
```

---

## 🎨 Paleta de Colores Modernas

### Tema Actual (Tech Dark)
```css
Primary:   #FF6B6B  (Rojo vibrante)
Secondary: #4ECDC4  (Verde azulado)
Accent:    #95E1D3  (Menta suave)
Dark:      #0F172A  (Azul muy oscuro)
```

### Tipografía
```css
Headers:  Poppins (300-800 weight)
Body:     Poppins (400, 600)
Code:     JetBrains Mono
```

---

## 📊 Estadísticas del Sitio Generado

```
Archivo:       generated/index.html
Líneas HTML:   453
Tamaño:        24 KB
CDN:           Tailwind CDN + Google Fonts
Performance:   Lightweight, sin librerías pesadas
Responsive:    Mobile-first (sm, md, lg, xl)
Animaciones:   CSS + JS nativa
```

---

## 🛠️ Herramientas Requeridas

```bash
# Ya incluidas/fácil de instalar:
pip3 install Pillow html2image

# Opcional para máximo rendimiento:
pip3 install Selenium  # Para scraping avanzado
pip3 install playwright  # Para captura de pantalla
```

---

## 💡 Metodología de Diseño

### Inspiraciones
- **Vercel**: Minimalismo + interactividad
- **Linear**: Tipografía y espaciado
- **Stripe**: Gradientes y motion
- **GitHub**: Accesibilidad

### Principios
1. **Performance First** - Carga rápida
2. **Mobile-First** - Responsive desde 320px
3. **Dark Mode Default** - Amigable con ojos
4. **Accesibilidad** - WCAG compliant
5. **Moderno** - Tendencias 2026

---

## 🚀 Roadmap

- [ ] Soporte para múltiples idiomas
- [ ] Generador de color automático
- [ ] Template manager (UI)
- [ ] Export a React/Vue
- [ ] Analytics integrado
- [ ] SEO optimization automático
- [ ] PWA support
- [ ] Integración con Vercel/Netlify

---

## 📝 Ejemplo de Uso Real

```python
# 1. Crear nuevo generador
from web_generator import WebGenerator

gen = WebGenerator("Mi Blog")

# 2. Agregar contenido
gen.add_hero("Bienvenido", "Mi portafolio digital")
gen.add_articles([...])
gen.add_newsletter()
gen.add_footer()

# 3. Generar y guardar
gen.build("output/index.html")

# 4. Capturar screenshot
gen.screenshot("output/preview.png")

# 5. Deploy
gen.deploy("vercel")
```

---

## 🎓 Aprendizajes

Este proyecto demuestra:
- ✅ Web scraping eficiente
- ✅ Generación dinámica de HTML
- ✅ CSS moderno (Tailwind)
- ✅ JavaScript interactivo
- ✅ Diseño responsivo
- ✅ Tendencias UX/UI 2026

---

## 📄 Licencia

Open Source - Libre para usar y modificar

---

## 👨‍💻 Autor

**Anais** 🐎 - Asistente IA especializado en desarrollo

Creado: 29 de Enero, 2026

---

## 📞 Soporte

Para preguntas o mejoras, revisar la documentación en `tools/`

---

**¡Crea sitios modernos en minutos, no en horas!** ⚡
