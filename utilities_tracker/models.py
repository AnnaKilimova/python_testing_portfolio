from .db_config import db 
from decimal import Decimal
from typing import Optional

# === Association table for many-to-many (Service ↔ ReminderTemplate) ===
service_reminder = db.Table(
    'service_reminder',
    db.Column('service_id', db.Integer, db.ForeignKey('service.id'), primary_key=True),
    db.Column('reminder_template_id', db.Integer, db.ForeignKey('reminder_template.id'), primary_key=True)
)

class Service(db.Model):
    """Represents a service for which measurements are recorded.

    Attributes:
        id (int): Primary key.
        name (str): Unique service name (e.g., "Electricity").
        unit (str): Unit of measurement (e.g., "kWh", "m³", "GB").
        description (str | None): Optional free-text description.
        measurements (List[Measurement]): One-to-many relationship with Measurement.
        reminders (List[ReminderTemplate]): Many-to-many relationship with ReminderTemplate.

    Relationships:
        - One Service ↔ Many Measurements
          Implemented with `service_id` foreign key in Measurement.
          Configured with `back_populates='service'`, making it bidirectional.
          Sorted by Measurement.date in descending order.
          Cascade: "all, delete-orphan":
            - "all": apply operations to child objects together with parent.
            - "delete-orphan": orphaned Measurement objects are removed automatically.
        - Many-to-Many with ReminderTemplate through association table `service_reminder`.

    Notes:
        - `order_by='Measurement.date.desc()'` ensures `service.measurements` is sorted
          by date descending (latest first).
        - Cascade applies at ORM level (Python), not necessarily at DB constraint level.
    """
    __tablename__ = 'service'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=True)  
    unit = db.Column(db.String(20), nullable=False)
    description = db.Column(db.Text, nullable=True)

    measurements = db.relationship(
        'Measurement',
        back_populates='service',
        order_by='Measurement.date.desc()',
        cascade='all, delete-orphan'
    )

    reminders = db.relationship(
        'ReminderTemplate',
        secondary=service_reminder,
        back_populates='services'
    )

    def __repr__(self) -> str:
        """String representation for debugging."""
        return f"<Service(id={self.id}, name={self.name}, unit={self.unit})>"

    def last_measurement(self) -> Optional["Measurement"]:
        """Returns the latest measurement for this service.

        Returns:
            Measurement | None: The most recent measurement, or None if none exist.

        Notes:
            - Uses the `measurements` relationship (already ordered desc by date).
            - Equivalent to `service.measurements[0]` if list is not empty.
        """
        return self.measurements[0] if self.measurements else None

    def consumption_for_month(self, year: int, month: int) -> Decimal:
        """Calculates total consumption for a given service within a specific month.

        This method computes the difference in recorded measurements for the
        specified month (`year` and `month`). The logic is as follows:

        1. All measurements for the service are first sorted in chronological order.
        2. The function iterates through each measurement (`m`) that belongs to
        the requested month.
        3. For the first measurement of the month:
            - The previous measurement *before* the first day of the month
            (if any) is located.
            - The difference between the current value and the last known
            previous value is added to the total consumption.
        4. For subsequent measurements within the same month:
            - The difference between the current and previous measurement values
            (within the same month) is accumulated.
        5. If no measurements exist before the start of the month, the consumption
        is calculated starting from zero.

        Args:
            year (int): Target year for which to calculate consumption.
            month (int): Target month (1-12).

        Returns:
            Decimal: Total consumption for the specified month.
                    Returns Decimal("0") if no valid measurements exist.

        Notes:
            - The calculation assumes that measurement values are *cumulative*
            (i.e., represent the total meter reading, not per-period consumption).
            - The method relies on `self.measurements` relationship being already
            loaded; otherwise, an additional query may be executed.
            - The method handles sparse data (missing months) gracefully.
            - Uses Python's `Decimal` type for precise arithmetic.

        Example:
            Suppose the following measurements exist for the service:
                - 2025-01-01: 120.0
                - 2025-02-01: 150.0
                - 2025-02-20: 180.0
            Then:
                service.consumption_for_month(2025, 2) → Decimal("60.0")

        """
        ms = sorted(self.measurements, key=lambda m: m.date)

        total = Decimal("0")
        prev_value = None

        for m in ms:
            if m.date.year == year and m.date.month == month:
                if prev_value is None:
                    prev = next((x for x in reversed(ms) if x.date < m.date), None)
                    prev_value = prev.value if prev else Decimal("0")

                total += m.value - prev_value

                prev_value = m.value

        return total
 

class Measurement(db.Model):
    """Represents a recorded measurement for a service.

    Attributes:
        id (int): Primary key.
        date (date): Measurement date (indexed).
        value (Decimal): Recorded value (precision: 12 total digits, 3 decimal places).
        note (str | None): Optional note.
        service_id (int): Foreign key to Service.
        service (Service): Relationship back to Service.

    Relationships:
        - Each Measurement belongs to exactly one Service (many-to-one).
        - Defined via `service_id` foreign key and `service` relationship.

    Notes:
        - ForeignKey ensures relational integrity in the DB.
        - Relationship provides Python-level shortcut (`measurement.service` instead of explicit JOIN).
    """
    __tablename__ = 'measurement'
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date, nullable=False, index=True)
    value = db.Column(db.Numeric(12, 3), nullable=False)
    note = db.Column(db.String(255), nullable=True)

    service_id = db.Column(db.Integer, db.ForeignKey('service.id'), nullable=False, index=True)
    service = db.relationship('Service', back_populates='measurements')

    @property
    def consumption_from_previous(self):
        """Returns the difference between the current measurement and the previous one.

        The "previous" measurement is defined as:
        - Same service_id
        - Earlier date than the current one
        - Closest by date (maximum date < current date)

        Returns:
            Decimal: Difference between current and previous measurement values.
            None: If no previous measurement exists.

        Notes:
            - Executes a database query each time the property is accessed.
            - Implementation ignores measurements on the same date.
              (Consider using datetime instead of date for higher granularity.)
            - Requires that the current object is persisted in the session.
            - If not persisted or session is closed, property may trigger additional queries.
        """
        prev = Measurement.query.filter(
            Measurement.service_id == self.service_id,
            Measurement.date < self.date
        ).order_by(Measurement.date.desc()).first()
        if not prev:
            return None
        return self.value - prev.value
    

class ReminderTemplate(db.Model):
    """Template for scheduling reminders.

    Attributes:
        id (int): Primary key.
        day_of_month (int): Day of month (1-31).
        time (time | None): Optional reminder time.
        note (str | None): Optional description.
        services (List[Service]): Many-to-many relationship to services.

    Relationships:
        - Many-to-many with Service via association table `service_reminder`.
        - Bidirectional: ReminderTemplate.services ↔ Service.reminders.
    """
    __tablename__ = 'reminder_template'
    id = db.Column(db.Integer, primary_key=True)
    day_of_month = db.Column(db.Integer, nullable=False) 
    time = db.Column(db.Time, nullable=True) 
    note = db.Column(db.String(255), nullable=True)

    services = db.relationship(
        'Service',
        secondary=service_reminder,
        back_populates='reminders'
    )

    def __repr__(self):
        """String representation for debugging."""
        return f"<ReminderTemplate(id={self.id}, day={self.day_of_month}, time={self.time})>"

