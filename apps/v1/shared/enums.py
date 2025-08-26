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

class DiscountType(models.TextChoices):
    PERCENT = 'percent', 'Percent'
    AMOUNT = 'amount', 'Amount'

class FAQCategories(models.TextChoices):
    GENERAL = 'general', 'General'
    ACCOUNT = 'account', 'Account'
    SERVICES = 'services', 'Services'
    RIDE = 'ride', 'Ride'

# --- Seats Count ---
class SeatsCountChoices(models.TextChoices):
    ONE_SEAT = "one_seat", "One Seat"
    TWO_SEATS = "two_seats", "Two Seats"
    FULL = "full", "Full"

# --- Promo Information Type ---
class PromoInformationType(models.TextChoices):
    TERMS_AND_CONDITIONS = "terms_and_conditions", "Terms and Conditions"
    HOW_TO_USE = "how_to_use", "How to Use"
    ADDITIONAL_INFORMATION = "additional_information", "Additional Information"

# --- Payment Status ---
class PaymentStatuses(models.TextChoices):
    PENDING = "pending", "Pending"
    PAID = "paid", "Paid"
    FAILED = "failed", "Failed"
    REFUNDED = "refunded", "Refunded"

# --- Appointment Status ---
class AppointmentStatuses(models.TextChoices):
    PENDING = "pending", "Pending"
    SCHEDULED = "scheduled", "Scheduled"
    CANCELED = "canceled", "Canceled"
    RESCHEDULED = "rescheduled", "Rescheduled"
    APPROVED = "approved", "Approved"
    ONGOING = "ongoing", "Ongoing"
    COMPLETED = "completed", "Completed"
    REFUNDED = "refunded", "Refunded"

# --- Reason Type ---
class ReasonTypes(models.TextChoices):
    CHANGE_IN_PLANS = "change_in_plans", "Change in Plans"
    WAITING_FOR_LONG_TIME = "waiting_for_long_time", "Waiting for Long Time"
    UNABLE_TO_CONTACT_DRIVER = "unable_to_contact_driver", "Unable to Contact Driver"
    DRIVER_DENIED_TO_GO_TO_DESTINATION = "driver_denied_to_go_to_destination", "Driver Denied to Go to Destination"
    DRIVER_DENIED_TO_GO_TO_PICKUP = "driver_denied_to_go_to_pickup", "Driver Denied to Go to Pickup"
    WRONG_ADDRESS_SHOWN = "wrong_address_shown", "Wrong Address Shown"
    THIS_PRICE_IS_NOT_REASONABLE = "this_price_is_not_reasonable", "This Price is Not Reasonable"
    EMERGENCY_SITUATION = "emergency_sitation", "Emergency Situation"
    BOOKING_MISTAKE = "booking_mistake", "Booking Mistake"
    POOR_WEATHER_CONDITIONS = "poor_weather_conditions", "Poor Weather Conditions"
    OTHER = "other", "Other"
