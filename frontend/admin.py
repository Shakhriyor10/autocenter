from django.contrib import admin

from frontend.models import Banner, Brand, Car, CarBanner


class CarBannerInline(admin.TabularInline):
    model = CarBanner
    extra = 1
    fields = ("media_type", "image", "video_url", "title", "sort_order", "is_active")


@admin.register(Banner)
class BannerAdmin(admin.ModelAdmin):
    list_display = ("title", "sort_order", "is_active", "created_at")
    list_filter = ("is_active",)
    search_fields = ("title", "short_description")
    list_editable = ("sort_order", "is_active")


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
    inlines = (CarBannerInline,)


@admin.register(CarBanner)
class CarBannerAdmin(admin.ModelAdmin):
    list_display = ("car", "media_type", "sort_order", "is_active", "created_at")
    list_filter = ("media_type", "is_active")
    search_fields = ("car__title", "car__model_name", "title")


admin.site.register(Brand)
