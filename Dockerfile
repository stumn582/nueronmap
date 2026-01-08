FROM python:3.9-slim

# 환경 변수
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# 작업 디렉토리
WORKDIR /app

# 시스템 패키지
RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# requirements 먼저 복사 (캐시 최적화)
COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

# 소스 복사
COPY . .

# 포트 오픈
EXPOSE 8000

# Gunicorn 실행
CMD ["gunicorn", "--workers", "2", "--bind", "0.0.0.0:8000", "app:app"]

