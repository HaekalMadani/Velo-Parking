from django.urls import path
from . import views

urlpatterns = [
    path('', views.homepage, name='homepage'),
    path('navigate/<latitude>/<longitude>/<place>/', views.navigate_view, name='navigate'),
    path('occupancyjuvisy/<int:station_id>/', views.occupancy_view, name='occupancyjuvisy'),
    path('occupancy_city/', views.occupancy_city, name='occupancy_city'),
    path('feedback/', views.feedback_view, name='Feedback'),
    path('feedback/thanks/', views.feedback_thanks_view, name='thanks'),
    path('user/', views.userProfile, name='user')
]
