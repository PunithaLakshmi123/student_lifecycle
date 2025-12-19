from rest_framework import viewsets
from .models import Student, Course, Enrollment, Semester, Grade, AttendanceRecord, Promotion
from .serializers import (
    StudentSerializer, CourseSerializer, EnrollmentSerializer,
    SemesterSerializer, GradeSerializer, AttendanceSerializer, PromotionSerializer
)

import csv
from django.http import HttpResponse
from rest_framework.decorators import action


class StudentViewSet(viewsets.ModelViewSet):
    queryset = Student.objects.all().order_by('roll_no')
    serializer_class = StudentSerializer

    @action(detail=False, methods=['get'], url_path='export')
    def export(self, request):
        """Return a CSV download of all students."""
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="students.csv"'

        writer = csv.writer(response)
        writer.writerow(['id', 'first_name', 'last_name', 'email', 'enrollment_date'])
        for s in Student.objects.order_by('id'):
            writer.writerow([
                s.id,
                s.first_name,
                s.last_name,
                s.email or '',
                s.enrollment_date.isoformat() if getattr(s, 'enrollment_date', None) else '',
            ])

        return response


class CourseViewSet(viewsets.ModelViewSet):
    queryset = Course.objects.all().order_by('code')
    serializer_class = CourseSerializer


class EnrollmentViewSet(viewsets.ModelViewSet):
    queryset = Enrollment.objects.all()
    serializer_class = EnrollmentSerializer


class SemesterViewSet(viewsets.ModelViewSet):
    queryset = Semester.objects.all().order_by('start_date')
    serializer_class = SemesterSerializer


from .permissions import IsAdminOrTeacher


class GradeViewSet(viewsets.ModelViewSet):
    queryset = Grade.objects.all()
    serializer_class = GradeSerializer
    permission_classes = [IsAdminOrTeacher]


class AttendanceViewSet(viewsets.ModelViewSet):
    queryset = AttendanceRecord.objects.all()
    serializer_class = AttendanceSerializer
    permission_classes = [IsAdminOrTeacher]


class PromotionViewSet(viewsets.ModelViewSet):
    queryset = Promotion.objects.all()
    serializer_class = PromotionSerializer
    permission_classes = [IsAdminOrTeacher]


# --- Server-rendered UI views (Django templates) ---
from django.views.generic import View, ListView, DetailView, CreateView, UpdateView, DeleteView, TemplateView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import get_object_or_404
from .models import Student, Course


class HomeView(TemplateView):
    template_name = 'home.html'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['student_count'] = Student.objects.count()
        ctx['course_count'] = Course.objects.count()
        return ctx


class IsAdminOrTeacherMixin(UserPassesTestMixin):
    def test_func(self):
        user = self.request.user
        if not user.is_authenticated:
            return False
        if user.is_staff:
            return True
        return user.groups.filter(name__in=['Admin', 'Teacher']).exists()


class StudentListView(ListView):
    model = Student
    template_name = 'students/student_list.html'
    context_object_name = 'students'
    paginate_by = 20
    ordering = ['roll_no']



class StudentDetailView(DetailView):
    model = Student
    template_name = 'students/student_detail.html'
    context_object_name = 'student'


class StudentExportCSVView(View):
    """Export students as CSV for download (web view)."""
    def get(self, request, *args, **kwargs):
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="students.csv"'

        writer = csv.writer(response)
        writer.writerow(['id', 'first_name', 'last_name', 'email', 'enrollment_date'])
        for s in Student.objects.order_by('id'):
            writer.writerow([
                s.id,
                s.first_name,
                s.last_name,
                s.email or '',
                s.enrollment_date.isoformat() if getattr(s, 'enrollment_date', None) else '',
            ])
        return response


class StudentCreateView(LoginRequiredMixin, IsAdminOrTeacherMixin, CreateView):
    model = Student
    fields = ['first_name', 'last_name', 'dob', 'gender', 'admission_date', 'roll_no', 'email', 'phone', 'address', 'current_class', 'is_active']
    template_name = 'students/student_form.html'
    success_url = reverse_lazy('students:list')


class StudentUpdateView(LoginRequiredMixin, IsAdminOrTeacherMixin, UpdateView):
    model = Student
    fields = ['first_name', 'last_name', 'dob', 'gender', 'admission_date', 'roll_no', 'email', 'phone', 'address', 'current_class', 'is_active']
    template_name = 'students/student_form.html'
    success_url = reverse_lazy('students:list')


class StudentDeleteView(LoginRequiredMixin, IsAdminOrTeacherMixin, DeleteView):
    model = Student
    template_name = 'students/student_confirm_delete.html'
    success_url = reverse_lazy('students:list')


# Course views
class CourseListView(LoginRequiredMixin, ListView):
    model = Course
    template_name = 'students/course_list.html'
    context_object_name = 'courses'


class CourseCreateView(LoginRequiredMixin, IsAdminOrTeacherMixin, CreateView):
    model = Course
    fields = ['code', 'name', 'description']
    template_name = 'students/course_form.html'
    success_url = reverse_lazy('students:courses')


class CourseUpdateView(LoginRequiredMixin, IsAdminOrTeacherMixin, UpdateView):
    model = Course
    fields = ['code', 'name', 'description']
    template_name = 'students/course_form.html'
    success_url = reverse_lazy('students:courses')


# Enrollment views
class EnrollmentListView(LoginRequiredMixin, ListView):
    model = Enrollment
    template_name = 'students/enrollment_list.html'
    context_object_name = 'enrollments'


class EnrollmentCreateView(LoginRequiredMixin, IsAdminOrTeacherMixin, CreateView):
    model = Enrollment
    fields = ['student', 'course', 'semester']
    template_name = 'students/enrollment_form.html'
    success_url = reverse_lazy('students:enrollments')


class EnrollmentDeleteView(LoginRequiredMixin, IsAdminOrTeacherMixin, DeleteView):
    model = Enrollment
    template_name = 'students/enrollment_confirm_delete.html'
    success_url = reverse_lazy('students:enrollments') 
