FROM python:3.11.3

WORKDIR /app

COPY requirements.txt .

COPY bot.py .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["python", "bot.py"]