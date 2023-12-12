"""
Tests for the Group model and related views.

These tests cover the creation and behavior of the Group model, as well as the views
associated with group management, listing, and detail.

GroupModelTest:
- test_group_creation: Test if a Group can be created successfully.
- test_group_str_method: Test the string representation (__str__) of the Group.

GroupListViewTests:
- test_group_list_view_with_authenticated_user: Test the group list view with an authenticated user.
- test_group_list_view_with_unauthenticated_user: Test the group list view with an unauthenticated user.
- test_group_detail_view_with_authenticated_user: Test the group detail view with an authenticated user.
- test_create_group_view_rendered_correctly: Test the create_group view for correct rendering.
- test_create_group_successfully: Test creating a group successfully.
- test_create_group_invalid_form: Test creating a group with an invalid form.
- test_join_group_view: Test joining a group successfully.
- test_join_group_view_already_member: Test joining a group when already a member.
- test_join_group_view_unauthenticated_user: Test joining a group with an unauthenticated user.
- test_delete_group_view: Test deleting a group successfully.
- test_delete_group_view_unauthorized_user: Test deleting a group with an unauthorized user.

GroupDetailViewTests:
- test_update_group_view_with_authenticated_user_and_creator: Test updating a group with the authenticated creator.
- test_update_group_view_with_authenticated_user_and_not_creator: Test updating a group with an authenticated user who is not the creator.
- test_leave_group_view_with_authenticated_user_and_member: Test leaving a group with an authenticated user who is a member.
"""

from django.contrib.auth.models import User
from .models import Group
from django.test import TestCase, Client
from django.urls import reverse
from .forms import GroupForm


class GroupModelTest(TestCase):
    def tearDown(self):
        """
        Clean up the database after each test.

        This method is called after each test case and is responsible for cleaning up the
        database by deleting all Group and User objects created during the test. It ensures
        that the test environment is reset to a clean state, preventing interference between
        different tests.

        Usage:
        This method is automatically called by the Django test runner after each test case.
        You do not need to manually invoke it in your test cases.

        Example:
        ```python
        class YourTestCase(TestCase):
            def setUp(self):
                # Your test setup code

            def test_example(self):
                # Your test logic

            def tearDown(self):
                # Clean up is handled automatically after each test
        ```

        Note:
        - This method is part of the TestCase class provided by the Django testing framework.
        - It uses the `Group.objects.all().delete()` and `User.objects.all().delete()` methods
        to delete all instances of the Group and User models in the database.

        """
        Group.objects.all().delete()
        User.objects.all().delete()
        
        
    def setUp(self):
        """
        Set up a sample user for testing.

        This method is called before each test case to create a sample user for testing purposes.
        The user is created using the Django `User.objects.create_user` method with a predefined
        username ('testuser') and password ('testpassword'). This user can be used in various test
        cases to simulate scenarios involving authenticated users.

        Usage:
        In your test methods, you can access the created user using `self.user`.

        Example:
        ```python
        def test_example(self):
            # Access the sample user
            user = self.user

            # Your test logic using the sample user
            # ...
        ```

        Note:
        It's recommended to create any additional objects or perform any setup required for your
        specific test case within the respective test methods to maintain isolation between tests.

        """
        self.user = User.objects.create_user(username='testuser', password='testpassword')


    def test_group_creation(self):
        """
        Test the creation of a Group instance.

        Creates a sample Group instance and checks if the attributes are set correctly.

        Assertions:
        - Checks if the group name, description, tags, creator, place, latitude, and longitude
        are set as expected.

        Example Usage:
        ```
        # Create a sample user
        user = User.objects.create_user(username='testuser', password='testpassword')

        # Set up the test case with the user
        self.client.force_login(user)

        # Run the test to create a sample Group instance
        self.test_group_creation()
        ```
        """
        group = Group.objects.create(
            name='Sample Group',
            description='Sample description',
            tags='sample, group',
            creator=self.user,
            place='New York',
            latitude=40.7128,
            longitude=-74.0060
        )

        # Check if the group was created successfully
        self.assertEqual(group.name, 'Sample Group')
        self.assertEqual(group.description, 'Sample description')
        self.assertEqual(group.tags, 'sample, group')
        self.assertEqual(group.creator, self.user)
        self.assertEqual(group.place, 'New York')
        self.assertEqual(group.latitude, 40.7128)
        self.assertEqual(group.longitude, -74.0060)


    def test_group_str_method(self):
        """
        Test the string representation (__str__) of the Group model.

        This test case creates a sample Group object and checks if the __str__ method
        returns the expected string representation, which should be the group's name.

        Test Steps:
        1. Create a sample Group object with specific attributes.
        2. Call the __str__ method on the Group object.
        3. Assert that the returned string matches the expected name of the group.

        Example:
        ```python
        def test_group_str_method(self):
            group = Group.objects.create(
                name='Sample Group',
                description='Sample description',
                tags='sample, group',
                creator=self.user,
                place='New York',
                latitude=40.7128,
                longitude=-74.0060
            )

            # Check if __str__ returns the group's name
            self.assertEqual(str(group), 'Sample Group')
        ```
        """
        group = Group.objects.create(
            name='Sample Group',
            description='Sample description',
            tags='sample, group',
            creator=self.user,
            place='New York',
            latitude=40.7128,
            longitude=-74.0060
        )

        # Check if __str__ returns the group's name
        self.assertEqual(str(group), 'Sample Group')


class GroupListViewTests(TestCase):
    def tearDown(self):
        """
        Clean up the database after each test.

        This method is called after each test case and is responsible for cleaning up the
        database by deleting all Group and User objects created during the test. It ensures
        that the test environment is reset to a clean state, preventing interference between
        different tests.

        Usage:
        This method is automatically called by the Django test runner after each test case.
        You do not need to manually invoke it in your test cases.

        Example:
        ```python
        class YourTestCase(TestCase):
            def setUp(self):
                # Your test setup code

            def test_example(self):
                # Your test logic

            def tearDown(self):
                # Clean up is handled automatically after each test
        ```

        Note:
        - This method is part of the TestCase class provided by the Django testing framework.
        - It uses the `Group.objects.all().delete()` and `User.objects.all().delete()` methods
        to delete all instances of the Group and User models in the database.

        """
        Group.objects.all().delete()
        User.objects.all().delete()
    
    
    def setUp(self):
        """
        Set up the initial state for testing.

        This method is called before each test case. It creates a test user, two test groups,
        and a client for making requests.

        Attributes:
            user (User): A test user created using `User.objects.create_user`.
            group1 (Group): The first test group created using `Group.objects.create`.
            group2 (Group): The second test group created using `Group.objects.create`.
            client (Client): An instance of Django's test client (`Client`) for making requests.

        Usage:
            Override this method in your test class to set up any necessary fixtures or
            preconditions for your test cases.

        Example:
            ```python
            def setUp(self):
                # Custom setup logic
                # ...
                super().setUp()
            ```
        """
        # Create a test user
        self.user = User.objects.create_user(username='testuser', password='testpassword')

        # Create test groups
        self.group1 = Group.objects.create(name='Group 1', creator=self.user)
        self.group2 = Group.objects.create(name='Group 2', creator=self.user)

        # Create a client for making requests
        self.client = Client()


    def test_group_list_view_with_authenticated_user(self):
        """
        Test the group_list view with an authenticated user.

        This test case verifies that the group_list view returns a status code of 200 (OK) and
        contains the expected groups when accessed by an authenticated user.

        Steps:
        1. Log in the test user using the Django test client.
        2. Make a GET request to the group_list view.
        3. Check that the response status code is 200.
        4. Check that the response contains the names of the expected groups (e.g., 'Group 1', 'Group 2').

        This test ensures that the group_list view works correctly and displays the appropriate groups
        when accessed by an authenticated user.

        Args:
            None

        Returns:
            None
        """
        # Log in the test user
        self.client.login(username='testuser', password='testpassword')

        # Make a GET request to the group_list view
        response = self.client.get(reverse('group_list'))

        # Check that the response status code is 200 (OK)
        self.assertEqual(response.status_code, 200)

        # Check that the response contains the expected groups
        self.assertContains(response, 'Group 1')
        self.assertContains(response, 'Group 2')


    def test_group_list_view_with_unauthenticated_user(self):
        """
        Test the behavior of the group_list view when accessed by an unauthenticated user.

        The test performs the following steps:
        1. Sends a GET request to the group_list view without logging in.
        2. Asserts that the response status code is 302 (Redirect).
        3. Asserts that the user is redirected to the login page, including the correct 'next' parameter.

        This test is designed to ensure that unauthenticated users are redirected to the login page
        when attempting to access the group_list view, and the 'next' parameter correctly captures
        the original requested URL.

        Usage:
        - Run this test as part of a Django TestCase for testing view behavior.
        - Ensure that the 'reverse' function is correctly used to generate the expected login URL.
        """
        response = self.client.get(reverse('group_list'))

        # Check that the response status code is 302 (Redirect)
        self.assertEqual(response.status_code, 302)

        # Check that the user is redirected to the login page with the correct 'next' parameter
        self.assertRedirects(response, f'/accounts/login/?next={reverse("group_list")}')
        
        # Make a GET request to the group_list view without logging in
        response = self.client.get(reverse('group_list'))

        # Check that the response status code is 302 (Redirect)
        self.assertEqual(response.status_code, 302)

        # Check that the user is redirected to the login page
        self.assertRedirects(response, f'/accounts/login/?next={reverse("group_list")}')


    def test_group_detail_view_with_authenticated_user(self):
        """
        Test the group detail view for an authenticated user.

        This test function logs in a user, accesses the group detail view, and checks that:
        - The response status code is 200 (OK).
        - The correct group is present in the context.
        - The rendered HTML contains the group's name.

        Args:
            self: The test case instance.

        Returns:
            None: This test function does not return any value.

        Raises:
            AssertionError: If any of the test conditions fail.
        """
        # Log in the user
        self.client.login(username='testuser', password='testpassword')

        # Access the group detail view
        response = self.client.get(reverse('group_detail', args=[self.group1.id]))

        # Check that the response status code is 200 (OK)
        self.assertEqual(response.status_code, 200)

        # Check that the correct group is present in the context
        self.assertEqual(response.context['group'], self.group1)

        # Check that the rendered HTML contains the group's name
        self.assertContains(response, self.group1.name)


    def test_create_group_view_rendered_correctly(self):
        """
        Test that the create_group view is rendered correctly.

        This test case logs in a user, accesses the create_group view using the client,
        and checks that the view is rendered with the expected status code, template,
        form presence, and form type.

        Steps:
        1. Log in the user with the provided username and password.
        2. Access the create_group view using the client.
        3. Check that the view returns a status code of 200 (OK).
        4. Check that the correct template, 'groups/create_group.html', is used.
        5. Check that the response contains an HTML form element.
        6. Check that the context variable 'form' in the response is an instance of the GroupForm.

        Note: Replace 'testuser' and 'testpassword' with valid username and password for an existing user.
        """
        # Log in the user
        self.client.login(username='testuser', password='testpassword')

        # Access the create_group view using the client
        response = self.client.get(reverse('create_group'))

        # Check that the view is rendered correctly
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'groups/create_group.html')
        self.assertContains(response, '<form')
        self.assertIsInstance(response.context['form'], GroupForm)


    def test_create_group_successfully(self):
        """
        Test the successful creation of a group through the create_group view.

        Steps:
        1. Log in the user with valid credentials.
        2. Prepare valid form data for creating a new group.
        3. Access the create_group view with a valid POST request using the prepared form data.
        4. Check that the view responds with a redirect status code (302).
        5. Verify that the number of Group objects in the database has increased by 1.
        6. Retrieve the newly created group from the database.
        7. Check that the group attributes match the provided form data.
        8. Ensure that the creator of the group is the logged-in user.
        9. Confirm that the group has one member, which is the creator.
        
        This test case covers the scenario where a user successfully creates a group through the
        create_group view by providing valid form data. It ensures that the group is stored in the
        database with the correct attributes and that the creator is automatically added as a member.

        Note: This test assumes the existence of a logged-in user ('testuser') and other groups
        (self.group1 and self.group2) that might be present in the database before running the test.
        """
        # Log in the user
        self.client.login(username='testuser', password='testpassword')

        # Prepare valid form data
        form_data = {
            'name': 'Test Group',
            'description': 'This is a test group',
            'tags': 'tag1, tag2',
            'place': 'Test Place',
            'latitude': 40.7128,
            'longitude': -74.0060,
        }

        # Access the create_group view with a valid POST request
        response = self.client.post(reverse('create_group'), data=form_data)

        # Check that the group is created successfully
        self.assertEqual(response.status_code, 302)  # Redirect status code
        self.assertEqual(Group.objects.count(), 3)  # Updated count for multiple tests
        new_group = Group.objects.exclude(id__in=[self.group1.id, self.group2.id]).first()
        self.assertEqual(new_group.name, 'Test Group')
        self.assertEqual(new_group.description, 'This is a test group')
        self.assertEqual(new_group.creator, self.user)
        self.assertEqual(new_group.members.count(), 1)
        self.assertIn(self.user, new_group.members.all())


    def test_create_group_invalid_form(self):
        """
        Test the create_group view with an invalid form submission.

        This test logs in the user, attempts to create a group by sending an invalid
        POST request to the create_group view, and checks that the form is not valid
        and the view is re-rendered.

        Steps:
        1. Log in the user with the credentials 'testuser' and 'testpassword'.
        2. Access the create_group view by sending an invalid POST request (empty data).
        3. Check that the response status code is 200 (OK).
        4. Check that the 'groups/create_group.html' template is used for rendering.
        5. Check that the HTML response contains a form.
        6. Check that the context contains an instance of the GroupForm.
        7. Check that the HTML response contains the error message 'This field is required.'

        This test ensures that the create_group view correctly handles invalid form submissions
        by re-rendering the form with appropriate error messages.

        Dependencies:
        - This test assumes the existence of a GroupForm for group creation.

        Usage:
        Run this test using a testing framework like Django's TestCase class.
        """
        # Log in the user
        self.client.login(username='testuser', password='testpassword')

        # Access the create_group view with an invalid POST request
        response = self.client.post(reverse('create_group'), data={})

        # Check that the form is not valid and the view is re-rendered
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'groups/create_group.html')
        self.assertContains(response, '<form')
        self.assertIsInstance(response.context['form'], GroupForm)
        self.assertContains(response, 'This field is required.')  # Example error message


    def test_join_group_view(self):
        """
        Test the behavior of the join_group view.

        This test case checks the following scenarios:
        1. Log in the user with valid credentials.
        2. Access the join_group view with a valid group_id.
        3. Verify that the user is added to the group's members.
        4. Confirm that the response status code is a redirect (302).
        5. Ensure redirection to the user_group_list view.

        Returns:
            None: This test function does not return any value but raises AssertionError if the tests fail.
        """
        # Log in the user
        self.client.login(username='testuser', password='testpassword')

        # Access the join_group view with a valid group_id
        response = self.client.get(reverse('join_group', args=[self.group1.id]))

        # Check that the user is added to the group's members
        self.assertEqual(response.status_code, 302)  # Redirect status code
        self.assertIn(self.user, self.group1.members.all())
        self.assertRedirects(response, reverse('user_group_list'))


    def test_join_group_view_already_member(self):
        """
        Test the join_group view when the user is already a member of the group.

        Steps:
        1. Log in the user with credentials 'testuser' and 'testpassword'.
        2. Add the user to the group (`self.group1`).
        3. Access the join_group view with a valid group_id (`self.group1.id`).
        4. Check that the user is not added again to the group.
        - Assert that the response status code is 302 (Redirect).
        - Assert that the group members count remains 1 (No duplicate entries).
        - Assert that the response redirects to the 'user_group_list' URL.

        This test ensures that attempting to join a group when the user is already a member
        does not result in duplicate entries and correctly redirects to the user's group list.
        """
        # Log in the user
        self.client.login(username='testuser', password='testpassword')

        # Add the user to the group
        self.group1.members.add(self.user)

        # Access the join_group view with a valid group_id
        response = self.client.get(reverse('join_group', args=[self.group1.id]))

        # Check that the user is not added again
        self.assertEqual(response.status_code, 302)  # Redirect status code
        self.assertEqual(self.group1.members.count(), 1)  # No duplicate entries
        self.assertRedirects(response, reverse('user_group_list'))


    def test_join_group_view_unauthenticated_user(self):
        """
        Test the behavior of the join_group view when an unauthenticated user tries to access it.

        The test simulates an unauthenticated user attempting to join a group by accessing the join_group view.
        The expected behavior is a redirect to the login page, and the test checks whether the response status code is
        302 (redirect) and verifies that the redirection URL includes the next parameter pointing to the join_group page.

        Args:
            self: The TestCase instance.

        Returns:
            None: The test asserts the expected behavior.

        Usage:
            Run this test case using a Django test runner to ensure that the join_group view behaves correctly for
            unauthenticated users.
        """
        # Access the join_group view without logging in
        response = self.client.get(reverse('join_group', args=[self.group1.id]))

        # Check that the user is redirected to the login page
        self.assertEqual(response.status_code, 302)  # Redirect status code
        self.assertRedirects(response, f'/accounts/login/?next={reverse("join_group", args=[self.group1.id])}')


    def test_delete_group_view(self):
        """
        Test the delete_group view.

        This test checks whether the delete_group view correctly deletes a group when accessed by an authenticated user
        and redirects them to the group_list view after deletion.

        Steps:
        1. Log in the user using the client's login method.
        2. Access the delete_group view by making a GET request with a valid group_id (self.group1.id).
        3. Verify that the response status code is a redirect (302).
        4. Verify that the total number of groups in the database is reduced by 1 after the deletion.
        5. Verify that the response redirects to the group_list view using assertRedirects.

        Args:
            self: The test case instance.

        Returns:
            None
        """
        # Log in the user
        self.client.login(username='testuser', password='testpassword')

        # Access the delete_group view with a valid group_id
        response = self.client.get(reverse('delete_group', args=[self.group1.id]))

        # Check that the group is deleted successfully
        self.assertEqual(response.status_code, 302)  # Redirect status code
        self.assertEqual(Group.objects.count(), 1)  # One group is deleted
        self.assertRedirects(response, reverse('group_list'))


    def test_delete_group_view_unauthorized_user(self):
        """
        Test the delete_group view when an unauthorized user attempts to delete a group.

        The test scenario involves creating a new user, logging in with the created user,
        and attempting to access the delete_group view with a valid group_id. The expected
        behavior is that the unauthorized user should not be allowed to delete the group,
        resulting in a 404 (Not Found) status code and no groups being deleted.

        Test Steps:
        1. Create a new user with username 'unauthorized' and password 'unauthorizedpass'.
        2. Log in the unauthorized user.
        3. Attempt to access the delete_group view with a valid group_id (self.group1.id).
        4. Verify that the response status code is 404 (Not Found).
        5. Verify that no groups are deleted (Group.objects.count() should remain the same).

        """
        # Create a new user
        unauthorized_user = User.objects.create_user(username='unauthorized', password='unauthorizedpass')

        # Log in the unauthorized user
        self.client.login(username='unauthorized', password='unauthorizedpass')

        # Access the delete_group view with a valid group_id
        response = self.client.get(reverse('delete_group', args=[self.group1.id]))

        # Check that the user is not allowed to delete the group
        self.assertEqual(response.status_code, 404)  # Not Found status code
        self.assertEqual(Group.objects.count(), 2)  # No groups are deleted
        

class GroupDetailViewTests(TestCase):
    """
    Test case for the views related to group details.

    This class includes tests for the 'update_group' and 'leave_group' views.

    Test Functions:
    - `test_update_group_view_with_authenticated_user_and_creator`: 
        Test if an authenticated user and the creator of the group can access the 'update_group' view successfully.
    - `test_update_group_view_with_authenticated_user_and_not_creator`: 
        Test if an authenticated user who is not the creator of the group receives a 404 response when trying to access the 'update_group' view.
    - `test_leave_group_view_with_authenticated_user_and_member`: 
        Test if an authenticated user who is a member of the group can successfully leave the group.

    Note: The `tearDown` method is used to clean up the database after each test by deleting all groups and users.
    """
    def tearDown(self):
        # Clean up the database after each test
        Group.objects.all().delete()
        User.objects.all().delete()
    
    
    def setUp(self):
        # Create a test user
        self.user = User.objects.create_user(username='testuser', password='testpassword')

        # Create a test group
        self.group = Group.objects.create(name='Test Group', creator=self.user)
        self.group.members.add(self.user)

        # Create a client for making requests
        self.client = Client()


    def test_update_group_view_with_authenticated_user_and_creator(self):
        """
        Test the 'update_group' view when an authenticated user, who is also the creator of the group, accesses the view.

        Steps:
        1. Log in the test user with valid credentials.
        2. Access the 'update_group' view with the ID of the test group.
        3. Check that the response status code is 200 (OK).
        4. Check that the correct group is present in the context.
        5. Check that the view is rendered with the correct template ('groups/update_group.html').

        Expected Behavior:
        - The test user should be able to access the 'update_group' view.
        - The response status code should be 200.
        - The correct group should be available in the context.
        - The view should be rendered using the 'groups/update_group.html' template.

        Note: This test assumes the existence of the 'update_group' view, the 'Group' model, and the specified template.
        Make sure to customize the view name and template path based on your actual implementation.
        """
        # Log in the test user
        self.client.login(username='testuser', password='testpassword')

        # Access the update_group view
        response = self.client.get(reverse('update_group', args=[self.group.id]))

        # Check that the response status code is 200 (OK)
        self.assertEqual(response.status_code, 200)

        # Check that the correct group is present in the context
        self.assertEqual(response.context['group'], self.group)

        # Check that the view is rendered with the correct template
        self.assertTemplateUsed(response, 'groups/update_group.html')


    def test_update_group_view_with_authenticated_user_and_not_creator(self):
        """
        Test the update_group view when an authenticated user (not the creator) attempts to access it.

        Steps:
        1. Create another user.
        2. Log in with the newly created user.
        3. Attempt to access the update_group view for a group created by a different user.
        4. Verify that the response status code is 404 (Not Found).

        This test ensures that an authenticated user who is not the creator of the group
        cannot access the update_group view for groups they did not create.

        Args:
            self: The test case instance.

        Returns:
            None: This test does not return anything.

        Raises:
            AssertionError: If the response status code is not 404.

        Usage:
            Run this test to ensure that the update_group view correctly restricts access
            to authenticated users who are not the creators of the group.
        """
        # Create another user
        another_user = User.objects.create_user(username='anotheruser', password='anotherpassword')

        # Log in the other user
        self.client.login(username='anotheruser', password='anotherpassword')

        # Access the update_group view with another user who is not the creator
        response = self.client.get(reverse('update_group', args=[self.group.id]))

        # Check that the response status code is 404 (Not Found)
        self.assertEqual(response.status_code, 404)


    def test_leave_group_view_with_authenticated_user_and_member(self):
        """
        Test the leave_group view with an authenticated user who is a member of the group.

        Steps:
        1. Log in the test user.
        2. Access the leave_group view by sending a POST request.
        3. Check that the user is removed from the group's members.
        4. Check that the response redirects to the user's group list.

        Returns:
            None: This test function doesn't return any value.

        Raises:
            AssertionError: If any of the test conditions fail.

        Dependencies:
            - This test assumes the existence of an authenticated user named 'testuser' with password 'testpassword'.
            - The 'self.group' variable should represent a valid group object with an associated user membership.

        Usage:
            Call this test function using a testing framework such as Django's TestCase.
            Example: `python manage.py test your_app.tests.TestGroupViews.test_leave_group_view_with_authenticated_user_and_member`
        """
        # Log in the test user
        self.client.login(username='testuser', password='testpassword')

        # Access the leave_group view
        response = self.client.post(reverse('leave_group', args=[self.group.id]))

        # Check that the user is removed from the group's members
        self.assertFalse(self.group.members.filter(id=self.user.id).exists())

        # Check that the response redirects to the user's group list
        self.assertRedirects(response, reverse('user_group_list'))