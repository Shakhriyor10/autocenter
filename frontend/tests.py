from decimal import Decimal

from django.core.exceptions import ValidationError
from django.test import TestCase
from django.urls import reverse

from frontend.models import Brand, Car, CarBanner


class CarBannerTests(TestCase):
    def setUp(self):
        self.brand = Brand.objects.create(name="Toyota")
        self.car = Car.objects.create(
            title="Toyota Camry",
            brand=self.brand,
            model_name="Camry",
            engine_type=Car.EngineType.ATMOSPHERIC,
            engine_volume=Decimal("2.5"),
            transmission_type=Car.TransmissionType.AUTOMATIC,
            price=Decimal("35000"),
        )

    def test_video_banner_requires_video_url(self):
        banner = CarBanner(car=self.car, media_type=CarBanner.MediaType.VIDEO)

        with self.assertRaises(ValidationError):
            banner.full_clean()

    def test_car_detail_page_renders(self):
        response = self.client.get(reverse("car_detail", kwargs={"car_id": self.car.id}))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.car.model_name)
