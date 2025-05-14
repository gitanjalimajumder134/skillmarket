from rest_framework.permissions import BasePermission

class AllowUnauthenticatedForLoginRegister(BasePermission):
    def has_permission(self, request, view):
        return (
            view.__class__.__name__ in ['LoginUser', 'RegisterUser']  # allow unauthenticated access
            or request.user and request.user.is_authenticated         # else require auth
        )