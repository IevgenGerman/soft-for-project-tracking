from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from monitor.models import Language, Location, Project, Team


class AdminAccessTests(TestCase):
    def setUp(self):
        self.admin_user = get_user_model().objects.create_superuser(
            username="admin", email="admin@example.com", password="x8Kj29!"
        )
        self.client.force_login(self.admin_user)

    def test_location_listed(self):
        location = Location.objects.create(country="Ukraine", city="Kyiv")
        url = reverse("admin:monitor_location_changelist")

        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, location.city)
        self.assertContains(response, location.country)

    def test_location_slug_hidden_on_add_page(self):
        url = reverse("admin:monitor_location_add")

        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertNotContains(response, 'name="slug"')

    def test_team_listed(self):
        team = Team.objects.create(name="Automation")
        url = reverse("admin:monitor_team_changelist")

        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, team.name)

    def test_project_listed(self):
        location = Location.objects.create(country="Ukraine", city="Kyiv")
        team = Team.objects.create(name="Automation")
        project = Project.objects.create(
            name="Substation Upgrade",
            start_date="2026-01-01",
            progress_percent=50,
            payment_percent=30,
            location=location,
            team=team,
        )
        url = reverse("admin:monitor_project_changelist")

        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, project.name)

    def test_language_listed(self):
        language = Language.objects.create(name="English")
        url = reverse("admin:monitor_language_changelist")

        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, language.name)

    def test_teammember_listed(self):
        url = reverse("admin:monitor_teammember_changelist")

        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.admin_user.username)

    def test_teammember_add_page_shows_team_info_fields(self):
        url = reverse("admin:monitor_teammember_add")

        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'name="role"')
        self.assertContains(response, 'name="years_of_experience"')
        self.assertContains(response, 'name="license_number"')

    def test_teammember_change_page_shows_team_info_fields(self):
        url = reverse("admin:monitor_teammember_change", args=[self.admin_user.pk])

        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'name="role"')
        self.assertContains(response, 'name="license_number"')


class AdminAccessDeniedForRegularUserTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="regular", password="password123"
        )
        self.client.force_login(self.user)

    def test_non_staff_user_cannot_access_admin(self):
        url = reverse("admin:monitor_location_changelist")

        response = self.client.get(url)

        self.assertNotEqual(response.status_code, 200)
