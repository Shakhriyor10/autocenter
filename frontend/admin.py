from django.contrib import admin
from modeltranslation.admin import TranslationAdmin, TranslationTabularInline

from frontend.models import Banner, Brand, Car, CarBanner, CarColor, CarFeature, ContactRequest


@admin.register(Banner)
class BannerAdmin(TranslationAdmin):
    list_display = ("title", "car", "sort_order", "is_active", "created_at")
    list_filter = ("is_active",)
    search_fields = ("title", "short_description")
    list_editable = ("sort_order", "is_active")


class CarColorInline(TranslationTabularInline):
    model = CarColor
    extra = 1
    fields = ("name", "primary_color", "secondary_color", "image", "sort_order")


class CarBannerInline(TranslationTabularInline):
    model = CarBanner
    extra = 1
    max_num = 5
    fields = ("image", "video", "short_description", "sort_order", "is_active")


class CarFeatureInline(TranslationTabularInline):
    model = CarFeature
    extra = 1
    max_num = 8
    fields = ("image", "video", "title", "description", "position", "is_active")


@admin.register(Car)
class CarAdmin(TranslationAdmin):
    list_display = (
        "title",
        "brand",
        "model_name",
        "navbar_position",
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
    list_editable = ("navbar_position",)
    inlines = (CarBannerInline, CarColorInline, CarFeatureInline)


@admin.register(CarColor)
class CarColorAdmin(TranslationAdmin):
    list_display = ("car", "name", "primary_color", "secondary_color", "sort_order")
    list_filter = ("car__brand",)
    search_fields = ("car__title", "car__model_name", "name")


@admin.register(CarBanner)
class CarBannerAdmin(TranslationAdmin):
    list_display = ("car", "short_description", "sort_order", "is_active")
    list_filter = ("car__brand", "is_active")
    search_fields = ("car__title", "car__model_name", "short_description")


@admin.register(Brand)
class BrandAdmin(TranslationAdmin):
    search_fields = ("name",)


@admin.register(CarFeature)
class CarFeatureAdmin(TranslationAdmin):
    list_display = ("car", "title", "position", "is_active")
    list_filter = ("car__brand", "is_active")
    search_fields = ("car__title", "car__model_name", "title", "description")


@admin.register(ContactRequest)
class ContactRequestAdmin(admin.ModelAdmin):
    list_display = ("name", "phone", "created_at")
    search_fields = ("name", "phone", "message")
    readonly_fields = ("name", "phone", "message", "created_at")
    ordering = ("-created_at",)
