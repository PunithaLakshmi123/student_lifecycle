from django.test import TestCase
from django.db import IntegrityError
from students.models import Student, Course, Enrollment, Semester, Grade, AttendanceRecord, Promotion


class ModelsTest(TestCase):
    def setUp(self):
        self.student = Student.objects.create(first_name='John', last_name='Doe', roll_no='R001')
        self.course = Course.objects.create(code='C01', name='Math')
        self.semester = Semester.objects.create(name='2025_S1')
        self.enrollment = Enrollment.objects.create(student=self.student, course=self.course, semester=self.semester.name)

    def test_grade_percentage(self):
        g = Grade.objects.create(enrollment=self.enrollment, assessment_type='EX', score=45, max_score=50)
        self.assertAlmostEqual(float(g.percentage), 90.0)

    def test_attendance_unique(self):
        AttendanceRecord.objects.create(student=self.student, course=self.course, date='2025-12-01', status='P')
        with self.assertRaises(IntegrityError):
            AttendanceRecord.objects.create(student=self.student, course=self.course, date='2025-12-01', status='A')

    def test_promotion_create(self):
        promo = Promotion.objects.create(student=self.student, from_class='Grade 1', to_class='Grade 2', promoted_on='2025-06-01')
        self.assertEqual(str(promo).split(':')[0], str(self.student))