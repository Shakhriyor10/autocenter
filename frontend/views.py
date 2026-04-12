from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect, render

from frontend.models import Banner, Car, ContactRequest


def get_navbar_cars():
    return (
        Car.objects.select_related("brand")
        .filter(navbar_photo__isnull=False)
        .exclude(navbar_photo="")
        .order_by("navbar_position", "brand__name", "model_name")
    )


def index(request):
    expensive_cars = (
        Car.objects.select_related("brand")
        .filter(is_hot=True)
        .order_by("-price")
    )

    popular_vehicles = Car.objects.select_related("brand").order_by("-price")

    banner = Banner.objects.filter(is_active=True).order_by("?").first()

    return render(
        request,
        "index4.html",
        {
            "banner": banner,
            "expensive_cars": expensive_cars,
            "popular_vehicles": popular_vehicles,
            "navbar_cars": get_navbar_cars(),
        },
    )


def contact(request):
    if request.method == "POST":
        name = request.POST.get("name", "").strip()
        phone = request.POST.get("phone", "").strip()
        message_text = request.POST.get("message", "").strip()
        if name and phone:
            ContactRequest.objects.create(name=name, phone=phone, message=message_text)
            messages.success(request, "Успешно отправлено, скоро с вами свяжемся.")
        else:
            messages.error(request, "Заполните обязательные поля: имя и номер телефона.")

        return redirect("contact")

    return render(request, "contact.html", {"navbar_cars": get_navbar_cars()})


def car_detail(request, pk):
    car = get_object_or_404(
        Car.objects.select_related("brand").prefetch_related("colors", "banners", "features"),
        pk=pk,
    )
    banners = [
        banner
        for banner in car.banners.all()
        if banner.is_active and (banner.image or banner.video)
    ][:5]
    banner_slides = [
        {
            "image": banner.image.url if banner.image else None,
            "video": banner.video.url if banner.video else None,
            "short_description": banner.short_description,
        }
        for banner in banners
    ]
    color_images = [color for color in car.colors.all() if color.image]
    features = [
        feature
        for feature in car.features.all()
        if feature.is_active and (feature.image or feature.video)
    ][:8]

    main_photo = None
    if color_images:
        # В детальном просмотре главная фотография должна соответствовать
        # первому доступному цвету автомобиля.
        main_photo = color_images[0].image
    elif car.first_photo:
        main_photo = car.first_photo
    elif banners and banners[0].image:
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
            "navbar_cars": get_navbar_cars(),
        },
    )