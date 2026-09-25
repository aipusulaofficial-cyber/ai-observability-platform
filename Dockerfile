FROM python:3.12-slim
WORKDIR /app
COPY . .
CMD ["python","ai_observability_platform.py"]
