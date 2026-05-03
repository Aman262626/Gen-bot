from flask import Flask, request, jsonify

from image_gen import generate_image

app = Flask(__name__)


@app.route("/img", methods=["GET", "POST"])
def img():
    if request.method == "GET":
        prompt = request.args.get("prompt", "human")
    else:
        prompt = (request.json or {}).get("prompt", "human")

    result = generate_image(prompt)

    return jsonify(result)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
