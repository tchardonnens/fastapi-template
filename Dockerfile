FROM python:3.12-alpine as builder

WORKDIR /app

COPY requirements.txt .

RUN apk add --no-cache gcc musl-dev
RUN pip install uv
RUN uv pip install --system -r requirements.txt

FROM python:3.12-alpine

WORKDIR /app

COPY --from=builder /usr/local/lib/python3.12/site-packages /usr/local/lib/python3.12/site-packages
COPY --from=builder /usr/local/bin /usr/local/bin

COPY . .

RUN python -m compileall -b .

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0"]