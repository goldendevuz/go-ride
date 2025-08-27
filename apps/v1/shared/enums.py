from django.db import models
from django.utils.translation import gettext_lazy as _


# --- Auth status ---
class AuthStatus(models.TextChoices):
    NEW = "new", _("New")
    CODE_VERIFIED = "code_verified", _("Code Verified")
    DONE = "done", _("Done")


# --- Verification type ---
class AuthType(models.TextChoices):
    VIA_PHONE = "via_phone", _("Via Phone")
    VIA_EMAIL = "via_email", _("Via Email")


# --- Notification ---
class NotificationStates(models.TextChoices):
    NEW = "new", _("New")
    READ = "read", _("Read")


# --- Theme ---
class ThemeChoices(models.TextChoices):
    SYSTEM = "system", _("System")
    LIGHT = "light", _("Light")
    DARK = "dark", _("Dark")


# --- Gender ---
class GenderChoices(models.TextChoices):
    MALE = "male", _("Male")
    FEMALE = "female", _("Female")


# --- Role ---
class RoleChoices(models.TextChoices):
    PASSENGER = "passenger", _("Passenger")
    CUSTOMER = "customer", _("Customer")
    DRIVER = "driver", _("Driver")
    MANAGER = "manager", _("Manager")
    ADMIN = "admin", _("Admin")
    SUPER_ADMIN = "super_admin", _("Super Admin")


# --- Expiry times ---
PHONE_EXPIRE = 2  # minutes
EMAIL_EXPIRE = 2  # minutes


# --- Payment Status ---
class PaymentStatuses(models.TextChoices):
    PENDING = "pending", _("Pending")
    PAID = "paid", _("Paid")
    FAILED = "failed", _("Failed")
    REFUNDED = "refunded", _("Refunded")

class DiscountType(models.TextChoices):
    PERCENT = 'percent', _('Percent')
    AMOUNT = 'amount', _('Amount')

class FAQCategories(models.TextChoices):
    GENERAL = 'general', _('General')
    ACCOUNT = 'account', _('Account')
    SERVICES = 'services', _('Services')
    RIDE = 'ride', _('Ride')

# --- Seats Count ---
class SeatsCountChoices(models.TextChoices):
    ONE_SEAT = "one_seat", _("One Seat")
    TWO_SEATS = "two_seats", _("Two Seats")
    FULL = "full", _("Full")

# --- Promo Information Type ---
class PromoInformationType(models.TextChoices):
    TERMS_AND_CONDITIONS = "terms_and_conditions", _("Terms and Conditions")
    HOW_TO_USE = "how_to_use", _("How to Use")
    ADDITIONAL_INFORMATION = "additional_information", _("Additional Information")

# --- Appointment Status ---
class AppointmentStatuses(models.TextChoices):
    PENDING = "pending", _("Pending")
    SCHEDULED = "scheduled", _("Scheduled")
    CANCELED = "canceled", _("Canceled")
    RESCHEDULED = "rescheduled", _("Rescheduled")
    APPROVED = "approved", _("Approved")
    ONGOING = "ongoing", _("Ongoing")
    COMPLETED = "completed", _("Completed")
    REFUNDED = "refunded", _("Refunded")

# --- Reason Type ---
class ReasonTypes(models.TextChoices):
    CHANGE_IN_PLANS = "change_in_plans", _("Change in Plans")
    WAITING_FOR_LONG_TIME = "waiting_for_long_time", _("Waiting for Long Time")
    UNABLE_TO_CONTACT_DRIVER = "unable_to_contact_driver", _("Unable to Contact Driver")
    DRIVER_DENIED_TO_GO_TO_DESTINATION = "driver_denied_to_go_to_destination", _("Driver Denied to Go to Destination")
    DRIVER_DENIED_TO_GO_TO_PICKUP = "driver_denied_to_go_to_pickup", _("Driver Denied to Go to Pickup")
    WRONG_ADDRESS_SHOWN = "wrong_address_shown", _("Wrong Address Shown")
    THIS_PRICE_IS_NOT_REASONABLE = "this_price_is_not_reasonable", _("This Price is Not Reasonable")
    EMERGENCY_SITUATION = "emergency_sitation", _("Emergency Situation")
    BOOKING_MISTAKE = "booking_mistake", _("Booking Mistake")
    POOR_WEATHER_CONDITIONS = "poor_weather_conditions", _("Poor Weather Conditions")
    OTHER = "other", _("Other")