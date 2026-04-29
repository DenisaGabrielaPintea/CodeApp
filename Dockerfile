# Folosim o imagine oficială de Python
FROM python:3.11-slim

# Setăm folderul de lucru în container
WORKDIR /app

# Copiem fișierul de dependențe
COPY requirements.txt .

# Instalăm dependențele
RUN pip install --no-cache-dir -r requirements.txt

# Copiem restul codului (app.py)
COPY . .

# Expunem portul 5050
EXPOSE 5050

# Comanda de pornire a aplicației
CMD ["python", "app.py"]