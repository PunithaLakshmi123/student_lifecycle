from rest_framework import permissions


def _in_group(user, group_name):
    return user.groups.filter(name=group_name).exists()


class IsAdminOrTeacher(permissions.BasePermission):
    """Allow access to staff users or users in the Teacher/Admin groups."""

    def has_permission(self, request, view):
        user = request.user
        if not user or not user.is_authenticated:
            return False
        if user.is_staff:
            return True
        return _in_group(user, 'Teacher') or _in_group(user, 'Admin')
