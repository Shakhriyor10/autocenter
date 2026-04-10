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
        Car.objects.select_related("brand").prefetch_related("colors", "banners"),
        pk=pk,
    )
    banners = [banner for banner in car.banners.all() if banner.is_active][:5]
    color_images = [color for color in car.colors.all() if color.image]

    main_photo = None
    if color_images:
        main_photo = color_images[0].image
    elif car.first_photo:
        main_photo = car.first_photo

    return render(
        request,
        "car_detail.html",
        {
            "car": car,
            "banners": banners,
            "color_images": color_images,
            "main_photo": main_photo,
        },
    )
