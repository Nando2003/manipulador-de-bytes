from django.urls import path
from manipulador_arquivos.views import HomeView

urlpatterns = [
    path('', HomeView.as_view(), name='home-page')
]