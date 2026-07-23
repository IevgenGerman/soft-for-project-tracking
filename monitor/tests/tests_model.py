from django.test import TestCase

from monitor.models import Language, Location, Project, Team, TeamMember


class LocationModelTests(TestCase):
    def setUp(self):
        self.location = Location.objects.create(country="Ukraine", city="Kyiv")

    def test_str(self):
        self.assertEqual(str(self.location), "Kyiv, Ukraine")

    def test_slug_is_generated_on_save(self):
        self.assertEqual(self.location.slug, "kyiv-ukraine")

    def test_existing_slug_is_not_overwritten(self):
        self.location.slug = "custom-slug"
        self.location.save()
        self.assertEqual(self.location.slug, "custom-slug")

    def test_get_absolute_url(self):
        expected = f"/locations/{self.location.slug}/"
        self.assertEqual(self.location.get_absolute_url(), expected)


class TeamModelTests(TestCase):
    def setUp(self):
        self.team = Team.objects.create(name="Automation")

    def test_str(self):
        self.assertEqual(str(self.team), "Automation")

    def test_slug_is_generated_on_save(self):
        self.assertEqual(self.team.slug, "automation")

    def test_get_absolute_url(self):
        expected = f"/teams/{self.team.slug}/"
        self.assertEqual(self.team.get_absolute_url(), expected)

    def test_name_must_be_unique(self):
        with self.assertRaises(Exception):
            Team.objects.create(name="Automation")


class LanguageModelTests(TestCase):
    def test_str(self):
        language = Language.objects.create(name="English")
        self.assertEqual(str(language), "English")


class ProjectModelTests(TestCase):
    def setUp(self):
        self.location = Location.objects.create(country="Ukraine", city="Kyiv")
        self.team = Team.objects.create(name="Automation")
        self.project = Project.objects.create(
            name="Substation Upgrade",
            start_date="2026-01-01",
            progress_percent=50,
            payment_percent=30,
            location=self.location,
            team=self.team,
        )

    def test_str(self):
        self.assertEqual(str(self.project), "Substation Upgrade")

    def test_slug_is_generated_on_save(self):
        self.assertEqual(self.project.slug, "substation-upgrade")

    def test_get_absolute_url(self):
        expected = f"/projects/{self.project.slug}/"
        self.assertEqual(self.project.get_absolute_url(), expected)

    def test_project_appears_in_location_projects(self):
        self.assertIn(self.project, self.location.projects.all())

    def test_project_appears_in_team_projects(self):
        self.assertIn(self.project, self.team.projects.all())


class TeamMemberModelTests(TestCase):
    def setUp(self):
        self.team = Team.objects.create(name="Automation")
        self.member = TeamMember.objects.create(
            username="jdoe",
            first_name="John",
            last_name="Doe",
            role="Engineer",
            team=self.team,
        )

    def test_str(self):
        self.assertEqual(str(self.member), "jdoe (John Doe)")

    def test_slug_is_generated_on_save(self):
        self.assertEqual(self.member.slug, "jdoe")

    def test_get_absolute_url(self):
        expected = f"/team-members/{self.member.slug}/"
        self.assertEqual(self.member.get_absolute_url(), expected)

    def test_years_of_experience_defaults_to_zero(self):
        self.assertEqual(self.member.years_of_experience, 0)

    def test_team_can_be_null(self):
        member = TeamMember.objects.create(username="nomember", role="Sales")
        self.assertIsNone(member.team)

    def test_member_appears_in_team_members(self):
        self.assertIn(self.member, self.team.members.all())

    def test_team_deletion_sets_member_team_to_null(self):
        self.team.delete()
        self.member.refresh_from_db()
        self.assertIsNone(self.member.team)

    def test_languages_can_be_assigned(self):
        english = Language.objects.create(name="English")
        self.member.languages.add(english)
        self.assertIn(english, self.member.languages.all())
