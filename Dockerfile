# Estágio 1: Build
FROM python:3.11-alpine AS builder
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir --user -r requirements.txt

# Estágio 2: Produção (Enxuta)
FROM python:3.11-alpine AS runner
WORKDIR /app

# Criação de usuário não-root por segurança
RUN addgroup -S appgroup && adduser -S appuser -G appgroup

COPY --from=builder /root/.local /home/appuser/.local
COPY main.py .

ENV PATH=/home/appuser/.local/bin:$PATH
USER appuser

EXPOSE 8000

# Healthcheck declarado no container
HEALTHCHECK --interval=30s --timeout=5s --start-period=5s --retries=3 \
  CMD wget --no-verbose --tries=1 --spider http://localhost:8000/health || exit 1

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
