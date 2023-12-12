from django.contrib.auth.models import User
from .models import Group
from django.test import TestCase, Client
from django.urls import reverse
from .forms import GroupForm


class GroupModelTest(TestCase):
    def setUp(self):
        # Create a sample user for testing
        self.user = User.objects.create_user(username='testuser', password='testpassword')


    def test_group_creation(self):
        """Test if a Group can be created."""
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
        """Test the string representation (__str__) of the Group."""
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
    def setUp(self):
        # Create a test user
        self.user = User.objects.create_user(username='testuser', password='testpassword')

        # Create test groups
        self.group1 = Group.objects.create(name='Group 1', creator=self.user)
        self.group2 = Group.objects.create(name='Group 2', creator=self.user)

        # Create a client for making requests
        self.client = Client()

    def test_group_list_view_with_authenticated_user(self):
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
        # Make a GET request to the group_list view without logging in
        response = self.client.get(reverse('group_list'))

        # Check that the response status code is 302 (Redirect)
        self.assertEqual(response.status_code, 302)

        # Check that the user is redirected to the login page
        self.assertRedirects(response, f'/accounts/login/?next={reverse("group_list")}')

    def test_group_detail_view_with_authenticated_user(self):
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
        # Log in the user
        self.client.login(username='testuser', password='testpassword')

        # Access the join_group view with a valid group_id
        response = self.client.get(reverse('join_group', args=[self.group1.id]))

        # Check that the user is added to the group's members
        self.assertEqual(response.status_code, 302)  # Redirect status code
        self.assertIn(self.user, self.group1.members.all())
        self.assertRedirects(response, reverse('user_group_list'))


    def test_join_group_view_already_member(self):
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
        # Access the join_group view without logging in
        response = self.client.get(reverse('join_group', args=[self.group1.id]))

        # Check that the user is redirected to the login page
        self.assertEqual(response.status_code, 302)  # Redirect status code
        self.assertRedirects(response, f'/accounts/login/?next={reverse("join_group", args=[self.group1.id])}')


    def test_delete_group_view(self):
        # Log in the user
        self.client.login(username='testuser', password='testpassword')

        # Access the delete_group view with a valid group_id
        response = self.client.get(reverse('delete_group', args=[self.group1.id]))

        # Check that the group is deleted successfully
        self.assertEqual(response.status_code, 302)  # Redirect status code
        self.assertEqual(Group.objects.count(), 1)  # One group is deleted
        self.assertRedirects(response, reverse('group_list'))


    def test_delete_group_view_unauthorized_user(self):
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
    def setUp(self):
        # Create a test user
        self.user = User.objects.create_user(username='testuser', password='testpassword')

        # Create a test group
        self.group = Group.objects.create(name='Test Group', creator=self.user)
        self.group.members.add(self.user)

        # Create a client for making requests
        self.client = Client()

    def test_update_group_view_with_authenticated_user_and_creator(self):
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
        # Create another user
        another_user = User.objects.create_user(username='anotheruser', password='anotherpassword')

        # Log in the other user
        self.client.login(username='anotheruser', password='anotherpassword')

        # Access the update_group view with another user who is not the creator
        response = self.client.get(reverse('update_group', args=[self.group.id]))

        # Check that the response status code is 404 (Not Found)
        self.assertEqual(response.status_code, 404)

    def test_leave_group_view_with_authenticated_user_and_member(self):
        # Log in the test user
        self.client.login(username='testuser', password='testpassword')

        # Access the leave_group view
        response = self.client.post(reverse('leave_group', args=[self.group.id]))

        # Check that the user is removed from the group's members
        self.assertFalse(self.group.members.filter(id=self.user.id).exists())

        # Check that the response redirects to the user's group list
        self.assertRedirects(response, reverse('user_group_list'))
        