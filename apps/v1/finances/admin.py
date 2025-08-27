from django.contrib import admin
from django.utils.html import format_html
from django.db import models as dj_models
from import_export import resources
from import_export.admin import ImportExportModelAdmin
from parler.admin import TranslatableAdmin, TranslatableStackedInline

from apps.v1.shared.admin import BaseAdmin
from .models import (
    Card,
    PaymentType,
    Payment,
    PromoInformation,
    Promotion,
    SupportedPayment,
    TopUp,
    Wallet,
)

# Helper function to get model fields
def get_model_fields(model):
    """
    Returns a tuple of field names, excluding ID.
    """
    return tuple(f.name for f in model._meta.fields if f.name != 'id')

# Helper function to get translatable fields
def get_translatable_fields(model):
    """
    Returns a list of field names that are translatable.
    """
    if hasattr(model, 'translations'):
        return [f.name for f in model.translations.fields]
    return []

def register_model(model):
    """
    Dynamically registers a model with the Django admin,
    handling both Translatable and non-Translatable models.
    """
    # Create dynamic resource class for import/export
    resource_class = type(
        f"{model.__name__}Resource",
        (resources.ModelResource,),
        {"Meta": type("Meta", (), {"model": model})}
    )

    # Base admin attributes
    admin_attrs = {
        "resource_classes": [resource_class],
        "list_filter": [],
        "search_fields": [],
    }

    # Build the list of admin base classes
    base_classes = [ImportExportModelAdmin, BaseAdmin]

    # Check for Parler integration and add the appropriate admin class
    if hasattr(model, 'translations'):
        base_classes.insert(0, TranslatableAdmin)
    
    # Get non-translatable fields for list_display and search
    translatable_fields = get_translatable_fields(model)
    non_translatable_fields = [
        f.name for f in model._meta.fields
        if f.name != 'id' and f.name not in translatable_fields
    ]
    
    # Handle non-translatable fields
    admin_attrs["list_display"] = list(non_translatable_fields)
    admin_attrs["list_filter"] = list(non_translatable_fields)
    admin_attrs["search_fields"] = list(non_translatable_fields)

    # Add custom image and text display methods
    image_fields = [f.name for f in model._meta.fields if isinstance(f, dj_models.ImageField)]
    text_fields = [f.name for f in model._meta.fields if isinstance(f, dj_models.TextField)]

    for field in text_fields:
        method_name = f"short_{field}"
        def make_text_preview(field_name):
            def short_text(self, obj):
                val = getattr(obj, field_name)
                return (val[:47] + "...") if val and len(val) > 50 else val
            short_text.short_description = field_name
            return short_text
        admin_attrs[method_name] = make_text_preview(field)
        admin_attrs["list_display"].append(method_name)

    for field in image_fields:
        method_name = f"show_{field}"
        def make_thumb_func(field_name):
            def thumb(self, obj):
                val = getattr(obj, field_name)
                if val and hasattr(val, 'url'):
                    return format_html(
                        '<a href="{0}" target="_blank">'
                        '<img src="{0}" width="100" height="100" style="object-fit: cover; border-radius: 4px;" />'
                        '</a>',
                        val.url
                    )
                return "-"
            thumb.short_description = field_name
            thumb.allow_tags = True
            return thumb
        admin_attrs[method_name] = make_thumb_func(field)
        admin_attrs["list_display"].append(method_name)
    
    # Parler specific configurations for translatable models
    if hasattr(model, 'translations'):
        # Add translated fields to list display
        admin_attrs["list_display"].extend(translatable_fields)
        # Parler handles search and filter for translated fields automatically
        # Removed the `__startswith` lookup as it is not needed with Parler's search
        admin_attrs["search_fields"].extend(translatable_fields)

    # Create and register the admin class
    admin_class = type(
        f"{model.__name__}Admin",
        tuple(base_classes),
        admin_attrs
    )

    admin.site.register(model, admin_class)

# List of models to register
registered_models = [
    Card,
    PaymentType,
    Payment,
    PromoInformation,
    Promotion,
    SupportedPayment,
    TopUp,
    Wallet,
]

for model in registered_models:
    try:
        register_model(model)
    except Exception as e:
        print(f"Failed to register {model.__name__}: {e}")