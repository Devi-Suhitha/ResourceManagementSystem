from django.db import models
from django.contrib.auth.models import User

from access_requests.models import AccessRequest


class AuditLog(models.Model):

    ACTION_CHOICES = [

        ('REQUESTED', 'Access Requested'),

        ('MANAGER_APPROVED', 'Manager Approved'),

        ('MANAGER_REJECTED', 'Manager Rejected'),

        ('IT_APPROVED', 'IT Admin Approved'),

        ('IT_REJECTED', 'IT Admin Rejected'),

        ('ACTIVATED', 'Access Activated'),

        ('EXPIRED', 'Access Expired'),
    ]

    access_request = models.ForeignKey(
        AccessRequest,
        on_delete=models.CASCADE,
        related_name='audit_logs'
    )

    performed_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    action = models.CharField(
        max_length=30,
        choices=ACTION_CHOICES
    )

    description = models.TextField()

    timestamp = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):

        return (
            f"{self.access_request} - "
            f"{self.action}"
        )