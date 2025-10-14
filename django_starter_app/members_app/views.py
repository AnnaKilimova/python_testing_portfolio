from django.shortcuts import render, redirect
from .models import Member
from .forms import MemberForm

# Create your views here.
def member_list(request):
    """Display a list of all members.

    This view gets all Member objects from the database,
    orders them by joined date (newest first),
    and sends them to the HTML template for display.

    Args:
        request (HttpRequest): The HTTP request object from the user.

    Returns:
        HttpResponse: Rendered HTML page with the list of members.
    """
    members = Member.objects.all().order_by('-joined_at')
    return render(request, 'members_app/member_list.html', {'members': members})

def member_create(request):
    """Create a new member using a form.

    If the request method is POST, the form data is validated and saved
    as a new Member object in the database.
    If the request method is GET, an empty form is displayed.

    Args:
        request (HttpRequest): The HTTP request object from the user.

    Returns:
        HttpResponse: Redirect to the member list if the form is valid,
        or the form page again if there are errors or it's a GET request.
    """
    if request.method == 'POST':
        form = MemberForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('members:list')
    else:
        form = MemberForm()

    return render(request, 'members_app/member_form.html', {'form': form})   