# 1. Use the official image to get the system dependencies (Linux drivers)
# We use this primarily for the OS-level libraries (libnss3, libgtk, etc)
FROM unclecode/crawl4ai:latest

# 2. Set environment variables to force Playwright to behave
# This ensures browsers are installed globally in the container, not just for one user
ENV PLAYWRIGHT_BROWSERS_PATH=/ms-playwright

# 3. Set working directory
WORKDIR /app

# 4. Copy requirements
COPY requirements.txt .

# 5. Install your Python libraries
# This step often upgrades Playwright, breaking the pre-installed browser link
RUN pip install --no-cache-dir -r requirements.txt

# 6. THE FIX: Force re-installation of the browser
# We use the 'root' user to install them globally so ANY user can find them.
# The 'chromium' arg keeps the image size smaller (skips Firefox/WebKit).
RUN playwright install chromium

# 7. Copy your application code
COPY . .

# 8. Expose your port
EXPOSE 9090

# 9. Run the application
CMD ["uvicorn", "fastapi_endpoints:app", "--host", "0.0.0.0", "--port", "9090"]