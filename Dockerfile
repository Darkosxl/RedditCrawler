# 1. Use the official image (Batteries Included)
# This comes with Python, Playwright, Chromium, and all Linux drivers pre-installed.
FROM unclecode/crawl4ai:latest

# 2. Set working directory
WORKDIR /app

# 3. Copy your requirements
# We do this first to cache dependencies
COPY requirements.txt .

# 4. Install YOUR extra libs (FastAPI, ScrapeOps, DotEnv)
# Note: crawl4ai is ALREADY installed in this image, so pip will skip it (fast).
RUN pip install --no-cache-dir -r requirements.txt

# 5. Copy your custom Python code
COPY . .

# 6. Expose your custom port
EXPOSE 9090

# 7. THE CRITICAL STEP:
# We override the default "crawl4ai server" command and run YOUR FastAPI app instead.
CMD ["uvicorn", "fastapi_endpoints:app", "--host", "0.0.0.0", "--port", "9090"]