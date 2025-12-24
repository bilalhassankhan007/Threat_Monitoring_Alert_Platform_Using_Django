from rest_framework.permissions import BasePermission, SAFE_METHODS


class EventPermissions(BasePermission):
    """
    - Any authenticated user can POST events (ingestion).
    - Admin only can list/retrieve events (optional hardening).
    """

    def has_permission(self, request, view):
        if request.method == "POST":
            return request.user.is_authenticated
        if request.method in SAFE_METHODS:
            return request.user.is_authenticated and request.user.is_admin_role
        return request.user.is_authenticated and request.user.is_admin_role


class AlertPermissions(BasePermission):
    """
    - Admin: full access to alert status update
    - Analyst: read-only alerts
    """

    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return request.user.is_authenticated
        return request.user.is_authenticated and request.user.is_admin_role
