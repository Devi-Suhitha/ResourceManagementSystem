from django.utils import timezone

from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404

from resource_management.models import Resource

from .forms import AccessRequestForm
from .models import AccessRequest

from accounts.models import EmployeeProfile
from django.contrib.auth.models import Group
from datetime import timedelta

@login_required
def request_access(request, resource_id):

    resource = get_object_or_404(
        Resource,
        id=resource_id,
        is_active=True
    )

    if request.method == 'POST':

        form = AccessRequestForm(
            request.POST
        )

        if form.is_valid():

            access_request = form.save(
                commit=False
            )

            access_request.user = request.user

            access_request.resource = resource

            access_request.save()

            return redirect(
                'my_access_requests'
            )

    else:

        form = AccessRequestForm()

    return render(
        request,
        'access_requests/request_form.html',
        {
            'form': form,
            'resource': resource
        }
    )


@login_required
def my_access_requests(request):

    update_expired_requests()

    requests = AccessRequest.objects.filter(
        user=request.user
    ).select_related(
        'resource',
        'manager_action_by',
        'it_action_by'
    )

    return render(
        request,
        'access_requests/my_requests.html',
        {
            'requests': requests
        }
    )
    
@login_required
def manager_requests(request):

    # Check whether the logged-in user is a Manager

    if not request.user.groups.filter(
        name='Manager'
    ).exists():

        return redirect('dashboard')


    # Get employees whose manager is the
    # currently logged-in manager

    team_members = EmployeeProfile.objects.filter(
        manager=request.user
    ).values_list(
        'user_id',
        flat=True
    )


    # Get pending requests from those employees

    requests = AccessRequest.objects.filter(
        user_id__in=team_members,
        status='Pending'
    ).select_related(
        'user',
        'resource'
    )


    return render(
        request,
        'access_requests/manager_requests.html',
        {
            'requests': requests
        }
    )
@login_required

def manager_action(request, request_id, action):

    # Make sure the logged-in user is a Manager
    if not request.user.groups.filter(
        name='Manager'
    ).exists():

        return redirect('dashboard')

    # Get the access request
    access_request = get_object_or_404(
        AccessRequest,
        id=request_id
    )

    # Check that the employee belongs to this manager
    is_team_member = EmployeeProfile.objects.filter(
        user=access_request.user,
        manager=request.user
    ).exists()

    if not is_team_member:

        return redirect('manager_requests')

    # Only allow actions on pending requests
    if access_request.status != 'Pending':

        return redirect('manager_requests')

    # Approve or reject
    if action == 'approve':

        access_request.status = 'Active'

        access_request.it_action_at = timezone.now()

        access_request.it_action_by = request.user

        access_request.access_start_date = timezone.now()

        access_request.access_expiry_date = (
            timezone.now()
            + timedelta(days=access_request.duration_days)
        )

    elif action == 'reject':

        access_request.status = 'Manager Rejected'

        access_request.manager_action_at = timezone.now()

        access_request.manager_action_by = request.user

    else:

        return redirect('manager_requests')

    access_request.save()  
    return redirect('manager_requests')


@login_required
def it_admin_requests(request):

    # Check whether the logged-in user is an IT Admin

    if not request.user.groups.filter(
        name='IT Admin'
    ).exists():

        return redirect('dashboard')


    # Get requests approved by Manager

    requests = AccessRequest.objects.filter(
        status='Manager Approved'
    ).select_related(
        'user',
        'resource'
    )


    return render(
        request,
        'access_requests/it_admin_requests.html',
        {
            'requests': requests
        }
    )
@login_required
def it_admin_action(request, request_id, action):

    # Check whether the logged-in user is an IT Admin

    if not request.user.groups.filter(
        name='IT Admin'
    ).exists():

        return redirect('dashboard')

    # Get the access request

    access_request = get_object_or_404(
        AccessRequest,
        id=request_id
    )

    # IT Admin can only process
    # Manager Approved requests

    if access_request.status != 'Manager Approved':

        return redirect('it_admin_requests')

    # Approve

    if action == 'approve':

        access_request.status = 'IT Approved'

        access_request.it_action_at = timezone.now()

        access_request.it_action_by = request.user

    # Reject

    elif action == 'reject':

        access_request.status = 'IT Rejected'

        access_request.it_action_at = timezone.now()

        access_request.it_action_by = request.user

    else:

        return redirect('it_admin_requests')

    access_request.save()

    return redirect('it_admin_requests')

def update_expired_requests():

    now = timezone.now()

    expired_requests = AccessRequest.objects.filter(
        status='Active',
        access_expiry_date__lte=now
    )

    expired_requests.update(
        status='Expired'
    )