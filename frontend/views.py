from django.shortcuts import render

from frontend.models import Car


def index(request):
    expensive_cars = Car.objects.select_related("brand").order_by("-price")[:8]
    popular_vehicles = (
        Car.objects.select_related("brand").filter(is_hot=True).order_by("-price")[:8]
    )
    return render(
        request,
        "index4.html",
        {
            "expensive_cars": expensive_cars,
            "popular_vehicles": popular_vehicles,
        },
    )
