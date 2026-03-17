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


class EngineType(models.Model):
    name = models.CharField("Тип двигателя", max_length=80, unique=True)

    class Meta:
        verbose_name = "Тип двигателя"
        verbose_name_plural = "Типы двигателей"
        ordering = ("name",)

    def __str__(self):
        return self.name


class TransmissionType(models.Model):
    name = models.CharField("Коробка передач", max_length=80, unique=True)

    class Meta:
        verbose_name = "Коробка передач"
        verbose_name_plural = "Коробки передач"
        ordering = ("name",)

    def __str__(self):
        return self.name


class Car(models.Model):
    title = models.CharField("Название", max_length=180)
    brand = models.ForeignKey(
        Brand,
        on_delete=models.PROTECT,
        related_name="cars",
        verbose_name="Бренд",
    )
    model_name = models.CharField("Название модели", max_length=180)
    engine_type = models.ForeignKey(
        EngineType,
        on_delete=models.PROTECT,
        related_name="cars",
        verbose_name="Тип двигателя",
    )
    engine_volume = models.DecimalField(
        "Объем двигателя (л)",
        max_digits=4,
        decimal_places=1,
        validators=[MinValueValidator(0.1)],
    )
    transmission_type = models.ForeignKey(
        TransmissionType,
        on_delete=models.PROTECT,
        related_name="cars",
        verbose_name="Коробка передач",
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Автомобиль"
        verbose_name_plural = "Автомобили"
        ordering = ("-created_at",)

    def __str__(self):
        return f"{self.brand.name} {self.model_name}"


class CarImage(models.Model):
    car = models.ForeignKey(
        Car,
        on_delete=models.CASCADE,
        related_name="images",
        verbose_name="Автомобиль",
    )
    image = models.ImageField("Фото", upload_to="cars/")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Фото автомобиля"
        verbose_name_plural = "Фото автомобилей"
        ordering = ("created_at",)

    def __str__(self):
        return f"Фото: {self.car}"

    def clean(self):
        super().clean()
        if not self.pk and self.car.images.count() >= 5:
            raise ValidationError("Можно добавить не более 5 фото для одного автомобиля.")

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)
