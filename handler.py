import requests
import runpod
import os
from flask import Flask, jsonify

# 初始化 Flask 用于 /ping 健康检查
app = Flask(__name__)

API_URL = "https://dashscope-intl.aliyuncs.com/compatible-mode/v1/chat/completions"
API_KEY = os.environ.get("DASHSCOPE_API_KEY")

@app.route("/ping", methods=["GET"])
def ping():
    return jsonify({"status": "ok"}), 200

def handler(event):
    try:
        if not API_KEY:
            return {"error": "DASHSCOPE_API_KEY not set"}
        
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

if __name__ == "__main__":
    import threading
    port = int(os.environ.get("PORT", 8080))
    threading.Thread(target=lambda: app.run(host="0.0.0.0", port=port, debug=False)).start()
    runpod.serverless.start({"handler": handler})
