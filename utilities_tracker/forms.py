from flask_wtf import FlaskForm 
from wtforms import StringField, TextAreaField, DecimalField, DateField, SubmitField, IntegerField, TimeField, SelectMultipleField, SelectField
from wtforms.validators import DataRequired, Length, Optional, NumberRange

class ServiceForm(FlaskForm):
    """Form for creating or editing a Service.

    Purpose:
        Collects the data required to create or update a Service entity,
        which represents a measurable utility or resource (e.g., "Electricity", "Water").

    Attributes:
        name (StringField):
            Service name (e.g., "Electricity", "Gas", "Water", "Mobile data").
            - Validators: DataRequired(), Length(max=100)

        unit (StringField):
            Unit of measurement (e.g., "kWh", "m³", "GB", "L").
            - Validators: DataRequired(), Length(max=20)

        description (TextAreaField):
            Optional free-text description (up to 250 characters).
            - Validators: Optional(), Length(max=250)

        submit (SubmitField):
            Submit button for saving the form.
            Used by templates to detect which button was pressed when multiple exist.
    """
    name = StringField("Name", validators=[DataRequired(), Length(max=100)])
    unit = StringField("Unit", validators=[DataRequired(), Length(max=20)])
    description = TextAreaField("Description", validators=[Optional(), Length(max=250)])
    submit = SubmitField("Save")

class MeasurementForm(FlaskForm):
    """Form for creating or editing a Measurement.

    Purpose:
        Collects data required to record a measurement (reading) for a specific Service.
        Each measurement corresponds to a dated value (e.g., meter reading for electricity or water).

    Attributes:
        service_id (SelectField):
            The related Service to which this measurement belongs.
            - Examples: "Electricity", "Water", "Gas".
            - Coercion: int (ensures the selected value is converted to integer).
            - Validators: DataRequired()
            - Notes:
                The list of available services must be provided dynamically
                in the Flask route before rendering:
                form.service_id.choices = [(service.id, service.name), ...]

        date (DateField):
            The date of the measurement (YYYY-MM-DD format).
            - Example: 2025-10-05
            - Validators: DataRequired()
            - Notes:
                Represents only the calendar date (without time component).
                Useful for monthly or daily tracking of service usage.

        value (DecimalField):
            Recorded numerical reading for the given date.
            - Example: 1532.75
            - Validators: DataRequired()
            - Notes:
                Stores decimal values to maintain precision (avoids float rounding errors).
                Typically corresponds to the actual meter reading or measured total.

        note (StringField):
            Optional short comment for the measurement.
            - Examples: "Estimated reading", "Manual entry", "Automatic import".
            - Validators: Optional(), Length(max=255)
            - Notes:
                Helps clarify the measurement’s origin or purpose.

        submit (SubmitField):
            Submit button for saving the measurement.
            Used by templates to detect which button was pressed when multiple exist.
    """
    service_id = SelectField("Service", coerce=int, validators=[DataRequired()]) 
    date = DateField("Date", format="%Y-%m-%d", validators=[DataRequired()])
    value = DecimalField("Value", validators=[DataRequired()])
    note = StringField("Note", validators=[Optional(), Length(max=255)])
    submit = SubmitField("Save")

class ReminderTemplateForm(FlaskForm):
    """Form for creating or editing a ReminderTemplate.

    Purpose:
        Defines a recurring reminder configuration for one or more Services.
        Each template specifies when (day/time) reminders should be sent,
        and which services they apply to.

    Attributes:
        day_of_month (IntegerField):
            Day of the month on which the reminder should occur.
            - Range: 1-31
            - Example: 15
            - Validators: DataRequired(), NumberRange(1, 31)
            - Notes:
                For months with fewer than 31 days, handling behavior depends on your
                scheduling logic (e.g., run on the last available day).

        time (TimeField):
            Optional reminder time of day.
            - Examples: 09:00, 18:30
            - Validators: Optional()
            - Notes:
                If omitted, the reminder is considered “all-day” or executed
                according to the system's default time setting.

        note (StringField):
            Optional short note or description for this reminder.
            - Examples: "Submit electricity reading", "Check gas meter".
            - Validators: Optional(), Length(max=255)
            - Notes:
                Helps users understand the purpose of the reminder.

        services (SelectMultipleField):
            List of associated Services for this reminder template.
            - Examples: ["Electricity", "Water"]
            - Coercion: int
            - Validators: Optional()
            - Notes:
                Enables selection of multiple services via a multi-select input.
                Must be populated dynamically in the route:
                form.services.choices = [(service.id, service.name), ...]

        submit (SubmitField):
            Submit button for saving the reminder template.
            Used by templates to confirm submission.
    """
    day_of_month = IntegerField("Day of Month", validators=[DataRequired(), NumberRange(1, 31)])
    time = TimeField("Time", validators=[Optional()])
    note = StringField("Note", validators=[Optional(), Length(max=255)])
    services = SelectMultipleField("Services", coerce=int, validators=[Optional()])
    submit = SubmitField("Save")


class DeleteForm(FlaskForm):
    """A minimal form containing only a CSRF token and a button (optional)."""
    submit = SubmitField("Remove")
