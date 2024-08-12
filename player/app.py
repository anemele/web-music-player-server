import random
from functools import wraps

from flask import Flask, redirect, render_template, send_file

from .jobs import ITEMS, LENGTH

app = Flask(__name__)

app.secret_key = '789hdhfijbjnb4868ghjvh'


def require_login(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        # if session.get('state') != 'login':
        #     return redirect('/login')
        return func(*args, **kwargs)

    return wrapper


@app.route('/')
@require_login
def index():
    return redirect('/music')


@app.get('/music')
@require_login
def get_music_page():
    items = ITEMS.copy()
    random.shuffle(items)
    return render_template('index.html', items=items)


# @app.get('/login')
# def get_login():
#     return render_template('login.html')


# @app.post('/login')
# def post_login():
#     # print(request.form) # POST
#     # print(request.args) # GET

#     if request.form.get('pwd') != PASSWORD:
#         return jsonify(code=1, msg="ERROR_PASSWORD")

#     session['state'] = 'login'
#     return jsonify(code=0)


@app.route('/music/<int:id>')
@require_login
def get_music(id: int):
    if 0 <= id < LENGTH:
        return send_file(ITEMS[id].path)
    return render_template('404.html')


def main():
    app.run(host='0.0.0.0', port=80, debug=True)


if __name__ == '__main__':
    main()
