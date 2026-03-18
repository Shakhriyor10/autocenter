from django.shortcuts import render

from frontend.models import Banner, Car


def index(request):
    expensive_cars = Car.objects.select_related("brand").order_by("-price")[:8]
    popular_vehicles = (
        Car.objects.select_related("brand").filter(is_hot=True).order_by("-price")[:8]
    )
    banners = Banner.objects.filter(is_active=True).order_by("sort_order", "-created_at")
    return render(
        request,
        "index4.html",
        {
            "banners": banners,
            "expensive_cars": expensive_cars,
            "popular_vehicles": popular_vehicles,
        },
    )
