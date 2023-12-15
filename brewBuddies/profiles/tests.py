"""
Module: tests.py
Test cases for the Profile model and associated views.

Classes:
- ProfileModelTest: Test cases for the Profile model.
- ProfileViewsTest: Test cases for the views related to user profiles.

"""

from django.test import TestCase
from django.contrib.auth.models import User
from .models import Profile
from django.urls import reverse

class ProfileModelTest(TestCase):
    def setUp(self):
        """
        Set up test data, including creating a test user.

        Creates a test user with the username 'testuser' and password 'testpassword'.
        """
        # Create a test user
        self.user = User.objects.create_user(username='testuser', password='testpassword')

    def test_profile_creation(self):
        """
        Test profile creation.

        This test ensures that a profile is created with default values when a user is created.

        1. Create a user.
        2. Retrieve the associated profile.
        3. Assert that the profile is created with default values:
            - 'name': None
            - 'title': None
            - 'desc': None
            - 'profile_img': 'images/default.png'

        This test verifies that the profile creation process sets the default values correctly.
        """
        # Test that a profile is created when a user is created
        profile = Profile.objects.get(user=self.user)
        self.assertEqual(profile.name, None)
        self.assertEqual(profile.title, None)
        self.assertEqual(profile.desc, None)
        self.assertEqual(profile.profile_img.name, 'images/default.png')

    def test_profile_str_method(self):
        """
        Test the __str__ method of the profile model.

        This test ensures that the __str__ method of the Profile model returns
        the username of the associated user. It verifies that calling str() on a
        Profile instance returns the expected string representation.

        Test Steps:
        1. Retrieve the Profile instance associated with the test user.
        2. Call the __str__ method on the Profile instance.
        3. Assert that the returned string is equal to the username of the associated user ('testuser').
        """
        # Test the __str__ method of the profile model
        profile = Profile.objects.get(user=self.user)
        self.assertEqual(str(profile), 'testuser')

    def test_profile_deletion(self):
        """
        Test profile deletion.

        Ensures that a user's profile is deleted when the user account is deleted.

        Steps:
        1. Delete the user account.
        2. Attempt to retrieve the corresponding profile using the user's ID.
        3. Assert that the Profile.DoesNotExist exception is raised, indicating the successful deletion of the profile.

        Raises:
            Profile.DoesNotExist: If the profile associated with the user does not exist after the user is deleted.
        """
        # Test that a profile is deleted when a user is deleted
        self.user.delete()
        with self.assertRaises(Profile.DoesNotExist):
            Profile.objects.get(user=self.user)

    def test_profile_update(self):
        """
        Test updating user profile fields.

        This test case ensures that user profile fields can be updated successfully.
        
        Steps:
        1. Retrieve the user's profile using the user instance.
        2. Update the profile fields, such as name, title, and description.
        3. Save the changes to the profile.
        
        The test asserts that the profile fields are updated correctly.

        """
        # Test updating profile fields
        profile = Profile.objects.get(user=self.user)
        profile.name = 'Victor Kostin'
        profile.title = 'Tester'
        profile.desc = 'A passionate developer'
        profile.save()

        updated_profile = Profile.objects.get(user=self.user)
        self.assertEqual(updated_profile.name, 'Victor Kostin')
        self.assertEqual(updated_profile.title, 'Tester')
        self.assertEqual(updated_profile.desc, 'A passionate developer')

    def test_profile_img_upload(self):
        """
        Test uploading a profile image.

        This test case checks whether a profile image can be successfully uploaded.
        
        Steps:
        1. Retrieve the user's profile from the database.
        2. Set the profile image field to a test image path.
        3. Save the profile.
        4. Retrieve the updated profile from the database.
        5. Assert that the profile image path in the updated profile matches the expected path.

        This test ensures that the profile image upload functionality is working as expected.
        """
        # Test uploading a profile image
        profile = Profile.objects.get(user=self.user)
        profile.profile_img = 'images/test_image.jpg'
        profile.save()

        updated_profile = Profile.objects.get(user=self.user)
        self.assertEqual(updated_profile.profile_img.name, 'images/test_image.jpg')


    class ProfileViewsTest(TestCase):
        def setUp(self):
            """
            Set up test data, including creating a test user and logging in.

            Creates a test user with the username 'testuser' and password 'testpassword'.
            Logs in the test user for authenticated views testing.
            """
            self.user = User.objects.create_user(username='testuser', password='testpassword')
            self.client.login(username='testuser', password='testpassword')

        def test_index_view_redirects_to_map(self):
            """
            Test redirection from index view to map view.

            This test checks whether the index view properly redirects to the '/map/' URL.

            Returns:
                None: This test method does not return any value.

            Raises:
                AssertionError: If the index view does not redirect to the expected URL.

            Usage:
                To execute this test, call it within a Django TestCase or appropriate testing framework.

            Example:
                ```
                class MyTests(TestCase):
                    def test_index_view_redirects_to_map(self):
                        # ... setup and other test methods ...
                        self.test_index_view_redirects_to_map()
                ```
            """
            response = self.client.get(reverse('index'))
            self.assertRedirects(response, '/map/')

        def test_profile_view_GET(self):
            """
            Test the profile view for a GET request.

            This test ensures that the profile view returns a 200 status code and uses the expected template.

            Test Steps:
            1. Make a GET request to the profile view.
            2. Check that the response status code is 200.
            3. Check that the response uses the 'profiles/edit_profile.html' template.

            Example:
            ```python
            def test_profile_view_GET(self):
                response = self.client.get(reverse('profile'))
                self.assertEqual(response.status_code, 200)
                self.assertTemplateUsed(response, 'profiles/edit_profile.html')
            ```
            """
            response = self.client.get(reverse('profile'))
            self.assertEqual(response.status_code, 200)
            self.assertTemplateUsed(response, 'profiles/edit_profile.html')

        def test_profile_view_POST_valid_form(self):
            """
            Test profile view for a POST request with a valid form.

            This test verifies that the profile view responds with a 302 status code,
            indicating a redirection after a successful form submission.

            Steps:
            1. Make a POST request to the profile view with a valid form.
            2. Check that the response status code is 302, indicating a redirect.

            """
            response = self.client.post(reverse('profile'), {'field_name': 'field_value'})
            self.assertEqual(response.status_code, 302)  # Redirect after successful form submission

        def test_profile_view_POST_invalid_form(self):
            """
            Test the profile view for a POST request with an invalid form.

            This test checks that when a POST request is made to the profile view with invalid form data,
            the view returns a 200 status code and displays the expected form error message.

            Test Steps:
            1. Make a POST request to the 'profile' view with invalid form data.
            2. Assert that the response status code is 200, indicating a successful request.
            3. Assert that the form used in the response has an error for the specified field ('field_name').
            4. Assert that the error message for the specified field is 'This field is required.'

            Example:
            ```
            response = self.client.post(reverse('profile'), {'invalid_field': 'invalid_value'})
            self.assertEqual(response.status_code, 200)
            self.assertFormError(response, 'form', 'field_name', 'This field is required.')
            ```
            """
            response = self.client.post(reverse('profile'), {'invalid_field': 'invalid_value'})
            self.assertEqual(response.status_code, 200)
            self.assertFormError(response, 'form', 'field_name', 'This field is required.')

        def test_login_user_view_GET(self):
            """
            Test the login user view for GET request.

            This test ensures that when a GET request is made to the login user view,
            it returns a 200 status code, indicating a successful response.
            Additionally, it checks that the view uses the expected template for rendering.

            Assertions:
            - The HTTP response status code should be 200 (OK).
            - The template used for rendering should be 'profiles/login_page.html'.

            Usage:
            Run this test to verify the behavior of the login user view when accessed with a GET request.
            """
            response = self.client.get(reverse('login_user'))
            self.assertEqual(response.status_code, 200)
            self.assertTemplateUsed(response, 'profiles/login_page.html')

        def test_login_user_view_POST_valid_credentials(self):
            """
            Test the login_user view with valid credentials using the POST method.

            This test case checks whether the login_user view correctly handles a POST request
            with valid credentials. The test client sends a POST request with a username and password
            to the login_user view using the reverse URL lookup. The expected behavior is a redirect
            status code (302) indicating a successful login.

            Args:
                None

            Returns:
                None

            Raises:
                AssertionError: If the response status code is not 302.

            Usage:
                Run this test as part of your Django TestCase class to ensure proper functionality
                of the login_user view with valid credentials.
            """
            response = self.client.post(reverse('login_user'), {'username': 'testuser', 'password': 'testpassword'})
            self.assertEqual(response.status_code, 302)  # Redirect after successful login

        def test_login_user_view_POST_invalid_credentials(self):
            """
            Test the login user view for a POST request with invalid credentials.

            This test verifies that when a POST request is made to the login_user view with
            incorrect credentials, the view responds with a 302 status code, indicating a
            redirect, and redirects the user to the login page.

            Returns:
                None

            Raises:
                AssertionError: If the response status code is not 302 or if the view does not
                redirect to the login page.
            """
            response = self.client.post(reverse('login_user'), {'username': 'testuser', 'password': 'wrongpassword'})
            self.assertEqual(response.status_code, 302)  # Redirect to login page

        def test_register_user_view_GET(self):
            """
            Test the register user view for a GET request.

            This test ensures that when a GET request is made to the register user view,
            the view returns a 200 status code and uses the expected template ('profiles/register_page.html').

            Test Steps:
            1. Use the Django test client to simulate a GET request to the register user view.
            2. Assert that the response status code is 200, indicating a successful request.
            3. Assert that the response uses the expected template ('profiles/register_page.html').

            This test verifies the initial rendering of the register user page.

            Usage:
            ```
            response = self.client.get(reverse('register_user'))
            self.assertEqual(response.status_code, 200)
            self.assertTemplateUsed(response, 'profiles/register_page.html')
            ```
            """
            response = self.client.get(reverse('register_user'))
            self.assertEqual(response.status_code, 200)
            self.assertTemplateUsed(response, 'profiles/register_page.html')

        def test_register_user_view_POST_valid_form(self):
            """
            Test the register user view for a POST request with a valid form.

            This test ensures that the register user view processes a POST request with a valid form
            and returns a 302 status code, indicating a successful registration and redirection.

            Method:
            1. Send a POST request to the register user view with valid registration data.
            2. Check that the response status code is 302, indicating a successful registration.
            """
            response = self.client.post(reverse('register_user'), {'username': 'newuser', 'password1': 'newpassword', 'password2': 'newpassword'})
            self.assertEqual(response.status_code, 302)  # Redirect after successful registration

        def test_register_user_view_POST_invalid_form(self):
            """
            Test the register user view for a POST request with a valid form.

            This test ensures that the register user view returns a 302 status code
            after successfully processing a valid registration form.

            Test Steps:
            1. Send a POST request to the register user view with valid form data.
            2. Assert that the response status code is 302, indicating a successful registration.
            3. Optionally, perform additional assertions based on your application's behavior.

            Usage:
            - Run this test method using a testing framework (e.g., Django's TestCase class).
            - Customize the form data to match your registration form's fields.
            - Update the reverse('register_user') to match the actual URL name for your register user view.
            - Add any additional assertions or checks based on your application's behavior.

            Example:
            ```
            response = self.client.post(reverse('register_user'), {'username': 'newuser', 'password1': 'newpassword', 'password2': 'newpassword'})
            self.assertEqual(response.status_code, 302)
            ```

            Returns:
            - None
            - Raises an AssertionError if the test fails.
            """
            response = self.client.post(reverse('register_user'), {'username': 'newuser', 'password1': 'password', 'password2': 'wrongpassword'})
            self.assertEqual(response.status_code, 200)
            self.assertFormError(response, 'form', 'password2', 'The two password fields didn’t match.')

        def test_logout_user_view(self):
            """
            Test the logout user view.

            Ensures that the logout user view returns a 302 status code after the user logs out.

            This test checks whether the user is redirected to another page (status code 302)
            after successfully logging out using the 'logout_user' view.

            Args:
                self: The test case instance.

            Returns:
                None

            Raises:
                AssertionError: If the status code returned by the view is not 302.

            Usage:
                Run this test to verify the behavior of the 'logout_user' view in your Django project.

            Example:
                ```
                def test_logout_user_view(self):
                    response = self.client.get(reverse('logout_user'))
                    self.assertEqual(response.status_code, 302)  # Redirect after logout
                ```
            """
            response = self.client.get(reverse('logout_user'))
            self.assertEqual(response.status_code, 302)  # Redirect after logout
            