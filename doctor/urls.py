from django.urls import path
from . import views

app_name="doctor"
urlpatterns = [
    path('signup/', views.DoctorCreationView.as_view(), name="signup"),
    path('dashboard/', views.DashBoardView.as_view(), name="dashboard"),
    path('profile/', views.DoctorProfileUpdate.as_view(), name="profile"),
    path('patient/<slug:slug>/', views.PatientDetailView.as_view(), name="patientdetail"),
    path('appointments/', views.AppointmentListView.as_view(), name="appointments"),
    path('report/<int:pk>/', views.ReportView.as_view(), name="report"),
    path('makereport/<slug:slug>/', views.CreateReportView.as_view(), name="makereport"),
    path('makeprescription/<slug:slug>/', views.CreatePrescriptionView.as_view(), name="makeprescription"),
    path('notifications/', views.NotificationListView.as_view(), name="notifications"),
    path('makecall/', views.MakeCall.as_view(), name='call'),
    path('sendmessage/', views.SendMessage.as_view(), name="sendmessage"),
]
