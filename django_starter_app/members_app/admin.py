from django.contrib import admin
from .models import Member

# Register your models here.

@admin.register(Member)
class MemberAdmin(admin.ModelAdmin):
    """Admin configuration for the Member model.

    This class defines how the Member model is displayed and managed
    in the Django admin panel.

    Attributes:
        list_display (tuple): Fields that are shown in the list view.
        search_fields (tuple): Fields that can be searched.

    Notes:
        courses - ManyToManyField which cannot be specified directly in list_display.
    """
    list_display = ('first_name', 'last_name', 'email', 'joined_at')
    search_fields = ('first_name', 'last_name', 'email',)
