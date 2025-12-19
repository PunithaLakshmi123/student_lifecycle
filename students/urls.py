from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    StudentViewSet, CourseViewSet, EnrollmentViewSet,
    SemesterViewSet, GradeViewSet, AttendanceViewSet, PromotionViewSet
)

router = DefaultRouter()
router.register(r'students', StudentViewSet)
router.register(r'courses', CourseViewSet)
router.register(r'enrollments', EnrollmentViewSet)
router.register(r'semesters', SemesterViewSet)
router.register(r'grades', GradeViewSet)
router.register(r'attendance', AttendanceViewSet)
router.register(r'promotions', PromotionViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
