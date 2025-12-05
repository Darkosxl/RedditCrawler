# Use Apify's Python image with Playwright support
FROM apify/actor-python-playwright:3.11

# Copy requirements and install dependencies
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Install Playwright browsers (needed by crawl4ai)
RUN playwright install chromium
RUN playwright install-deps chromium

# Copy actor code
COPY . ./

# Run the actor
CMD ["python", "main.py"]
