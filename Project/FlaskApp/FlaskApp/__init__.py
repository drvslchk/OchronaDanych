from main import main as main_blueprint
from auth import auth as auth_blueprint
from flask import Flask
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from database import db, User, fillDefault
from config import Config

# inicjalizacja

app = Flask(__name__)

app.config['SECRET_KEY'] = Config.SECRET_KEY
app.config['SQLALCHEMY_DATABASE_URI'] = Config.SQLALCHEMY_DATABASE_URL


# Tworzenie bazy danych
db.init_app(app)
with app.app_context():
    db.drop_all()
    db.create_all()
    db.session.commit()
    fillDefault()

# Ścieżki związane z autoryzacją
app.register_blueprint(auth_blueprint)
#mail = Mail(app)

# Ścieżki ogólne
app.register_blueprint(main_blueprint)

# manager logowań
login_manager = LoginManager()
login_manager.login_view = 'auth.login'
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


if __name__ == "__main__":
    app.run(ssl_context=(
        'certs/cert.pem', 'certs/key.pem'))
