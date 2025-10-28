from extensions import db
from flask_login import current_user

class Budget(db.Model):
    __tablename__ = "budgets"  # optional but good practice for clarity
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    category = db.Column(db.String(50), nullable=False)
    limit = db.Column(db.Float, nullable=False, default=200)

    def __repr__(self):
        return f"<Budget {self.category}: ${self.limit}>"
