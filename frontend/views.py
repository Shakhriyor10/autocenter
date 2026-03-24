from django.shortcuts import render
from django.db.models import QuerySet
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