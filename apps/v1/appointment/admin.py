from django.contrib import admin
from import_export import resources
from import_export.admin import ImportExportModelAdmin

from apps.v1.shared.admin import BaseAdmin
from .models import Appointment, Reason, Review, ReviewLike, Rate

class AppointmentResource(resources.ModelResource):
    class Meta:
        model = Appointment

class RateResource(resources.ModelResource):
    class Meta:
        model = Rate

class ReasonResource(resources.ModelResource):
    class Meta:
        model = Reason

class ReviewResource(resources.ModelResource):
    class Meta:
        model = Review

class ReviewLikeResource(resources.ModelResource):
    class Meta:
        model = ReviewLike

@admin.register(Appointment)
class AppointmentAdmin(ImportExportModelAdmin, BaseAdmin):
    resource_classes = [AppointmentResource]
    list_display = tuple(f.name for f in Appointment._meta.fields if f.name not in ('id',))
    list_filter = ('status', 'doctor', 'patient', 'date')
    search_fields = ('doctor__owner__username', 'patient__username', 'status')
    readonly_fields = ('created_at', 'updated_at')
    ordering = ('-date',)

@admin.register(Rate)
class RateAdmin(ImportExportModelAdmin, BaseAdmin):
    resource_classes = [RateResource]
    list_display = tuple(f.name for f in Rate._meta.fields if f.name not in ('id',))
    list_filter = ('appointment', 'rating')
    search_fields = ('appointment__doctor__owner__username', 'appointment__patient__username')
    readonly_fields = ('created_at', 'updated_at')
    ordering = ('-created_at',)

@admin.register(Reason)
class ReasonAdmin(ImportExportModelAdmin, BaseAdmin):
    resource_classes = [ReasonResource]
    list_display = tuple(f.name for f in Reason._meta.fields if f.name not in ('id',))
    list_filter = ('type',)
    search_fields = ('description',)
    readonly_fields = ('created_at', 'updated_at')
    ordering = ('-created_at',)

@admin.register(Review)
class ReviewAdmin(ImportExportModelAdmin, BaseAdmin):
    resource_classes = [ReviewResource]
    list_display = tuple(f.name for f in Review._meta.fields if f.name not in ('id',))
    list_filter = ('appointment', 'rating')
    search_fields = ('appointment__doctor__owner__username', 'appointment__patient__username', 'comment')
    readonly_fields = ('created_at', 'updated_at')
    ordering = ('-created_at',)

@admin.register(ReviewLike)
class ReviewLikeAdmin(ImportExportModelAdmin, BaseAdmin):
    resource_classes = [ReviewLikeResource]
    list_display = tuple(f.name for f in ReviewLike._meta.fields if f.name not in ('id',))
    list_filter = ('review', 'user')
    search_fields = ('review__comment', 'user__username')
    readonly_fields = ('created_at', 'updated_at')
    ordering = ('-created_at',)