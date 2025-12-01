# 1. Use the official image (Has system deps pre-installed)
FROM unclecode/crawl4ai:latest

# 2. Set working directory
WORKDIR /app

# 3. Copy requirements
COPY requirements.txt .

# 4. Install libs (This likely UPGRADES Playwright, breaking the existing browser link)
RUN pip install --no-cache-dir -r requirements.txt

# 5. THE FIX: Re-install the browser to match the NEW Playwright version
# Since the base image already has the Linux system libs (drivers), 
# we don't need '--with-deps', we just need the binary.
RUN playwright install chromium

# 6. Copy your code
COPY . .

# 7. Expose port
EXPOSE 9090

# 8. Run
CMD ["uvicorn", "fastapi_endpoints:app", "--host", "0.0.0.0", "--port", "9090"]