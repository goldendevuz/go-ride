from django import forms
from django.contrib import admin
from import_export import resources
from import_export.admin import ImportExportModelAdmin

from apps.v1.shared.admin import BaseAdmin
from .models import User, UserConfirmation, Profile

class UserConfirmationResource(resources.ModelResource):
    class Meta:
        model = UserConfirmation

class UserResource(resources.ModelResource):
    class Meta:
        model = User

class ProfileResource(resources.ModelResource):
    class Meta:
        model = Profile

class CustomUserForm(forms.ModelForm):
    class Meta:
        model = User
        exclude = ()

@admin.register(Profile)
class ProfileAdmin(ImportExportModelAdmin, BaseAdmin):
    resource_classes = [ProfileResource]
    list_display = tuple(f.name for f in Profile._meta.fields if f.name not in ('id',))
    list_filter = ('gender',)
    search_fields = ('user__username',)

@admin.register(UserConfirmation)
class UserConfirmationAdmin(ImportExportModelAdmin, BaseAdmin):
    resource_classes = [UserConfirmationResource]
    list_display = tuple(f.name for f in UserConfirmation._meta.fields if f.name not in ('id',))
    list_filter = ('verify_type', 'is_confirmed')
    search_fields = ('verify_value', 'user__username')

@admin.register(User)
class UserAdmin(ImportExportModelAdmin, BaseAdmin):
    form = CustomUserForm
    resource_classes = [UserResource]
    list_display = tuple(f.name for f in User._meta.fields if f.name not in ('password', 'is_staff', 'is_superuser', 'id'))
    search_fields = ('username', 'email', 'phone')
    list_filter = ('auth_status', 'is_active')