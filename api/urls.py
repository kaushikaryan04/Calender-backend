from django.urls import path 
from .views import * 

urlpatterns = [
    path('event/' , EventListCreateView.as_view(), name = 'event-list-create'),
    path("events/<int:event_id>/", EventDetailView.as_view(), name="event-detail"),

]