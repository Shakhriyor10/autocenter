from django.contrib import admin
from django import forms
from modeltranslation.admin import TranslationAdmin, TranslationTabularInline

from frontend.models import Banner, Brand, Car, CarBanner, CarColor, CarFeature, ContactRequest, TeamMember


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
    class CarAdminForm(forms.ModelForm):
        engine_type_multi = forms.MultipleChoiceField(
            label="Тип двигателя",
            choices=Car.EngineType.choices,
            required=False,
            widget=forms.CheckboxSelectMultiple,
        )

        class Meta:
            model = Car
            fields = "__all__"

        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self.fields["engine_type_multi"].initial = self.instance.engine_type_values
            self.fields["engine_type"].widget = forms.HiddenInput()
            self.fields["engine_types"].widget = forms.HiddenInput()

        def clean_engine_type_multi(self):
            return ",".join(self.cleaned_data["engine_type_multi"])

        def save(self, commit=True):
            self.instance.engine_types = self.cleaned_data.get("engine_type_multi", "")
            if not self.instance.engine_type and self.instance.engine_type_values:
                self.instance.engine_type = self.instance.engine_type_values[0]
            return super().save(commit=commit)

    form = CarAdminForm
    list_display = (
        "title",
        "brand",
        "model_name",
        "navbar_position",
        "engine_types_display",
        "engine_volume",
        "fuel_consumption_l_100km",
        "battery_capacity_kwh",
        "drive_type",
        "transmission_type",
        "price",
        "discount_price",
        "discount_until",
        "is_hot",
        "created_at",
    )
    list_filter = ("brand", "drive_type", "transmission_type", "is_hot")
    search_fields = ("title", "model_name", "brand__name")
    list_editable = ("navbar_position",)
    inlines = (CarBannerInline, CarColorInline, CarFeatureInline)

    def engine_types_display(self, obj):
        return obj.engine_types_display
    engine_types_display.short_description = "Тип двигателя"


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


@admin.register(TeamMember)
class TeamMemberAdmin(TranslationAdmin):
    list_display = ("full_name", "position", "sort_order", "is_active")
    list_filter = ("is_active",)
    search_fields = ("full_name", "position", "short_description")
    list_editable = ("sort_order", "is_active")
