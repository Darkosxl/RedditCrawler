# 1. Use the official image (runs as 'appuser' by default)
FROM unclecode/crawl4ai:latest

# 2. THE FIX: Set the browser path to a folder the USER OWNS
# We point this to the user's internal home directory.
# No root access required. No VPS commands required.
ENV PLAYWRIGHT_BROWSERS_PATH=/home/appuser/pw-browsers

# 3. Set working directory
WORKDIR /app

# 4. Copy requirements
COPY requirements.txt .

# 5. Install Python libs
# This triggers the Playwright upgrade
RUN pip install --no-cache-dir -r requirements.txt

# 6. Install Chromium
# This now succeeds because we are writing to our own home folder
RUN playwright install chromium

# 7. Copy your code
COPY . .

# 8. Expose port
EXPOSE 9090

# 9. Run the app
CMD ["uvicorn", "fastapi_endpoints:app", "--host", "0.0.0.0", "--port", "9090"]