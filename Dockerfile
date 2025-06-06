FROM python:3.9-slim

ENV PYTHONUNBUFFERED=1
WORKDIR /app

# Install build tools and Python headers for packages that need compilation
RUN apt-get update && apt-get install -y --no-install-recommends \
        build-essential gcc libffi-dev \
        python3-dev python3-distutils \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt ./
# Upgrade pip to avoid build issues and install Python deps
RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir numpy==1.26.4 \
    && pip install --no-cache-dir -r requirements.txt

COPY . ./

CMD ["uvicorn", "embedding_service:app", "--host", "0.0.0.0", "--port", "8000"]
