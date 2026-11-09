from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from .models import Resource


@login_required
def resource_list(request):

    resources = Resource.objects.filter(
        is_active=True
    )

    return render(
        request,
        'resource_management/resource_list.html',
        {
            'resources': resources
        }
    )