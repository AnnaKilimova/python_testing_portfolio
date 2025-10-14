from django.db import models

# Create your models here.

class Course(models.Model):
    """Template for creating courses.

    Attributes:
        title (str): The title of the course (max 200 characters).
        description (str): Optional description of the course.
        start_date (date): Optional start date of the course.
        end_date (date): Optional end date of the course.
        created_at (datetime): The date and time when the course was created (added automatically).

    Notes:
        The difference between `blank` and `null`:
        - `blank=True` affects form validation (field can be empty in forms).
        - `null=True` affects the database (field can store NULL in DB).

    Relationships:
        Many-to-Many with Member through related name `members`.
    """
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


