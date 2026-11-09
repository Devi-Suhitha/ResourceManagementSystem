from django.db import models
from django.contrib.auth.models import User


class Resource(models.Model):

    RESOURCE_TYPES = [
        ('Development', 'Development'),
        ('Cloud', 'Cloud'),
        ('Project Management', 'Project Management'),
        ('Database', 'Database'),
        ('Application', 'Application'),
    ]

    name = models.CharField(
        max_length=100
    )

    description = models.TextField()

    resource_type = models.CharField(
        max_length=50,
        choices=RESOURCE_TYPES
    )

    owner = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    is_active = models.BooleanField(
        default=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return self.name