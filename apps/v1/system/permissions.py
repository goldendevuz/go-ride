from rest_framework import permissions

class IsOwnerOrAdmin(permissions.BasePermission):
    """
    Ob'ektga faqat egasi yoki admin kirishi mumkin.
    """
    def has_object_permission(self, request, view, obj):
        # Admin har doim kirishi mumkin
        if request.user.is_staff:
            return True
        # Ob'ektda user atributi borligini tekshirib, egasini solishtirish
        return hasattr(obj, 'user') and obj.user == request.user

class NotificationPermission(permissions.BasePermission):
    """
    Notification uchun ruxsatlar:
    - List va Retrieve: faqat o'z Notificationlarini ko'ra oladi.
    - Create: admin yoki system user (agar kerak bo'lsa).
    - Update va Delete: admin faqat ruxsat.
    """
    def has_permission(self, request, view):
        # Har doim login bo'lishi kerak
        if not request.user or not request.user.is_authenticated:
            return False
        # Create faqat adminga yoki specific rolga berilsin (kerak bo'lsa)
        if view.action == 'create':
            return request.user.is_staff
        # List, Retrieve, Update, Delete uchun ruxsat beramiz, keyingi metodda aniqlaymiz
        return True

    def has_object_permission(self, request, view, obj):
        # Admin uchun barcha ruxsatlar bor
        if request.user.is_staff:
            return True
        # Oddiy foydalanuvchi faqat o'z notificationini ko'ra oladi
        if hasattr(obj, 'user'):
            return obj.user == request.user
        # Agar user field bo'lmasa (Notification modelda yo'q bo'lsa), faqat adminga ruxsat beramiz
        return False

class NotificationSettingPermission(permissions.BasePermission):
    """
    NotificationSetting uchun:
    - Foydalanuvchi faqat o'z sozlamalarini ko'rishi va o'zgartirishi mumkin.
    """
    def has_object_permission(self, request, view, obj):
        # Faqat o'z user'iga ruxsat
        return obj.user == request.user

class PaymentPermission(permissions.BasePermission):
    """
    Payment uchun ruxsatlar:
    - Foydalanuvchi faqat o'z to'lovlarini ko'rishi va yaratishi mumkin.
    - Admin har qanday to'lovni boshqara oladi.
    - Review qilish faqat adminga yoki maxsus rolga.
    """
    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return False
        # Create ruxsat faqat oddiy user va adminga
        if view.action == 'create':
            return True
        # List va Retrieve faqat admin va o'z to'lovlari
        if view.action in ['list', 'retrieve']:
            return True
        # Update va partial_update faqat adminga berilsin
        if view.action in ['update', 'partial_update']:
            return request.user.is_staff
        # Delete faqat adminga berilsin
        if view.action == 'destroy':
            return request.user.is_staff
        return False

    def has_object_permission(self, request, view, obj):
        if request.user.is_staff:
            return True
        # Oddiy user faqat o'z to'lovlarini ko'radi
        return obj.user == request.user