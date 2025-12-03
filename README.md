# 🚀 Unified LLM Platform

Eine All-in-One Plattform für Open-Source Large Language Models (LLMs) - optimiert für KVM Debian Root-Server.

## ✨ Features

- 🤖 **Multi-Model Support**: Llama 3, Mistral, Qwen, Phi-3 und mehr
- 🔌 **OpenAI-kompatible API**: Drop-in Ersatz für OpenAI API
- 🎓 **Fine-Tuning**: LoRA/QLoRA Training integriert
- 🖥️ **Web Interface**: Modernes Dashboard mit Chat & Monitoring
- 🐳 **Docker Ready**: Ein Befehl zum Starten
- 📊 **Monitoring**: Resource Tracking & Metrics
- 🔒 **Sicher**: API Keys, Rate Limiting, CORS

## 🎯 Quick Start

```bash
git clone https://github.com/hbrwhizz/unified-llm-platform.git
cd unified-llm-platform
chmod +x scripts/install.sh
./scripts/install.sh
docker-compose up -d
```

Öffne: http://localhost:3000

## 📋 Voraussetzungen

- Debian 11/12 oder Ubuntu 20.04+
- Docker & Docker Compose
- 16GB+ RAM (32GB empfohlen)
- NVIDIA GPU mit 8GB+ VRAM (optional, aber empfohlen)
- 100GB+ freier Speicherplatz

## 🏗️ Architektur

```
┌─────────────────┐
│  Web Interface  │
│   (React)       │
└────────┬────────┘
         │
┌────────▼────────┐
│   Nginx Proxy   │
└────────┬────────┘
         │
┌────────▼────────┐
│  FastAPI Server │
│  (Backend)      │
└────────┬────────┘
         │
┌────────▼────────┐
│  Model Engine   │
│ (Transformers)  │
└─────────────────┘
```

## 🤖 Unterstützte Modelle

| Modell | Parameter | Quantisierung | Min. VRAM |
|--------|-----------|---------------|-----------|
| Llama 3.1 | 8B | 4-bit | 6GB |
| Mistral | 7B | 4-bit | 5GB |
| Qwen 2.5 | 7B | 4-bit | 5GB |
| Phi-3 | 3.8B | 4-bit | 3GB |

## 📚 Dokumentation

- [Installation Guide](docs/INSTALLATION.md)
- [API Dokumentation](docs/API.md)
- [Fine-Tuning Guide](docs/FINE_TUNING.md)
- [Deployment Guide](docs/DEPLOYMENT.md)

## 🚀 Entwicklung

```bash
# Backend
cd backend
pip install -r requirements.txt
uvicorn main:app --reload

# Frontend
cd frontend
npm install
npm start
```

## 📝 Lizenz

MIT License - siehe [LICENSE](LICENSE)

## 🤝 Contributing

Contributions sind willkommen! Siehe [CONTRIBUTING.md](CONTRIBUTING.md)

## 📧 Support

- Issues: https://github.com/hbrwhizz/unified-llm-platform/issues
- Discussions: https://github.com/hbrwhizz/unified-llm-platform/discussions

---

**⚡ Gebaut mit ❤️ für die Open-Source LLM Community**