from django.urls import path

from . import views


urlpatterns = [

    path(
        'request/<int:resource_id>/',
        views.request_access,
        name='request_access'
    ),

    path(
        'my-requests/',
        views.my_access_requests,
        name='my_access_requests'
    ),
    path(
    'manager/',
    views.manager_requests,
    name='manager_requests'
),
    path(
    'manager/action/<int:request_id>/<str:action>/',
    views.manager_action,
    name='manager_action'
),
    path(
    'it-admin/',
    views.it_admin_requests,
    name='it_admin_requests'
),
    path(
    'it-admin/<int:request_id>/<str:action>/',
    views.it_admin_action,
    name='it_admin_action'
),
    

]