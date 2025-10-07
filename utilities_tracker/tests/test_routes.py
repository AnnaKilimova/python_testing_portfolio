from ..models import Service, Measurement
from datetime import date
from decimal import Decimal

def test_index_page(client):
    """Verify that the index page loads successfully.

    Purpose:
        Ensures that the root route ("/") is accessible and displays
        the list of available services.

    Test logic:
        - Send a GET request to the index route.
        - Check that the page loads and contains expected content.

    Args:
        client (FlaskClient): The Flask test client for simulating HTTP requests.

    Assertions:
        - HTTP response status code is 200 (OK).
        - The word "Services" appears in the HTML response.
    """
    response = client.get("/")
    assert response.status_code == 200
    assert b"Services" in response.data


def test_add_service(client, session):
    """Verify that a new service can be added via POST request.

    Purpose:
        Ensures that submitting the add service form correctly creates a new
        Service record and returns a success message.

    Test logic:
        - Send a POST request to /add_service with valid form data.
        - Follow redirects to the confirmation page.
        - Verify response content and database changes.

    Args:
        client (FlaskClient): The Flask test client.
        session (Session): The SQLAlchemy testing session.

    Assertions:
        - Response status is 200.
        - Success message and service name appear in the HTML.
        - A new Service record is created in the database.
    """
    response = client.post("/add_service", data={
        "name": "Gas",
        "unit": "m³",
        "description": "Natural gas",
        "submit": True
    }, follow_redirects=True)

    assert response.status_code == 200
    html = response.data.decode("utf-8")
    assert "Service" in html
    assert "Gas" in html
    assert "added successfully" in html

    s = Service.query.first()
    assert s.name == "Gas"


def test_service_detail_page(client, session):
    """Verify that the service detail page displays correctly.

    Purpose:
        Ensures that the detail view for an existing service can be accessed
        and renders the correct service information.

    Test logic:
        - Create a Service instance and commit it to the database.
        - Request its detail page via /service/<id>.
        - Verify the page loads and includes the service name.

    Args:
        client (FlaskClient): The Flask test client.
        session (Session): The SQLAlchemy testing session.

    Assertions:
        - Response status code is 200.
        - Service name is present in the response content.
    """
    s = Service(name="Water", unit="L")
    session.add(s)
    session.commit()

    response = client.get(f"/service/{s.id}")
    assert response.status_code == 200
    assert bytes(s.name, "utf-8") in response.data


def test_add_measurement(client, session):
    """Verify that a new measurement can be added via POST request.

    Purpose:
        Ensures that submitting the measurement form successfully creates
        a Measurement record and returns a success message.

    Test logic:
        - Create a Service.
        - Send a POST request to /add_measurement with valid data.
        - Follow redirects and check that the record appears in the database.

    Args:
        client (FlaskClient): The Flask test client.
        session (Session): The SQLAlchemy testing session.

    Assertions:
        - Response status is 200.
        - Success message appears in the response.
        - The new Measurement record is stored with correct value.
    """
    s = Service(name="Electricity", unit="kWh")
    session.add(s)
    session.commit()

    response = client.post("/add_measurement", data={
        "service_id": s.id,
        "date": "2025-10-01",
        "value": "123.45",
        "note": "First test reading",
        "submit": True
    }, follow_redirects=True)

    assert response.status_code == 200
    assert b"Measurement added successfully" in response.data

    m = Measurement.query.first()
    assert m.value == Decimal("123.45")


def test_delete_service(client, session):
    """Verify that deleting a service also removes related measurements.

    Purpose:
        Ensures that deleting a Service triggers cascade deletion of
        all associated Measurement records.

    Test logic:
        - Create a Service and related Measurement.
        - Send a POST request to /delete_service/<id>.
        - Verify that both the service and its measurements are deleted.

    Args:
        client (FlaskClient): The Flask test client.
        session (Session): The SQLAlchemy testing session.

    Assertions:
        - Response contains a success message.
        - Both Service and Measurement tables are empty after deletion.
    """
    s = Service(name="Test delete", unit="L")
    m = Measurement(service=s, date=date(2025, 1, 1), value=Decimal("10"))
    session.add_all([s, m])
    session.commit()

    response = client.post(f"/delete_service/{s.id}", data={"submit": True}, follow_redirects=True)
    assert b"deleted successfully" in response.data
    assert Service.query.count() == 0
    assert Measurement.query.count() == 0
