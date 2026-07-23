from django.contrib.auth.models import AbstractUser
from django.core.validators import MaxValueValidator
from django.db import models
from django.urls import reverse
from django.utils.text import slugify


class Location(models.Model):
    country = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, blank=True)

    class Meta:
        ordering = ["country", "city"]

    def __str__(self):
        return f"{self.city}, {self.country}"

    def get_absolute_url(self):
        return reverse("monitor:location-detail", kwargs={"slug": self.slug})

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(f"{self.city}-{self.country}")
        super().save(*args, **kwargs)


class Team(models.Model):
    name = models.CharField(max_length=255, unique=True)
    slug = models.SlugField(max_length=255, blank=True)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("monitor:team-detail", kwargs={"slug": self.slug})

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)


class Language(models.Model):
    name = models.CharField(max_length=100, unique=True)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name


class Project(models.Model):
    name = models.CharField(max_length=255)
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)
    progress_percent = models.PositiveSmallIntegerField(
        validators=[MaxValueValidator(100)]
    )
    payment_percent = models.PositiveSmallIntegerField(
        validators=[MaxValueValidator(100)]
    )
    slug = models.SlugField(max_length=255, blank=True)
    location = models.ForeignKey(
        Location, on_delete=models.CASCADE, related_name="projects"
    )
    team = models.ForeignKey(
        Team,
        on_delete=models.CASCADE,
        related_name="projects")

    class Meta:
        ordering = ["-start_date"]

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse(
            "monitor:project-detail",
            kwargs={"slug": self.slug})

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)


class TeamMember(AbstractUser):
    years_of_experience = models.PositiveSmallIntegerField(default=0)
    role = models.CharField(max_length=100)
    license_number = models.CharField(max_length=50, blank=True, null=True)
    slug = models.SlugField(max_length=255, blank=True)
    team = models.ForeignKey(
        Team,
        on_delete=models.SET_NULL,
        related_name="members",
        null=True,
        blank=True,
    )
    languages = models.ManyToManyField(
        Language,
        related_name="speakers",
        blank=True,
    )

    class Meta:
        verbose_name = "team member"
        verbose_name_plural = "team members"

    def __str__(self):
        return f"{self.username} ({self.first_name} {self.last_name})"

    def get_absolute_url(self):
        return reverse(
            "monitor:teammember-detail",
            kwargs={"slug": self.slug}
        )

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.username)
        super().save(*args, **kwargs)
