FROM unclecode/crawl4ai:latest

USER root
WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
RUN playwright install --with-deps chromium

COPY . .

EXPOSE 9090
CMD ["uvicorn", "fastapi_endpoints:app", "--host", "0.0.0.0", "--port", "9090"]