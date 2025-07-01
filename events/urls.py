from django.urls import path
from . import views

urlpatterns = [
    path('', views.EventView.as_view()),
    path('<int:event_id>/register/', views.EventRegister.as_view()),
    path('<int:event_id>/attendees/', views.EventAttendees.as_view()),
]