from rest_framework import permissions

class IsAppointmentOwnerOrDoctorOrAdmin(permissions.BasePermission):
    """
    Faqat appointment egasi (foydalanuvchi),
    tegishli shifokor yoki adminlarga ruxsat beradi.
    """
    def has_permission(self, request, view):
        # Bu yerda umumiy permission, masalan login qilinganligini tekshiramiz
        return request.user and request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        # Adminlarga to'liq ruxsat
        if request.user.is_staff or request.user.is_superuser:
            return True
        # Appointment egasi (foydalanuvchi)
        if hasattr(obj, 'user') and obj.user == request.user:
            return True
        # Appointment shifokori (agar doctor maydoni bor bo'lsa)
        if hasattr(obj, 'doctor') and obj.doctor.user == request.user:
            return True
        return False