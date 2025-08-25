from rest_framework import permissions

class IsOwnerOrAdmin(permissions.BasePermission):
    """
    Faqat obyekt egasi (Doctor.user) yoki adminlarga ruxsat beradi.
    """
    def has_object_permission(self, request, view, obj):
        # Adminlar to'liq ruxsatga ega
        if request.user.is_staff or request.user.is_superuser:
            return True
        # Obyekt egasi
        return hasattr(obj, 'user') and obj.user == request.user or request.user.is_staff

class IsDoctorOrAdmin(permissions.BasePermission):
    """
    Faqat doctor profili mavjud bo'lgan foydalanuvchi yoki adminlarga ruxsat beradi.
    """
    def has_permission(self, request, view):
        # Adminlarga ruxsat
        if request.user.is_staff or request.user.is_superuser:
            return True
        # Doctor profili borligini tekshirish
        return request.user.is_authenticated and hasattr(request.user, 'doctor_profile')