import os, uuid, json, qrcode, base64
from flask import Flask, render_template, request, redirect, url_for
from io import BytesIO

app = Flask(__name__)
DB_FILE = "wishes.json"

def load_db():
    if not os.path.exists(DB_FILE):
        return {}
    try:
        with open(DB_FILE, "r") as f:
            return json.load(f)
    except:
        return {}

def save_db(data):
    with open(DB_FILE, "w") as f:
        json.dump(data, f)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/create', methods=['POST'])
def create():
    db = load_db()
    wish_id = str(uuid.uuid4())[:8]
    db[wish_id] = {
        "name": request.form.get("name"),
        "message": request.form.get("message"),
        "theme": request.form.get("theme"),
    }
    save_db(db)
    return redirect(url_for('wish', wish_id=wish_id))

@app.route('/wish/<wish_id>')
def wish(wish_id):
    db = load_db()
    data = db.get(wish_id)
    if not data:
        return "<h1>Link Expired / Galat Link</h1>"

    link = request.url
    qr = qrcode.make(link)
    buffered = BytesIO()
    qr.save(buffered, format="PNG")
    qr_base64 = base64.b64encode(buffered.getvalue()).decode()

    return render_template('wish.html', data=data, qr=qr_base64, link=link)

if __name__ == '__main__':
    if not os.path.exists(DB_FILE):
        save_db({})
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 10000)))
