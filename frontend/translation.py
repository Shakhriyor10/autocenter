from modeltranslation.translator import TranslationOptions, register

from frontend.models import Banner, Brand, Car, CarBanner, CarColor, CarFeature, TeamMember


@register(Brand)
class BrandTranslationOptions(TranslationOptions):
    fields = ("name",)


@register(Banner)
class BannerTranslationOptions(TranslationOptions):
    fields = ("title", "short_description")


@register(Car)
class CarTranslationOptions(TranslationOptions):
    fields = ("title", "model_name")


@register(CarColor)
class CarColorTranslationOptions(TranslationOptions):
    fields = ("name",)


@register(CarBanner)
class CarBannerTranslationOptions(TranslationOptions):
    fields = ("short_description",)


@register(CarFeature)
class CarFeatureTranslationOptions(TranslationOptions):
    fields = ("title", "description")


@register(TeamMember)
class TeamMemberTranslationOptions(TranslationOptions):
    fields = ("full_name", "position", "short_description")
