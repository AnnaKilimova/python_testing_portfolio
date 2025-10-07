from __future__ import annotations
import pytest
from flask import Flask
from sqlalchemy.orm import Session
from ..app import create_app, db

@pytest.fixture
def app():
    """Creates a Flask application with an in-memory database for testing.

    Purpose:
        Provides a reusable application fixture that sets up and tears down
        the testing environment, including the database. When a test function
        declares `def test_x(app):`, pytest automatically discovers this fixture
        by name and injects the returned Flask app instance into the test.

    Behavior:
        - Calls `create_app()` (defined in app.py) to create a new Flask application.
        - Updates its configuration for testing using `app.config.update()`:
            * TESTING = True  
              Enables Flask's testing mode, providing better error handling and isolation.
            * SQLALCHEMY_DATABASE_URI = "sqlite:///:memory:"  
              Uses an in-memory SQLite database that exists only for the lifetime
              of the test session.
            * WTF_CSRF_ENABLED = False  
              Disables CSRF protection so that test POST requests don’t require
              a CSRF token.
        - Pushes an application context to make the app and database accessible.
        - Calls `db.create_all()` to create all database tables defined in the models.

    Yield behavior:
        The fixture uses `yield app` instead of `return app`:
            - `yield` allows pytest to resume the function *after* the test finishes,
              ensuring cleanup is always executed.
            - Everything before `yield` runs as setup; everything after runs as teardown.

    Teardown (executed after all dependent tests complete):
        - `db.session.remove()` clears the current SQLAlchemy session to release resources.
        - `db.drop_all()` removes all database tables from the in-memory database.

    Notes:
        - Using `sqlite:///:memory:` ensures each test suite runs in complete isolation.
        - This fixture is designed for functional and integration tests that require
          a temporary database without persisting data to disk.
    
    Returns:
        Flask: A fully configured Flask application instance ready for testing.
    """
    app = create_app()
    app.config.update({
        "TESTING": True,
        "SQLALCHEMY_DATABASE_URI": "sqlite:///:memory",
        "WTF_CSRF_ENABLED": False,
    })
    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()

@pytest.fixture
def client(app):
    """Provides a Flask test client for simulating HTTP requests.

    Purpose:
        Creates a reusable pytest fixture that returns a Flask test client
        configured to work with the testing application instance created by
        the `app` fixture. This allows tests to perform HTTP requests
        (GET, POST, etc.) without running a live server.

    Behavior:
        - Depends on the `app` fixture, ensuring that the Flask application
          and its testing context are properly initialized.
        - Calls `app.test_client()` to create a lightweight client that can
          send simulated HTTP requests to the Flask application.
        - All requests made through this client share the same application
          context, enabling access to app-specific resources such as
          database sessions, routes, and configuration.

    Notes:
        - The client simulates a browser without requiring an actual HTTP
          server or network communication.
        - Can be used in tests by including `client` as a function argument:
            def test_example(client):
                response = client.get("/")
                assert response.status_code == 200
        - Works seamlessly with other fixtures such as `session`.

    Args:
        app (Flask): The Flask application instance provided by the `app` fixture.

    Returns:
        FlaskClient: A Flask test client instance used to simulate HTTP requests.
    """
    return app.test_client()

@pytest.fixture
def session(app: Flask) -> Session:
    """Provides a SQLAlchemy session bound to the testing database.

    Purpose:
        Returns the active SQLAlchemy session so that tests can interact with
        the database directly (e.g., inserting, querying, or deleting data).

    Behavior:
        - Depends on the `app` fixture to ensure the Flask app and in-memory
          database are initialized first.
        - Returns `db.session`, which is automatically scoped to the current
          app context created by the `app` fixture.

    Notes:
        - Any database operations performed in tests using this fixture
          will be rolled back when the `app` fixture's teardown executes.
    Returns:
        Session: The active SQLAlchemy session bound to the testing database.
    """
    return db.session

