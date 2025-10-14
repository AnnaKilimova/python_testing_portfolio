from django.contrib import admin
from .models import Course

@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    """Admin configuration for the Course model.

    This class defines how the Course model is displayed and managed
    in the Django admin panel.

    Attributes:
        list_display (tuple): Fields that are shown in the list view.
        search_fields (tuple): Fields that can be searched.
    """
    list_display = ('title', 'start_date', 'end_date', 'created_at')
    search_fields = ('title', )

# Register your models here.
