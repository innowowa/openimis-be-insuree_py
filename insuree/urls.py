from django.urls import path
from .views import get_new_chfid

urlpatterns = [
    path('generate-chfid/', get_new_chfid, name='generate_chfid'),
]
