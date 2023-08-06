from django.forms import Form
from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model

User = get_user_model()


class PasswordChangeTestCase(TestCase):
    """Basic tests of the partial HTML password change view"""
    
    def setUp(self) -> None:
        """Get the url and create a user"""
        self.url = reverse("django_accounts_api:password_change")
        self.user = User.objects.create_user("test", password="test")
        return super().setUp()

    def testGetPasswordChange(self):
        """An unauthed get should get a 200 with a form"""
        response = self.client.get(self.url)
        assert response.status_code == 200
        assert "form" in response.context

    def testPostPasswordChange_unathenticated(self):
        """An unauthed post should get a 401"""
        response = self.client.post(self.url)
        assert response.status_code == 401

    def testPostPasswordChange_authenticated(self):
        """An authed post should get a 200"""
        self.client.force_login(self.user)
        response = self.client.post(self.url)
        assert response.status_code == 200
        assert len(response.context["form"].errors) == 3