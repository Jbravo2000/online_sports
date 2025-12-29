# Imagen base
FROM python:3.11-slim

# Directorio de trabajo
WORKDIR /app

# Copiar dependencias
COPY requirements.txt .

# Instalar dependencias
RUN pip install --no-cache-dir -r requirements.txt

# Copiar el código
COPY app.py .

# Exponer puerto
EXPOSE 5000

# Ejecutar la aplicación
CMD ["python", "app.py"]
