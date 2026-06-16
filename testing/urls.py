from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('finish/', views.finish_test, name='finish_test'),
    path('statistics/', views.statistics, name='statistics'),
    path('agent/', views.demo_agent, name='agent'),
]
