from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect,get_object_or_404

from access_requests.models import AccessRequest

from accounts.utils import (
    is_employee,
    is_manager,
    is_it_admin
)


@login_required
def dashboard(request):

    user = request.user

    if is_employee(user):
        return redirect('employee_dashboard')

    if is_manager(user):
        return redirect('manager_dashboard')

    if is_it_admin(user):
        return redirect('it_dashboard')

    return render(
        request,
        'dashboard/no_role.html'
    )


@login_required
def employee_dashboard(request):

    if not is_employee(request.user):
        return redirect('dashboard')

    return render(
        request,
        'dashboard/employee.html'
    )


@login_required
def manager_dashboard(request):

    if not is_manager(request.user):
        return redirect('dashboard')

    return render(
        request,
        'dashboard/manager.html'
    )
@login_required
def it_dashboard(request):

    if not request.user.groups.filter(
        name='IT Admin'
    ).exists():

        return redirect('dashboard')

    requests = AccessRequest.objects.filter(
        status='Manager Approved'
    ).select_related(
        'user',
        'resource'
    )

    return render(
        request,
        'dashboard/it_admin.html',
        {
            'requests': requests
        }
    )
    
    
@login_required
def it_admin_action(request, request_id, action):

    # Make sure the logged-in user is an IT Admin

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

        return redirect('it_dashboard')


    # Approve or Reject

    if action == 'approve':

        access_request.status = 'IT Approved'

    elif action == 'reject':

        access_request.status = 'IT Rejected'

    else:

        return redirect('it_dashboard')


    access_request.save()

    return redirect('it_dashboard')

# @login_required
# def it_dashboard(request):

#     if not is_it_admin(request.user):
#         return redirect('dashboard')

#     return render(
#         request,
#         'dashboard/it_admin.html'
#     )