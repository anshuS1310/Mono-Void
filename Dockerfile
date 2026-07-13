# ── Base image ─────────────────────────────────────────────────────────────────
FROM python:3.11-slim

# ── Working directory ───────────────────────────────────────────────────────────
WORKDIR /app

# ── Install dependencies first (layer caching) ─────────────────────────────────
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# ── Copy the rest of the project ───────────────────────────────────────────────
COPY . .

# ── Render dynamically assigns $PORT — Streamlit must listen on it ─────────────
ENV PORT=8501
EXPOSE 8501

# ── Start Streamlit ────────────────────────────────────────────────────────────
CMD streamlit run app.py \
    --server.port=$PORT \
    --server.address=0.0.0.0 \
    --server.headless=true \
    --server.enableCORS=false \
    --server.enableXsrfProtection=false
