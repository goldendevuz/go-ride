from rest_framework.permissions import BasePermission, SAFE_METHODS

class IsAdminOrReadOnly(BasePermission):
    """
    Read-only (GET, HEAD, OPTIONS) ruxsat barchaga (login bo'lsin yoki bo'lmasin).
    Yozish (POST, PUT, PATCH, DELETE) faqat admin (is_staff) foydalanuvchilarga.
    """
    def has_permission(self, request, view):
        # Agar GET, HEAD, OPTIONS bo'lsa, barchaga ruxsat
        if request.method in SAFE_METHODS:
            return True
        # Boshqa metodlar uchun faqat adminlarga ruxsat
        return request.user and request.user.is_authenticated and request.user.is_staff