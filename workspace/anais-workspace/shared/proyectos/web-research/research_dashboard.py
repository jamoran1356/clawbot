#!/usr/bin/env python3
"""
Web Research Dashboard - Interfaz web moderna para investigación
FastAPI + HTML5 + Tailwind CSS
"""

from fastapi import FastAPI, Query, HTTPException
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware
import asyncio
import json
from typing import List, Dict
from datetime import datetime
from research_engine import WebResearchEngine

app = FastAPI(
    title="Research Dashboard",
    description="Motor de investigación web con interfaz visual",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

engine = WebResearchEngine()

@app.get("/", response_class=HTMLResponse)
async def dashboard():
    """Interfaz web del dashboard"""
    return """
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>🔬 Web Research Engine - Dashboard</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <link href="https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;600;700;800&display=swap" rel="stylesheet">
    <style>
        * { font-family: 'Poppins', sans-serif; }
        
        .gradient-brand {
            background: linear-gradient(135deg, #6366F1 0%, #8B5CF6 100%);
        }
        
        .gradient-text {
            background: linear-gradient(135deg, #6366F1 0%, #8B5CF6 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
        }
        
        .card-hover {
            transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        }
        
        .card-hover:hover {
            transform: translateY(-8px);
            box-shadow: 0 20px 40px rgba(99, 102, 241, 0.2);
        }
        
        .loader {
            border: 4px solid #f3f4f6;
            border-top: 4px solid #6366F1;
            border-radius: 50%;
            width: 40px;
            height: 40px;
            animation: spin 1s linear infinite;
        }
        
        @keyframes spin {
            0% { transform: rotate(0deg); }
            100% { transform: rotate(360deg); }
        }
        
        ::selection {
            background: #6366F1;
            color: white;
        }
    </style>
</head>
<body class="bg-slate-950 text-white">
    <!-- Navigation -->
    <nav class="bg-slate-900 border-b border-slate-800 sticky top-0 z-50">
        <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
            <div class="flex justify-between items-center h-16">
                <div class="flex items-center space-x-3">
                    <div class="text-3xl">🔬</div>
                    <div>
                        <h1 class="text-xl font-bold gradient-text">Research Engine</h1>
                        <p class="text-xs text-gray-400">Investigación Web Inteligente</p>
                    </div>
                </div>
                <div class="hidden md:flex space-x-4">
                    <a href="#docs" class="hover:text-indigo-400 transition">Documentación</a>
                    <a href="#examples" class="hover:text-indigo-400 transition">Ejemplos</a>
                </div>
            </div>
        </div>
    </nav>

    <!-- Hero Section -->
    <section class="relative py-20 px-4 bg-gradient-to-b from-indigo-900/20 to-slate-950">
        <div class="max-w-5xl mx-auto text-center">
            <h2 class="text-5xl font-bold mb-6">
                <span class="gradient-text">Investiga la Web</span>
            </h2>
            <p class="text-xl text-gray-300 mb-12">
                Búsqueda, extracción y análisis automático de información en tiempo real
            </p>

            <!-- Search Box -->
            <div class="bg-slate-800 rounded-2xl p-8 border border-slate-700 mb-8">
                <div class="space-y-4">
                    <div>
                        <input 
                            type="text" 
                            id="searchQuery"
                            placeholder="¿Qué deseas investigar? (ej: AI trends 2026)"
                            class="w-full px-6 py-4 bg-slate-900 text-white rounded-xl border border-indigo-500/50 focus:outline-none focus:border-indigo-500 text-lg"
                        >
                    </div>
                    <div class="flex gap-4">
                        <input 
                            type="number" 
                            id="depthInput"
                            min="1" 
                            max="10" 
                            value="3"
                            placeholder="Profundidad"
                            class="px-4 py-2 bg-slate-900 border border-slate-700 rounded-lg text-white w-32"
                        >
                        <button 
                            onclick="startResearch()"
                            class="gradient-brand text-white px-8 py-4 rounded-xl font-semibold hover:shadow-lg hover:shadow-indigo-500/50 transition flex-1"
                        >
                            🔍 Investigar
                        </button>
                    </div>
                </div>
            </div>

            <!-- Features Grid -->
            <div class="grid grid-cols-1 md:grid-cols-3 gap-6">
                <div class="card-hover bg-slate-800 border border-slate-700 rounded-xl p-6">
                    <div class="text-4xl mb-4">🔎</div>
                    <h3 class="font-bold mb-2">Búsqueda Global</h3>
                    <p class="text-gray-400 text-sm">Acceso a múltiples fuentes de información</p>
                </div>
                <div class="card-hover bg-slate-800 border border-slate-700 rounded-xl p-6">
                    <div class="text-4xl mb-4">📊</div>
                    <h3 class="font-bold mb-2">Análisis Profundo</h3>
                    <p class="text-gray-400 text-sm">Extracción y análisis automático de contenido</p>
                </div>
                <div class="card-hover bg-slate-800 border border-slate-700 rounded-xl p-6">
                    <div class="text-4xl mb-4">⚡</div>
                    <h3 class="font-bold mb-2">Resultados Rápidos</h3>
                    <p class="text-gray-400 text-sm">Procesamiento veloz en tiempo real</p>
                </div>
            </div>
        </div>
    </section>

    <!-- Results Section -->
    <section class="py-20 px-4">
        <div class="max-w-6xl mx-auto">
            <div id="loadingSpinner" style="display:none;" class="text-center py-12">
                <div class="flex justify-center mb-4">
                    <div class="loader"></div>
                </div>
                <p class="text-gray-400">Investigando...</p>
            </div>

            <div id="resultsContainer" style="display:none;">
                <h2 class="text-4xl font-bold mb-2 gradient-text">Resultados</h2>
                <p id="queryText" class="text-gray-400 mb-8"></p>

                <!-- Stats -->
                <div class="grid grid-cols-1 md:grid-cols-4 gap-4 mb-12">
                    <div class="bg-gradient-to-br from-indigo-900/50 to-indigo-900/20 border border-indigo-500/30 rounded-xl p-6">
                        <div class="text-3xl font-bold text-indigo-400" id="statTotal">0</div>
                        <div class="text-gray-400">Resultados</div>
                    </div>
                    <div class="bg-gradient-to-br from-purple-900/50 to-purple-900/20 border border-purple-500/30 rounded-xl p-6">
                        <div class="text-3xl font-bold text-purple-400" id="statExtracted">0</div>
                        <div class="text-gray-400">Extraídos</div>
                    </div>
                    <div class="bg-gradient-to-br from-pink-900/50 to-pink-900/20 border border-pink-500/30 rounded-xl p-6">
                        <div class="text-3xl font-bold text-pink-400" id="statAnalyzed">0</div>
                        <div class="text-gray-400">Analizados</div>
                    </div>
                    <div class="bg-gradient-to-br from-cyan-900/50 to-cyan-900/20 border border-cyan-500/30 rounded-xl p-6">
                        <div class="text-3xl font-bold text-cyan-400" id="statRelevance">0%</div>
                        <div class="text-gray-400">Relevancia</div>
                    </div>
                </div>

                <!-- Results List -->
                <div id="resultsList" class="space-y-4"></div>

                <!-- Download JSON -->
                <div class="text-center mt-12">
                    <button 
                        onclick="downloadResults()"
                        class="bg-gradient-to-r from-indigo-600 to-purple-600 text-white px-8 py-3 rounded-lg font-semibold hover:shadow-lg transition"
                    >
                        💾 Descargar Resultados (JSON)
                    </button>
                </div>
            </div>
        </div>
    </section>

    <!-- Examples Section -->
    <section id="examples" class="py-20 px-4 bg-slate-900/50">
        <div class="max-w-6xl mx-auto">
            <h2 class="text-4xl font-bold mb-12 text-center gradient-text">Ejemplos de Búsqueda</h2>
            
            <div class="grid grid-cols-1 md:grid-cols-3 gap-6">
                <div 
                    class="card-hover bg-slate-800 border border-slate-700 rounded-xl p-6 cursor-pointer hover:border-indigo-500"
                    onclick="setSearchQuery('AI trends 2026')"
                >
                    <h3 class="font-bold mb-2 text-lg">🤖 IA 2026</h3>
                    <p class="text-gray-400 mb-4">Tendencias en inteligencia artificial</p>
                    <span class="text-indigo-400 text-sm">→ Investigar</span>
                </div>
                
                <div 
                    class="card-hover bg-slate-800 border border-slate-700 rounded-xl p-6 cursor-pointer hover:border-indigo-500"
                    onclick="setSearchQuery('FastAPI Python web framework')"
                >
                    <h3 class="font-bold mb-2 text-lg">⚡ FastAPI</h3>
                    <p class="text-gray-400 mb-4">Framework web moderno para APIs</p>
                    <span class="text-indigo-400 text-sm">→ Investigar</span>
                </div>
                
                <div 
                    class="card-hover bg-slate-800 border border-slate-700 rounded-xl p-6 cursor-pointer hover:border-indigo-500"
                    onclick="setSearchQuery('Web3 blockchain cryptocurrency')"
                >
                    <h3 class="font-bold mb-2 text-lg">🔗 Web3</h3>
                    <p class="text-gray-400 mb-4">Descentralización y blockchain</p>
                    <span class="text-indigo-400 text-sm">→ Investigar</span>
                </div>
            </div>
        </div>
    </section>

    <!-- Footer -->
    <footer class="border-t border-slate-800 py-12 px-4 bg-slate-900/50">
        <div class="max-w-6xl mx-auto text-center text-gray-500">
            <p>🔬 Web Research Engine v1.0 | Creado por Anais 🐎</p>
            <p class="text-xs mt-2">Generado: 29 de Enero, 2026</p>
        </div>
    </footer>

    <script>
        let currentResearch = null;

        function setSearchQuery(query) {
            document.getElementById('searchQuery').value = query;
        }

        async function startResearch() {
            const query = document.getElementById('searchQuery').value.trim();
            const depth = parseInt(document.getElementById('depthInput').value) || 3;

            if (!query) {
                alert('Por favor ingresa una búsqueda');
                return;
            }

            // Show loading
            document.getElementById('loadingSpinner').style.display = 'block';
            document.getElementById('resultsContainer').style.display = 'none';

            try {
                const response = await fetch(`/api/research?query=${encodeURIComponent(query)}&depth=${depth}`);
                const data = await response.json();

                currentResearch = data;
                displayResults(data, query);

                document.getElementById('loadingSpinner').style.display = 'none';
                document.getElementById('resultsContainer').style.display = 'block';
            } catch (error) {
                alert('Error: ' + error.message);
                document.getElementById('loadingSpinner').style.display = 'none';
            }
        }

        function displayResults(data, query) {
            document.getElementById('queryText').textContent = `Resultados para: "${query}"`;
            
            const summary = data.summary || {};
            document.getElementById('statTotal').textContent = summary.total_sources || 0;
            document.getElementById('statExtracted').textContent = summary.total_extracted || 0;
            document.getElementById('statAnalyzed').textContent = summary.total_analyzed || 0;
            document.getElementById('statRelevance').textContent = Math.round(summary.avg_relevance || 0) + '%';

            const resultsList = document.getElementById('resultsList');
            resultsList.innerHTML = '';

            const results = data.stages?.search?.results || [];
            
            if (results.length === 0) {
                resultsList.innerHTML = '<p class="text-center text-gray-400">No se encontraron resultados</p>';
                return;
            }

            results.forEach((result, index) => {
                const resultHTML = `
                    <div class="card-hover bg-slate-800 border border-slate-700 rounded-xl p-6 hover:border-indigo-500">
                        <div class="flex items-start justify-between mb-3">
                            <span class="text-2xl font-bold text-indigo-400">${index + 1}</span>
                            <span class="px-3 py-1 bg-indigo-500/20 text-indigo-300 rounded-full text-xs">Relevancia: ${(result.score || 0).toFixed(1)}</span>
                        </div>
                        <h3 class="font-bold text-lg mb-2 hover:text-indigo-400 transition">
                            <a href="${result.url}" target="_blank">${result.title}</a>
                        </h3>
                        <p class="text-gray-400 mb-4">${result.snippet || 'Sin descripción'}</p>
                        <div class="flex items-center justify-between">
                            <span class="text-sm text-gray-500">🔗 ${new URL(result.url).hostname}</span>
                            <a href="${result.url}" target="_blank" class="text-indigo-400 hover:text-indigo-300 text-sm">Ver más →</a>
                        </div>
                    </div>
                `;
                resultsList.innerHTML += resultHTML;
            });
        }

        function downloadResults() {
            if (!currentResearch) return;
            
            const dataStr = JSON.stringify(currentResearch, null, 2);
            const dataBlob = new Blob([dataStr], { type: 'application/json' });
            const url = URL.createObjectURL(dataBlob);
            const link = document.createElement('a');
            link.href = url;
            link.download = `research_${new Date().getTime()}.json`;
            link.click();
        }

        // Enter key to search
        document.getElementById('searchQuery').addEventListener('keypress', function(e) {
            if (e.key === 'Enter') startResearch();
        });
    </script>
</body>
</html>
    """

@app.get("/api/research")
async def research_api(query: str = Query(..., min_length=1), depth: int = Query(3, ge=1, le=10)):
    """API de investigación"""
    try:
        research = await engine.search_and_analyze(query, depth)
        return research
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/health")
async def health():
    """Health check"""
    return {"status": "ok"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8001,
        log_level="info"
    )
