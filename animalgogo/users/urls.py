from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from . import views


urlpatterns = [
    path('users/', views.CustomUserList.as_view()), #/users/
    path('users/<int:pk>/', views.CustomUserDetail.as_view()), #/users/<id>/
    path('users/me/', views.MeDetail.as_view()), #/users/me/
]

urlpatterns = format_suffix_patterns(urlpatterns)
