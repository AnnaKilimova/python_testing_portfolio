from flask import Blueprint, render_template, redirect, url_for, flash, request, abort
from datetime import date
from .db_config import db
from .models import Service, Measurement, ReminderTemplate
from .forms import ServiceForm, MeasurementForm, ReminderTemplateForm, DeleteForm

bp = Blueprint("routes", __name__)

@bp.route("/")
def index() -> str:
    """Render and return the application's home page (root path "/").

    Summary:
      This view function retrieves the list of all services and the reminder
      templates that match today's day-of-month, then renders the "index.html"
      template with this data. The page is intended to be a lightweight
      dashboard: a service index plus any reminders that are due today.

    Behavior and Database Access:
      - The function executes two read-only ORM queries:
          1. Query all Service rows ordered by Service.name.
          2. Query ReminderTemplate rows filtered by day_of_month == today.day.
      - No database write operations occur in this view.
      - Queries are executed when .all() is called; until then they are ORM query objects.

    Return: str.
      The HTML string returned by Flask's render_template. In Flask this
      string is used as the response body for the HTTP response.

    Local variables (types and intent):
      - services (List[Service]):
          A list of Service model instances (SQLAlchemy objects) loaded from the
          database. Each Service instance provides attributes such as `name`,
          `unit`, and relationships like `measurements`. The index template should
          iterate this list to present a concise summary of known services.
      - today (datetime.date):
          The current calendar date (year, month, day) obtained via date.today().
          Used both for display and for selecting reminders that match today's date.
      - reminders_today (List[ReminderTemplate]):
          A list of ReminderTemplate model instances whose `day_of_month` equals
          the current day (today.day). These represent recurring reminders that
          are considered active or due on the present date.

    Template contract: 
      Template name: "index.html"

    Context variables passed to the template (names and types):
        - services (List[Service]): iterate to list available services.
        - reminders_today (List[ReminderTemplate]): iterate to list today's reminders.
        - today (datetime.date): display the date in headings or localized text.

    Example (what the template might do):
      The index.html template can iterate `services` and render each service's
      name and unit, link to a service detail page, show a quick last-reading,
      and display `reminders_today` beneath a "Reminders for <date>" heading.
    """
    services = Service.query.order_by(Service.name).all()
    today = date.today()
    reminders_today = ReminderTemplate.query.filter_by(day_of_month=today.day).all()

    return render_template(
        "index.html",
        services = services,
        reminders_today=reminders_today,
        today=today
    )

@bp.route("/service/<int:service_id>")
def service_detail(service_id: int) -> str:
    """Render and return the detailed view page for a single Service record.

    Summary:
      This view function handles GET requests to the route `/service/<service_id>`.
      It retrieves the `Service` model instance corresponding to the provided
      primary key (service_id), loads its associated `Measurement` records via the
      SQLAlchemy relationship `service.measurements`, and renders the
      "service_detail.html" template. The page displays the service's basic
      information and the full history of measurements for that service.

    URL structure: /service/<int:service_id>.
      - <int:service_id> is a dynamic path parameter. Flask's `int` converter
        ensures that only integer values are accepted. These are then
        passed into the function as the parameter `service_id`.

    Parameters: service_id : int.
      Primary key of the `Service` object to retrieve from the database.
      This is provided by the URL segment `<int:service_id>`.

    Database access:
      - A single SELECT query is performed to load the `Service` record with
        the given primary key. `get_or_404(service_id)` returns the object if found,
        otherwise aborts the request with HTTP 404.
      - Accessing `service.measurements` triggers a second SELECT query to
        load all associated `Measurement` records (lazy-loading by default).
        The order of these measurements is determined by the relationship
        configuration in the `Service` model (e.g. `order_by=Measurement.date.desc()`).

    Template:
      Template name: "service_detail.html"
      Context variables passed to the template:
      - service (Service): the retrieved `Service` instance.
      - measurements (List[Measurement]): list of associated measurement records.
      - delete_form (DeleteForm): a Flask-WTF form instance providing a CSRF token
        for secure deletion of individual measurements.

    Return: str.
      The rendered HTML page as a string. Flask uses this as the response
      body for the HTTP 200 OK response.

    Usage notes:
      - Endpoint naming: If the blueprint is called "routes", the endpoint
        for this view is "routes.service_detail". Use `url_for("routes.service_detail", service_id=...)`
        to generate links to this page in templates.
      - If the number of measurements grows large, consider adding pagination
        or limiting the query size to improve performance.
      - If the template iterates over measurements and accesses properties
        that perform further queries (e.g., consumption calculations), this may
        lead to N+1 query patterns. Precomputing such values in the view
        function is recommended for performance-critical use cases.
      - The `delete_form` is intended for embedding in delete buttons/forms next to
        measurements. Each delete submission posts to `routes.delete_measurement`.
    """
    service = Service.query.get_or_404(service_id)
    measurements = service.measurements
    delete_form = DeleteForm()

    return render_template(
        "service_detail.html",
        service=service,
        measurements=measurements,
        delete_form=delete_form
    )

@bp.route("/add_service", methods=["GET", "POST"])
def add_service() -> str:
    """Render and process the "Add Service" form (path: "/add_service").

    Summary:
      This view allows users to create a new `Service` record by filling out a form.
      It supports both HTTP GET (to display the blank form) and HTTP POST (to process
      the submitted data). When the form is successfully validated, the new service
      is inserted into the database and the user is redirected back to the home page.

    HTTP Methods:
      - GET: Render the form so the user can input a new service's data.
      - POST: Validate the submitted data, insert a new `Service` row, flash a success
        message, and redirect to the home page.

    Behavior and Database Access:
      1. A `ServiceForm` instance is created unconditionally at the start.
      2. On POST submission, `form.validate_on_submit()` is called:
        - It returns True only if the request is POST and all field validators pass.
      3. A new `Service` object is created from the cleaned form data:
        - `name`: required string, stripped of surrounding whitespace.
        - `unit`: required string, stripped of whitespace.
        - `description`: optional string; stripped if present, otherwise stored as None.
      4. The object is added to the SQLAlchemy session (`db.session.add`) and then
        persisted to the database with `db.session.commit()`.
      5. A Flask flash message is displayed, and the user is redirected to the
        index page (`url_for("routes.index")`).
      6. If validation fails or the request is GET, the blank or invalid form is
        rendered again.

    Local variables (types and intent):
      - form (ServiceForm):
          An instance of the Flask-WTF form defined in forms.py. It includes fields
          for service name, unit, optional description, and a submit button.
      - new_service (Service):
          A new SQLAlchemy model object representing the row to insert. It's created
          only if validation passes, right before committing.

    Return: str | werkzeug.wrappers.Response
      - On GET or failed validation: an HTML string for the add_service form page.
      - On successful POST: a redirect response to the index page.

    Template contract:
      Template name: "add_service.html"
      Context variables passed to the template:
        - form (ServiceForm): The form object to be rendered in the template,
          typically using Jinja2 macros or manual HTML form rendering.

    Related components:
      - Model: `Service` (models.py)
        Defines the database structure for services with attributes: id, name, unit,
        description, and relationships to `Measurement` and `ReminderTemplate`.
      - Form: `ServiceForm` (forms.py)
        Specifies the expected fields, validators, and labels for user input.
      - Blueprint: "routes"
        This function belongs to the `routes` blueprint. Its endpoint name will be
        "routes.add_service", and it is referenced by `url_for("routes.add_service")`.

    Example user flow:
      1. User visits "/add_service" → sees empty form.
      2. User fills fields and submits.
      3. Data is validated; if valid → new row added, success message shown.
      4. User is redirected to the homepage and sees the new service in the list.
    """
    form = ServiceForm()
    if form.validate_on_submit():
        new_service = Service(
            name=form.name.data.strip(),
            unit=form.unit.data.strip(),
            description=form.description.data.strip() if form.description.data else None
        )
        db.session.add(new_service)
        db.session.commit()
        flash(f"Service '{new_service.name}' added successfully!", "success")
        return redirect(url_for("routes.index"))

    return render_template("add_service.html", form=form)

@bp.route("/edit_service/<int:service_id>", methods=["GET", "POST"])
def edit_service(service_id):
    """Render and process the "Edit Service" form (path: "/edit_service/<id>").

    Summary:
      This view allows users to update an existing `Service` record. The form is
      pre-filled with current service data and saved upon successful submission.

    Behavior:
      - On GET: Render form pre-populated with the service's current details.
      - On POST: Validate form data, update fields, commit changes, flash a
        success message, and redirect to the service detail page.

    Template:
      Template name: "edit_service.html".
      Context variables:
          - form (ServiceForm): Form instance used for editing.
          - service (Service): The service object being edited.

    Return: str | werkzeug.wrappers.Response
      - GET or invalid POST → render edit form.
      - Valid POST → redirect to the updated service detail page.
    """
    service = Service.query.get_or_404(service_id)
    form = ServiceForm(obj=service)  
    if form.validate_on_submit():
        service.name = form.name.data.strip()
        service.unit = form.unit.data.strip()
        service.description = form.description.data.strip() if form.description.data else None
        db.session.commit()
        flash(f"Service '{service.name}' updated successfully!", "success")
        return redirect(url_for("routes.service_detail", service_id=service.id))

    return render_template("edit_service.html", form=form, service=service)

@bp.route("/delete_service/<int:service_id>", methods=["POST"])
def delete_service(service_id):
    """Delete a service and all its related records (path: "/delete_service/<id>", method: POST).

    Summary:
      This view deletes a `Service` record and all its associated measurements and
      reminder links. It is triggered by a POST request for security reasons and
      redirects the user to the index page after deletion.

    Behavior:
      1. Validate CSRF token using `DeleteForm`.
      2. Retrieve the target service by primary key (`service_id`).
      3. Delete the service from the session. Related measurements are automatically
        removed via cascade configuration.
      4. Commit the transaction, flash a success message, and redirect to the home page.

    Return: werkzeug.wrappers.Response
      Redirect to the index page after successful deletion.

    Security:
      - Accepts only POST requests.
      - CSRF protection provided by `DeleteForm`.

    Template usage:
      Typically triggered from `service_detail.html` via:
          <form method="POST" action="{{ url_for('routes.delete_service', service_id=service.id) }}">
              {{ delete_form.csrf_token }}
              <button type="submit">Delete service</button>
          </form>
    """
    service = Service.query.get_or_404(service_id)

    db.session.delete(service)
    db.session.commit()
    flash(f"Service '{service.name}' deleted successfully!", "success")
    return redirect(url_for("routes.index"))

@bp.route("/add_measurement", methods=["GET", "POST"])
def add_measurement():
    """Render and process the "Add Measurement" form (path: "/add_measurement").

    Summary:
      This view function allows users to record a new measurement for a specific
      service. It displays a form with fields for service selection, measurement
      date, numerical value, and an optional note. Upon successful validation,
      the measurement is stored in the database, and the user is redirected back
      to the home page with a success message.

    HTTP Methods:
      - GET: Display the empty form for adding a measurement.
      - POST: Validate the form data and insert a new `Measurement` row into
        the database.

    Behavior and Database Access:
      1. A `MeasurementForm` instance is created at the beginning.
      2. The form's `service_id` field (SelectField) is dynamically populated with
        choices taken from all `Service` records in the database. Each choice is
        a tuple `(id, name)` so that the dropdown displays the service name and
        submits its numeric ID.
      3. On POST submission, `form.validate_on_submit()` is called:
        - Returns True if the request is POST and all fields pass validation.
      4. If validation succeeds:
        - A new `Measurement` object is constructed using the form data:
          * `date` (datetime.date): the measurement date.
          * `value` (Decimal): the numeric reading.
          * `note` (str | None): optional note; may be empty.
          * `service_id` (int): foreign key pointing to the selected service.
        - The object is added to the SQLAlchemy session and committed to the database.
      5. A success flash message is displayed.
      6. The user is redirected to the home page ("/") to avoid duplicate submissions.
      7. If the form is invalid or the request is GET, the form is rendered again.

    Local variables (types and intent):
      - form (MeasurementForm):
          Flask-WTF form instance containing the following fields:
          `service_id` (SelectField), `date` (DateField), `value` (DecimalField),
          `note` (StringField), and a submit button.
      - new_measurement (Measurement):
          A new SQLAlchemy model object created only if the form validates.
          Represents a single row to insert into the `measurement` table.

    Return:
      str | werkzeug.wrappers.Response
          - GET or invalid POST → HTML string for the measurement form page.
          - Valid POST → redirect response to the index page.

    Template contract:
      Template name: "add_measurement.html".
      Context variables:
          - form (MeasurementForm): the form object, used by the template to render
            fields, errors, and submission controls.

    Related components:
      - Model: `Measurement` (models.py)
        Represents a single measurement reading, with a foreign key to `Service`.
        Fields include `id`, `date`, `value`, `note`, and `service_id`.
      - Model: `Service` (models.py)
        Provides the available service list for the dropdown menu.
      - Form: `MeasurementForm` (forms.py)
        Defines fields, types, and validators for measurement input.
      - Blueprint: "routes"
        This route is registered in the `routes` blueprint. Its endpoint name is
        `routes.add_measurement`.

    Example user flow:
      1. User visits "/add_measurement" and sees a form with a dropdown list of services.
      2. User selects a service, chooses a date, enters a numeric value and (optionally) a note.
      3. On submission, the data is validated and stored in the database.
      4. A success message is shown, and the user is redirected to the home page.
    """
    form = MeasurementForm()

    form.service_id.choices = [(s.id, s.name) for s in Service.query.order_by(Service.name).all()]

    if form.validate_on_submit():
        new_measurement = Measurement(
            date=form.date.data,
            value=form.value.data,
            note=form.note.data,
            service_id=form.service_id.data
        )
        db.session.add(new_measurement)
        db.session.commit()
        flash("Measurement added successfully!", "success")
        return redirect(url_for("routes.index"))

    return render_template("add_measurement.html", form=form)

@bp.route("/delete/<int:id>", methods=["POST"])
def delete_measurement(id):
    """Delete a measurement by its ID (path: "/delete/<id>", method: POST).

    Summary:
      This view handles the deletion of a specific `Measurement` record from the
      database. It is designed to be triggered by a POST request (e.g., a form
      submission or an AJAX call) rather than a GET request, in accordance with
      REST principles for destructive operations. After deletion, the user is
      redirected to the corresponding service detail page.

    HTTP Methods:
      - POST: Deletes the specified measurement from the database and redirects.

    Behavior and Database Access:
      1. Validate CSRF token using `DeleteForm.validate_on_submit()`.
        If validation fails, the request aborts with HTTP 400.
      2. Retrieve the target measurement by its primary key `id` using
        `Measurement.query.get_or_404(id)`.  
        - If no measurement with this ID exists, a 404 error is returned.
      3. Delete the retrieved measurement from the SQLAlchemy session.
      4. Commit the transaction to persist the deletion.
      5. Flash an informational message confirming successful deletion.
      6. Redirect the user to the service detail page corresponding to the
        measurement's `service_id`. This ensures the user sees the updated
        measurement list for that service.

    Local variables (types and intent):
      - id (int): The primary key of the `Measurement` to delete.  
        Captured from the URL via Flask's route converter `<int:id>`.
      - measurement (Measurement):
          SQLAlchemy model instance retrieved from the database. If not found,
          a 404 response is automatically raised by `get_or_404()`.

    Return: werkzeug.wrappers.Response.
      A redirect response to the service detail page after successful deletion.

    Related components:
      - Model: `Measurement` (models.py)
        Represents a single measurement. Deletion removes the corresponding row
        from the `measurement` table.
      - Blueprint: "routes"
        This route belongs to the "routes" blueprint. Its endpoint name is
        `routes.delete_measurement`.
      - Redirect target: `routes.service_detail`
        The redirection uses `url_for("routes.service_detail", service_id=...)` to return
        the user to the page for the service that owned the deleted measurement.

    Security and best practices:
      - This route accepts only POST requests to prevent accidental deletions
        via URL visits or search engine crawlers.
      - In templates, the deletion should be triggered using a `<form method="POST">`
        with a CSRF token (provided by Flask-WTF), not a plain hyperlink.

    Example usage:
      In a service detail template, each measurement might have a small "Delete"
      button next to it:
          <form action="{{ url_for('routes.delete_measurement', id=m.id) }}" method="post">
              {{ form.csrf_token }}
              <button type="submit" class="btn btn-danger btn-sm">Delete</button>
          </form>
    """
    form = DeleteForm()
    if not form.validate_on_submit():
        abort(400, description="Bad request: CSRF token missing or invalid.")

    measurement = Measurement.query.get_or_404(id)
    sid = measurement.service_id
    db.session.delete(measurement)
    db.session.commit()
    flash("The meter reading has been deleted.", "info")
    return redirect(url_for("routes.service_detail", service_id=sid))

@bp.route("/reminder_templates", methods=["GET", "POST"])
def reminder_templates():
    """Render and process the Reminder Templates management page
    (path: "/reminder_templates").

    Summary:
      This view allows users to create and manage recurring reminder templates.
      A reminder template defines a day of the month, time of day, an optional
      note, and the list of services to which the reminder applies. The page
      displays both a creation form and a list of all existing templates.

    HTTP Methods:
      - GET: Renders the reminder templates page with an empty form and a list
        of all existing templates.
      - POST: Processes the submitted form to create a new `ReminderTemplate`
        and associate it with the selected services.

    Behavior and Database Access:
      1. A `ReminderTemplateForm` instance is created.
      2. The `services` field (SelectMultipleField) is dynamically populated with
        choices retrieved from the `Service` table, ordered by service name.
        Each choice is a tuple `(id, name)` for proper rendering in a multiselect UI.
      3. If the form is submitted and validated:
        - A new `ReminderTemplate` instance is created with `day_of_month`,
          `time`, and `note` from the form.
        - The selected services are loaded from the database using a filter
          on their IDs (provided by `form.services.data`).
        - These service objects are assigned to the template's `services`
          relationship, establishing many-to-many links.
        - The new template is added to the session and committed.
        - A success flash message is displayed.
        - The user is redirected back to the same page to see the updated list.
      4. For GET requests or invalid submissions:
        - All reminder templates are loaded and displayed in a list.

    Local variables (types and intent):
      - form (ReminderTemplateForm):
          Flask-WTF form instance containing fields:
          - `day_of_month` (IntegerField): day (1-31) on which the reminder repeats.
          - `time` (TimeField): time of day for the reminder.
          - `note` (StringField): optional descriptive note.
          - `services` (SelectMultipleField[int]): IDs of services the reminder applies to.
      - new_template (ReminderTemplate):
          A newly created SQLAlchemy object representing the reminder template.
      - selected_services (List[Service]):
          The Service model instances corresponding to the selected IDs in the form.
          These are assigned to the `services` relationship of the template.
      - reminders (List[ReminderTemplate]):
          All existing reminder templates, loaded to be displayed below the form.

    Return: str | werkzeug.wrappers.Response
      - GET or invalid POST → HTML string of the management page.
      - Valid POST → redirect response to refresh the list after creation.

    Template contract:
      Template name: "reminder_list.html"
      Context variables:
          - form (ReminderTemplateForm): Used to render the creation form.
          - reminders (List[ReminderTemplate]): Displayed as a list/table of existing templates.
      Context variables:
      - form (ReminderTemplateForm): Used to render the creation form.
      - reminders (List[ReminderTemplate]): Displayed as a list/table of existing templates.
      - delete_form (DeleteForm): Provides CSRF protection for delete buttons in the template.

    Related components:
      - Model: `ReminderTemplate` (models.py)
        Represents a recurring reminder pattern. Has fields for day, time, note,
        and a many-to-many relationship with `Service`.
      - Model: `Service` (models.py)
        Provides the available service list to which reminders can be attached.
      - Form: `ReminderTemplateForm` (forms.py)
        Defines validation and fields for creating a new reminder template.
      - Blueprint: "routes"
        This route is part of the "routes" blueprint. Its endpoint name is
        `routes.reminder_templates`.

    Security and best practices:
      - Only POST requests are used for creating new templates to prevent accidental
        submissions via URL.
      - The form should include CSRF protection (provided by Flask-WTF).
      - Displaying existing templates allows the user to see all configured reminders
        at a glance, enabling future editing or deletion features.

    Example usage:
      1. User opens "/reminder_templates" and sees:
        - A form to create a new reminder template.
        - A list of all previously created templates.
      2. User selects one or more services, chooses a day of the month and time,
        enters an optional note, and submits the form.
      3. A new `ReminderTemplate` record is created and linked to the selected
        services.
      4. The page refreshes and displays the new template in the list.

    """
    form = ReminderTemplateForm()

    form.services.choices = [(s.id, s.name) for s in Service.query.order_by(Service.name).all()]

    if form.validate_on_submit():
        new_template = ReminderTemplate(
            day_of_month=form.day_of_month.data,
            time=form.time.data,
            note=form.note.data
        )

        selected_services = Service.query.filter(Service.id.in_(form.services.data)).all()
        new_template.services = selected_services

        db.session.add(new_template)
        db.session.commit()
        flash("Reminder template created!", "success")
        return redirect(url_for("routes.reminder_templates"))

    reminders = ReminderTemplate.query.order_by(ReminderTemplate.day_of_month).all()

    delete_form = DeleteForm()

    return render_template(
        "reminder_list.html",
        form=form,
        reminders=reminders,
        delete_form=delete_form
    )

@bp.route("/edit_reminder/<int:id>", methods=["GET", "POST"])
def edit_reminder(id):
    """Render and process the "Edit Reminder" form (path: "/edit_reminder/<id>").

    Summary:
      This view allows users to edit an existing `ReminderTemplate` record.
      It pre-populates the form with the current reminder values and updates
      them upon valid form submission.

    Behavior:
      - On GET: Renders the edit form populated with the reminder's data.
      - On POST: Validates input, updates the reminder fields and associated
        services, commits the changes, flashes a success message, and redirects
        back to the reminders list.

    Template:
      Template name: "edit_reminder.html".
      Context variables:
          - form (ReminderTemplateForm): Pre-populated form for editing.
          - reminder (ReminderTemplate): The reminder being edited.

    Return: str | werkzeug.wrappers.Response    
      - GET or invalid POST → HTML string with form.
      - Valid POST → redirect to `/reminder_templates`.
    """
    reminder = ReminderTemplate.query.get_or_404(id)
    form = ReminderTemplateForm(obj=reminder)

    form.services.choices = [(s.id, s.name) for s in Service.query.order_by(Service.name).all()]

    if form.validate_on_submit():
        reminder.day_of_month = form.day_of_month.data
        reminder.time = form.time.data
        reminder.note = form.note.data

        selected_services = Service.query.filter(Service.id.in_(form.services.data)).all()
        reminder.services = selected_services

        db.session.commit()
        flash("Reminder updated!", "success")
        return redirect(url_for("routes.reminder_templates"))

    form.services.data = [s.id for s in reminder.services]

    return render_template("edit_reminder.html", form=form, reminder=reminder)

@bp.route("/delete_reminder/<int:id>", methods=["POST"])
def delete_reminder(id):
    """Delete a reminder template by its ID (path: "/delete_reminder/<id>", method: POST).

    Summary:
      This view deletes a `ReminderTemplate` record from the database. It requires
      a POST request with valid CSRF token and redirects to the reminders list
      upon successful deletion.

    Behavior:
      1. Validate CSRF token using `DeleteForm`.
      2. Retrieve the reminder by ID or return 404.
      3. Delete the reminder and commit the transaction.
      4. Flash a confirmation message and redirect back to the reminders list.

    Return: werkzeug.wrappers.Response
      Redirect response to `/reminder_templates`.

    Security:
      - Accepts only POST requests.
      - Requires a CSRF token from `DeleteForm` for safety.

    Related components:
      - Model: `ReminderTemplate` (models.py)
      - Blueprint endpoint: `routes.delete_reminder`
    """
    form = DeleteForm()
    if not form.validate_on_submit():
        abort(400, description="Bad request: CSRF token missing or invalid.")

    reminder = ReminderTemplate.query.get_or_404(id)
    db.session.delete(reminder)
    db.session.commit()
    flash("Reminder deleted.", "info")
    return redirect(url_for("routes.reminder_templates"))

@bp.route("/calendar")
def calendar_view():
    """Render a calendar view of all recorded measurements (path: "/calendar").

    Summary:
      This view generates a simple calendar-style visualization of all
      `Measurement` records in the system. Each measurement is represented
      as an event on the calendar, containing the date and the associated service.
      The page is intended as a quick overview of when measurements were
      recorded across all services.

    HTTP Methods:
      - GET: Retrieve all measurements from the database, prepare them as
        calendar events, and render the `calendar.html` template.

    Behavior and Database Access:
      1. All `Measurement` records are queried from the database.
      2. A list of event dictionaries is constructed, where each dictionary
        contains:
        - `date`: ISO-formatted string of the measurement date.
        - `service`: the name of the related `Service`.
      3. The `events` list is passed to the template for rendering, e.g., as
        a calendar grid or a list of events per day.
      4. No database modifications occur; this is a read-only view.

    Local variables (types and intent):
      - measurements (List[Measurement]):
          All measurement objects loaded from the database. Each object has
          attributes `date`, `value`, `note`, and a relationship `service`.
      - events (List[Dict[str, str]]):
          A list of dictionaries representing calendar events. Each dictionary
          has keys:
          * "date" (str): ISO-formatted date string.
          * "service" (str): name of the service for that measurement.

    Return: str.
      The HTML string returned by `render_template("calendar.html")`.
      It contains the calendar view populated with all measurement events.

    Template contract:
      Template name: "calendar.html".
      Context variables:
          - events (List[Dict[str, str]]): Iterated in the template to display
            measurements on a calendar. Each event contains `date` and `service`.

    Related components:
    - Model: `Measurement` (models.py)
      Provides the measurements to display.
    - Model: `Service` (models.py)
      Used to get the service name for each measurement.
    - Blueprint: "routes"
      This route is registered in the "routes" blueprint. Its endpoint name
      is `routes.calendar_view`.

    Example usage:
    1. User navigates to "/calendar".
    2. The server queries all measurements and builds `events`.
    3. The `calendar.html` template displays each event on a calendar,
       optionally highlighting which service the measurement belongs to.
    4. The user sees a complete overview of measurement activity by date.

    Notes:
    - Currently, all measurements are included; for large datasets, consider
      paginating or filtering by month/year to improve performance.
    - This view does not provide editing capabilities; it is strictly
      read-only visualization.
    """
    measurements = Measurement.query.all()
    events = [{"date": m.date.isoformat(), "service": m.service.name} for m in measurements]

    return render_template("calendar.html", events=events)




