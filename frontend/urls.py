from django.urls import path

from frontend.views import about, car_detail, contact, index

urlpatterns = [
    path('', index, name='index'),
    path('about/', about, name='about'),
    path('cars/<int:pk>/', car_detail, name='car_detail'),
    path('contact/', contact, name='contact'),
]