from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from monitor.models import Location, Project, Team

INDEX_URL = reverse("monitor:index")
SIGNUP_URL = reverse("monitor:signup")
LOCATION_LIST_URL = reverse("monitor:location-list")
TEAM_LIST_URL = reverse("monitor:team-list")
PROJECT_LIST_URL = reverse("monitor:project-list")
TEAMMEMBER_LIST_URL = reverse("monitor:teammember-list")


class PublicAccessTests(TestCase):
    """Pages that require login should redirect anonymous users."""

    def test_index_login_required(self):
        response = self.client.get(INDEX_URL)
        self.assertNotEqual(response.status_code, 200)

    def test_location_list_login_required(self):
        response = self.client.get(LOCATION_LIST_URL)
        self.assertNotEqual(response.status_code, 200)

    def test_team_list_login_required(self):
        response = self.client.get(TEAM_LIST_URL)
        self.assertNotEqual(response.status_code, 200)

    def test_project_list_login_required(self):
        response = self.client.get(PROJECT_LIST_URL)
        self.assertNotEqual(response.status_code, 200)

    def test_teammember_list_login_required(self):
        response = self.client.get(TEAMMEMBER_LIST_URL)
        self.assertNotEqual(response.status_code, 200)

    def test_signup_page_is_public(self):
        response = self.client.get(SIGNUP_URL)
        self.assertEqual(response.status_code, 200)


class PrivateIndexTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="test_user", password="password123"
        )
        self.client.force_login(self.user)

    def test_index_page_loads(self):
        response = self.client.get(INDEX_URL)
        self.assertEqual(response.status_code, 200)

    def test_visit_counter_increments(self):
        self.client.get(INDEX_URL)
        response = self.client.get(INDEX_URL)
        self.assertEqual(response.context["num_visits"], 2)


class PrivateLocationTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="test_user", password="password123"
        )
        self.client.force_login(self.user)

    def test_retrieve_locations(self):
        Location.objects.create(country="Ukraine", city="Kyiv")
        Location.objects.create(country="Poland", city="Warsaw")

        response = self.client.get(LOCATION_LIST_URL)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            list(response.context["location_list"]),
            list(Location.objects.all()),
        )

    def test_retrieve_location_detail(self):
        location = Location.objects.create(country="Ukraine", city="Kyiv")

        response = self.client.get(
            reverse("monitor:location-detail", args=[location.slug])
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context["location"], location)

    def test_create_location(self):
        response = self.client.post(
            reverse("monitor:location-create"),
            data={"country": "Germany", "city": "Berlin"},
        )

        self.assertEqual(response.status_code, 302)
        self.assertTrue(Location.objects.filter(city="Berlin").exists())


class PrivateTeamTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="test_user", password="password123"
        )
        self.client.force_login(self.user)

    def test_retrieve_teams(self):
        Team.objects.create(name="Automation")
        Team.objects.create(name="Protection")

        response = self.client.get(TEAM_LIST_URL)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(list(response.context["team_list"]),
                         list(Team.objects.all()))

    def test_create_team(self):
        response = self.client.post(
            reverse("monitor:team-create"), data={"name": "Substations"}
        )

        self.assertEqual(response.status_code, 302)
        self.assertTrue(Team.objects.filter(name="Substations").exists())


class PrivateProjectTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="test_user", password="password123"
        )
        self.client.force_login(self.user)
        self.location = Location.objects.create(country="Ukraine", city="Kyiv")
        self.team = Team.objects.create(name="Automation")

    def test_retrieve_projects(self):
        Project.objects.create(
            name="Substation Upgrade",
            start_date="2026-01-01",
            progress_percent=50,
            payment_percent=30,
            location=self.location,
            team=self.team,
        )

        response = self.client.get(PROJECT_LIST_URL)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            list(response.context["project_list"]),
            list(Project.objects.all()),
        )

    def test_create_project(self):
        response = self.client.post(
            reverse("monitor:project-create"),
            data={
                "name": "Substation Upgrade",
                "start_date": "2026-01-01",
                "progress_percent": 10,
                "payment_percent": 5,
                "location": self.location.pk,
                "team": self.team.pk,
            },
        )

        self.assertEqual(response.status_code, 302)
        self.assertTrue(Project.objects.filter(
            name="Substation Upgrade").exists())


class PrivateTeamMemberTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="test_user", password="password123"
        )
        self.client.force_login(self.user)

    def test_retrieve_team_members(self):
        response = self.client.get(TEAMMEMBER_LIST_URL)

        self.assertEqual(response.status_code, 200)
        self.assertIn(self.user, response.context["teammember_list"])


class SignUpTests(TestCase):
    def test_signup_creates_user_and_logs_in(self):
        response = self.client.post(
            SIGNUP_URL,
            data={
                "username": "newmember",
                "password1": "x8Kj29fLpqw!",
                "password2": "x8Kj29fLpqw!",
                "first_name": "New",
                "last_name": "Member",
                "email": "new@example.com",
                "years_of_experience": 1,
                "role": "Engineer",
            },
        )

        self.assertEqual(response.status_code, 302)
        self.assertTrue(
            get_user_model().objects.filter(username="newmember").exists()
        )
        self.assertTrue(response.wsgi_request.user.is_authenticated)
