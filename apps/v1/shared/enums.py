from django.db import models


# --- Auth status ---
class AuthStatus(models.TextChoices):
    NEW = "new", "New"
    CODE_VERIFIED = "code_verified", "Code Verified"
    DONE = "done", "Done"


# --- Verification type ---
class AuthType(models.TextChoices):
    VIA_PHONE = "via_phone", "Via Phone"
    VIA_EMAIL = "via_email", "Via Email"


# --- Notification ---
class NotificationStates(models.TextChoices):
    NEW = "new", "New"
    READ = "read", "Read"


# --- Theme ---
class ThemeChoices(models.TextChoices):
    SYSTEM = "system", "System"
    LIGHT = "light", "Light"
    DARK = "dark", "Dark"


# --- Gender ---
class GenderChoices(models.TextChoices):
    MALE = "male", "Male"
    FEMALE = "female", "Female"


# --- Role ---
class RoleChoices(models.TextChoices):
    PASSENGER = "passenger", "Passenger"
    CUSTOMER = "customer", "Customer"
    DRIVER = "driver", "Driver"
    MANAGER = "manager", "Manager"
    ADMIN = "admin", "Admin"
    SUPER_ADMIN = "super_admin", "Super Admin"


# --- Expiry times ---
PHONE_EXPIRE = 2  # minutes
EMAIL_EXPIRE = 2  # minutes

from django.db import models


class PaymentStatuses(models.TextChoices):
    PENDING = "pending", "Pending"
    PAID = "paid", "Paid"
    FAILED = "failed", "Failed"
    REFUNDED = "refunded", "Refunded"
