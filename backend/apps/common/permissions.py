from rest_framework.permissions import BasePermission


class IsRole(BasePermission):
    allowed_roles = []

    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated and request.user.role in self.allowed_roles


class IsSupplier(IsRole):
    allowed_roles = ['supplier', 'admin']


class IsDriver(IsRole):
    allowed_roles = ['driver', 'admin']


class IsCustomer(IsRole):
    allowed_roles = ['customer', 'admin']


class IsAdmin(IsRole):
    allowed_roles = ['admin']
