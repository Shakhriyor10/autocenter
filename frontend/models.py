from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator
from django.db import models
from django.utils.translation import gettext_lazy as _


class Brand(models.Model):
    name = models.CharField("Название бренда", max_length=120, unique=True)

    class Meta:
        verbose_name = "Бренд"
        verbose_name_plural = "Бренды"
        ordering = ("name",)

    def __str__(self):
        return self.name


class Banner(models.Model):
    title = models.CharField("Название", max_length=200)
    short_description = models.CharField("Короткое описание", max_length=255)
    image = models.ImageField("Фото", upload_to="banners/")
    mobile_image = models.ImageField(
        "Фото для мобильной версии",
        upload_to="banners/mobile/",
        null=True,
        blank=True,
    )
    car = models.ForeignKey(
        "Car",
        on_delete=models.SET_NULL,
        related_name="homepage_banners",
        verbose_name="Автомобиль для кнопки",
        null=True,
        blank=True,
    )
    sort_order = models.PositiveIntegerField("Порядок сортировки", default=0)
    is_active = models.BooleanField("Активный", default=True)
    created_at = models.DateTimeField("Дата создания", auto_now_add=True)
    updated_at = models.DateTimeField("Дата обновления", auto_now=True)

    class Meta:
        verbose_name = "Баннер"
        verbose_name_plural = "Баннеры"
        ordering = ("sort_order", "-created_at")

    def __str__(self):
        return self.title


class Car(models.Model):
    class EngineType(models.TextChoices):
        TURBO = "turbo", _("Турбина")
        ELECTRIC = "electric", _("Электрический")
        HYBRID = "hybrid", _("Гибрид")
        ATMOSPHERIC = "atmospheric", _("Атмосферный")
        DIESEL = "diesel", _("Дизель")

    class TransmissionType(models.TextChoices):
        AUTOMATIC = "automatic", _("Автомат")
        MANUAL = "manual", _("Механика")
        ROBOT = "robot", _("Робот")
        CVT = "cvt", _("Вариатор")

    class DriveType(models.TextChoices):
        RWD = "rwd", _("Задний (RWD)")
        FWD = "fwd", _("Передний (FWD)")

    title = models.CharField("Название", max_length=180)
    brand = models.ForeignKey(
        Brand,
        on_delete=models.PROTECT,
        related_name="cars",
        verbose_name="Бренд",
    )
    model_name = models.CharField("Название модели", max_length=180)
    engine_type = models.CharField(
        "Тип двигателя",
        max_length=20,
        choices=EngineType.choices,
        blank=True,
        default="",
    )
    engine_types = models.CharField(
        "Типы двигателя (множественный выбор)",
        max_length=120,
        blank=True,
        default="",
    )
    engine_volume = models.DecimalField(
        "Объем двигателя (л)",
        max_digits=4,
        decimal_places=1,
        blank=True,
        null=True,
    )
    drive_type = models.CharField(
        "Привод",
        max_length=10,
        choices=DriveType.choices,
        blank=True,
        default="",
    )
    dimensions_mm = models.CharField(
        "Габариты (мм)",
        max_length=120,
        blank=True,
        help_text="Например: 4890 × 1900 × 1450",
    )
    electric_range_km = models.PositiveIntegerField(
        "Запас хода на электричестве (км)",
        blank=True,
        null=True,
    )
    total_range_km = models.PositiveIntegerField(
        "Общий запас хода (км)",
        blank=True,
        null=True,
    )
    horsepower_hp = models.PositiveIntegerField(
        "Мощность (л.с.)",
        blank=True,
        null=True,
    )
    max_speed_kmh = models.PositiveIntegerField(
        "Максимальная скорость (км/ч)",
        blank=True,
        null=True,
    )
    transmission_type = models.CharField(
        "Коробка передач",
        max_length=20,
        choices=TransmissionType.choices,
        default=TransmissionType.AUTOMATIC,
    )
    photo_1 = models.ImageField("Фото 1", upload_to="cars/", null=True, blank=True)
    photo_2 = models.ImageField("Фото 2", upload_to="cars/", null=True, blank=True)
    photo_3 = models.ImageField("Фото 3", upload_to="cars/", null=True, blank=True)
    photo_4 = models.ImageField("Фото 4", upload_to="cars/", null=True, blank=True)
    photo_5 = models.ImageField("Фото 5", upload_to="cars/", null=True, blank=True)
    navbar_photo = models.ImageField(
        "Фото для навбара",
        upload_to="cars/navbar/",
        null=True,
        blank=True,
    )
    navbar_position = models.PositiveIntegerField("Позиция в навбаре", default=0)
    price = models.DecimalField(
        "Цена",
        max_digits=12,
        decimal_places=2,
        validators=[MinValueValidator(0)],
    )
    discount_price = models.DecimalField(
        "Цена со скидкой",
        max_digits=12,
        decimal_places=2,
        validators=[MinValueValidator(0)],
        null=True,
        blank=True,
    )
    discount_until = models.DateField("Скидка до", null=True, blank=True)
    is_hot = models.BooleanField("Горячий продукт", default=False)
    created_at = models.DateTimeField("Дата создания", auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Автомобиль"
        verbose_name_plural = "Автомобили"
        ordering = ("-created_at",)

    def __str__(self):
        return f"{self.brand.name} {self.model_name}"

    def clean(self):
        super().clean()
        if self.engine_types:
            selected_values = [value for value in self.engine_types.split(",") if value]
            valid_values = {choice[0] for choice in self.EngineType.choices}
            invalid_values = [value for value in selected_values if value not in valid_values]
            if invalid_values:
                raise ValidationError({"engine_types": "Выбраны некорректные типы двигателя."})
            self.engine_types = ",".join(dict.fromkeys(selected_values))
        if self.discount_price and self.discount_price > self.price:
            raise ValidationError("Цена со скидкой не может быть больше основной цены.")

    @property
    def first_photo(self):
        return self.photo_1 or self.photo_2 or self.photo_3 or self.photo_4 or self.photo_5

    @property
    def engine_type_values(self):
        if self.engine_types:
            return [value for value in self.engine_types.split(",") if value]
        if self.engine_type:
            return [self.engine_type]
        return []

    @property
    def engine_type_labels(self):
        labels_map = dict(self.EngineType.choices)
        return [labels_map[value] for value in self.engine_type_values if value in labels_map]

    @property
    def engine_types_display(self):
        return ", ".join(str(label) for label in self.engine_type_labels)


class CarColor(models.Model):
    car = models.ForeignKey(
        Car,
        on_delete=models.CASCADE,
        related_name="colors",
        verbose_name="Автомобиль",
    )
    name = models.CharField("Название цвета", max_length=80, blank=True)
    primary_color = models.CharField("Основной цвет (HEX)", max_length=7)
    secondary_color = models.CharField("Второй цвет (HEX)", max_length=7, blank=True)
    image = models.ImageField("Фото этого цвета", upload_to="cars/colors/")
    sort_order = models.PositiveIntegerField("Порядок", default=0)

    class Meta:
        verbose_name = "Цвет автомобиля"
        verbose_name_plural = "Цвета автомобилей"
        ordering = ("sort_order", "id")

    def __str__(self):
        label = self.name or self.primary_color
        if self.secondary_color:
            return f"{self.car}: {label} / {self.secondary_color}"
        return f"{self.car}: {label}"

    def clean(self):
        super().clean()
        for field_name in ("primary_color", "secondary_color"):
            value = getattr(self, field_name)
            if not value:
                continue
            if len(value) != 7 or not value.startswith("#"):
                raise ValidationError({field_name: "Цвет должен быть в формате HEX, например #FFFFFF"})

    @property
    def swatch_style(self):
        if self.secondary_color:
            return (
                "background: linear-gradient(90deg, "
                f"{self.primary_color} 0 50%, {self.secondary_color} 50% 100%);"
            )
        return f"background-color: {self.primary_color};"


class CarBanner(models.Model):
    car = models.ForeignKey(
        Car,
        on_delete=models.CASCADE,
        related_name="banners",
        verbose_name="Автомобиль",
    )
    image = models.ImageField(
        "Фото баннера",
        upload_to="cars/banners/",
        blank=True,
        null=True,
    )
    video = models.FileField(
        "Видео баннера",
        upload_to="cars/banners/videos/",
        blank=True,
        null=True,
    )
    short_description = models.CharField("Короткое описание", max_length=160, blank=True, default="")
    sort_order = models.PositiveIntegerField("Порядок", default=0)
    is_active = models.BooleanField("Активный", default=True)

    class Meta:
        verbose_name = "Баннер автомобиля"
        verbose_name_plural = "Баннеры автомобиля"
        ordering = ("sort_order", "id")

    def __str__(self):
        if self.short_description:
            return f"{self.car}: {self.short_description[:40]}"
        return f"{self.car}: Баннер без описания"

    def clean(self):
        super().clean()
        if not self.image and not self.video:
            raise ValidationError("Для баннера нужно добавить фото или видео.")
        if not self.car_id:
            return

        banners_count = CarBanner.objects.filter(car_id=self.car_id).exclude(pk=self.pk).count()
        if banners_count >= 5:
            raise ValidationError("Для одного автомобиля можно добавить максимум 5 баннеров.")


class CarFeature(models.Model):
    car = models.ForeignKey(
        Car,
        on_delete=models.CASCADE,
        related_name="features",
        verbose_name="Автомобиль",
    )
    image = models.ImageField(
        "Фото характеристики",
        upload_to="cars/features/",
        blank=True,
        null=True,
    )
    video = models.FileField(
        "Видео характеристики",
        upload_to="cars/features/videos/",
        blank=True,
        null=True,
    )
    title = models.CharField("Название характеристики", max_length=180)
    description = models.TextField("Описание характеристики")
    position = models.PositiveIntegerField("Позиция", default=1)
    is_active = models.BooleanField("Активный", default=True)

    class Meta:
        verbose_name = "Характеристика автомобиля"
        verbose_name_plural = "Характеристики автомобилей"
        ordering = ("position", "id")

    def __str__(self):
        return f"{self.car}: {self.title}"

    def clean(self):
        super().clean()
        if not self.image and not self.video:
            raise ValidationError("Для характеристики нужно добавить фото или видео.")
        if not self.car_id:
            return

        features_count = CarFeature.objects.filter(car_id=self.car_id).exclude(pk=self.pk).count()
        if features_count >= 8:
            raise ValidationError("Для одного автомобиля можно добавить максимум 8 характеристик.")


class ContactRequest(models.Model):
    name = models.CharField("Имя", max_length=120)
    phone = models.CharField("Номер телефона", max_length=40)
    message = models.TextField("Сообщение", blank=True)
    created_at = models.DateTimeField("Дата заявки", auto_now_add=True)

    class Meta:
        verbose_name = "Заявка"
        verbose_name_plural = "Заявки"
        ordering = ("-created_at",)

    def __str__(self):
        return f"{self.name} ({self.phone})"
