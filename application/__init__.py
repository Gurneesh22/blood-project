from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager

app = Flask(__name__, static_folder='static')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SECRET_KEY'] = 'a2b3c4d5e6f7g8h9i0j1k2l3m4n5o6p7y'
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = "login_page"
login_manager.login_message_category = "info"

@login_manager.user_loader
def load_user(user_id):
    from application.models import User 
    return User.query.get(int(user_id))

from application import routes
from application.models import User, Item

# Create all database tables
with app.app_context():
    db.drop_all()  # This will drop all existing tables
    db.create_all()  # This will create new tables with the updated schema