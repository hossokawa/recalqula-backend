from django.urls import path
from .views import CalculatePumpPowerView

urlpatterns = [
    path(
        "calculate/", CalculatePumpPowerView.as_view(), name="calcular_potencia"
    )
]
