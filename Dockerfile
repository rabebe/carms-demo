FROM python:3.10.19-slim

# Set working directory
WORKDIR /code

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    libc-dev \
    && rm -rf /var/lib/apt/lists/*

# Install python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copy the app and data folders
# Note: Ensure local structure matches these paths
COPY ./app ./app
COPY ./data ./data
COPY ./dagster_pipeline ./dagster_pipeline

# Expose FastAPI port
EXPOSE 8000

# Run the application
CMD ["uvicorn", "app.api:app", "--host", "0.0.0.0", "--port", "8000"]