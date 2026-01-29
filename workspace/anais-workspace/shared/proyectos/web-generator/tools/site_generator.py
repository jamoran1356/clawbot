#!/usr/bin/env python3
"""
Site Generator - Crea sitios web modernos desde contenido
"""

import json
from pathlib import Path

class SiteGenerator:
    """Generador de sitios web con diseño moderno"""
    
    def __init__(self, name, theme="dark"):
        self.name = name
        self.theme = theme
        self.content = {}
        
    def generate_html(self, content):
        """Genera HTML5 moderno con Tailwind CSS"""
        
        html = f"""<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{content['hero']['title']} | {self.name}</title>
    <meta name="description" content="{content['hero']['subtitle']}">
    
    <!-- Fonts -->
    <link href="https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;600;700;800&family=JetBrains+Mono:wght@400;600&display=swap" rel="stylesheet">
    
    <!-- Tailwind CSS -->
    <script src="https://cdn.tailwindcss.com"></script>
    <script>
        tailwind.config = {{
            theme: {{
                extend: {{
                    fontFamily: {{
                        poppins: ['Poppins', 'sans-serif'],
                        mono: ['JetBrains Mono', 'monospace'],
                    }},
                    colors: {{
                        primary: '#FF6B6B',
                        secondary: '#4ECDC4',
                        accent: '#95E1D3',
                        dark: '#0F172A',
                    }}
                }}
            }}
        }}
    </script>
    
    <style>
        * {{
            font-family: 'Poppins', sans-serif;
        }}
        
        .code-block {{
            font-family: 'JetBrains Mono', monospace;
        }}
        
        .gradient-primary {{
            background: linear-gradient(135deg, #FF6B6B 0%, #FF8E8E 100%);
        }}
        
        .gradient-secondary {{
            background: linear-gradient(135deg, #4ECDC4 0%, #44A9A1 100%);
        }}
        
        .gradient-accent {{
            background: linear-gradient(135deg, #95E1D3 0%, #7CCCC9 100%);
        }}
        
        .gradient-dark {{
            background: linear-gradient(135deg, #0F172A 0%, #1E293B 100%);
        }}
        
        .card-hover {{
            transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        }}
        
        .card-hover:hover {{
            transform: translateY(-8px);
            box-shadow: 0 20px 40px rgba(0, 0, 0, 0.2);
        }}
        
        .glow {{
            animation: glow 2s ease-in-out infinite;
        }}
        
        @keyframes glow {{
            0%, 100% {{ opacity: 1; }}
            50% {{ opacity: 0.8; }}
        }}
        
        .blur-bg {{
            backdrop-filter: blur(10px);
            background: rgba(15, 23, 42, 0.7);
        }}
        
        .text-gradient {{
            background: linear-gradient(135deg, #FF6B6B 0%, #4ECDC4 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
        }}
        
        ::selection {{
            background: #FF6B6B;
            color: white;
        }}
        
        ::-webkit-scrollbar {{
            width: 8px;
        }}
        
        ::-webkit-scrollbar-track {{
            background: #0F172A;
        }}
        
        ::-webkit-scrollbar-thumb {{
            background: #FF6B6B;
            border-radius: 4px;
        }}
        
        ::-webkit-scrollbar-thumb:hover {{
            background: #FF8E8E;
        }}
    </style>
</head>
<body class="bg-gradient-dark text-white">
    <!-- Navigation -->
    <nav class="blur-bg sticky top-0 z-50 border-b border-gray-700/30">
        <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
            <div class="flex justify-between items-center h-16">
                <div class="flex items-center space-x-2">
                    <span class="text-2xl font-bold text-gradient">💻</span>
                    <span class="text-xl font-bold">{self.name}</span>
                </div>
                <div class="hidden md:flex space-x-8">
                    <a href="#featured" class="hover:text-primary transition">Artículos</a>
                    <a href="#categories" class="hover:text-primary transition">Categorías</a>
                    <a href="#newsletter" class="hover:text-primary transition">Newsletter</a>
                    <a href="#" class="hover:text-primary transition">Contacto</a>
                </div>
                <button class="md:hidden text-2xl">☰</button>
            </div>
        </div>
    </nav>

    <!-- Hero Section -->
    <section class="relative min-h-screen flex items-center justify-center overflow-hidden">
        <!-- Animated Background -->
        <div class="absolute inset-0 overflow-hidden">
            <div class="absolute top-0 left-1/4 w-96 h-96 bg-primary rounded-full mix-blend-multiply filter blur-3xl opacity-20 animate-pulse"></div>
            <div class="absolute top-0 right-1/4 w-96 h-96 bg-secondary rounded-full mix-blend-multiply filter blur-3xl opacity-20 animate-pulse animation-delay-2000"></div>
            <div class="absolute bottom-0 left-1/2 w-96 h-96 bg-accent rounded-full mix-blend-multiply filter blur-3xl opacity-20 animate-pulse animation-delay-4000"></div>
        </div>

        <div class="relative z-10 max-w-5xl mx-auto px-4 text-center">
            <h1 class="text-6xl md:text-7xl font-bold mb-6">
                <span class="text-gradient">{content['hero']['title']}</span>
            </h1>
            <p class="text-xl md:text-2xl text-gray-300 mb-8 max-w-2xl mx-auto">
                {content['hero']['subtitle']}
            </p>
            <div class="flex flex-col sm:flex-row gap-4 justify-center">
                <button class="gradient-primary text-white px-8 py-4 rounded-lg font-semibold text-lg hover:shadow-lg hover:shadow-red-500/50 transition transform hover:scale-105">
                    {content['hero']['cta']}
                </button>
                <button class="border-2 border-gray-600 text-white px-8 py-4 rounded-lg font-semibold text-lg hover:border-primary hover:text-primary transition">
                    Saber Más
                </button>
            </div>
        </div>
    </section>

    <!-- Featured Articles -->
    <section id="featured" class="py-20 px-4 relative">
        <div class="max-w-7xl mx-auto">
            <h2 class="text-5xl font-bold mb-4 text-center">
                <span class="text-gradient">Artículos Destacados</span>
            </h2>
            <p class="text-gray-400 text-center mb-16 max-w-2xl mx-auto">
                Explora los artículos más relevantes sobre las últimas tendencias en tecnología
            </p>

            <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
"""
        
        # Featured articles
        for article in content['featured_articles']:
            html += f"""
                <div class="card-hover group bg-gradient-to-br from-gray-900 to-black border border-gray-800 rounded-xl p-8 overflow-hidden">
                    <div class="absolute top-0 left-0 w-20 h-20 text-6xl opacity-20 group-hover:scale-110 transition">
                        {article['icon']}
                    </div>
                    
                    <div class="mb-6 inline-block px-4 py-2 rounded-full text-sm font-semibold" style="background: {article['color']}20; color: {article['color']}">
                        {article['category']}
                    </div>
                    
                    <h3 class="text-2xl font-bold mb-3 group-hover:text-primary transition">
                        {article['title']}
                    </h3>
                    
                    <p class="text-gray-400 mb-6">
                        {article['excerpt']}
                    </p>
                    
                    <div class="flex justify-between items-center pt-6 border-t border-gray-800">
                        <div class="flex flex-col">
                            <span class="text-sm text-gray-500">{article['author']}</span>
                            <span class="text-xs text-gray-600">{article['date']}</span>
                        </div>
                        <a href="#" class="text-primary font-semibold hover:translate-x-2 transition">→</a>
                    </div>
                </div>
"""
        
        html += """
            </div>
        </div>
    </section>

    <!-- Recent Articles List -->
    <section class="py-20 px-4 bg-black/50">
        <div class="max-w-4xl mx-auto">
            <h2 class="text-4xl font-bold mb-12 text-center">Últimos Artículos</h2>
            
            <div class="space-y-4">
"""
        
        for article in content['recent_articles']:
            html += f"""
                <div class="group cursor-pointer p-6 rounded-lg border border-gray-800 hover:border-primary hover:bg-gray-900/50 transition">
                    <div class="flex justify-between items-start">
                        <div>
                            <h3 class="text-lg font-semibold group-hover:text-primary transition mb-2">
                                {article['title']}
                            </h3>
                            <span class="text-sm text-gray-500">{article['category']} • {article['date']}</span>
                        </div>
                        <span class="text-2xl text-primary group-hover:translate-x-2 transition">→</span>
                    </div>
                </div>
"""
        
        html += """
            </div>
        </div>
    </section>

    <!-- Categories -->
    <section id="categories" class="py-20 px-4 relative">
        <div class="max-w-6xl mx-auto">
            <h2 class="text-4xl font-bold mb-12 text-center">
                <span class="text-gradient">Categorías</span>
            </h2>
            
            <div class="grid grid-cols-2 md:grid-cols-5 gap-4">
"""
        
        for category in content['categories']:
            html += f"""
                <div class="card-hover text-center p-6 rounded-lg border border-gray-800 hover:border-opacity-0" style="background: {category['color']}10">
                    <div class="text-3xl font-bold mb-2" style="color: {category['color']}">{category['count']}</div>
                    <div class="text-sm text-gray-400">{category['name']}</div>
                </div>
"""
        
        html += """
            </div>
        </div>
    </section>

    <!-- Newsletter -->
    <section id="newsletter" class="py-20 px-4">
        <div class="max-w-4xl mx-auto">
            <div class="gradient-primary rounded-2xl p-12 text-center">
                <h2 class="text-4xl font-bold mb-4 text-white">
                    {content['newsletter']['title']}
                </h2>
                <p class="text-lg text-white/80 mb-8">
                    {content['newsletter']['subtitle']}
                </p>
                
                <div class="flex gap-4 max-w-md mx-auto">
                    <input type="email" placeholder="{content['newsletter']['placeholder']}" 
                           class="flex-1 px-6 py-3 rounded-lg text-black focus:outline-none focus:ring-2 focus:ring-white">
                    <button class="bg-black text-primary px-8 py-3 rounded-lg font-semibold hover:scale-105 transition">
                        Suscribirse
                    </button>
                </div>
            </div>
        </div>
    </section>

    <!-- Footer -->
    <footer class="border-t border-gray-800 py-16 px-4">
        <div class="max-w-6xl mx-auto">
            <div class="grid grid-cols-1 md:grid-cols-4 gap-12 mb-12">
                <div>
                    <div class="flex items-center space-x-2 mb-4">
                        <span class="text-2xl">💻</span>
                        <span class="text-xl font-bold">{content['footer']['company']}</span>
                    </div>
                    <p class="text-gray-500">{content['footer']['tagline']}</p>
                </div>
                
                <div>
                    <h4 class="font-semibold mb-4">Enlaces</h4>
                    <ul class="space-y-2">
"""
        
        for link in content['footer']['links']:
            html += f'                        <li><a href="{link["url"]}" class="text-gray-400 hover:text-primary transition">{link["name"]}</a></li>\n'
        
        html += """
                    </ul>
                </div>
                
                <div colspan="2">
                    <h4 class="font-semibold mb-4">Síguenos</h4>
                    <div class="flex space-x-4">
"""
        
        for social in content['footer']['social']:
            html += f'                        <a href="{social["url"]}" class="text-gray-400 hover:text-primary transition text-lg">{social["icon"]}</a>\n'
        
        html += f"""
                    </div>
                </div>
            </div>
            
            <div class="border-t border-gray-800 pt-8 text-center text-gray-500">
                <p>&copy; 2026 {content['footer']['company']}. Creado con <span class="text-primary">❤️</span> por Anais 🐎</p>
            </div>
        </div>
    </footer>

    <script>
        // Smooth scrolling
        document.querySelectorAll('a[href^="#"]').forEach(anchor => {{
            anchor.addEventListener('click', function (e) {{
                e.preventDefault();
                const target = document.querySelector(this.getAttribute('href'));
                if (target) {{
                    target.scrollIntoView({{ behavior: 'smooth' }});
                }}
            }});
        }});

        // Animate on scroll
        const observer = new IntersectionObserver((entries) => {{
            entries.forEach(entry => {{
                if (entry.isIntersecting) {{
                    entry.target.style.opacity = '1';
                    entry.target.style.transform = 'translateY(0)';
                }}
            }});
        }}, {{ threshold: 0.1 }});

        document.querySelectorAll('.card-hover').forEach(card => {{
            card.style.opacity = '0';
            card.style.transform = 'translateY(20px)';
            card.style.transition = 'all 0.6s ease-out';
            observer.observe(card);
        }});
    </script>
</body>
</html>
"""
        
        return html
    
    def save(self, output_path, content):
        """Guarda el sitio generado"""
        html = self.generate_html(content)
        
        path = Path(output_path)
        path.parent.mkdir(parents=True, exist_ok=True)
        
        with open(path, 'w', encoding='utf-8') as f:
            f.write(html)
        
        print(f"✅ Sitio generado: {output_path}")
        return path

if __name__ == "__main__":
    from scraper import WebScraper
    
    scraper = WebScraper()
    content = scraper.get_content()
    
    generator = SiteGenerator("TechHub")
    generator.save("/workspace/anais-workspace/shared/proyectos/web-generator/generated/index.html", content)
