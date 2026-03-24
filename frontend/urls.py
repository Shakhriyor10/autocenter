from django.urls import path

from frontend.views import car_detail, index

urlpatterns = [
    path('', index, name='index'),
    path('cars/<int:car_id>/', car_detail, name='car_detail'),
]
