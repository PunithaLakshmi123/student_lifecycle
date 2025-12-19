from django.contrib import admin
from .models import Student, Course, Enrollment, Semester, Grade, AttendanceRecord, Promotion


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ('roll_no', 'first_name', 'last_name', 'current_class', 'is_active')
    search_fields = ('first_name', 'last_name', 'roll_no', 'email')


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('code', 'name')
    search_fields = ('code', 'name')


@admin.register(Enrollment)
class EnrollmentAdmin(admin.ModelAdmin):
    list_display = ('student', 'course', 'semester', 'enrolled_on')
    list_filter = ('semester',)


@admin.register(Semester)
class SemesterAdmin(admin.ModelAdmin):
    list_display = ('name', 'start_date', 'end_date', 'is_active')
    list_filter = ('is_active',)


@admin.register(Grade)
class GradeAdmin(admin.ModelAdmin):
    list_display = ('enrollment', 'assessment_type', 'score', 'max_score', 'percentage')
    list_filter = ('assessment_type',)


@admin.register(AttendanceRecord)
class AttendanceAdmin(admin.ModelAdmin):
    list_display = ('student', 'course', 'date', 'status')
    list_filter = ('status', 'course')


@admin.register(Promotion)
class PromotionAdmin(admin.ModelAdmin):
    list_display = ('student', 'from_class', 'to_class', 'promoted_on')
    list_filter = ('promoted_on',) 
