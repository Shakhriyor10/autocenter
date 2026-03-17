from django.shortcuts import render

from frontend.models import Car


def index(request):
    cars = Car.objects.select_related("brand")
    return render(request, "index4.html", {"cars": cars})
