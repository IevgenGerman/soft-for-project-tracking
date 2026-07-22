from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import generic

from monitor.forms import ProjectForm, TeamMemberCreationForm
from monitor.models import Location, Project, Team, TeamMember


@login_required
def index(request):
    """Home page with record counts and a visit counter."""
    num_visits = request.session.get("num_visits", 0)
    request.session["num_visits"] = num_visits + 1

    context = {
        "num_locations": Location.objects.count(),
        "num_teams": Team.objects.count(),
        "num_projects": Project.objects.count(),
        "num_team_members": TeamMember.objects.count(),
        "num_visits": num_visits + 1,
    }
    return render(request, "monitor/index.html", context=context)


class LocationListView(LoginRequiredMixin, generic.ListView):
    model = Location
    paginate_by = 5


class LocationDetailView(LoginRequiredMixin, generic.DetailView):
    model = Location


class LocationCreateView(LoginRequiredMixin, generic.CreateView):
    model = Location
    fields = "__all__"
    success_url = reverse_lazy("monitor:location-list")


class LocationUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Location
    fields = "__all__"
    success_url = reverse_lazy("monitor:location-list")


class LocationDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Location
    success_url = reverse_lazy("monitor:location-list")


class TeamListView(LoginRequiredMixin, generic.ListView):
    model = Team
    paginate_by = 5


class TeamDetailView(LoginRequiredMixin, generic.DetailView):
    model = Team
    queryset = Team.objects.prefetch_related("members", "projects")


class TeamCreateView(LoginRequiredMixin, generic.CreateView):
    model = Team
    fields = "__all__"
    success_url = reverse_lazy("monitor:team-list")


class TeamUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Team
    fields = "__all__"
    success_url = reverse_lazy("monitor:team-list")


class TeamDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Team
    success_url = reverse_lazy("monitor:team-list")


class ProjectListView(LoginRequiredMixin, generic.ListView):
    model = Project
    paginate_by = 5

    def get_queryset(self):
        return Project.objects.select_related("location", "team")


class ProjectDetailView(LoginRequiredMixin, generic.DetailView):
    model = Project


class ProjectCreateView(LoginRequiredMixin, generic.CreateView):
    model = Project
    form_class = ProjectForm
    success_url = reverse_lazy("monitor:project-list")


class ProjectUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Project
    form_class = ProjectForm
    success_url = reverse_lazy("monitor:project-list")


class ProjectDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Project
    success_url = reverse_lazy("monitor:project-list")


class TeamMemberListView(LoginRequiredMixin, generic.ListView):
    model = TeamMember
    paginate_by = 5

    def get_queryset(self):
        return TeamMember.objects.prefetch_related("languages", "team")


class TeamMemberDetailView(LoginRequiredMixin, generic.DetailView):
    model = TeamMember
    queryset = TeamMember.objects.prefetch_related(
        "languages", "team", "team__projects"
    )


class TeamMemberCreateView(LoginRequiredMixin, generic.CreateView):
    model = TeamMember
    form_class = TeamMemberCreationForm
    success_url = reverse_lazy("monitor:teammember-list")


class TeamMemberUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = TeamMember
    fields = (
        "first_name",
        "last_name",
        "email",
        "years_of_experience",
        "role",
        "license_number",
        "team",
        "languages",
    )
    success_url = reverse_lazy("monitor:teammember-list")


class TeamMemberDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = TeamMember
    success_url = reverse_lazy("monitor:teammember-list")
