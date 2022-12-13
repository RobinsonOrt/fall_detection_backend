from Server import app, db

with app.app_context():
    class Role(db.Model):
        role_id = db.Column(db.Integer, primary_key=True)
        role_name = db.Column(db.String(12), nullable=False)
        role_description = db.Column(db.String(32), nullable=False)

        def __init__(self, role_name, role_description):
            self.role_name = role_name
            self.role_description = role_description

    db.create_all()