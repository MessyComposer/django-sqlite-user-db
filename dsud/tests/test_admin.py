from django.contrib import admin
from django.test import TestCase
from django.urls import reverse
from dsud.admin import UserAdmin
from dsud.templatetags.user_filters import user_id_to_username
from django.contrib.auth import get_user_model

User = get_user_model()


class TestAdmin(TestCase):
    def setUp(self):
        self.credentials = {"id": 1337, "username": "user_1337", "password": "secret"}
        self.user = User.objects.create_user(**self.credentials)
        self.admin_user = User.objects.create_superuser("admin", "password")
        
    def test_set_user(self):
        self.client.force_login(self.admin_user)
        response = self.client.get(reverse('dsud:set_user'), {'user_id': self.user.id})
        self.assertEqual(self.client.session['admin_user_id'], str(self.user.id))
        self.assertEqual(response.status_code, 302)

    def test_unset_user(self):
        self.client.force_login(self.admin_user)
        response = self.client.get(reverse('dsud:unset_user'))
        self.assertNotIn('admin_user_id', self.client.session)
        self.assertEqual(response.status_code, 302)

    def test_switch_user_button(self):
        user_admin = UserAdmin(User, admin.site)
        button_html = user_admin.switch_user_button(self.user)
        expected_url = reverse('dsud:set_user') + f'?user_id={self.user.id}'
        self.assertIn(expected_url, button_html)
        self.assertIn('Switch User', button_html)

    def test_user_id_to_username(self):
        username = user_id_to_username(self.user.id)
        self.assertEqual(username, self.user.username)
        
        username = user_id_to_username(-1)
        self.assertEqual(username, 'Unknown User')
    
    