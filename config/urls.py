from django.contrib import admin
from django.urls import path, include


urlpatterns = [

    path(
        'admin/',
        admin.site.urls
    ),

    path(
        'accounts/',
        include('django.contrib.auth.urls')
    ),

    path(
        'dashboard/',
        include('dashboard.urls')
    ),
    
    path(
    'resources/',
    include('resource_management.urls')
),
    
    path(
    'access-requests/',
    include('access_requests.urls')
),

]