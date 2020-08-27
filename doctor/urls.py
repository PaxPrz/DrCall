from django.urls import path
from . import views

app_name="doctor"
urlpatterns = [
    path('signup/', views.DoctorCreationView.as_view(), name="signup"),
    path('dashboard/', views.DashBoardView.as_view(), name="dashboard"),
    path('profile/', views.DoctorProfileUpdate.as_view(), name="profile"),
    path('patient/<slug:slug>/', views.PatientDetailView.as_view(), name="patientdetail"),
    path('appointments/', views.AppointmentListView.as_view(), name="appointments"),
    path('makeprescription/<slug:slug>/', views.CreatePrescriptionView.as_view(), name="makeprescription"),
]
