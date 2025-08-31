from django.contrib import admin
from django.utils.html import format_html
from django.db import models as dj_models
from import_export import resources
from import_export.admin import ImportExportModelAdmin
from parler.admin import TranslatableAdmin
from parler.models import TranslatableModel

from apps.v1.shared.admin import BaseAdmin
from .models import (
    Chat,
    ContactSupport,
    FAQ,
    Message,
    NotificationSetting,
    Notification,
)

# Helper function to get translatable fields
def get_translatable_fields(model):
    """
    Returns a list of field names that are translatable.
    """
    try:
        # Correctly access the translated fields via the model's _meta
        # This will raise an AttributeError for non-Translatable models
        return [f.name for f in model._meta.translated_fields]
    except AttributeError:
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

    # Determine base class based on Parler inheritance
    is_translatable = issubclass(model, TranslatableModel)
    
    # Get non-translatable and translatable fields
    translatable_fields = get_translatable_fields(model)
    non_translatable_fields = [
        f.name for f in model._meta.fields
        if f.name not in translatable_fields
    ]
    
    # Base admin attributes
    admin_attrs = {
        "resource_classes": [resource_class],
        "list_display": list(non_translatable_fields) + translatable_fields,
        "list_filter": list(non_translatable_fields),
        "search_fields": list(non_translatable_fields),
    }

    # Add Parler-specific search fields
    if is_translatable:
        # Parler handles search for translated fields via a different lookup
        for field in translatable_fields:
            # The search field lookup for Parler should be the field name
            admin_attrs["search_fields"].append(f"{field}")

    # Add custom display methods for text and image fields
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
        admin_attrs["list_display"].insert(0, method_name)

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
            return thumb
        admin_attrs[method_name] = make_thumb_func(field)
        admin_attrs["list_display"].append(method_name)

    # Determine admin base classes
    base_classes = (ImportExportModelAdmin, BaseAdmin)
    if is_translatable:
        base_classes = (TranslatableAdmin,) + base_classes

    # Create and register the admin class
    admin_class = type(
        f"{model.__name__}Admin",
        base_classes,
        admin_attrs
    )
    admin.site.register(model, admin_class)


# List of models to register
registered_models = [
    Chat,
    ContactSupport,
    FAQ,
    Message,
    NotificationSetting,
    Notification,
]

for model in registered_models:
    try:
        register_model(model)
    except Exception as e:
        print(f"Failed to register {model.__name__}: {e}")