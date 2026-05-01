# 标准RunPod无服务器处理脚本
import runpod
import requests
import os
from flask import Flask, jsonify

# 初始化Flask用于健康检查
app = Flask(__name__)

API_URL = "https://dashscope-intl.aliyuncs.com/compatible-mode/v1/chat/completions"
API_KEY = os.environ.get("DASHSCOPE_API_KEY")

@app.route("/ping", methods=["GET"])
def ping():
    return jsonify({"status": "ok"}), 200

def handler(event):
    try:
        if not API_KEY:
            return {"error": "DASHSCOPE_API_KEY not set in environment variables"}
        
        input_data = event["input"]
        headers = {
            "Authorization": f"Bearer {API_KEY}",
            "Content-Type": "application/json"
        }
        resp = requests.post(API_URL, json=input_data, headers=headers, timeout=30)
        resp.raise_for_status()
        return resp.json()
    except Exception as e:
        return {"error": str(e)}

# RunPod标准入口
runpod.serverless.start({"handler": handler})

# 启动健康检查服务
if __name__ == "__main__":
    import threading
    port = int(os.environ.get("PORT", 8080))
    threading.Thread(target=lambda: app.run(host="0.0.0.0", port=port, debug=False)).start()
    runpod.serverless.start({"handler": handler})
