from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator
from django.db import models


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
        TURBO = "turbo", "Турбина"
        ELECTRIC = "electric", "Электрический"
        HYBRID = "hybrid", "Гибрид"
        ATMOSPHERIC = "atmospheric", "Атмосферный"
        DIESEL = "diesel", "Дизель"

    class TransmissionType(models.TextChoices):
        AUTOMATIC = "automatic", "Автомат"
        MANUAL = "manual", "Механика"
        ROBOT = "robot", "Робот"
        CVT = "cvt", "Вариатор"

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
        default=EngineType.ATMOSPHERIC,
    )
    engine_volume = models.DecimalField(
        "Объем двигателя (л)",
        max_digits=4,
        decimal_places=1,
        validators=[MinValueValidator(0.1)],
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
        if self.discount_price and self.discount_price > self.price:
            raise ValidationError("Цена со скидкой не может быть больше основной цены.")

    @property
    def first_photo(self):
        return self.photo_1 or self.photo_2 or self.photo_3 or self.photo_4 or self.photo_5


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
    image = models.ImageField("Фото баннера", upload_to="cars/banners/")
    short_description = models.CharField("Короткое описание", max_length=160)
    sort_order = models.PositiveIntegerField("Порядок", default=0)
    is_active = models.BooleanField("Активный", default=True)

    class Meta:
        verbose_name = "Баннер автомобиля"
        verbose_name_plural = "Баннеры автомобиля"
        ordering = ("sort_order", "id")

    def __str__(self):
        return f"{self.car}: {self.short_description[:40]}"

    def clean(self):
        super().clean()
        if not self.car_id:
            return

        banners_count = CarBanner.objects.filter(car_id=self.car_id).exclude(pk=self.pk).count()
        if banners_count >= 5:
            raise ValidationError("Для одного автомобиля можно добавить максимум 5 баннеров.")