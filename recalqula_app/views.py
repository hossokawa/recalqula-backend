from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import CalculationInputSerializer, CalculationResultSerializer


class CalculatePumpPowerView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = CalculationInputSerializer(data=request.data)
        if serializer.is_valid():
            # Extract validated data
            data = serializer.validated_data

            # --- Perform your pump power calculation here ---
            # This is a placeholder for your actual calculation logic
            # For demonstration, let's just echo back some data and a dummy power.
            potencia_estimada = (
                data["diametroSuccao"]
                * data["comprimentoRecalque"]
                * data["vazao"]
            ) / 100.0
            message = "Cálculo realizado com sucesso!"

            result = {
                "sucesso": True,
                "potencia_estimada": potencia_estimada,
                "mensagem": message,
                "received_data": data,  # Echo back received data for debugging/verification
            }
            result_serializer = CalculationResultSerializer(data=result)
            result_serializer.is_valid(
                raise_exception=True
            )  # Ensure the result matches the schema
            return Response(result_serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
