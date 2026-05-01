FROM python:3.10-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# 指定RunPod识别的标准启动命令
CMD ["python", "/app/rp_handler.py"]
