from flask import Flask, render_template, url_for


app = Flask(__name__)


@app.route('/')
@app.route('/index')
def index():
    param = {}
    param['title'] = 'Домашняя страница'
    return render_template('base.html', **param)


@app.route('/training/<prof>')
def training(prof):
    param = {}
    param['prof'] = prof
    param['spaceship_1'] = f"src={url_for('static', filename='img/spaceship_1.jpg')}"
    param['spaceship_2'] = f"src={url_for('static', filename='img/spaceship_2.jpg')}"
    return render_template('index.html', **param)


if __name__ == '__main__':
    app.run(port=8080, host='127.0.0.1')
