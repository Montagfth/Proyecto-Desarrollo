FROM python:3.12-slim

# Evita archivos .pyc y fuerza salida inmediata en consola
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

# Copiar requirements primero para aprovechar la caché
COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

# Copiar el resto del proyecto
COPY . .

# Crear carpeta para modelos
RUN mkdir -p models

CMD ["python", "main.py"]