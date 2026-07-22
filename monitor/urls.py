from django.urls import path

from monitor.views import (
    LocationCreateView,
    LocationDeleteView,
    LocationDetailView,
    LocationListView,
    LocationUpdateView,
    ProjectCreateView,
    ProjectDeleteView,
    ProjectDetailView,
    ProjectListView,
    ProjectUpdateView,
    TeamCreateView,
    TeamDeleteView,
    TeamDetailView,
    TeamListView,
    TeamMemberCreateView,
    TeamMemberDeleteView,
    TeamMemberDetailView,
    TeamMemberListView,
    TeamMemberUpdateView,
    TeamUpdateView,
    index,
)

app_name = "monitor"

urlpatterns = [
    path("", index, name="index"),
    path("locations/", LocationListView.as_view(), name="location-list"),
    path(
        "locations/create/",
        LocationCreateView.as_view(),
        name="location-create",
    ),
    path(
        "locations/<slug:slug>/",
        LocationDetailView.as_view(),
        name="location-detail",
    ),
    path(
        "locations/<slug:slug>/update/",
        LocationUpdateView.as_view(),
        name="location-update",
    ),
    path(
        "locations/<slug:slug>/delete/",
        LocationDeleteView.as_view(),
        name="location-delete",
    ),
    path("teams/", TeamListView.as_view(), name="team-list"),
    path("teams/create/", TeamCreateView.as_view(), name="team-create"),
    path(
        "teams/<slug:slug>/",
        TeamDetailView.as_view(),
        name="team-detail",
    ),
    path(
        "teams/<slug:slug>/update/",
        TeamUpdateView.as_view(),
        name="team-update",
    ),
    path(
        "teams/<slug:slug>/delete/",
        TeamDeleteView.as_view(),
        name="team-delete",
    ),
    path("projects/", ProjectListView.as_view(), name="project-list"),
    path(
        "projects/create/",
        ProjectCreateView.as_view(),
        name="project-create",
    ),
    path(
        "projects/<slug:slug>/",
        ProjectDetailView.as_view(),
        name="project-detail",
    ),
    path(
        "projects/<slug:slug>/update/",
        ProjectUpdateView.as_view(),
        name="project-update",
    ),
    path(
        "projects/<slug:slug>/delete/",
        ProjectDeleteView.as_view(),
        name="project-delete",
    ),
    path(
        "team-members/",
        TeamMemberListView.as_view(),
        name="teammember-list",
    ),
    path(
        "team-members/create/",
        TeamMemberCreateView.as_view(),
        name="teammember-create",
    ),
    path(
        "team-members/<slug:slug>/",
        TeamMemberDetailView.as_view(),
        name="teammember-detail",
    ),
    path(
        "team-members/<slug:slug>/update/",
        TeamMemberUpdateView.as_view(),
        name="teammember-update",
    ),
    path(
        "team-members/<slug:slug>/delete/",
        TeamMemberDeleteView.as_view(),
        name="teammember-delete",
    ),
]
