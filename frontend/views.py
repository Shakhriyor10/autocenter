from django.shortcuts import render

from frontend.models import Car


def index(request):
    cars = Car.objects.select_related(
        "brand", "engine_type", "transmission_type"
    ).prefetch_related("images")
    return render(request, "index4.html", {"cars": cars})
