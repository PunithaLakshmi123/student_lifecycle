from django.db import models


class Student(models.Model):
    GENDER_CHOICES = [('M', 'Male'), ('F', 'Female'), ('O', 'Other')]

    first_name = models.CharField(max_length=64)
    last_name = models.CharField(max_length=64)
    dob = models.DateField(null=True, blank=True)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, blank=True)
    admission_date = models.DateField(null=True, blank=True)
    roll_no = models.CharField(max_length=32, unique=True)
    email = models.EmailField(null=True, blank=True)
    phone = models.CharField(max_length=20, null=True, blank=True)
    address = models.TextField(null=True, blank=True)
    current_class = models.CharField(max_length=64, blank=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.roll_no} - {self.first_name} {self.last_name}"


class Course(models.Model):
    code = models.CharField(max_length=16, unique=True)
    name = models.CharField(max_length=128)
    description = models.TextField(blank=True)

    def __str__(self):
        return f"{self.code} - {self.name}"


class Enrollment(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='enrollments')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='enrollments')
    semester = models.CharField(max_length=32)
    enrolled_on = models.DateField(auto_now_add=True)

    class Meta:
        unique_together = ('student', 'course', 'semester')

    def __str__(self):
        return f"{self.student} in {self.course} ({self.semester})"


class Semester(models.Model):
    name = models.CharField(max_length=64, unique=True)
    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)
    is_active = models.BooleanField(default=False)

    def __str__(self):
        return self.name


class Grade(models.Model):
    ASSESSMENT_CHOICES = [
        ('EX', 'Exam'),
        ('AS', 'Assignment'),
        ('PR', 'Project'),
        ('OT', 'Other'),
    ]

    enrollment = models.ForeignKey(Enrollment, on_delete=models.CASCADE, related_name='grades')
    assessment_type = models.CharField(max_length=2, choices=ASSESSMENT_CHOICES, default='EX')
    score = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True)
    max_score = models.DecimalField(max_digits=6, decimal_places=2, default=100)
    percentage = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    letter_grade = models.CharField(max_length=4, blank=True)
    remarks = models.TextField(blank=True)
    recorded_on = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if self.score is not None and self.max_score:
            try:
                self.percentage = (self.score / self.max_score) * 100
            except Exception:
                self.percentage = None
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.enrollment} - {self.assessment_type} : {self.percentage}%"


class AttendanceRecord(models.Model):
    STATUS_CHOICES = [('P', 'Present'), ('A', 'Absent'), ('L', 'Late')]

    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='attendance')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='attendance')
    date = models.DateField()
    status = models.CharField(max_length=1, choices=STATUS_CHOICES)
    remarks = models.TextField(blank=True)

    class Meta:
        unique_together = ('student', 'course', 'date')

    def __str__(self):
        return f"{self.student} - {self.course} on {self.date}: {self.status}"


class Promotion(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='promotions')
    from_class = models.CharField(max_length=64)
    to_class = models.CharField(max_length=64)
    promoted_on = models.DateField()
    effective_semester = models.ForeignKey(Semester, on_delete=models.SET_NULL, null=True, blank=True)
    notes = models.TextField(blank=True)

    def __str__(self):
        return f"{self.student}: {self.from_class} -> {self.to_class} on {self.promoted_on}"
