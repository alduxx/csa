from django.contrib import admin
from django.urls import path

from cadastro import views
from financeiro import views as fviews


urlpatterns = [
    path('admin/', admin.site.urls),
    path('recibos/upload/', fviews.upload),
    path('', views.extrato)
]
