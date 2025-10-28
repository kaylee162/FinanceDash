from flask import Flask
from dotenv import load_dotenv
import os

from extensions import db, login_manager   # <── use shared instances

def create_app():
    load_dotenv()
    app = Flask(__name__, instance_relative_config=True)

    app.config["SECRET_KEY"] = os.getenv("FLASK_SECRET_KEY", "dev-key")
    app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv(
        "DATABASE_URL", "sqlite:///finance.db"
    )
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    # initialize extensions
    db.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = "auth.login"

    # import models AFTER db.init_app
    from models import User, Transaction, load_user
    login_manager.user_loader(load_user)

    with app.app_context():
        from models import User, Transaction
        from models_budget import Budget 
        db.create_all()

    # register blueprints
    from routes_auth import auth_bp
    from routes_transactions import txn_bp
    from routes_dashboard import dash_bp
    app.register_blueprint(auth_bp)
    app.register_blueprint(txn_bp)
    app.register_blueprint(dash_bp)

    return app


if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)
