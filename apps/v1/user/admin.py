from django import forms
from django.contrib import admin
from import_export import resources
from import_export.admin import ImportExportModelAdmin

from apps.v1.shared.admin import BaseAdmin
from .models import User, UserConfirmation, Profile

# Resource classes
class UserResource(resources.ModelResource):
    class Meta:
        model = User

class ProfileResource(resources.ModelResource):
    class Meta:
        model = Profile

class UserConfirmationResource(resources.ModelResource):
    class Meta:
        model = UserConfirmation

# Custom form to hide password
class CustomUserForm(forms.ModelForm):
    class Meta:
        model = User
        exclude = ('password',)

# Admin classes
@admin.register(User)
class UserAdmin(ImportExportModelAdmin, BaseAdmin):
    form = CustomUserForm
    resource_classes = [UserResource]
    list_display = tuple(f.name for f in User._meta.fields if f.name not in (
        'password', 'groups', 'user_permissions', 'is_staff', 'is_superuser'
    ))
    search_fields = ('username', 'email', 'phone')
    list_filter = ('role', 'auth_status', 'is_active')
    readonly_fields = ('last_login', 'date_joined')

@admin.register(UserConfirmation)
class UserConfirmationAdmin(ImportExportModelAdmin, BaseAdmin):
    resource_classes = [UserConfirmationResource]
    list_display = tuple(f.name for f in UserConfirmation._meta.fields if f.name)
    list_filter = ('verify_type', 'is_confirmed')
    search_fields = ('verify_value', 'user__username')

@admin.register(Profile)
class ProfileAdmin(ImportExportModelAdmin, BaseAdmin):
    resource_classes = [ProfileResource]
    list_display = tuple(f.name for f in Profile._meta.fields if f.name)
    list_filter = ('gender',)
    search_fields = ('user__username',)