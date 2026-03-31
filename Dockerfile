FROM python:3.12-slim

WORKDIR /app

RUN apt-get update && apt-get install -y \
    git \
    curl \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

RUN curl -LsSf https://astral.sh/uv/install.sh | sh
ENV PATH="/root/.local/bin:$PATH"

COPY requirements.txt .
RUN uv pip install --system -r requirements.txt

COPY rlm_source/pyproject.toml ./rlm_source/
RUN uv pip install --system -e ./rlm_source

COPY ui/package.json ui/package-lock.json* ./
RUN cd ui && npm install && npm run build

COPY . .

RUN mkdir -p logs data

ENV PYTHONUNBUFFERED=1
ENV ENVIRONMENT=docker

EXPOSE 8000 8765

CMD ["python", "app.py"]
