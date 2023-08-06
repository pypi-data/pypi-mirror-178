from django.contrib.auth.models import Group, User
from django.db import models


class Country(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Office(models.Model):
    country = models.ForeignKey(Country, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class UserRole(models.Model):
    office = models.ForeignKey(Office, on_delete=models.CASCADE)
    group = models.ForeignKey(Group, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="roles")

    def __str__(self):
        return ""

    class Meta:
        unique_together = ("office", "group", "user")


class Employee(models.Model):
    office = models.ForeignKey(Office, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name
