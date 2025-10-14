from django.test import TestCase
from .models import Course
from members_app.models import Member
from .forms import CourseForm
from django.urls import reverse, resolve
from django.test import SimpleTestCase
from .views import course_list, course_create
from django.contrib import admin

# ======== test_models =======

class CourseModelTest(TestCase):
    """Test cases for the Course model.

    Description:
        This class tests that the Course model behaves correctly when creating
        new course instances and when converting them to strings.

    Steps performed:
        - Create Course objects and verify that fields are saved correctly.
        - Check that the `created_at` field is automatically generated.
        - Verify that the `__str__()` method returns the course title.

    Notes:
        The tests use Django's built-in `TestCase`, which creates a temporary
        database for each test run. This ensures that tests do not affect
        real project data.
    """
    def test_course_creation(self) -> None:
        """Test that a Course instance is created and stored correctly.

        Steps:
            1. Use `Course.objects.create()` to create a new Course object.
               This method builds and saves the object in one step.
            2. Verify that the title matches the value given during creation.
            3. Confirm that the `created_at` field is automatically filled
               by Django due to the `auto_now_add=True` parameter.

        Returns:
            None
        """
        course = Course.objects.create(title="Python Basics", description="Learn Python")
        self.assertEqual(course.title, "Python Basics")
        self.assertTrue(course.created_at)

    def test_course_str_method(self):
        """Test the string representation of the Course model.

        Steps:
            1. Create a new Course instance with a simple title.
            2. Convert the Course to a string using `str(course)`.
            3. Check that it returns the title, confirming that
               the `__str__()` method in the model is implemented correctly.

        Returns:
            None
        """
        course = Course.objects.create(title="Django")
        self.assertEqual(str(course), "Django")


class MemberModelTest(TestCase):
    """Test cases for the Member model and its relationship with Course.

    Description:
        This class ensures that Member objects can be created correctly and
        that the many-to-many relationship between Member and Course works
        from both directions.

    Relationships:
        - `Member.courses` provides access to all courses that a member is linked to.
        - `Course.members` (created by `related_name='members'`) provides
          access to all members assigned to that course.

    Notes:
        The relationship between Member and Course is automatically handled
        by Django through an intermediate table. The `.add()` method is used
        to link existing objects together without re-creating them.
    """
    def test_member_creation_and_course_relation(self) -> None:
        """Test that a Member can be created and linked to a Course.

        Steps:
            1. Create a new Course instance using `Course.objects.create()`.
            2. Create a new Member instance using `Member.objects.create()`.
               The `last_name` field is optional, so it can be skipped.
            3. Use `member.courses.add(course)` to create a link between
               the member and the course. This updates the many-to-many
               table in the background.
            4. Use `member.courses.all()` to confirm that the course
               is listed under this member.
            5. Use `course.members.all()` to confirm that the member
               is listed under this course (reverse relationship).

        Returns:
            None
        """
        course = Course.objects.create(title="Math")
        member = Member.objects.create(first_name="Alice", email="alice@example.com")
        member.courses.add(course)
        self.assertIn(course, member.courses.all())
        self.assertIn(member, course.members.all())

# ======== test_forms =======

class CourseFormTest(TestCase):
    """Test cases for the CourseForm class.

    Description:
        This class contains tests that check the behavior of the CourseForm,
        which is a Django ModelForm connected to the Course model.
        The tests ensure that the form correctly validates both valid
        and invalid input data.

    Notes:
        - Each test runs in an isolated environment using Django's TestCase.
          This means the test database is created automatically before tests
          and removed afterward.
        - The form is bound to the Course model through the Meta class,
          which defines which fields are included in the form.
    """
    def test_valid_form(self):
        """Test that CourseForm accepts valid data.

        Steps:
            1. Create a dictionary called `data` that simulates data
               submitted from a web form. The keys correspond to the
               model fields listed in CourseForm.Meta.fields:
               'title', 'description', 'start_date', and 'end_date'.
            2. Provide values in the correct formats. For dates,
               Django expects the ISO format 'YYYY-MM-DD'.
            3. Pass this dictionary to `CourseForm(data=data)`, which
               creates a bound form (a form connected to data).
            4. Call `form.is_valid()` to trigger Django's validation process.
               - If all fields are valid, it returns True and populates
                 the `cleaned_data` dictionary.
            5. Use `self.assertTrue(form.is_valid())` to confirm that
               the form correctly validates when all input is proper.

        Notes:
            - `CourseForm` is a subclass of `forms.ModelForm`.
              It automatically creates form fields based on the Course model.
            - The validation process checks data types, required fields,
              and field formats.

        References:
            - Django ModelForm documentation:
              https://docs.djangoproject.com/en/stable/topics/forms/modelforms/
            - Form validation:
              https://docs.djangoproject.com/en/stable/ref/forms/api/#django.forms.Form.is_valid
        """
        data = {
            'title': 'Python Advanced',
            'description': 'Deep dive into Python',
            'start_date': '2025-10-15',
            'end_date': '2025-12-10'
        }
        form = CourseForm(data=data)
        self.assertTrue(form.is_valid())

    def test_invalid_date_format(self):
        """Test that CourseForm rejects an invalid date format.

        Steps:
            1. Create a dictionary `data` with an invalid date format
               for the 'start_date' field. Instead of 'YYYY-MM-DD',
               it uses 'DD.MM.YYYY' which Django does not recognize by default.
            2. Pass this data to `CourseForm(data=data)` to create
               a bound form instance.
            3. Call `form.is_valid()`, which runs Django's validation
               and detects that the date format is incorrect.
            4. Confirm with `self.assertFalse(form.is_valid())` that
               the form fails validation.
            5. Check that the key 'start_date' appears in `form.errors`
               using `self.assertIn('start_date', form.errors)`, proving
               that the date field caused the validation failure.

        Notes:
            - By default, Django's `DateField` expects the ISO format
              'YYYY-MM-DD'. If a different format like 'DD.MM.YYYY'
              should be accepted, you can define `input_formats` in
              the field or widget configuration.
            - `form.errors` is a dictionary containing field names as keys
              and lists of error messages as values.

        References:
            - Django DateField input formats:
              https://docs.djangoproject.com/en/stable/ref/forms/fields/#django.forms.DateField
            - Form error handling:
              https://docs.djangoproject.com/en/stable/ref/forms/api/#django.forms.Form.errors
        """
        data = {
            'title': 'Invalid Course',
            'start_date': '15.10.2025',
        }
        form = CourseForm(data=data)
        self.assertFalse(form.is_valid())
        self.assertIn('start_date', form.errors)

# ======== test_views =======

class CourseViewsTest(TestCase):
    """Test cases for course-related views.

    Description:
        This class verifies that the views connected to the Course model
        work correctly, including:
        - displaying a list of courses,
        - rendering the course creation form,
        - processing form submissions to create a new course.

        It uses Django's built-in test client to simulate user requests
        (GET and POST) and check that the correct templates, status codes,
        and database actions occur.

    Notes:
        - The test class inherits from Django's TestCase, which automatically
          sets up a temporary test database for each test.
        - The `reverse()` function is used to resolve URL names into actual paths.
        - The test client (`self.client`) is used to imitate browser requests
          without running a server.

    References:
        - Django TestCase:
          https://docs.djangoproject.com/en/stable/topics/testing/overview/
        - Django test client:
          https://docs.djangoproject.com/en/stable/topics/testing/tools/#the-test-client
        - URL reversing:
          https://docs.djangoproject.com/en/stable/ref/urlresolvers/#reverse
    """

    def test_course_list_view(self) -> None:
        """Test that the course list view displays existing courses.

        Steps:
            1. Create a Course object in the test database using Django ORM.
            2. Use the test client to send a GET request to the view
               with the URL name 'courses:list'.
            3. Confirm that the response returns HTTP 200 (OK).
            4. Verify that the correct HTML template 'courses_app/course_list.html'
               is used to render the page.
            5. Check that the course title appears in the rendered page content.

        Notes:
            - The ORM call `Course.objects.create()` inserts a new record
              into the test database.
            - The method `self.assertContains()` checks that the rendered page
              includes the expected text.
            - The `assertTemplateUsed()` method confirms the correct template was used.

        References:
            - Template testing:
              https://docs.djangoproject.com/en/stable/topics/testing/tools/#asserttemplateused
            - Content testing:
              https://docs.djangoproject.com/en/stable/topics/testing/tools/#assertcontains
        """
        Course.objects.create(title="Math")
        response = self.client.get(reverse('courses:list'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'courses_app/course_list.html')
        self.assertContains(response, "Math")

    def test_course_create_view_get(self) -> None:
        """Test that the course creation form is displayed correctly.

        Steps:
            1. Send a GET request to the view with the URL name 'courses:create'.
            2. Check that the response returns HTTP 200 (OK),
               meaning the page loaded successfully.
            3. Verify that the correct HTML template
               'courses_app/course_form.html' is rendered.

        Notes:
            - The GET request simulates a user opening the course creation page
              in a browser.
            - The `assertTemplateUsed()` method ensures that the view
              uses the correct form template.

        References:
            - Django GET requests in tests:
              https://docs.djangoproject.com/en/stable/topics/testing/tools/#django.test.Client.get
        """
        response = self.client.get(reverse('courses:create'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'courses_app/course_form.html')

    def test_course_create_view_post(self) -> None:
        """Test that a new course is created after submitting valid form data.

        Steps:
            1. Send a POST request to the 'courses:create' view
               with valid form data (title and description).
            2. Confirm that the response returns HTTP 302 (redirect),
               indicating successful form submission.
            3. Verify that a new Course object with the given title
               has been created in the database.

        Notes:
            - A POST request simulates a user submitting the form in a browser.
            - The redirect (302) confirms that `redirect('courses:list')`
              was triggered after successful validation.
            - The ORM query `Course.objects.filter(...).exists()` checks
              whether the course was saved correctly.

        References:
            - Django POST requests in tests:
              https://docs.djangoproject.com/en/stable/topics/testing/tools/#django.test.Client.post
            - Redirect responses:
              https://developer.mozilla.org/en-US/docs/Web/HTTP/Status/302
            - Django QuerySet.exists():
              https://docs.djangoproject.com/en/stable/ref/models/querysets/#exists
        """
        response = self.client.post(reverse('courses:create'), {
            'title': 'Physics',
            'description': 'Study physics'
        })
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Course.objects.filter(title='Physics').exists())

# ======== test_urls =======

class TestUrls(SimpleTestCase):
    """Test cases for URL routing in the courses application.

    Description:
        This class verifies that each named URL in the courses app
        correctly maps to its corresponding view function.
        It ensures that the URL configuration (urls.py) is properly linked
        to the correct views defined in courses_app/views.py.

        These tests use Django's reverse() and resolve() utilities:
        - reverse(): converts a URL name (from urls.py) into its actual path.
        - resolve(): takes a URL path and determines which view function
          should handle it.

    Notes:
        - The test class inherits from SimpleTestCase because no database
          operations are performed.
        - If URL names or view imports are changed, these tests will help
          identify broken links between URLs and views.

    References:
        - SimpleTestCase:
          https://docs.djangoproject.com/en/stable/topics/testing/tools/#simpletestcase
        - reverse():
          https://docs.djangoproject.com/en/stable/ref/urlresolvers/#reverse
        - resolve():
          https://docs.djangoproject.com/en/stable/ref/urlresolvers/#resolve
    """

    def test_list_url_resolves(self) -> None:
        """Test that the 'courses:list' URL name maps to the course_list view.

        Steps:
            1. Use reverse('courses:list') to get the actual URL path
               defined in urls.py for listing courses.
            2. Call resolve(url) to check which view function is linked
               to this path.
            3. Verify that the resolved function equals course_list,
               confirming that the URL is correctly configured.

        Notes:
            - reverse() looks up the URL pattern by its 'name' argument
              from urls.py and returns the corresponding path as a string.
            - resolve() performs the reverse - it identifies which view
              should handle a given URL path.
            - The assertEqual() method confirms that both functions match.

        References:
            - Django URL dispatcher:
              https://docs.djangoproject.com/en/stable/topics/http/urls/
            - assertEqual():
              https://docs.python.org/3/library/unittest.html#unittest.TestCase.assertEqual
        """
        url = reverse('courses:list')
        self.assertEqual(resolve(url).func, course_list)

    def test_create_url_resolves(self) -> None:
        """Test that the 'courses:create' URL name maps to the course_create view.

        Steps:
            1. Use reverse('courses:create') to generate the actual path
               from the URL name defined in urls.py.
            2. Use resolve(url) to find out which view function
               is assigned to this path.
            3. Confirm that the resolved function equals course_create,
               ensuring that the route is correctly set up.

        Notes:
            - This test ensures that when a user visits the course creation
              URL, Django routes the request to the right view.
            - Such tests are helpful after refactoring URLs or moving views
              to different files.

        References:
            - Django reverse() and resolve():
              https://docs.djangoproject.com/en/stable/ref/urlresolvers/
        """
        url = reverse('courses:create')
        self.assertEqual(resolve(url).func, course_create)

# ======== test_admin =======

class AdminTest(TestCase):
    """Test case for verifying that the Course model is registered in the Django admin site.

    Description:
        This test checks if the Course model is properly registered in the Django admin interface.
        Registering a model in admin.py allows administrators to manage Course objects
        (add, edit, delete, or view them) through the Django admin panel.

        The test uses Django's built-in admin.site._registry attribute, which stores
        all models that have been registered with the admin site. If a model is missing
        from this registry, it means it won't appear in the admin dashboard.

    Steps:
        1. Import the Course model and the global admin site object.
        2. Use the assertIn() method to check whether the Course model
           exists in admin.site._registry.
        3. If it is registered correctly, the test will pass; if not, it will fail.

    Notes:
        - This test does not interact with the database directly.
        - It only verifies that admin.py includes a line such as:
              admin.site.register(Course)
        - The _registry attribute is a dictionary where keys are model classes
          and values are their corresponding ModelAdmin instances.

    References:
        - Django Admin site API:
          https://docs.djangoproject.com/en/stable/ref/contrib/admin/
        - admin.site.register():
          https://docs.djangoproject.com/en/stable/ref/contrib/admin/#django.contrib.admin.site.register
        - assertIn():
          https://docs.python.org/3/library/unittest.html#unittest.TestCase.assertIn
    """

    def test_course_registered_in_admin(self) -> None:
        """Test that the Course model is registered in the Django admin site.

        Steps:
            1. Access the admin.site._registry dictionary, which lists all models
               currently registered in the admin interface.
            2. Check that the Course model is one of the registered models
               using assertIn().
            3. If Course is found in the registry, it means the model is correctly
               set up for management in the admin panel.

        Notes:
            - admin.site._registry is mainly for internal use but safe for testing
              registration.
            - This test ensures that developers didn't forget to register Course
              after adding or modifying models.

        References:
            - Django admin site registry:
              https://docs.djangoproject.com/en/stable/ref/contrib/admin/#django.contrib.admin.AdminSite._registry
        """
        self.assertIn(Course, admin.site._registry)
