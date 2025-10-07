from datetime import date, time
from decimal import Decimal
from ..forms import ServiceForm, MeasurementForm, ReminderTemplateForm

def test_service_form_valid(app):
    """Verify that ServiceForm validates correctly with valid data.

    Purpose:
        Ensures that the ServiceForm passes validation when all required fields
        are filled with valid data.

    Test logic:
        - Create a ServiceForm instance with valid name, unit, and description.
        - Validate the form within the Flask application context.

    Args:
        app (Flask): The Flask application instance for testing context.

    Assertions:
        - The form passes validation successfully.
    """
    with app.app_context():
        form = ServiceForm(name="Electricity", unit="kWh", description="Power usage")
        assert form.validate()


def test_service_form_missing_name(app):
    """Verify that ServiceForm validation fails when 'name' is missing.

    Purpose:
        Ensures that the 'name' field is required and that appropriate
        validation errors are triggered if omitted.

    Test logic:
        - Create a ServiceForm without a name.
        - Validate and check that the expected error message appears.

    Args:
        app (Flask): The Flask application instance for testing context.

    Assertions:
        - Form validation fails.
        - The 'name' field contains a 'This field is required.' error.
    """
    with app.app_context():
        form = ServiceForm(name="", unit="m³")
        assert not form.validate()
        assert "This field is required." in form.name.errors[0]


def test_measurement_form_valid(app):
    """Verify that MeasurementForm validates correctly with valid data.

    Purpose:
        Confirms that the form accepts valid values for service, date, and value
        fields, and that manual assignment of service choices works as expected.

    Test logic:
        - Create a MeasurementForm with valid field values.
        - Set the service choices manually to mimic database behavior.
        - Validate the form.

    Args:
        app (Flask): The Flask application instance for testing context.

    Assertions:
        - The form passes validation successfully.
    """
    with app.app_context():
        form = MeasurementForm(
            service_id=1,
            date=date(2025, 1, 1),
            value=Decimal("123.45"),
            note="Test note"
        )
        form.service_id.choices = [(1, "Electricity")]
        
        assert form.validate()


def test_reminder_template_form_valid(app):
    """Verify that ReminderTemplateForm validates correctly with valid input.

    Purpose:
        Ensures that a ReminderTemplateForm instance with valid day, time,
        and note passes validation.

    Test logic:
        - Create a ReminderTemplateForm with valid data.
        - Validate the form.

    Args:
        app (Flask): The Flask application instance for testing context.

    Assertions:
        - The form passes validation successfully.
    """
    with app.app_context():
        form = ReminderTemplateForm(
            day_of_month=15,
            time=time(8, 30),
            note="Reminder test"
        )
        assert form.validate()


def test_reminder_template_form_invalid_day(app):
    """Verify that ReminderTemplateForm validation fails for invalid day values.

    Purpose:
        Ensures that the 'day_of_month' field enforces its range constraint
        (1 through 31) and triggers validation errors otherwise.

    Test logic:
        - Create a form with day_of_month outside the valid range.
        - Validate the form.

    Args:
        app (Flask): The Flask application instance for testing context.

    Assertions:
        - The form fails validation due to invalid day value.
    """
    with app.app_context():
        form = ReminderTemplateForm(day_of_month=50)
        assert not form.validate()
