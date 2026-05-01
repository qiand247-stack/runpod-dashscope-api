import runpod
import requests
import os

API_URL = "https://dashscope-intl.aliyuncs.com/compatible-mode/v1/chat/completions"
API_KEY = os.environ.get("DASHSCOPE_API_KEY")

def handler(event):
    if not API_KEY:
        return {"error": "DASHSCOPE_API_KEY not set"}
    
    input_data = event["input"]
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }
    response = requests.post(API_URL, json=input_data, headers=headers, timeout=30)
    response.raise_for_status()
    return response.json()

# RunPod 强制要求的启动入口
runpod.serverless.start({"handler": handler})
