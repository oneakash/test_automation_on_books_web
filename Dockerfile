FROM mcr.microsoft.com/playwright/python:v1.49.0-noble
WORKDIR /app
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    NODE_OPTIONS=""

COPY requirements.txt .
RUN pip install --no-cache-dir --retries 5 --timeout 60 -r requirements.txt

COPY . .
RUN mkdir -p reports/html allure-results test-results
CMD ["pytest", "--browser", "chromium"]