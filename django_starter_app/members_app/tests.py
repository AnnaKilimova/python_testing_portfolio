from django.test import TestCase
from .models import Member
from courses_app.models import Course
from .forms import MemberForm
from django.urls import reverse, resolve
from django.test import SimpleTestCase
from .views import member_list, member_create
from django.contrib import admin

# ======== test_models =======

class MemberModelTest(TestCase):
    """Test cases for the Member model.

    Description:
        This class tests that the Member model behaves correctly when creating
        new model instances and when converting them to strings.

    Steps performed:
        - Create Member objects and verify that fields are saved correctly.
        - Check that the `joined_at` field is automatically generated.
        - Verify that the `__str__()` method returns the model first_name.

    Notes:
        The tests use Django's built-in `TestCase`, which creates a temporary
        database for each test run. This ensures that tests do not affect
        real project data.
    """
    def test_member_creation(self) -> None:
        """Test that a Member instance is created and stored correctly.

        Steps:
            1. Use `Member.objects.create()` to create a new Member object.
               This method builds and saves the object in one step.
            2. Verify that the first_name matches the value given during creation.
            3. Confirm that the `joined_at` field is automatically filled
               by Django due to the `auto_now_add=True` parameter.

        Returns:
            None
        """
        member = Member.objects.create(first_name="Merlin", last_name="Monro", email="test@gmail.com")
        self.assertEqual(member.first_name, "Merlin")
        self.assertTrue(member.joined_at)

    def test_member_str_method(self):
        """Test the string representation of the Member model.

        Steps:
            1. Create a new Member instance with simple first_name and last_name.
            2. Convert the Member to a string using `str(member)`.
            3. Check that it returns the first_name and last_name, confirming that
               the `__str__()` method in the model is implemented correctly.

        Returns:
            None
        """
        member = Member.objects.create(first_name="Merlin", last_name="Monro")
        self.assertEqual(str(member), "Merlin Monro")


class CourseModelTest(TestCase):
    """Test cases for the Course model and its relationship with Member.

    Description:
        This class ensures that Course objects can be created correctly and
        that the many-to-many relationship between Member and Course works
        from both directions.

    Relationships:
        - `Course.members` (created by `related_name='members'`) provides
          access to all members assigned to that course.
        - `Member.courses` provides access to all courses that a member is linked to.

    Notes:
        The relationship between Member and Course is automatically handled
        by Django through an intermediate table. The `.add()` method is used
        to link existing objects together without re-creating them.
    """
    def test_course_creation_and_member_relation(self) -> None:
        """Test that a Course can be created and linked to a Member.

        Steps:
            1. Create a new Member instance using `Member.objects.create()`.
               The `last_name` field is optional, so it can be skipped.
            2. Create a new Course instance using `Course.objects.create()`.  
            3. Use `course.members.add(member)` to create a link between
               the course and the member. This updates the many-to-many
               table in the background.
            4. Use `course.members.all()` to confirm that the member
               is listed under this course.
            5. Use `member.courses.all()` to confirm that the course
               is listed under this member (reverse relationship).

        Returns:
            None
        """
        member = Member.objects.create(first_name="Merlin", email='test@gmail.com')
        course = Course.objects.create(title="Cinema Art")
        course.members.add(member)
        self.assertIn(member, course.members.all())
        self.assertIn(course, member.courses.all())

# ======== test_forms =======

class MemberFormTest(TestCase):
    """Test cases for the MemberForm class.

    Description:
        This class contains tests that check the behavior of the MemberForm,
        which is a Django ModelForm connected to the Member model.
        The tests ensure that the form correctly validates both valid
        and invalid input data.

    Notes:
        - Each test runs in an isolated environment using Django's TestCase.
          This means the test database is created automatically before tests
          and removed afterward.
        - The form is bound to the Member model through the Meta class,
          which defines which fields are included in the form.
    """
    def test_valid_form(self):
        """Test that MemberForm accepts valid data.

        Steps:
            1. Create a dictionary called `data` that simulates data
               submitted from a web form. The keys correspond to the
               model fields listed in MemberForm.Meta.fields:
               'first_name', 'last_name' and 'email'.
            2. Provide values in the correct formats. For email,
               Django expects the email address validator, 'something@something.something'.
            3. Pass this dictionary to `MemberForm(data=data)`, which
               creates a bound form (a form connected to data).
            4. Call `form.is_valid()` to trigger Django's validation process.
               - If all fields are valid, it returns True and populates
                 the `cleaned_data` dictionary.
            5. Use `self.assertTrue(form.is_valid())` to confirm that
               the form correctly validates when all input is proper.

        Notes:
            - `MemberForm` is a subclass of `forms.ModelForm`.
              It automatically creates form fields based on the Member model.
            - The validation process checks data types, required fields,
              and field formats.

        References:
            - Django ModelForm documentation:
              https://docs.djangoproject.com/en/stable/topics/forms/modelforms/
            - Form validation:
              https://docs.djangoproject.com/en/stable/ref/forms/api/#django.forms.Form.is_valid
        """
        data = {
            'first_name': 'Merlin',
            'last_name': 'Monroe',
            'email': 'test@gmail.com',
        }
        form = MemberForm(data=data)
        self.assertTrue(form.is_valid())

    def test_invalid_email_format(self):
        """Test that MemberForm rejects an invalid date format.

        Steps:
            1. Create a dictionary `data` with an invalid email address ('test@gmail' — missing top-level domain).
            2. Pass this data to `MemberForm(data=data)` to create
               a bound form instance.
            3. Call `form.is_valid()`, which runs Django's validation
               and detects that the date format is incorrect.
            4. Confirm that validation fails.
            5. Check that 'email' appears in form.errors, proving that the email field caused the issue.

        Notes:
            - By default, Django's `EmailField` expects the email address validator, 
              'something@something.something'. If a different format like 'something@something'
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
            'first_name': 'Merlin',
            'email': 'test@gmail',
        }
        form = MemberForm(data=data)
        self.assertFalse(form.is_valid())
        self.assertIn('email', form.errors)

# ======== test_views =======

class MemberViewsTest(TestCase):
    """Test cases for member-related views.

    Description:
        This class verifies that the views connected to the Member model
        work correctly, including:
        - displaying a list of members,
        - rendering the member creation form,
        - processing form submissions to create a new member.

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

    def test_member_list_view(self) -> None:
        """Test that the member list view displays existing members.

        Steps:
            1. Create a Member object in the test database using Django ORM.
            2. Use the test client to send a GET request to the view
               with the URL name 'members:list'.
            3. Confirm that the response returns HTTP 200 (OK).
            4. Verify that the correct HTML template 'members_app/member_list.html'
               is used to render the page.
            5. Check that the member first_name and email appear in the rendered page content.

        Notes:
            - The ORM call `Member.objects.create()` inserts a new record
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
        Member.objects.create(first_name="Merlin", email="test@gmai.com")
        response = self.client.get(reverse('members:list'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'members_app/member_list.html')
        self.assertContains(response, "Merlin")
        self.assertContains(response, "test@gmai.com")

    def test_member_create_view_get(self) -> None:
        """Test that the member creation form is displayed correctly.

        Steps:
            1. Send a GET request to the view with the URL name 'members:create'.
            2. Check that the response returns HTTP 200 (OK),
               meaning the page loaded successfully.
            3. Verify that the correct HTML template
               'members_app/member_form.html' is rendered.

        Notes:
            - The GET request simulates a user opening the member creation page
              in a browser.
            - The `assertTemplateUsed()` method ensures that the view
              uses the correct form template.

        References:
            - Django GET requests in tests:
              https://docs.djangoproject.com/en/stable/topics/testing/tools/#django.test.Client.get
        """
        response = self.client.get(reverse('members:create'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'members_app/member_form.html')

    def test_member_create_view_post(self) -> None:
        """Test that a new member is created after submitting valid form data.

        Steps:
            1. Send a POST request to the 'members:create' view
               with valid form data (first_name, last_name and email).
            2. Confirm that the response returns HTTP 302 (redirect),
               indicating successful form submission.
            3. Verify that a new Member object with the given first_name and email
               has been created in the database.

        Notes:
            - A POST request simulates a user submitting the form in a browser.
            - The redirect (302) confirms that `redirect('members:list')`
              was triggered after successful validation.
            - The ORM query `Member.objects.filter(...).exists()` checks
              whether the member was saved correctly.

        References:
            - Django POST requests in tests:
              https://docs.djangoproject.com/en/stable/topics/testing/tools/#django.test.Client.post
            - Redirect responses:
              https://developer.mozilla.org/en-US/docs/Web/HTTP/Status/302
            - Django QuerySet.exists():
              https://docs.djangoproject.com/en/stable/ref/models/querysets/#exists
        """
        response = self.client.post(reverse('members:create'), {
            'first_name': 'Merlin',
            'email': 'test@gmail.com',
        })
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Member.objects.filter(first_name='Merlin').exists())
        self.assertTrue(Member.objects.filter(email='test@gmail.com').exists())

# ======== test_urls =======

class TestUrls(SimpleTestCase):
    """Test cases for URL routing in the members application.

    Description:
        This class verifies that each named URL in the members app
        correctly maps to its corresponding view function.
        It ensures that the URL configuration (urls.py) is properly linked
        to the correct views defined in members_app/views.py.

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
        """Test that the 'members:list' URL name maps to the member_list view.

        Steps:
            1. Use reverse('members:list') to get the actual URL path
               defined in urls.py for listing members.
            2. Call resolve(url) to check which view function is linked
               to this path.
            3. Verify that the resolved function equals members_list,
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
        url = reverse('members:list')
        self.assertEqual(resolve(url).func, member_list)

    def test_create_url_resolves(self) -> None:
        """Test that the 'members:create' URL name maps to the member_create view.

        Steps:
            1. Use reverse('members:create') to generate the actual path
               from the URL name defined in urls.py.
            2. Use resolve(url) to find out which view function
               is assigned to this path.
            3. Confirm that the resolved function equals member_create,
               ensuring that the route is correctly set up.

        Notes:
            - This test ensures that when a user visits the member creation
              URL, Django routes the request to the right view.
            - Such tests are helpful after refactoring URLs or moving views
              to different files.

        References:
            - Django reverse() and resolve():
              https://docs.djangoproject.com/en/stable/ref/urlresolvers/
        """
        url = reverse('members:create')
        self.assertEqual(resolve(url).func, member_create)

# ======== test_admin =======

class AdminTest(TestCase):
    """Test case for verifying that the Member model is registered in the Django admin site.

    Description:
        This test checks if the Member model is properly registered in the Django admin interface.
        Registering a model in admin.py allows administrators to manage Member objects
        (add, edit, delete, or view them) through the Django admin panel.

        The test uses Django's built-in admin.site._registry attribute, which stores
        all models that have been registered with the admin site. If a model is missing
        from this registry, it means it won't appear in the admin dashboard.

    Steps:
        1. Import the Member model and the global admin site object.
        2. Use the assertIn() method to check whether the Member model
           exists in admin.site._registry.
        3. If it is registered correctly, the test will pass; if not, it will fail.

    Notes:
        - This test does not interact with the database directly.
        - It only verifies that admin.py includes a line such as:
              admin.site.register(Member)
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

    def test_member_registered_in_admin(self) -> None:
        """Test that the Member model is registered in the Django admin site.

        Steps:
            1. Access the admin.site._registry dictionary, which lists all models
               currently registered in the admin interface.
            2. Check that the Member model is one of the registered models
               using assertIn().
            3. If Member is found in the registry, it means the model is correctly
               set up for management in the admin panel.

        Notes:
            - admin.site._registry is mainly for internal use but safe for testing
              registration.
            - This test ensures that developers didn't forget to register Member
              after adding or modifying models.

        References:
            - Django admin site registry:
              https://docs.djangoproject.com/en/stable/ref/contrib/admin/#django.contrib.admin.AdminSite._registry
        """
        self.assertIn(Member, admin.site._registry)
