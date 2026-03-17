from django.contrib import admin

from frontend.models import Brand, Car, CarImage, EngineType, TransmissionType


class CarImageInline(admin.TabularInline):
    model = CarImage
    extra = 1
    max_num = 5


@admin.register(Car)
class CarAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "brand",
        "model_name",
        "engine_type",
        "engine_volume",
        "transmission_type",
    )
    list_filter = ("brand", "engine_type", "transmission_type")
    search_fields = ("title", "model_name", "brand__name")
    inlines = (CarImageInline,)


admin.site.register(Brand)
admin.site.register(EngineType)
admin.site.register(TransmissionType)
