from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views import RegisterAPI, UserAPI, ProductListAPI, CartAPI, ClearCartAPI

urlpatterns = [
    path("register/", RegisterAPI.as_view()),
    path("login/", TokenObtainPairView.as_view()),
    path("token/refresh/", TokenRefreshView.as_view()),
    path("user/", UserAPI.as_view()),

    path("products/", ProductListAPI.as_view()),
    path("cart/", CartAPI.as_view()),
    path("cart/clear/", ClearCartAPI.as_view()),
]