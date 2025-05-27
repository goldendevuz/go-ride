from django.contrib import admin
from import_export import resources
from import_export.admin import ImportExportModelAdmin

from apps.v1.shared.admin import BaseAdmin
from .models import Notification, NotificationSetting, Payment

class NotificationResource(resources.ModelResource):
    class Meta:
        model = Notification

class NotificationSettingResource(resources.ModelResource):
    class Meta:
        model = NotificationSetting

class PaymentResource(resources.ModelResource):
    class Meta:
        model = Payment

@admin.register(Notification)
class NotificationAdmin(ImportExportModelAdmin, BaseAdmin):
    resource_classes = [NotificationResource]
    list_display = tuple(f.name for f in Notification._meta.fields if f.name not in ('id',))
    list_filter = ()
    search_fields = ('title', 'message')
    ordering = ('-created_at',)

@admin.register(NotificationSetting)
class NotificationSettingAdmin(ImportExportModelAdmin, BaseAdmin):
    resource_classes = [NotificationSettingResource]
    list_display = tuple(f.name for f in NotificationSetting._meta.fields if f.name not in ('id',))
    list_filter = ()
    search_fields = ('user__username',)
    ordering = ('-created_at',)

@admin.register(Payment)
class PaymentAdmin(ImportExportModelAdmin, BaseAdmin):
    resource_classes = [PaymentResource]
    list_display = tuple(f.name for f in Payment._meta.fields if f.name not in ('id',))
    list_filter = ('status', 'method')
    search_fields = ('transaction_id', 'user__username')
    ordering = ('-created_at',)