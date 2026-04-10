from django.contrib import admin

from frontend.models import Banner, Brand, Car, CarBanner, CarColor, CarFeature


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


class CarBannerInline(admin.TabularInline):
    model = CarBanner
    extra = 1
    max_num = 5
    fields = ("image", "short_description", "sort_order", "is_active")


class CarFeatureInline(admin.TabularInline):
    model = CarFeature
    extra = 1
    max_num = 8
    fields = ("image", "title", "description", "position", "is_active")


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
    inlines = (CarBannerInline, CarColorInline, CarFeatureInline)


@admin.register(CarColor)
class CarColorAdmin(admin.ModelAdmin):
    list_display = ("car", "name", "primary_color", "secondary_color", "sort_order")
    list_filter = ("car__brand",)
    search_fields = ("car__title", "car__model_name", "name")


@admin.register(CarBanner)
class CarBannerAdmin(admin.ModelAdmin):
    list_display = ("car", "short_description", "sort_order", "is_active")
    list_filter = ("car__brand", "is_active")
    search_fields = ("car__title", "car__model_name", "short_description")


admin.site.register(Brand)


@admin.register(CarFeature)
class CarFeatureAdmin(admin.ModelAdmin):
    list_display = ("car", "title", "position", "is_active")
    list_filter = ("car__brand", "is_active")
    search_fields = ("car__title", "car__model_name", "title", "description")
