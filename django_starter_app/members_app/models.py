from django.db import models
from courses_app.models import Course

# Create your models here.

class Member(models.Model):
    """Template for creating members.

    Attributes:
        first_name (str): First name (max 100 characters).
        last_name (str): Optional last name (max 100 characters).
        email (str): Unique email address.
        courses (ManyToManyField): Many-to-many relationship with Course model.
                                   This creates a reverse attribute `members`
                                   inside Course to access all members of that course.
        joined_at (datetime): The date and time when the member joined (added automatically).

    Relationships:
        Many-to-Many with Course through related name `members`.
    """
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100, blank=True)
    email = models.EmailField(unique=True)
    courses = models.ManyToManyField(Course, related_name='members', blank=True)
    joined_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}".strip()
