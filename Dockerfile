FROM python:3.11-slim

WORKDIR /app

RUN python -m venv /opt/venv

RUN /opt/venv/bin/pip install --upgrade pip

COPY requirements.txt .
RUN /opt/venv/bin/pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000

CMD ["/opt/venv/bin/uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
