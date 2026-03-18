# Folosim o versiune ușoară de Python
FROM python:3.9-slim

# Setăm folderul de lucru în container
WORKDIR /app

# Copiem fișierul cu dependințe și le instalăm
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiem codul aplicației
COPY Adunare.py .

# Expunem portul pe care rulează Flask
EXPOSE 5050

# Comanda care pornește aplicația
CMD ["python", "Adunare.py"]