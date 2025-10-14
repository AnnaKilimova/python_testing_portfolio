from django import forms
from .models import Course

class CourseForm(forms.ModelForm):
    """A form for creating and updating Course objects.

    This form is connected to the Course model and includes
    the main fields used to add or edit a course.

    Attributes:
        Meta (class): Defines the model and fields used in the form.
    """
    class Meta:
        model = Course
        fields = ['title', 'description', 'start_date', 'end_date']