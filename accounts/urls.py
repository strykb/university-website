from django.urls import path
from .views import (RegisterView,TutorsListView,
    StudentsListView, TechniciansListView, UserUpdateView,
    PendingUsersListView, ApproveStudentUpdateView)

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('tutors/', TutorsListView.as_view(), name='tutors_list'),
    path('students/', StudentsListView.as_view(), name='students_list'),
    path('technicians/', TechniciansListView.as_view(), name='technicians_list'),
    path('pending-users/', PendingUsersListView.as_view(), name='pending_users'),
    path('approve/<int:pk>', ApproveStudentUpdateView.as_view(), name='approve_student'),
    path('<int:pk>', UserUpdateView.as_view(), name='edit_user'),
]