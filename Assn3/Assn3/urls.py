"""
URL configuration for Assn3 project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from destinations import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name='index'),
    path('users/new', views.newUsers, name='newUsers'),
    path('sessions/new', views.newSessions, name='newSessions'),
    path('users', views.users, name='users'),
    path('sessions', views.sessions, name='sessions'),
    path('sessions/destroy', views.sessionsDestroy, name='sessionsDestroy'),
    path('destinations', views.destinations, name='destinations'),
    path('destinations/new', views.newDestinations, name='destinationsNew'),
    path('destinations/<int:id>', views.destinationsId, name='destinationsId'),
    path('destinations/<int:id>/update', views.updateDestination, name='updateDestination'),
    path('destinations/<int:id>/destroy', views.destroyDestinationsId, name='destroyDestinationsId'),
]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)