# 🩺 BreastCancer Agent-IA (LLM Assistant)

**Stack**: Python 3.11, FastAPI, OpenAI (LLM), LangChain + Chroma (RAG), Pydantic Settings, MLflow, pytest, Docker, GitHub Actions

> ⚠️ **Aviso clínico**: Este asistente es **apoyo informativo** para el área de cáncer de mama. **No** reemplaza juicio médico ni ofrece diagnóstico/indicaciones definitivas. Siempre remite a **consulta médica presencial**.

---

## 📁 Estructura

```
BreastCancer Agent-IA/
├─ app/
│  ├─ config.py
│  ├─ server.py
│  ├─ prompts/system_breast_cancer_es.txt
│  ├─ chains/assistant.py
│  ├─ tools/{calculator.py, search_knowledge.py}
│  ├─ telemetry/mlflow_utils.py
│  ├─ security/auth.py
│  └─ rag/{loader.py, embedder.py, vectorstore.py, retriever.py}
├─ scripts/{index_knowledge.py, evaluate.py}
├─ data/knowledge/         # Coloca aquí tus guías internas (PDF/MD/TXT)
├─ tests/test_server.py
├─ vectorstore/            # Persistencia Chroma (se crea tras indexar)
├─ .github/workflows/ci.yml
├─ requirements.txt, Dockerfile, docker-compose.yml, Makefile
├─ .env.example, .gitignore, LICENSE, README.md
```

---

## 🚀 Instalación y ejecución (Manual)

### 1) Prerrequisitos
- Python 3.11+
- Docker + Docker Compose (opcional pero recomendado)
- Clave de API de OpenAI
- (Opcional) Cuenta GitHub si quieres CI/CD

### 2) Configura variables
```bash
cp .env.example .env
# Edita .env y coloca tu OPENAI_API_KEY y API_KEY
```

### 3) (Opcional) Ejecutar con Docker
```bash
docker compose up --build
# App: http://localhost:8000/docs
# MLflow: http://localhost:5000
```

### 4) Ejecutar localmente (sin Docker)
```bash
python -m venv .BreastCancer-Agent-IA
source .BreastCancer-Agent-IA/bin/activate   # En Windows: .\BreastCancer-Agent-IA\Scripts\activate
pip install -r requirements.txt
uvicorn app.server:app --reload --host 0.0.0.0 --port 8000
```

### 5) Indexar conocimiento (RAG)
Coloca PDFs/TXT/MD en `data/knowledge/` y luego:
```bash
python scripts/index_knowledge.py --root data/knowledge
```

### 6) Probar endpoint con API Key
```bash
curl -X POST http://localhost:8000/chat   -H "Content-Type: application/json"   -H "X-API-Key: supersecreto_local"   -d '{"text":"¿Qué implica un BI-RADS 3?"}'
```

### 7) Evaluación con MLflow
```bash
python scripts/evaluate.py
# Revisa métricas/artefactos en http://localhost:5000
```

### 8) Subir a GitHub
```bash
git init
git add .
git commit -m "feat: breast cancer LLM assistant (RAG + MLflow)"
# git remote add origin https://github.com/<tu_usuario>/BreastCancer-Agent-IA.git
# git push -u origin main
```

---

## 🔒 Seguridad y privacidad
- No subas PHI a repos públicos. Usa GitHub privado o manejo de secretos.
- Autenticación por **API Key** requerida en `/chat`.
- Guardrails clínicos y recordatorio explícito de consulta médica.

## 🧪 CI/CD
- Workflow `ci.yml`: instala dependencias, ejecuta tests y construye imagen Docker.
- Puedes extenderlo para publicar en GHCR o desplegar en tu plataforma favorita (Render, Railway, ECS).

## 🧩 Extensiones
- Añade OAuth/SSO, evaluación avanzada (Elo, rubricas), observabilidad (Prometheus/Grafana), y tracing (OpenTelemetry).

---

## ❓ Soporte rápido
- Si `chromadb` no persiste, verifica permisos de `vectorstore/`.
- Si no ves `usage` en OpenAI, actualiza `openai` a la versión indicada.

¡Éxito con tu asistente! 💙
