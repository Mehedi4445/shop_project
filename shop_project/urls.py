from django.contrib import admin
from django.http import JsonResponse
from django.urls import include, path


def home(request):
    return JsonResponse({
        "message": "Shop Product API",
        "products": "/api/products/",
    })


urlpatterns = [
    path("", home),
    path("admin/", admin.site.urls),
    path("api/", include("products.urls")),
]