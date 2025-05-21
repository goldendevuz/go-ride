from django.contrib import admin
from import_export import resources
from import_export.admin import ImportExportModelAdmin

from apps.v1.shared.admin import BaseAdmin
from .models import Doctor, WorkingHour, Favorite, History, SecuritySetting

class DoctorResource(resources.ModelResource):
    class Meta:
        model = Doctor

class FavoriteResource(resources.ModelResource):
    class Meta:
        model = Favorite

class HistoryResource(resources.ModelResource):
    class Meta:
        model = History

class SecuritySettingResource(resources.ModelResource):
    class Meta:
        model = SecuritySetting

class WorkingHourResource(resources.ModelResource):
    class Meta:
        model = WorkingHour

@admin.register(Doctor)
class DoctorAdmin(ImportExportModelAdmin, BaseAdmin):
    resource_classes = [DoctorResource]
    list_display = tuple(f.name for f in Doctor._meta.fields if f.name not in ('id',))
    list_filter = ('specialty',)
    search_fields = ('owner__username', 'owner__email', 'specialty__name')
    readonly_fields = ('created_at', 'updated_at')
    ordering = ('-created_at',)

@admin.register(Favorite)
class FavoriteAdmin(ImportExportModelAdmin, BaseAdmin):
    resource_classes = [FavoriteResource]
    list_display = tuple(f.name for f in Favorite._meta.fields if f.name not in ('id',))
    list_filter = ('doctor', 'user')
    search_fields = ('user__username', 'doctor__owner__username')
    readonly_fields = ('created_at', 'updated_at')
    ordering = ('-created_at',)

@admin.register(History)
class HistoryAdmin(ImportExportModelAdmin, BaseAdmin):
    resource_classes = [HistoryResource]
    list_display = tuple(f.name for f in History._meta.fields if f.name not in ('id',))
    list_filter = ('doctor', 'action')
    search_fields = ('doctor__owner__username', 'action')
    readonly_fields = ('created_at', 'updated_at')
    ordering = ('-created_at',)

@admin.register(SecuritySetting)
class SecuritySettingAdmin(ImportExportModelAdmin, BaseAdmin):
    resource_classes = [SecuritySettingResource]
    list_display = tuple(f.name for f in SecuritySetting._meta.fields if f.name not in ('id',))
    list_filter = ('user',)
    search_fields = ('user__username',)
    readonly_fields = ('created_at', 'updated_at')
    ordering = ('-created_at',)

@admin.register(WorkingHour)
class WorkingHourAdmin(ImportExportModelAdmin, BaseAdmin):
    resource_classes = [WorkingHourResource]
    list_display = tuple(f.name for f in WorkingHour._meta.fields if f.name not in ('id',))
    list_filter = ('doctor', 'day_of_week')
    search_fields = ('doctor__owner__username',)
    readonly_fields = ('created_at', 'updated_at')
    ordering = ('doctor', 'day_of_week')