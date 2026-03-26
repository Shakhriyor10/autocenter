from django.shortcuts import get_object_or_404, render

from frontend.models import Banner, Car


def index(request):
    expensive_cars = Car.objects.select_related("brand").order_by("-price")[:8]

    popular_vehicles = (
        Car.objects.select_related("brand")
        .filter(is_hot=True)
        .order_by("-price")[:8]
    )

    banner = Banner.objects.filter(is_active=True).order_by("?").first()

    return render(
        request,
        "index4.html",
        {
            "banner": banner,
            "expensive_cars": expensive_cars,
            "popular_vehicles": popular_vehicles,
        },
    )


def car_detail(request, car_id):
    car = get_object_or_404(Car.objects.select_related("brand"), pk=car_id)
    car_banners = car.banners.filter(is_active=True)

    gallery_photos = [
        photo for photo in [car.photo_1, car.photo_2, car.photo_3, car.photo_4, car.photo_5] if photo
    ]

    return render(
        request,
        "car_detail.html",
        {
            "car": car,
            "car_banners": car_banners,
            "gallery_photos": gallery_photos,
        },
    )