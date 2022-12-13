from Server import app,db
from datetime import datetime

with app.app_context():
    class Employee(db.Model):
        employee_id = db.Column(db.Integer, primary_key=True)
        name = db.Column(db.String(24), nullable=False)
        last_name = db.Column(db.String(24), nullable=False)
        email = db.Column(db.String(32), nullable=False)
        phone = db.Column(db.String(12), nullable=False)
        created_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
        is_active = db.Column(db.Boolean, nullable=False, default=True)
        user_id = db.Column(db.Integer, db.ForeignKey('user.user_id'), nullable=False)

        def __init__(self, name, last_name, email, phone, created_date, is_active, user_id):
            self.name = name
            self.last_name = last_name
            self.email = email
            self.phone = phone
            self.created_date = created_date
            self.is_active = is_active
            self.user_id = user_id

    db.create_all()