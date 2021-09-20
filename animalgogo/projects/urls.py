from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from . import views

urlpatterns = [
    path('projects/', views.ProjectList.as_view()), #/projects/
    path('projects/<int:pk>/', views.ProjectDetail.as_view()),  # /projects/<pk>
    path('pledges/', views.PledgeList.as_view()) #/pledges/
]

urlpatterns = format_suffix_patterns(urlpatterns)
