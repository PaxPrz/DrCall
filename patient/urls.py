from django.urls import path
from . import views

app_name="patient"
urlpatterns = [
    path('signup/', views.PatientCreationView.as_view(), name="signup"),
    path('dashboard/', views.DashBoardView.as_view(), name="dashboard"),
    path('profile/', views.PatientProfileUpdate.as_view(), name="profile"),
    path('search/', views.DoctorListView.as_view(), name="search"),
    path('doctor/<slug:slug>/', views.DoctorDetailView.as_view(), name="doctordetail"),
    path('makeappointment/<slug:slug>/', views.MakeAppointmentView.as_view(), name="makeappointment"),
    path('appointments/', views.ListAppointmentView.as_view(), name="appointments"),
    path('reports/', views.ListReportView.as_view(), name="reports"),
    path('makereport/', views.CreateReportView.as_view(), name="makereport"),
    path('report/<int:pk>/', views.ReportDetailView.as_view(), name="report"),
    path('prescriptions/', views.PrescriptionView.as_view(), name="prescriptions"),
]
