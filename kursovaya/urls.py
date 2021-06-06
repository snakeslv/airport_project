"""kursovaya URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
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
from django.urls import path, include
from kursovaya import views
from django.conf.urls import url


urlpatterns = [

    path('admin/', admin.site.urls),
    url(r'^airports/$', views.airports, name='airports'),
    path('', views.main, name='main'),
    url(r'^flights/(?P<number>[0-9]+)/$', views.flights, name='flights'),
    url(r'^input/$', views.input, name='input'),
    url(r'^register/$', views.register, name='register'),
    url(r'^zelolka/$', views.zelolka, name='zelolka'),
    url(r'^passengers/(?P<airport_id>[0-9]+)/(?P<temp_flight_id>[0-9]+)/$', views.passengers, name='passengers'),
    url(r'^flight_register/(?P<airport_id>[0-9]+)/(?P<temp_flight_id>[0-9]+)', views.flight_register, name='flight_register'),
    url(r'^frs/$', views.frs, name='frs'),
    url(r'^delete_flight/(?P<airport_id>[0-9]+)/(?P<flight_id>[0-9]+)', views.delete_flight, name='delete_flight'),
    url(r'^flights_edit_page/(?P<airport_id>[0-9]+)/(?P<flight_id>[0-9]+)', views.flights_edit_page, name='flights_edit_page'),
    url(r'^delete_passenger/(?P<airport_id>[0-9]+)/(?P<flight_id>[0-9]+)/(?P<pass_lastname>[\w\-]+)/(?P<pass_firstname>[\w\-]+)/(?P<pass_secondname>[\w\-]+)/$', views.delete_passenger, name='delete_passenger'),
    url(r'^passengers_edit_page/(?P<airport_id>[0-9]+)/(?P<flight_id>[0-9]+)/(?P<pass_lastname>[\w\-]+)/(?P<pass_firstname>[\w\-]+)/(?P<pass_secondname>[\w\-]+)/$', views.passengers_edit_page, name='passengers_edit_page'),
    url(r'^emp_frs/$', views.emp_frs, name='frs'),
    url(r'^delete_airport/(?P<airport_id>[0-9]+)/', views.delete_airport, name='delete_airport'),
    url(r'^airports_edit_page/(?P<airport_id>[0-9]+)/', views.airports_edit_page, name='airports_edit_page'),
    url(r'^airports_edit/(?P<airport_id>[0-9]+)/', views.airports_edit, name='airports_edit'),
    url(r'^flights_edit/(?P<airport_id>[0-9]+)/(?P<flight_id>[0-9]+)', views.flights_edit, name='flights_edit'),
    url(r'^input_airports/', views.input_airports, name='input_airports'),
    url(r'^admin_panel/', views.admin_panel, name='admin_panel'),
    url(r'^change_group/', views.change_group, name='change_group'),
    url(r'^pass_edit/(?P<airport_id>[0-9]+)/(?P<flight_id>[0-9]+)/(?P<pass_lastname>[\w\-]+)/(?P<pass_firstname>[\w\-]+)/(?P<pass_secondname>[\w\-]+)/$', views.pass_edit, name='pass_edit'),



]

urlpatterns += [
    url(r'^accounts/', include('django.contrib.auth.urls')),
]