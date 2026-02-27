from flask import Flask
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy

from config import Config
from mindease.time_utils import format_local, local_now


db = SQLAlchemy()
login_manager = LoginManager()


@login_manager.user_loader
def load_user(user_id):
    from mindease.models import User

    return User.query.get(int(user_id))


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)

    login_manager.init_app(app)
    login_manager.login_view = "auth.login"
    login_manager.login_message = "Please log in to continue."
    login_manager.login_message_category = "info"

    from mindease.routes.auth import auth_bp
    from mindease.routes.chat import chat_bp
    from mindease.routes.main import main_bp
    from mindease.routes.mood import mood_bp
    from mindease.routes.pages import pages_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(main_bp)
    app.register_blueprint(chat_bp)
    app.register_blueprint(mood_bp)
    app.register_blueprint(pages_bp)

    @app.context_processor
    def inject_globals():
        return {
            "current_year": local_now().year,
            "format_local_time": format_local,
        }

    with app.app_context():
        db.create_all()

    return app
