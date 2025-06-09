# Imagine de bază cu Python
FROM python:3.11

# Setează directorul de lucru în container
WORKDIR /app

# Copiază fișierele proiectului în container
COPY . .

# Instalează dependințele
RUN pip install --no-cache-dir -r requirements.txt

# Expune portul pe care rulează FastAPI
EXPOSE 8000

# Comanda de rulare a aplicației
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
