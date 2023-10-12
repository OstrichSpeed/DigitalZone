from flask import Flask
from datetime import datetime
from flask import render_template
from flask import request

app = Flask(__name__)

@app.route("/")
def index():
    now = datetime.now()
    user = {'username': 'Евгений'}
    if now.hour > 5 and now.hour < 12:
        time_of_day = "morning"
    elif now.hour >= 12 and now.hour < 17:
        time_of_day = "day"
    elif now.hour >= 17 and now.hour < 23:
        time_of_day = "evening"
    items = ["один", "два", "три", "четыре", "пять"]

    return render_template('index.html',
    title='Home',
    user=user,
    time_of_day=time_of_day,
    items=items)

# http://127.0.0.1:5000/simple?a=5&some=10&b=hello
# https://yandex.ru/search/?lr=5&clid=2270456&win=536&text=asdf
@app.route("/simple")
def simple():
    a = request.args.get("a", default=0, type=float)
    b = request.args.get("b",default=0, type = float)
    return f"<h1>{a}+{b}={a+b}</h1>"


@app.route("/hello")
def hello_world():
    now = datetime.now()
    return f"<p>Hello, World! {now}</p>"

@app.route("/styled")
def hello_styles():
    now = datetime.now()
    return f"""
    <h1>Заголовок</h1>
    <p>Hello, World!</p>
    <p>Текущее время {now}</p>
    """