import os

from flask import Flask, render_template, url_for
from . import db

app = Flask(__name__)

app.config.from_mapping(
    DATABASE=os.path.join(app.instance_path, 'tourdeflask.sqlite'),
)

# ensure the instance folder exists
try:
    os.makedirs(app.instance_path)
except OSError:
    pass

db.init_app(app)


@app.route('/')
def main():  # put application's code here
    return render_template('index.html')


if __name__ == '__main__':
    app.run(debug=true)
