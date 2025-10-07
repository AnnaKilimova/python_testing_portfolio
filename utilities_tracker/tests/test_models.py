from ..models import Service, Measurement, ReminderTemplate
from datetime import date, time
from decimal import Decimal
from sqlalchemy.orm import Session

def test_create_service(session: Session):
    """Verify that a Service object can be created and persisted to the database.

    Purpose:
        Ensures that a new Service entity is correctly saved in the database
        with all its core attributes: name, unit, and description.

    Test logic:
        - Create a new Service instance.
        - Add it to the session and commit.
        - Retrieve the first record from the database and verify its fields.

    Args:
        session (Session): Active SQLAlchemy session bound to the testing database.

    Assertions:
        - The retrieved Service has the same name, unit, and description as provided.
    """
    service = Service(name="Water", unit="m³", description="Tap water")
    session.add(service)
    session.commit()

    s = Service.query.first()
    assert s.name == "Water"
    assert s.unit == "m³"
    assert s.description == "Tap water"

def test_add_measurements(session):
    """Verify that measurements are correctly added and sorted by date (descending).

    Purpose:
        Tests the one-to-many relationship between Service and Measurement,
        ensuring that:
        - multiple measurements can be attached to a single service;
        - the relationship returns them sorted by date descending (latest first).

    Test logic:
        - Create a Service.
        - Add two Measurement objects with different dates.
        - Commit and verify the ordering of the related measurements.

    Args:
        session (Session): Active SQLAlchemy session bound to the testing database.

    Assertions:
        - The service has exactly two measurements.
        - The first measurement (index 0) corresponds to the latest date.
    """
    service = Service(name="Electricity", unit="kWh")
    session.add(service)
    session.commit()

    m1 = Measurement(service_id=service.id, date=date(2025, 1, 1), value=Decimal("100.0"))
    m2 = Measurement(service_id=service.id, date=date(2025, 2, 1), value=Decimal("120.0"))
    session.add_all([m1, m2])
    session.commit()

    assert len(service.measurements) == 2
    assert service.measurements[0].date == date(2025, 2, 1)

def test_consumption_for_month(session):
    """Verify the correctness of Service.consumption_for_month() calculation.

    Purpose:
        Tests that the total consumption for a specific month is computed correctly
        based on the differences between consecutive measurements within that month.

    Test logic:
        - Create a Service with three measurements.
        - Two of them belong to February 2025, one to January.
        - The method should sum only February differences.

    Args:
        session (Session): Active SQLAlchemy session bound to the testing database.

    Assertions:
        - The computed total consumption equals the expected difference sum.
    """
    service = Service(name="Gas", unit="m³")
    session.add(service)
    session.commit()

    session.add_all([
        Measurement(service_id=service.id, date=date(2025, 1, 1), value=Decimal("10.0")),
        Measurement(service_id=service.id, date=date(2025, 2, 1), value=Decimal("15.0")),
        Measurement(service_id=service.id, date=date(2025, 2, 28), value=Decimal("18.0")),
    ])
    session.commit()

    result = service.consumption_for_month(2025, 2)
    assert result == Decimal("8.0") # (15 - 10) + (18 - 15)

def test_service_with_reminders(session):
    """Verify the many-to-many relationship between Service and ReminderTemplate.

    Purpose:
        Ensures that reminders can be associated with one or more services
        and that this bidirectional relationship works both ways.

    Test logic:
        - Create a Service and a ReminderTemplate.
        - Link them through the many-to-many relationship.
        - Commit and verify that each side correctly references the other.

    Args:
        session (Session): Active SQLAlchemy session bound to the testing database.

    Assertions:
        - The Service has the ReminderTemplate in its reminders list.
        - The ReminderTemplate has the Service in its services list.
    """
    service = Service(name="Heating", unit="Gcal")
    reminder = ReminderTemplate(day_of_month=5, time=time(8, 0), note="Check boiler")
    reminder.services.append(service)

    session.add_all([service, reminder])
    session.commit()

    s = Service.query.first()
    r = ReminderTemplate.query.first()

    assert s.reminders[0].note == "Check boiler"
    assert r.services[0].name == "Heating"

def test_consumption_from_previous(session):
    """Verify Measurement.consumption_from_previous property behavior.

    Purpose:
        Ensures that the property correctly computes the difference in measurement
        values between the current record and the previous one for the same service.

    Test logic:
        - Create two measurements for the same service.
        - The first measurement has no previous value, so the property should return None.
        - The second measurement should correctly compute the difference.

    Args:
        session (Session): Active SQLAlchemy session bound to the testing database.

    Assertions:
        - The second measurement returns the correct difference (Decimal("15.0")).
        - The first measurement returns None.
    """
    service = Service(name="Water", unit="m³")
    session.add(service)
    session.commit()

    m1 = Measurement(service_id=service.id, date=date(2025, 1, 1), value=Decimal("50.0"))
    m2 = Measurement(service_id=service.id, date=date(2025, 1, 15), value=Decimal("65.0"))
    session.add_all([m1, m2])
    session.commit()

    assert m2.consumption_from_previous == Decimal("15.0")
    assert m1.consumption_from_previous is None  # no previous measurement

def test_cascade_delete_measurements(session):
    """Verify that deleting a Service cascades deletion of its Measurements.

    Purpose:
        Ensures that the 'cascade="all, delete-orphan"' configuration
        in the Service.measurements relationship behaves correctly.

    Test logic:
        - Create a Service with two Measurements.
        - Delete the Service.
        - Confirm that related Measurements are also removed automatically.

    Args:
        session (Session): Active SQLAlchemy session bound to the testing database.

    Assertions:
        - Initially, there are two measurements in the database.
        - After deleting the Service, both the Service and its Measurements are gone.
    """
    service = Service(name="Electricity", unit="kWh")
    session.add(service)
    session.commit()

    m1 = Measurement(service_id=service.id, date=date(2025, 1, 1), value=Decimal("100"))
    m2 = Measurement(service_id=service.id, date=date(2025, 2, 1), value=Decimal("200"))
    session.add_all([m1, m2])
    session.commit()

    assert Measurement.query.count() == 2

    session.delete(service)
    session.commit()

    assert Service.query.count() == 0
    assert Measurement.query.count() == 0 





