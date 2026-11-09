from django.db import models
from django.contrib.auth.models import User
from resource_management.models import Resource


class AccessRequest(models.Model):

    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Manager Approved', 'Manager Approved'),
        ('Manager Rejected', 'Manager Rejected'),
        ('IT Approved', 'IT Approved'),
        ('IT Rejected', 'IT Rejected'),
        ('Active', 'Active'),
        ('Expired', 'Expired'),
    ]

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='access_requests'
    )

    resource = models.ForeignKey(
        Resource,
        on_delete=models.CASCADE,
        related_name='access_requests'
    )

    reason = models.TextField()

    duration_days = models.PositiveIntegerField()

    status = models.CharField(
        max_length=30,
        choices=STATUS_CHOICES,
        default='Pending'
    )

    requested_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    manager_action_at = models.DateTimeField(
        null=True,
        blank=True
    )

    manager_action_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='manager_actions'
    )

    it_action_at = models.DateTimeField(
        null=True,
        blank=True
    )

    it_action_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='it_actions'
    )
    access_start_date = models.DateTimeField(
    null=True,
    blank=True
    )

    access_expiry_date = models.DateTimeField(
        null=True,
        blank=True
    )

    def __str__(self):
        return f"{self.user.username} - {self.resource.name}"