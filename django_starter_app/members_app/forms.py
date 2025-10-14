from django import forms
from .models import Member

class MemberForm(forms.ModelForm):
    """A form for creating and updating Member objects.

    This form is connected to the Member model and includes
    the main fields used to add or edit a member.

    Attributes:
        Meta (class): Defines the model and fields used in the form.
    """
    class Meta:
        model = Member
        fields = ['first_name', 'last_name', 'email']

