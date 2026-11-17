from flask import Flask, render_template, request

import base64, json, re
from openai import OpenAI

client = OpenAI(base_url="https://krchoi.com/gemma4/v1", api_key="none")

def ask(prompt, image_bytes=None, mime="image/jpeg"):
    content = [{"type": "text", "text": prompt}]
    if image_bytes:
        url = f"data:{mime};base64," + base64.b64encode(image_bytes).decode()
        content.append({"type": "image_url", "image_url": {"url": url}})
    r = client.chat.completions.create(model="gemma4", messages=[{"role": "user", "content": content}])
    return r.choices[0].message.content

def parse_json(text):
    m = re.search(r"```(?:json)?\s*(.*?)```", text, re.S)
    try:
        return json.loads(m.group(1) if m else text)
    except (json.JSONDecodeError, TypeError):
        return None


app = Flask(__name__)
app.config["MAX_CONTENT_LENGTH"] = 20 * 1024 * 1024  # 사진은 20MB까지

RECEIPT_PROMPT = """이 사진은 영수증이다. 산 항목의 이름과 금액을 읽어라.
다음 JSON으로만 답하고 다른 말은 쓰지 마라.
{"items": [{"name": "항목 이름", "price": 12000}]}
price는 원 단위 정수로, 쉼표와 '원'을 빼고 적는다. 합계·부가세·거스름돈 줄은 항목에 넣지 않는다.
영수증이 아니거나 글자를 읽을 수 없으면 {"items": []} 로 답한다."""


def to_int(value):
    """'17,000원' 같은 글자를 17000으로 바꾼다. 숫자가 없으면 None."""
    digits = re.sub(r"[^\d]", "", str(value or ""))
    return int(digits) if digits else None


def split(total, people):
    """나눠 낼 금액을 계산해 화면에 줄 dict를 만든다."""
    each, rest = divmod(total, people)
    return {"total": total, "people": people, "each": each, "rest": rest}


def read_people(form):
    people = to_int(form.get("people"))
    if not people:
        return None, "인원수를 1 이상으로 넣어 주세요."
    return people, None


@app.route("/", methods=["GET", "POST"])
def index():
    ctx = {"form": request.form, "items": None, "result": None, "error": None}
    if request.method == "GET":
        return render_template("index.html", **ctx)

    mode = request.form.get("mode", "calc")
    people, error = read_people(request.form)

    if mode == "calc":
        amount = to_int(request.form.get("amount"))
        if not amount:
            error = error or "금액을 넣어 주세요."
        if not error:
            ctx["result"] = split(amount, people)

    elif mode == "receipt":
        photo = request.files.get("photo")
        if not photo or not photo.filename:
            error = "영수증 사진을 골라 주세요."
        else:
            try:
                answer = ask(RECEIPT_PROMPT, photo.read(), photo.mimetype or "image/jpeg")
            except Exception as e:
                answer = None
                error = f"AI 서버에 연결하지 못했습니다. ({type(e).__name__})"
            if answer is not None:
                data = parse_json(answer)
                items = []
                if isinstance(data, dict) and isinstance(data.get("items"), list):
                    for it in data["items"]:
                        if isinstance(it, dict):
                            price = to_int(it.get("price"))
                            if price:
                                items.append({"name": str(it.get("name", "")).strip() or "항목", "price": price})
                if not items:
                    error = "읽지 못했습니다. 영수증이 잘 보이게 다시 찍어 주세요."
                else:
                    ctx["items"] = items
                    # 인원수가 없으면 목록만 보여 주고, 인원수 안내(error)는 그대로 띄운다
                    if people:
                        ctx["result"] = split(sum(i["price"] for i in items), people)

    elif mode == "items":
        # 읽은 목록을 사람이 고친 뒤 다시 계산한다
        names = request.form.getlist("name")
        prices = request.form.getlist("price")
        items = []
        for name, price in zip(names, prices):
            p = to_int(price)
            if p:
                items.append({"name": name.strip() or "항목", "price": p})
        ctx["items"] = items
        if not items:
            error = error or "금액이 있는 항목이 없습니다."
        elif people:
            ctx["result"] = split(sum(i["price"] for i in items), people)

    ctx["error"] = error
    return render_template("index.html", **ctx)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
