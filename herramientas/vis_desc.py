#!/usr/bin/env python3
"""Describe una imagen con el modelo de vision local (llama.cpp :8081, base64 directo)."""
import base64, json, mimetypes, sys, urllib.request

URL = "http://localhost:8081/v1/chat/completions"
MODEL = "Qwen3.5-2B-Q8_0.gguf"


def ask(path, prompt, max_tokens=400):
    mt = mimetypes.guess_type(path)[0] or "image/png"
    b64 = base64.b64encode(open(path, "rb").read()).decode()
    payload = {
        "model": MODEL,
        "messages": [{
            "role": "user",
            "content": [
                {"type": "text", "text": prompt},
                {"type": "image_url", "image_url": {"url": f"data:{mt};base64,{b64}"}},
            ],
        }],
        "temperature": 0.1,
        "max_tokens": max_tokens,
    }
    req = urllib.request.Request(
        URL, data=json.dumps(payload).encode(),
        headers={"Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=600) as r:
        d = json.load(r)
    return d["choices"][0]["message"].get("content") or ""


if __name__ == "__main__":
    path, prompt = sys.argv[1], sys.argv[2]
    print(ask(path, prompt, int(sys.argv[3]) if len(sys.argv) > 3 else 400))
