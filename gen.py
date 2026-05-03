from flask import Flask, request, jsonify
import requests, json, re
from user_agent import generate_user_agent as a

app = Flask(__name__)

BASE = "https://www.free-ai-online.com/"


def n(s, u):
    r = s.get(u, headers={"User-Agent": a()})
    r.raise_for_status()

    for p in [
        r'var\s+mwai_nonce\s*=\s*["\']([a-f0-9]+)["\']',
        r'"nonce":"([a-f0-9]+)"',
        r'<meta\s+name=["\']wp-nonce["\']\s+content=["\']([a-f0-9]+)["\']',
        r'<meta\s+name=["\']nonce["\']\s+content=["\']([a-f0-9]+)["\']',
        r'x-wp-nonce:\s*["\']?([a-f0-9]+)["\']?'
    ]:
        m = re.search(p, r.text, re.I)
        if m:
            return m.group(1)


@app.route("/img", methods=["GET", "POST"])
def img():
    prompt = request.args.get("prompt") if request.method == "GET" else (request.json or {}).get("prompt", "human")

    s = requests.Session()
    nonce = n(s, BASE)
    if not nonce:
        return jsonify({"error": "nonce not found"}), 500

    payload = {
        "botId": "AI IMAGE",
        "customId": None,
        "session": "69d532dce3118",
        "chatId": "3tz0gw4axx3",
        "contextId": 766,
        "messages": [
            {
                "id": "ejv7c2t6x2v",
                "role": "assistant",
                "content": "Hello! What image do you want?",
                "who": "AI: "
            }
        ],
        "newMessage": prompt,
        "newFileId": None,
        "newFileIds": None,
        "stream": True
    }

    headers = {
        "User-Agent": a(),
        "Accept": "text/event-stream",
        "Content-Type": "application/json",
        "x-wp-nonce": nonce,
        "origin": BASE,
        "referer": "https://www.free-ai-online.com/free-square-ai-image-generator/"
    }

    r = s.post(
        BASE + "wp-json/mwai-ui/v1/chats/submit",
        data=json.dumps(payload),
        headers=headers,
        stream=True
    )

    image_url = None

    for l in r.iter_lines(decode_unicode=True):
        if l and l.startswith("data:"):
            try:
                d = json.loads(l[6:])

                if d.get("type") == "end":
                    e = json.loads(d.get("data", "{}"))
                    imgs = e.get("images", [])
                    if imgs:
                        image_url = imgs[0]
            except:
                pass

    return jsonify({
        "success": bool(image_url),
        "image_url": image_url
    })


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)