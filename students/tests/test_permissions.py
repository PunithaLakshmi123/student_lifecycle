from django.test import TestCase
from django.contrib.auth.models import User, Group
from rest_framework.test import APIClient
from students.models import Student, Course, Enrollment, Semester, Grade


class PermissionTests(TestCase):
    def setUp(self):
        # create objects
        self.student = Student.objects.create(first_name='Alice', last_name='Test', roll_no='T001')
        self.course = Course.objects.create(code='PHY101', name='Physics')
        self.semester = Semester.objects.create(name='2025_FA')
        self.enrollment = Enrollment.objects.create(student=self.student, course=self.course, semester=self.semester.name)

        # users
        self.teacher = User.objects.create_user('teacher', 't@example.com', 'pass')
        self.student_user = User.objects.create_user('stu', 's@example.com', 'pass')
        self.other = User.objects.create_user('other', 'o@example.com', 'pass')

        # groups
        teacher_group, _ = Group.objects.get_or_create(name='Teacher')
        student_group, _ = Group.objects.get_or_create(name='Student')
        teacher_group.user_set.add(self.teacher)
        student_group.user_set.add(self.student_user)

        self.api = APIClient()

    def test_teacher_can_create_grade(self):
        self.api.force_authenticate(self.teacher)
        data = {
            'enrollment': self.enrollment.id,
            'assessment_type': 'EX',
            'score': '40.00',
            'max_score': '50.00'
        }
        resp = self.api.post('/api/grades/', data, format='json')
        self.assertIn(resp.status_code, (201, 200))

    def test_student_cannot_create_grade(self):
        self.api.force_authenticate(self.student_user)
        data = {
            'enrollment': self.enrollment.id,
            'assessment_type': 'EX',
            'score': '30.00',
            'max_score': '50.00'
        }
        resp = self.api.post('/api/grades/', data, format='json')
        self.assertIn(resp.status_code, (401, 403))

    def test_anon_cannot_create_grade(self):
        data = {
            'enrollment': self.enrollment.id,
            'assessment_type': 'EX',
            'score': '25.00',
            'max_score': '50.00'
        }
        resp = self.api.post('/api/grades/', data, format='json')
        self.assertIn(resp.status_code, (401, 403))

    def test_teacher_can_view_attendance(self):
        # attendance endpoint should be readable by teacher
        self.api.force_authenticate(self.teacher)
        resp = self.api.get('/api/attendance/')
        self.assertIn(resp.status_code, (200, 204))

    def test_student_cannot_create_attendance(self):
        self.api.force_authenticate(self.student_user)
        data = {
            'student': self.student.id,
            'course': self.course.id,
            'date': '2025-12-01',
            'status': 'P'
        }
        resp = self.api.post('/api/attendance/', data, format='json')
        self.assertIn(resp.status_code, (401, 403))
