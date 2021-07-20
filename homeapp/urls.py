from django.urls import path, include
from homeapp import views

urlpatterns = [
    path('', views.login_user, name='login'),
    path('logout', views.logout_user, name='logout'),
    path('patient', views.patient, name='patient'),
    path('doctor', views.doctor, name='doctor'),
    path('dashboard', views.dashboard, name='dashboard'),
    # path('doctordetails', views.doctordetails, name='doctordetails'),
]
