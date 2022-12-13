from Server import app,db
from datetime import datetime
with app.app_context():
    class User(db.Model):
        user_id = db.Column(db.Integer, primary_key=True)
        name = db.Column(db.String(24), nullable=False)
        last_name = db.Column(db.String(24), nullable=False)
        email = db.Column(db.String(32), nullable=False)
        password = db.Column(db.String(124), nullable=False)
        phone = db.Column(db.String(12), nullable=False)
        created_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
        is_active = db.Column(db.Boolean, nullable=False, default=True)
        role_id = db.Column(db.Integer, db.ForeignKey('role.role_id'), nullable=False)

        def __init__(self, name, last_name, email, password, phone, created_date, is_active, role_id):
            self.name = name
            self.last_name = last_name
            self.email = email
            self.password = password
            self.phone = phone
            self.created_date = created_date
            self.is_active = is_active
            self.role_id = role_id

    db.create_all()
    