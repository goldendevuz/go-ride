from django.contrib import admin
from import_export import resources
from import_export.admin import ImportExportModelAdmin

from apps.v1.shared.admin import BaseAdmin
from apps.v1.system.models.language import Language
from apps.v1.system.models.payment_type import PaymentType
from .models import Notification, NotificationSetting, Payment

class LanguageResource(resources.ModelResource):
    class Meta:
        model = Language

class NotificationResource(resources.ModelResource):
    class Meta:
        model = Notification

class NotificationSettingResource(resources.ModelResource):
    class Meta:
        model = NotificationSetting

class PaymentTypeResource(resources.ModelResource):
    class Meta:
        model = PaymentType

class PaymentResource(resources.ModelResource):
    class Meta:
        model = Payment

@admin.register(Language)
class LanguageAdmin(ImportExportModelAdmin, BaseAdmin):
    resource_classes = [LanguageResource]
    list_display = tuple(f.name for f in Language._meta.fields if f.name not in ('id',))

@admin.register(Notification)
class NotificationAdmin(ImportExportModelAdmin, BaseAdmin):
    resource_classes = [NotificationResource]
    list_display = tuple(f.name for f in Notification._meta.fields if f.name not in ('id',))
    list_filter = ()
    search_fields = ('title', 'message')

@admin.register(NotificationSetting)
class NotificationSettingAdmin(ImportExportModelAdmin, BaseAdmin):
    resource_classes = [NotificationSettingResource]
    list_display = tuple(f.name for f in NotificationSetting._meta.fields if f.name not in ('id',))
    list_filter = ()
    search_fields = ('user__username',)

@admin.register(PaymentType)
class PaymentTypeAdmin(ImportExportModelAdmin, BaseAdmin):
    resource_classes = [PaymentTypeResource]
    list_display = tuple(f.name for f in PaymentType._meta.fields if f.name not in ('id',))

@admin.register(Payment)
class PaymentAdmin(ImportExportModelAdmin, BaseAdmin):
    resource_classes = [PaymentResource]
    list_display = tuple(f.name for f in Payment._meta.fields if f.name not in ('id',))
    list_filter = ('status',)
    search_fields = ('user__username',)
