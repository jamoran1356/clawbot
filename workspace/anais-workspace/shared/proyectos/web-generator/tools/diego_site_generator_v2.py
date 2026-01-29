#!/usr/bin/env python3
"""
Diego Urquijo Personal Brand Website Generator v2
Estructura: Hero → About → Producto → CTA → Testimonios → CTA → Garantía → Footer
"""

from pathlib import Path

class DiegoWebGeneratorV2:
    """Generador mejorado con estructura completa"""
    
    def __init__(self, content):
        self.content = content
        
    def generate_html(self):
        """Genera HTML5 con estructura completa"""
        
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
    
    <!-- Fonts -->
    <link href="https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;600;700;800&family=JetBrains+Mono:wght@400;600&display=swap" rel="stylesheet">
    
    <!-- Tailwind CSS -->
    <script src="https://cdn.tailwindcss.com"></script>
    
    <style>
        * {{ font-family: 'Poppins', sans-serif; }}
        
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
        
        @keyframes float {{
            0%, 100% {{ transform: translateY(0); }}
            50% {{ transform: translateY(-20px); }}
        }}
        
        .animate-float {{
            animation: float 3s ease-in-out infinite;
        }}
        
        .btn-primary {{
            @apply gradient-brand text-white px-8 py-4 rounded-lg font-semibold text-lg hover:shadow-lg hover:shadow-red-500/50 transition transform hover:scale-105;
        }}
        
        .btn-secondary {{
            @apply border-2 border-red-500 text-red-400 px-8 py-4 rounded-lg font-semibold text-lg hover:bg-red-500/10 transition;
        }}
        
        .section-title {{
            @apply text-5xl font-bold mb-4 text-center;
        }}
        
        .section-subtitle {{
            @apply text-gray-400 text-center mb-16 max-w-2xl mx-auto;
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
                    <a href="#producto" class="hover:text-red-400 transition">Producto</a>
                    <a href="#testimonios" class="hover:text-red-400 transition">Testimonios</a>
                    <a href="#garantia" class="hover:text-red-400 transition">Garantía</a>
                </div>
                <button class="gradient-brand text-white px-6 py-2 rounded-lg font-semibold hover:shadow-lg transition">
                    Conectar
                </button>
            </div>
        </div>
    </nav>

    <!-- ================================================================ -->
    <!-- 1. HERO SECTION -->
    <!-- ================================================================ -->
    <section class="relative min-h-screen flex items-center justify-center overflow-hidden pt-20">
        <div class="absolute inset-0 overflow-hidden">
            <div class="absolute top-20 left-10 w-80 h-80 bg-red-500 rounded-full mix-blend-multiply filter blur-3xl opacity-20 animate-float"></div>
            <div class="absolute top-40 right-10 w-80 h-80 bg-teal-500 rounded-full mix-blend-multiply filter blur-3xl opacity-20" style="animation: float 4s ease-in-out infinite 1s;"></div>
        </div>

        <div class="relative z-10 max-w-5xl mx-auto px-4 text-center">
            <div class="inline-block px-4 py-2 rounded-full bg-red-500/10 text-red-400 mb-6 font-semibold text-sm">
                ✨ Bienvenido a Soydiegoup
            </div>
            
            <h1 class="text-7xl font-bold mb-6 gradient-text">
                Diego Urquijo
            </h1>
            
            <p class="text-2xl text-gray-300 mb-4 font-light">
                {self.content['tagline']}
            </p>
            
            <p class="text-xl text-gray-400 mb-12 max-w-3xl mx-auto leading-relaxed">
                {self.content['hero']['subtitle']}
            </p>
            
            <div class="flex flex-col sm:flex-row gap-4 justify-center mb-16">
                <button class="btn-primary">
                    {self.content['hero']['cta']}
                </button>
                <button class="btn-secondary">
                    {self.content['hero']['secondary_cta']}
                </button>
            </div>

            <div class="absolute bottom-10 left-1/2 transform -translate-x-1/2 animate-bounce">
                <svg class="w-6 h-6 text-red-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 14l-7 7m0 0l-7-7m7 7V3"></path>
                </svg>
            </div>
        </div>
    </section>

    <!-- ================================================================ -->
    <!-- 2. ABOUT SECTION -->
    <!-- ================================================================ -->
    <section id="about" class="py-20 px-4 bg-gradient-to-b from-slate-900 to-slate-950">
        <div class="max-w-5xl mx-auto">
            <div class="grid grid-cols-1 md:grid-cols-2 gap-12 items-center">
                <!-- Contenido -->
                <div>
                    <h2 class="section-title text-left">
                        <span class="gradient-text">Sobre Mí</span>
                    </h2>
                    <p class="text-gray-300 text-lg leading-relaxed mb-6">
                        Soy Diego Urquijo, un creator y desarrollador full-stack apasionado por la tecnología y la educación. 
                        Con más de 5 años de experiencia, he trabajado en proyectos que transforman ideas en realidades digitales.
                    </p>
                    <p class="text-gray-300 text-lg leading-relaxed mb-6">
                        Mi misión es ayudar a otros a crecer en el mundo tech, compartiendo conocimiento puro y práctico.
                        Creo que la educación de calidad debería ser accesible para todos.
                    </p>
                    <p class="text-gray-300 text-lg leading-relaxed mb-8">
                        Combino desarrollo de software, estrategia digital y mentoría para crear soluciones completas.
                    </p>
                    
                    <!-- Stats -->
                    <div class="grid grid-cols-3 gap-4">
"""
        
        for stat in self.content['stats']:
            html += f"""
                        <div>
                            <div class="text-4xl font-bold gradient-text">{stat['value']}</div>
                            <div class="text-sm text-gray-400">{stat['label']}</div>
                        </div>
"""
        
        html += """
                    </div>
                </div>
                
                <!-- Imagen placeholder -->
                <div class="bg-gradient-to-br from-slate-800 to-slate-900 rounded-xl p-8 border border-slate-700 h-96 flex items-center justify-center">
                    <div class="text-center">
                        <div class="text-6xl mb-4">👨‍💻</div>
                        <p class="text-gray-400">Foto de Diego</p>
                    </div>
                </div>
            </div>
        </div>
    </section>

    <!-- ================================================================ -->
    <!-- 3. PRODUCTO SECTION -->
    <!-- ================================================================ -->
    <section id="producto" class="py-20 px-4">
        <div class="max-w-6xl mx-auto">
            <h2 class="section-title">
                <span class="gradient-text">Mi Producto</span>
            </h2>
            <p class="section-subtitle">
                Servicios integrales para tu transformación digital y crecimiento tech
            </p>

            <div class="grid grid-cols-1 md:grid-cols-3 gap-8">
"""
        
        for service in self.content['services']:
            html += f"""
                <div class="card-hover group bg-gradient-to-br from-slate-800 to-slate-900 border border-slate-700 rounded-xl p-8 hover:border-red-500/50">
                    <div class="text-6xl mb-6">{service['icon']}</div>
                    <h3 class="text-2xl font-bold mb-4 group-hover:text-red-400 transition">
                        {service['title']}
                    </h3>
                    <p class="text-gray-400 mb-6 leading-relaxed">
                        {service['description']}
                    </p>
                    <ul class="space-y-2 mb-6">
                        <li class="flex items-center text-gray-300">
                            <span class="text-red-400 mr-2">✓</span> Personalizado
                        </li>
                        <li class="flex items-center text-gray-300">
                            <span class="text-red-400 mr-2">✓</span> 1-a-1 Support
                        </li>
                        <li class="flex items-center text-gray-300">
                            <span class="text-red-400 mr-2">✓</span> Garantizado
                        </li>
                    </ul>
                    <a href="#" class="inline-block text-red-400 font-semibold hover:translate-x-2 transition">
                        Conocer más →
                    </a>
                </div>
"""
        
        html += """
            </div>
        </div>
    </section>

    <!-- ================================================================ -->
    <!-- 4. CTA SECTION #1 -->
    <!-- ================================================================ -->
    <section class="py-20 px-4 bg-black/50">
        <div class="max-w-4xl mx-auto text-center">
            <h2 class="text-4xl font-bold mb-6">
                ¿Listo para Transformar tu Proyecto?
            </h2>
            <p class="text-xl text-gray-300 mb-8">
                Agendar una consulta gratuita de 30 minutos
            </p>
            <button class="btn-primary">
                Agendar Llamada Gratuita
            </button>
        </div>
    </section>

    <!-- ================================================================ -->
    <!-- 5. TESTIMONIOS SECTION -->
    <!-- ================================================================ -->
    <section id="testimonios" class="py-20 px-4">
        <div class="max-w-6xl mx-auto">
            <h2 class="section-title">
                <span class="gradient-text">Lo que Dicen Sobre Mí</span>
            </h2>
            <p class="section-subtitle">
                Testimonios de clientes y estudiantes satisfechos
            </p>

            <div class="grid grid-cols-1 md:grid-cols-3 gap-8">
"""
        
        for testimonial in self.content['testimonials']:
            stars = "⭐" * testimonial['rating']
            html += f"""
                <div class="card-hover bg-gradient-to-br from-slate-800 to-slate-900 border border-slate-700 rounded-xl p-8">
                    <div class="mb-4 text-lg">{stars}</div>
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

    <!-- ================================================================ -->
    <!-- 6. CTA SECTION #2 -->
    <!-- ================================================================ -->
    <section class="py-20 px-4 bg-gradient-to-r from-red-500/20 to-red-500/0">
        <div class="max-w-4xl mx-auto text-center">
            <h2 class="text-4xl font-bold mb-6">
                Únete a Nuestra Comunidad
            </h2>
            <p class="text-xl text-gray-300 mb-8">
                Más de 50,000 personas aprendiendo y creciendo juntas
            </p>
            <div class="flex gap-4 justify-center flex-wrap">
                <button class="btn-primary">
                    Acceso a Comunidad
                </button>
                <button class="btn-secondary">
                    Conocer Más
                </button>
            </div>
        </div>
    </section>

    <!-- ================================================================ -->
    <!-- 7. GARANTÍA SECTION -->
    <!-- ================================================================ -->
    <section id="garantia" class="py-20 px-4 bg-black/50">
        <div class="max-w-6xl mx-auto">
            <h2 class="section-title">
                <span class="gradient-text">Garantía de Satisfacción</span>
            </h2>
            <p class="section-subtitle">
                Tu éxito es mi éxito
            </p>

            <div class="grid grid-cols-1 md:grid-cols-2 gap-12">
                <div class="space-y-6">
                    <div class="flex gap-4">
                        <div class="flex-shrink-0">
                            <div class="flex items-center justify-center h-12 w-12 rounded-md gradient-brand">
                                <span class="text-2xl">✓</span>
                            </div>
                        </div>
                        <div>
                            <h3 class="text-xl font-bold text-white mb-2">Satisfacción Garantizada 30 Días</h3>
                            <p class="text-gray-400">Si no estás satisfecho con mi servicio, te devuelvo el 100% en los primeros 30 días</p>
                        </div>
                    </div>

                    <div class="flex gap-4">
                        <div class="flex-shrink-0">
                            <div class="flex items-center justify-center h-12 w-12 rounded-md gradient-brand">
                                <span class="text-2xl">✓</span>
                            </div>
                        </div>
                        <div>
                            <h3 class="text-xl font-bold text-white mb-2">Soporte de Por Vida</h3>
                            <p class="text-gray-400">Acceso permanente a mensajes directos para dudas relacionadas a lo que trabajamos</p>
                        </div>
                    </div>

                    <div class="flex gap-4">
                        <div class="flex-shrink-0">
                            <div class="flex items-center justify-center h-12 w-12 rounded-md gradient-brand">
                                <span class="text-2xl">✓</span>
                            </div>
                        </div>
                        <div>
                            <h3 class="text-xl font-bold text-white mb-2">Actualizaciones Gratis</h3>
                            <p class="text-gray-400">Acceso a todas las actualizaciones y mejoras futuras sin costo adicional</p>
                        </div>
                    </div>

                    <div class="flex gap-4">
                        <div class="flex-shrink-0">
                            <div class="flex items-center justify-center h-12 w-12 rounded-md gradient-brand">
                                <span class="text-2xl">✓</span>
                            </div>
                        </div>
                        <div>
                            <h3 class="text-xl font-bold text-white mb-2">Certificado Profesional</h3>
                            <p class="text-gray-400">Certificado verificable al completar el programa</p>
                        </div>
                    </div>
                </div>

                <!-- CTA en garantía -->
                <div class="bg-gradient-to-br from-red-500/20 to-red-500/10 border border-red-500/30 rounded-xl p-12 flex flex-col justify-center">
                    <div class="text-6xl mb-4">🛡️</div>
                    <h3 class="text-2xl font-bold mb-4">100% Seguro</h3>
                    <p class="text-gray-300 mb-8">
                        No hay riesgo. Protegemos tu inversión con nuestras garantías.
                    </p>
                    <button class="btn-primary w-full">
                        Empezar Ahora Sin Riesgo
                    </button>
                </div>
            </div>
        </div>
    </section>

    <!-- ================================================================ -->
    <!-- 8. FOOTER -->
    <!-- ================================================================ -->
    <footer class="border-t border-slate-800 py-16 px-4 bg-black/80">
        <div class="max-w-6xl mx-auto">
            <!-- Links y Info -->
            <div class="grid grid-cols-1 md:grid-cols-4 gap-12 mb-12">
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
                    <h4 class="font-semibold mb-4">Producto</h4>
                    <ul class="space-y-2">
                        <li><a href="#" class="text-gray-400 hover:text-red-400 transition">Servicios</a></li>
                        <li><a href="#" class="text-gray-400 hover:text-red-400 transition">Testimonios</a></li>
                        <li><a href="#" class="text-gray-400 hover:text-red-400 transition">Garantía</a></li>
                        <li><a href="#" class="text-gray-400 hover:text-red-400 transition">Blog</a></li>
                    </ul>
                </div>
                
                <div>
                    <h4 class="font-semibold mb-4">Comunidad</h4>
                    <ul class="space-y-2">
                        <li><a href="#" class="text-gray-400 hover:text-red-400 transition">Discord</a></li>
                        <li><a href="#" class="text-gray-400 hover:text-red-400 transition">YouTube</a></li>
                        <li><a href="#" class="text-gray-400 hover:text-red-400 transition">Twitter</a></li>
                        <li><a href="#" class="text-gray-400 hover:text-red-400 transition">LinkedIn</a></li>
                    </ul>
                </div>
                
                <div>
                    <h4 class="font-semibold mb-4">Legal</h4>
                    <ul class="space-y-2">
                        <li><a href="#" class="text-gray-400 hover:text-red-400 transition">Privacidad</a></li>
                        <li><a href="#" class="text-gray-400 hover:text-red-400 transition">Términos</a></li>
                        <li><a href="#" class="text-gray-400 hover:text-red-400 transition">Contacto</a></li>
                    </ul>
                </div>
            </div>
            
            <!-- Separador -->
            <div class="border-t border-slate-800 pt-8 text-center text-gray-500">
                <p>&copy; {self.content['footer']['year']} {self.content['footer']['company']}. Todos los derechos reservados.</p>
                <p class="text-xs mt-2">Hecho con <span class="text-red-500">❤️</span> por Anais 🐎</p>
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
        
        print(f"✅ Sitio Diego Urquijo v2 generado: {output_path}")
        return path

if __name__ == "__main__":
    from diego_urquijo_scraper import get_diego_urquijo_content
    
    content = get_diego_urquijo_content()
    generator = DiegoWebGeneratorV2(content)
    generator.save("/workspace/anais-workspace/shared/proyectos/web-generator/generated/soydiegoup_v2.html")
