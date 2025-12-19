from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType


class Command(BaseCommand):
    help = 'Create default groups and assign permissions (Admin, Teacher, Student)'

    def handle(self, *args, **options):
        # Create groups
        admin_group, _ = Group.objects.get_or_create(name='Admin')
        teacher_group, _ = Group.objects.get_or_create(name='Teacher')
        student_group, _ = Group.objects.get_or_create(name='Student')

        # Grant Admin all permissions
        all_perms = Permission.objects.all()
        admin_group.permissions.set(all_perms)

        # Assign teacher permissions
        teacher_perms = []
        models_to_allow = ['course', 'enrollment', 'grade', 'attendancerecord', 'promotion']
        for model in models_to_allow:
            perms = Permission.objects.filter(content_type__model=model)
            for p in perms:
                teacher_perms.append(p)
        teacher_group.permissions.set(teacher_perms)

        # Assign student permissions (view only for own records)
        student_perms = Permission.objects.filter(codename__startswith='view_')
        student_group.permissions.set(student_perms)

        self.stdout.write(self.style.SUCCESS('Default groups created/updated: Admin, Teacher, Student'))
