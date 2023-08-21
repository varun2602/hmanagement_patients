from django.urls import path 
from . import views 

urlpatterns = [
    path('', views.index, name = "index"),
    path('login', views.login_view, name = 'login'),
    path('register', views.register_view, name = 'register'),
    path('validate_name', views.validate_name, name = 'validate_name'),
    path('logout', views.logout_view, name = 'logout'),
    path('deactivate', views.deactivate, name = 'deactivate'),
    path('book_appointment', views.book_appointment, name = 'book_appointment'),
    path('test_route1', views.test_route, name = 'test_route1'),
    path('get_confirmed_appointments_pat', views.get_confirmed_appointments, name = 'get_confirmed_appointments_pat'),
    path('bill_show', views.bill_show, name = 'bill_show')
]