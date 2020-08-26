from django.urls import path
from . import views

app_name="patient"
urlpatterns = [
    path('signup/', views.PatientCreationView.as_view(), name="signup"),
    path('dashboard/', views.DashBoardView.as_view(), name="dashboard"),
    path('profile/', views.PatientProfileUpdate.as_view(), name="profile"),
    path('search/', views.DoctorListView.as_view(), name="search"),
    path('doctor/<slug:slug>/', views.DoctorDetailView.as_view(), name="doctordetail"),
]
