FROM unclecode/crawl4ai:latest

USER root
WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Install browsers to /app/.browsers - accessible regardless of runtime user
ENV PLAYWRIGHT_BROWSERS_PATH=/app/.browsers
RUN mkdir -p /app/.browsers && \
    playwright install chromium && \
    chmod -R 755 /app/.browsers

COPY . .

# Make everything readable by any user
RUN chmod -R 755 /app

EXPOSE 9090
CMD ["uvicorn", "fastapi_endpoints:app", "--host", "0.0.0.0", "--port", "9090"]