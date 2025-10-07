from flask import Flask
from .db_config import db
from .routes import bp as routes_bp
from flask_wtf.csrf import CSRFProtect


def create_app():
    """Application factory for creating and configuring the Flask app instance.

    Purpose:
        Implements the Flask Application Factory pattern.
        This function creates, configures, and returns a Flask application instance.
        It centralizes initialization of configuration, extensions, and blueprints,
        allowing the app to be created dynamically (e.g., for production, testing, or CLI).

    Behavior and configuration:
        - Creates a new Flask application object.
        - Applies configuration settings (secret key, database URI, SQLAlchemy options).
        - Initializes required Flask extensions (SQLAlchemy, CSRF protection).
        - Registers blueprints that define the app’s routes and views.
        - Optionally creates all database tables if they do not exist (for development/testing).

    Configuration:
        SECRET_KEY:
            - Used for securely signing the session cookie and CSRF tokens.
            - In production, this key should be stored securely (e.g., environment variable).

        SQLALCHEMY_DATABASE_URI:
            - SQLite database file: "services.db" in the project root.
            - For production, replace with a robust DB backend (PostgreSQL, MySQL, etc.).

        SQLALCHEMY_TRACK_MODIFICATIONS:
            - Disabled (False) to reduce overhead and suppress warnings.

    Extensions:
        db (SQLAlchemy):
            - Handles ORM mapping, model management, and database sessions.
            - Initialized via db.init_app(app).

        CSRFProtect (Flask-WTF):
            - Enables CSRF protection for all forms and POST routes.
            - Requires the SECRET_KEY to generate secure tokens.

    Blueprints:
        routes_bp:
            - Blueprint containing all app routes, views, and templates.
            - Registered with `app.register_blueprint(routes_bp)`.

    Development behavior:
        - Within an app context, creates all defined database tables using `db.create_all()`.
        - This is useful for local development and testing, but not recommended for production
          (migrations should be used instead, e.g., Flask-Migrate).

    Returns:
        Flask:
            A fully initialized Flask application instance ready to be run or imported elsewhere.

    Example:
        >>> from app import create_app
        >>> app = create_app()
        >>> app.run(debug=True)
    """
    app = Flask(__name__)

    # === Config ===
    app.config["SECRET_KEY"] = "the-secret-key"
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///services.db"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    # === Extensions ===
    db.init_app(app)
    CSRFProtect(app)

    # === Blueprints ===
    app.register_blueprint(routes_bp)

    # === Create tables (only for dev/testing) ===
    with app.app_context():
        db.create_all()

    return app


if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)
