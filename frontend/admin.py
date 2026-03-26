from django.contrib import admin

from frontend.models import Banner, Brand, Car, CarColor


@admin.register(Banner)
class BannerAdmin(admin.ModelAdmin):
    list_display = ("title", "sort_order", "is_active", "created_at")
    list_filter = ("is_active",)
    search_fields = ("title", "short_description")
    list_editable = ("sort_order", "is_active")


class CarColorInline(admin.TabularInline):
    model = CarColor
    extra = 1
    fields = ("name", "primary_color", "secondary_color", "image", "sort_order")


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
    inlines = (CarColorInline,)


@admin.register(CarColor)
class CarColorAdmin(admin.ModelAdmin):
    list_display = ("car", "name", "primary_color", "secondary_color", "sort_order")
    list_filter = ("car__brand",)
    search_fields = ("car__title", "car__model_name", "name")


admin.site.register(Brand)