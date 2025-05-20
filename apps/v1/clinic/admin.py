from django.contrib import admin
from import_export import resources
from import_export.admin import ImportExportModelAdmin

from apps.v1.shared.admin import BaseAdmin
from .models import Hospital, Specialty, Service, Banner, ContactUs

class HospitalResource(resources.ModelResource):
    class Meta:
        model = Hospital

class SpecialtyResource(resources.ModelResource):
    class Meta:
        model = Specialty

class ServiceResource(resources.ModelResource):
    class Meta:
        model = Service

class BannerResource(resources.ModelResource):
    class Meta:
        model = Banner

class ContactUsResource(resources.ModelResource):
    class Meta:
        model = ContactUs


@admin.register(Hospital)
class HospitalAdmin(ImportExportModelAdmin, BaseAdmin):
    resource_classes = [HospitalResource]
    list_display = tuple(f.name for f in Hospital._meta.fields if f.name)

@admin.register(Specialty)
class SpecialtyAdmin(ImportExportModelAdmin, BaseAdmin):
    resource_classes = [SpecialtyResource]
    list_display = tuple(f.name for f in Specialty._meta.fields if f.name)

@admin.register(Service)
class ServiceAdmin(ImportExportModelAdmin, BaseAdmin):
    resource_classes = [ServiceResource]
    list_display = tuple(f.name for f in Service._meta.fields if f.name)

@admin.register(Banner)
class BannerAdmin(ImportExportModelAdmin, BaseAdmin):
    resource_classes = [BannerResource]
    list_display = tuple(f.name for f in Banner._meta.fields if f.name)

@admin.register(ContactUs)
class ContactUsAdmin(ImportExportModelAdmin, BaseAdmin):
    resource_classes = [ContactUsResource]
    list_display = tuple(f.name for f in ContactUs._meta.fields if f.name)