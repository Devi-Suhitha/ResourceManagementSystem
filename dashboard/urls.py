from django.urls import path
from . import views


urlpatterns = [

    path(
        '',
        views.dashboard,
        name='dashboard'
    ),

    path(
        'employee/',
        views.employee_dashboard,
        name='employee_dashboard'
    ),

    path(
        'manager/',
        views.manager_dashboard,
        name='manager_dashboard'
    ),

    path(
        'it-admin/',
        views.it_dashboard,
        name='it_dashboard'
    ),
    
    path(
    'it-admin/<int:request_id>/<str:action>/',
    views.it_admin_action,
    name='it_admin_action'
),

]