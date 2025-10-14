from django.shortcuts import render, redirect
from .models import Course
from .forms import CourseForm

# Create your views here.
def course_list(request):
    """Display a list of all courses.

    This view gets all Course objects from the database,
    orders them by creation date (newest first),
    and sends them to the HTML template for display.

    Args:
        request (HttpRequest): The HTTP request object from the user.

    Returns:
        HttpResponse: Rendered HTML page with the list of courses.
    """
    courses = Course.objects.all().order_by('-created_at')
    return render(request, 'courses_app/course_list.html', {'courses': courses})

def course_create(request):
    """Create a new course using a form.

    If the request method is POST, the form data is validated and saved
    as a new Course object in the database.
    If the request method is GET, an empty form is displayed.

    Args:
        request (HttpRequest): The HTTP request object from the user.

    Returns:
        HttpResponse: Redirect to the course list if the form is valid,
        or the form page again if there are errors or it's a GET request.
    """
    if request.method == 'POST':
        form = CourseForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('courses:list')  
    else:
        form = CourseForm()

    return render(request, 'courses_app/course_form.html', {'form': form})   
