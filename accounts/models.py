from django.db import models
from django.contrib.auth.models import User


class EmployeeProfile(models.Model):

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE
    )

    manager = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='team_members'
    )

    department = models.CharField(
        max_length=100
    )

    def __str__(self):
        return self.user.username