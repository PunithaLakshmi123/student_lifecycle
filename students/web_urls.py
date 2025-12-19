from django.urls import path
from .views import (
    StudentListView, StudentDetailView, StudentCreateView, StudentUpdateView, StudentDeleteView, StudentExportCSVView,
    CourseListView, CourseCreateView, CourseUpdateView,
    EnrollmentListView, EnrollmentCreateView, EnrollmentDeleteView,
)

app_name = 'students'

urlpatterns = [
    # Students
    path('students/', StudentListView.as_view(), name='list'),
    path('students/new/', StudentCreateView.as_view(), name='create'),
    path('students/export/csv/', StudentExportCSVView.as_view(), name='export_csv'),
    path('students/<int:pk>/', StudentDetailView.as_view(), name='detail'),
    path('students/<int:pk>/edit/', StudentUpdateView.as_view(), name='edit'),
    path('students/<int:pk>/delete/', StudentDeleteView.as_view(), name='delete'),

    # Courses
    path('courses/', CourseListView.as_view(), name='courses'),
    path('courses/new/', CourseCreateView.as_view(), name='course_create'),
    path('courses/<int:pk>/edit/', CourseUpdateView.as_view(), name='course_edit'),

    # Enrollments
    path('enrollments/', EnrollmentListView.as_view(), name='enrollments'),
    path('enrollments/new/', EnrollmentCreateView.as_view(), name='enrollment_create'),
    path('enrollments/<int:pk>/delete/', EnrollmentDeleteView.as_view(), name='enrollment_delete'),
]
