import os

from flask import Flask, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
# init SQLAlchemy so we can use it later in our models
db = SQLAlchemy()

def create_app():


    app = Flask(__name__)
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass
    app.config['SECRET_KEY'] = '9OLWxND4o83j4K4iuopO'
    app.config.from_mapping(
        DATABASE=os.path.join(app.instance_path, 'tourdeflask.sqlite'),
    )
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///denik.db'    
    app.config['UPLOAD_FOLDER'] = os.path.abspath("app/static/backups/") #useless command (no impact on code)
    db.init_app(app)

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)


    from .models import User
    @login_manager.user_loader
    def load_user(user_id):
        # since the user_id is just the primary key of our user table, use it in the query for the user
        return User.query.get(int(user_id))

    # blueprint for api parts of app
    from .api import api as api_blueprint
    app.register_blueprint(api_blueprint)
    # blueprint for auth routes in our app
    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint)    
    # blueprint for data managing parts of app
    from .data_manage import data as data_blueprint
    app.register_blueprint(data_blueprint)
    # blueprint for non-auth parts of app
    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)



    @login_manager.unauthorized_handler
    def unauthorized_handler():
        flash('Pro tuto akci se musíte přihlásit','error')
        return redirect(url_for('auth.login'))
    return app

# ensure the instance folder exists
if __name__ == '__main__':
    create_app().run(debug=True)