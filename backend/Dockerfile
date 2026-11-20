# ============================================
# CoffeeCell Backend — Dockerfile
# ============================================
FROM python:3.12-slim

# Python optimizasyonları
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

WORKDIR /app

# Önce requirements'ı kopyala ve kur — cache'den faydalanmak için.
# Kod değişse bile requirements değişmediyse bu katman cache'den gelir.
COPY requirements.txt .
RUN pip install -r requirements.txt

# Sonra uygulama kodunu kopyala
COPY app/ ./app/

# FastAPI'nin dinleyeceği port
EXPOSE 8000

# Uygulamayı başlat (geliştirme modu — kod değişince otomatik yeniden yükler)
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]