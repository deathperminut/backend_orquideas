from rest_framework.permissions import BasePermission

class IsAdminUser(BasePermission):
    def has_permission(self, request, view):
        return bool(request.user and request.user.userprofile.role.name == 'Admin')

class IsUserWithRole(BasePermission):
    def has_permission(self, request, view):
        return bool(request.user and request.user.userprofile.role is not None)

