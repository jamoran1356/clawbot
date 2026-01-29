#!/usr/bin/env python3
"""
Diego Urquijo Personal Brand Website Generator
Sitio moderno y profesional para soydiegoup.com
"""

from pathlib import Path

class DiegoWebGenerator:
    """Generador especializado para Diego Urquijo"""
    
    def __init__(self, content):
        self.content = content
        
    def generate_html(self):
        """Genera HTML5 moderno para Diego Urquijo"""
        
        html = f"""<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{self.content['site_name']} | {self.content['tagline']}</title>
    <meta name="description" content="{self.content['hero']['subtitle']}">
    <meta name="author" content="Diego Urquijo">
    
    <!-- Open Graph -->
    <meta property="og:title" content="{self.content['site_name']}">
    <meta property="og:description" content="{self.content['tagline']}">
    <meta property="og:type" content="website">
    <meta property="og:url" content="https://soydiegoup.com">
    
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
                }}
            }}
        }}
    </script>
    
    <style>
        * {{
            font-family: 'Poppins', sans-serif;
        }}
        
        .gradient-brand {{
            background: linear-gradient(135deg, #FF6B6B 0%, #FF8E8E 100%);
        }}
        
        .gradient-text {{
            background: linear-gradient(135deg, #FF6B6B 0%, #4ECDC4 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
        }}
        
        .blur-bg {{
            backdrop-filter: blur(10px);
            background: rgba(15, 23, 42, 0.7);
        }}
        
        .card-hover {{
            transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        }}
        
        .card-hover:hover {{
            transform: translateY(-8px);
            box-shadow: 0 20px 40px rgba(255, 107, 107, 0.2);
        }}
        
        .text-shadow-brand {{
            text-shadow: 0 0 30px rgba(255, 107, 107, 0.3);
        }}
        
        @keyframes float {{
            0%, 100% {{ transform: translateY(0); }}
            50% {{ transform: translateY(-20px); }}
        }}
        
        .animate-float {{
            animation: float 3s ease-in-out infinite;
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
    </style>
</head>
<body class="bg-slate-950 text-white">
    <!-- Navigation -->
    <nav class="blur-bg sticky top-0 z-50 border-b border-slate-800">
        <div class="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8">
            <div class="flex justify-between items-center h-16">
                <div class="flex items-center space-x-3">
                    <div class="w-10 h-10 gradient-brand rounded-lg flex items-center justify-center font-bold">
                        DU
                    </div>
                    <span class="text-xl font-bold">{self.content['site_name']}</span>
                </div>
                <div class="hidden md:flex space-x-8">
                    <a href="#about" class="hover:text-red-400 transition">Sobre Mí</a>
                    <a href="#portfolio" class="hover:text-red-400 transition">Portafolio</a>
                    <a href="#services" class="hover:text-red-400 transition">Servicios</a>
                    <a href="#contact" class="hover:text-red-400 transition">Contacto</a>
                </div>
                <button class="gradient-brand text-white px-6 py-2 rounded-lg font-semibold hover:shadow-lg hover:shadow-red-500/50 transition">
                    Conectar
                </button>
            </div>
        </div>
    </nav>

    <!-- Hero Section -->
    <section class="relative min-h-screen flex items-center justify-center overflow-hidden pt-20">
        <div class="absolute inset-0 overflow-hidden">
            <div class="absolute top-20 left-10 w-80 h-80 bg-red-500 rounded-full mix-blend-multiply filter blur-3xl opacity-20 animate-float"></div>
            <div class="absolute top-40 right-10 w-80 h-80 bg-teal-500 rounded-full mix-blend-multiply filter blur-3xl opacity-20" style="animation: float 4s ease-in-out infinite 1s;"></div>
            <div class="absolute -bottom-20 left-1/2 w-80 h-80 bg-cyan-500 rounded-full mix-blend-multiply filter blur-3xl opacity-20" style="animation: float 5s ease-in-out infinite 2s;"></div>
        </div>

        <div class="relative z-10 max-w-5xl mx-auto px-4 text-center">
            <div class="text-7xl font-bold mb-6">
                <h1 class="gradient-text">Diego Urquijo</h1>
            </div>
            <p class="text-2xl text-gray-300 mb-4 font-light">
                {self.content['tagline']}
            </p>
            <p class="text-xl text-gray-400 mb-12 max-w-3xl mx-auto leading-relaxed">
                {self.content['hero']['subtitle']}
            </p>
            <div class="flex flex-col sm:flex-row gap-4 justify-center">
                <button class="gradient-brand text-white px-8 py-4 rounded-lg font-semibold text-lg hover:shadow-lg hover:shadow-red-500/50 transition transform hover:scale-105">
                    {self.content['hero']['cta']}
                </button>
                <button class="border-2 border-red-500 text-red-400 px-8 py-4 rounded-lg font-semibold text-lg hover:bg-red-500/10 transition">
                    {self.content['hero']['secondary_cta']}
                </button>
            </div>

            <!-- Scroll indicator -->
            <div class="absolute bottom-10 left-1/2 transform -translate-x-1/2 animate-bounce">
                <svg class="w-6 h-6 text-red-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 14l-7 7m0 0l-7-7m7 7V3"></path>
                </svg>
            </div>
        </div>
    </section>

    <!-- Stats Section -->
    <section class="py-16 px-4 bg-gradient-to-b from-slate-900 to-slate-950">
        <div class="max-w-6xl mx-auto">
            <div class="grid grid-cols-2 md:grid-cols-4 gap-8">
"""
        
        for stat in self.content['stats']:
            html += f"""
                <div class="text-center">
                    <div class="text-5xl font-bold gradient-text mb-2">{stat['value']}</div>
                    <div class="text-gray-400">{stat['label']}</div>
                </div>
"""
        
        html += """
            </div>
        </div>
    </section>

    <!-- Featured Projects -->
    <section id="portfolio" class="py-20 px-4">
        <div class="max-w-6xl mx-auto">
            <h2 class="text-5xl font-bold mb-4 text-center">
                <span class="gradient-text">Portafolio Destacado</span>
            </h2>
            <p class="text-gray-400 text-center mb-16 max-w-2xl mx-auto">
                Proyectos que demuestran mi expertise en desarrollo, estrategia digital y creación de contenido
            </p>

            <div class="grid grid-cols-1 md:grid-cols-3 gap-8">
"""
        
        for project in self.content['featured_projects']:
            html += f"""
                <div class="card-hover group bg-gradient-to-br from-slate-800 to-slate-900 border border-slate-700 rounded-xl p-8 overflow-hidden hover:border-red-500/50">
                    <div class="text-6xl mb-4 group-hover:scale-110 transition">{project['icon']}</div>
                    
                    <div class="inline-block px-3 py-1 rounded-full text-sm font-semibold mb-4" style="background: {project['color']}20; color: {project['color']}">
                        {project['category']}
                    </div>
                    
                    <h3 class="text-2xl font-bold mb-3 group-hover:text-red-400 transition">
                        {project['title']}
                    </h3>
                    
                    <p class="text-gray-400 mb-6">
                        {project['description']}
                    </p>
                    
                    <div class="flex flex-wrap gap-2 mb-6">
"""
        
        for tech in project.get('technologies', []):
            html += f'                        <span class="text-xs bg-slate-700 text-gray-300 px-3 py-1 rounded-full">{tech}</span>\n'
        
        html += """
                    </div>
                    
                    <a href="#" class="inline-block text-red-400 font-semibold hover:translate-x-2 transition">
                        Ver Proyecto →
                    </a>
                </div>
"""
        
        html += """
            </div>
        </div>
    </section>

    <!-- Services -->
    <section id="services" class="py-20 px-4 bg-black/50">
        <div class="max-w-6xl mx-auto">
            <h2 class="text-5xl font-bold mb-16 text-center">
                <span class="gradient-text">Servicios</span>
            </h2>

            <div class="grid grid-cols-1 md:grid-cols-2 gap-8">
"""
        
        for service in self.content['services']:
            html += f"""
                <div class="card-hover p-8 rounded-lg border border-slate-700 hover:border-red-500/50">
                    <div class="text-5xl mb-4">{service['icon']}</div>
                    <h3 class="text-2xl font-bold mb-3">{service['title']}</h3>
                    <p class="text-gray-400 leading-relaxed">{service['description']}</p>
                </div>
"""
        
        html += """
            </div>
        </div>
    </section>

    <!-- Skills -->
    <section class="py-20 px-4">
        <div class="max-w-6xl mx-auto">
            <h2 class="text-5xl font-bold mb-16 text-center">
                <span class="gradient-text">Habilidades</span>
            </h2>

            <div class="grid grid-cols-1 md:grid-cols-2 gap-12">
"""
        
        for skill_group in self.content['skills']:
            html += f"""
                <div>
                    <h3 class="text-2xl font-bold mb-6">{skill_group['category']}</h3>
                    <div class="flex flex-wrap gap-3">
"""
            for skill in skill_group['skills']:
                html += f"""
                        <span class="bg-gradient-to-r from-red-500/20 to-red-500/10 text-red-300 px-4 py-2 rounded-full font-semibold">
                            {skill}
                        </span>
"""
            html += """
                    </div>
                </div>
"""
        
        html += """
            </div>
        </div>
    </section>

    <!-- Testimonials -->
    <section class="py-20 px-4 bg-black/50">
        <div class="max-w-6xl mx-auto">
            <h2 class="text-5xl font-bold mb-16 text-center">
                <span class="gradient-text">Lo que Dicen Sobre Mí</span>
            </h2>

            <div class="grid grid-cols-1 md:grid-cols-3 gap-8">
"""
        
        for testimonial in self.content['testimonials']:
            stars = "⭐" * testimonial['rating']
            html += f"""
                <div class="card-hover bg-gradient-to-br from-slate-800 to-slate-900 border border-slate-700 rounded-xl p-8">
                    <div class="mb-4">{stars}</div>
                    <p class="text-gray-300 mb-6 italic">"{testimonial['text']}"</p>
                    <div>
                        <h4 class="font-bold text-white">{testimonial['author']}</h4>
                        <p class="text-sm text-gray-500">{testimonial['role']}</p>
                    </div>
                </div>
"""
        
        html += """
            </div>
        </div>
    </section>

    <!-- Recent Content -->
    <section class="py-20 px-4">
        <div class="max-w-4xl mx-auto">
            <h2 class="text-5xl font-bold mb-16 text-center">
                <span class="gradient-text">Contenido Reciente</span>
            </h2>

            <div class="space-y-4">
"""
        
        for content in self.content['recent_content']:
            html += f"""
                <div class="group cursor-pointer p-6 rounded-lg border border-slate-700 hover:border-red-500 hover:bg-red-500/5 transition">
                    <div class="flex justify-between items-start">
                        <div class="flex-1">
                            <h3 class="text-lg font-semibold group-hover:text-red-400 transition mb-2">
                                {content['title']}
                            </h3>
                            <div class="flex gap-4 text-sm text-gray-500">
                                <span>{content['date']}</span>
                                <span>•</span>
                                <span class="text-red-400">{content['platform']}</span>
                            </div>
                        </div>
                        <span class="text-2xl text-red-400 group-hover:translate-x-2 transition ml-4">→</span>
                    </div>
                </div>
"""
        
        html += """
            </div>
        </div>
    </section>

    <!-- CTA Section -->
    <section id="contact" class="py-20 px-4 relative overflow-hidden">
        <div class="absolute inset-0 bg-gradient-to-r from-red-500/20 to-red-500/0"></div>
        <div class="relative z-10 max-w-4xl mx-auto text-center">
            <h2 class="text-5xl font-bold mb-6">
                {self.content['cta_section']['title']}
            </h2>
            <p class="text-xl text-gray-300 mb-12">
                {self.content['cta_section']['subtitle']}
            </p>
            <button class="gradient-brand text-white px-12 py-4 rounded-lg font-semibold text-lg hover:shadow-lg hover:shadow-red-500/50 transition transform hover:scale-105">
                {self.content['cta_section']['button_text']}
            </button>
        </div>
    </section>

    <!-- Footer -->
    <footer class="border-t border-slate-800 py-16 px-4 bg-black/80">
        <div class="max-w-6xl mx-auto">
            <div class="grid grid-cols-1 md:grid-cols-3 gap-12 mb-12">
                <div>
                    <div class="flex items-center space-x-3 mb-4">
                        <div class="w-10 h-10 gradient-brand rounded-lg flex items-center justify-center font-bold">
                            DU
                        </div>
                        <div>
                            <h4 class="font-bold">{self.content['footer']['company']}</h4>
                            <p class="text-xs text-gray-500">{self.content['footer']['tagline']}</p>
                        </div>
                    </div>
                </div>
                
                <div>
                    <h4 class="font-semibold mb-4">Enlaces</h4>
                    <ul class="space-y-2">
"""
        
        for link in self.content['footer']['links']:
            html += f'                        <li><a href="{link["url"]}" class="text-gray-400 hover:text-red-400 transition">{link["name"]}</a></li>\n'
        
        html += """
                    </ul>
                </div>
                
                <div>
                    <h4 class="font-semibold mb-4">Sígueme</h4>
                    <div class="flex flex-wrap gap-4">
"""
        
        for social in self.content['social_links']:
            html += f'                        <a href="{social["url"]}" class="text-gray-400 hover:text-red-400 transition text-xl" title="{social["name"]}">{social["icon"]}</a>\n'
        
        html += f"""
                    </div>
                </div>
            </div>
            
            <div class="border-t border-slate-800 pt-8 text-center text-gray-500">
                <p>&copy; {self.content['footer']['year']} {self.content['footer']['company']}. Hecho con <span class="text-red-500">❤️</span> | Email: <a href="mailto:{self.content['footer']['email']}" class="text-red-400 hover:underline">{self.content['footer']['email']}</a></p>
                <p class="text-xs mt-4">Generado por Anais 🐎 | Web Generator System</p>
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
                    target.scrollIntoView({{ behavior: 'smooth', block: 'start' }});
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
    
    def save(self, output_path):
        """Guarda el sitio generado"""
        html = self.generate_html()
        
        path = Path(output_path)
        path.parent.mkdir(parents=True, exist_ok=True)
        
        with open(path, 'w', encoding='utf-8') as f:
            f.write(html)
        
        print(f"✅ Sitio Diego Urquijo generado: {output_path}")
        return path

if __name__ == "__main__":
    from diego_urquijo_scraper import get_diego_urquijo_content
    
    content = get_diego_urquijo_content()
    generator = DiegoWebGenerator(content)
    generator.save("/workspace/anais-workspace/shared/proyectos/web-generator/generated/soydiegoup.html")
