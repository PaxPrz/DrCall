from django.urls import path
from . import views

app_name="doctor"
urlpatterns = [
    path('signup/', views.DoctorCreationView.as_view(), name="signup"),
    path('dashboard/', views.DashBoardView.as_view(), name="dashboard"),
    path('profile/', views.DoctorProfileUpdate.as_view(), name="profile"),
]
