from django.test import TestCase
from django.urls import reverse



class ManifestTestCase(TestCase):
    """Basic tests of the manifest"""
    
    def setUp(self) -> None:
        """Get the url and create a user"""
        self.url = reverse("django_accounts_api:manifest")
        return super().setUp()

    def testGetMainfest(self):
        """An unauthed get should get a 200 with a form"""
        response = self.client.get(self.url)
        assert response.status_code == 200
        assert "check" in response.json()
        assert "login" in response.json()
        assert "logout" in response.json()
        assert "password_change" in response.json()
