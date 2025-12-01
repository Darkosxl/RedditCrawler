FROM unclecode/crawl4ai:latest

USER root
WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Install to BOTH locations to cover all cases
RUN playwright install chromium && \
    mkdir -p /home/appuser/.cache/ms-playwright && \
    cp -r /root/.cache/ms-playwright/* /home/appuser/.cache/ms-playwright/ && \
    chmod -R 755 /root/.cache/ms-playwright && \
    chmod -R 755 /home/appuser/.cache/ms-playwright

COPY . .
RUN chmod -R 755 /app

EXPOSE 9090
CMD ["uvicorn", "fastapi_endpoints:app", "--host", "0.0.0.0", "--port", "9090"]