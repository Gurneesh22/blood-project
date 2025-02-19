from application import db, bcrypt
from flask_login import UserMixin

class User(db.Model, UserMixin):
    id = db.Column(db.Integer(), primary_key=True)
    email_address = db.Column(db.String(length=50), unique=True, nullable=False)
    password_hash = db.Column(db.String(length=62), nullable=False)
    dob = db.Column(db.Date, nullable=False)
    blood_group = db.Column(db.String(length=3), nullable=False)
    city = db.Column(db.String(length=50), nullable=False)
    gender = db.Column(db.String(length=10), nullable=False)
    contact_number = db.Column(db.String(length=10), nullable=False)
    is_active_donor = db.Column(db.Boolean, default=False, nullable=False)
    last_donation_date = db.Column(db.Date, nullable=True)
    
    def set_password(self, plain_text_password):
        self.password_hash = bcrypt.generate_password_hash(plain_text_password).decode('utf-8')

    def check_password(self, attempted_password):
        return bcrypt.check_password_hash(self.password_hash, attempted_password)

    def __repr__(self):
        return f'User {self.email_address}'

class Item(db.Model):  # Blueprint class for an object
    id = db.Column(db.Integer(), primary_key=True)  # Primary key
    name = db.Column(db.String(length=30), unique=True, nullable=False)
    price = db.Column(db.Integer())
    barcode = db.Column(db.String(length=12), unique=True, nullable=False)
    description = db.Column(db.String(length=1024), nullable=False)
    owner = db.Column(db.Integer(), db.ForeignKey('user.id'))

    def __repr__(self):
        return f'Item {self.name}'