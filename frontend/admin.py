from django.contrib import admin

from frontend.models import Brand, Car


@admin.register(Car)
class CarAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "brand",
        "model_name",
        "engine_type",
        "engine_volume",
        "transmission_type",
        "price",
        "discount_price",
        "discount_until",
        "is_hot",
        "created_at",
    )
    list_filter = ("brand", "engine_type", "transmission_type", "is_hot")
    search_fields = ("title", "model_name", "brand__name")


admin.site.register(Brand)