from flask import Flask, flash
from flask_login import LoginManager
from models import User, SessionLocal, Base, engine

from auth import bp as auth_bp
from main import bp as main_bp

app = Flask(__name__)
app.secret_key = 'segredo123'

login_manager = LoginManager(app)
login_manager.login_view = 'auth.login' 

@login_manager.user_loader
def load_user(user_id):
    with SessionLocal() as session:
        user_data = session.get(User, user_id) 
        if user_data:
            return user_data
        return None

app.register_blueprint(auth_bp)
app.register_blueprint(main_bp)

if __name__ == '__main__':
    Base.metadata.create_all(bind=engine)
    app.run(debug=True)