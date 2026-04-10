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


def car_detail(request, pk):
    car = get_object_or_404(
        Car.objects.select_related("brand").prefetch_related("colors", "banners", "features"),
        pk=pk,
    )
    banners = [banner for banner in car.banners.all() if banner.is_active][:5]
    banner_slides = [
        {"image": banner.image.url, "short_description": banner.short_description}
        for banner in banners
        if banner.image
    ]
    color_images = [color for color in car.colors.all() if color.image]
    features = [feature for feature in car.features.all() if feature.is_active and feature.image][:8]

    main_photo = None
    if color_images:
        # В детальном просмотре главная фотография должна соответствовать
        # первому доступному цвету автомобиля.
        main_photo = color_images[0].image
    elif car.first_photo:
        main_photo = car.first_photo
    elif banners:
        # Баннер используем только как запасной вариант, когда нет обычных фото.
        main_photo = banners[0].image

    return render(
        request,
        "car_detail.html",
        {
            "car": car,
            "banners": banners,
            "banner_slides": banner_slides,
            "color_images": color_images,
            "main_photo": main_photo,
            "features": features,
        },
    )