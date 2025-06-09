from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import CalculationInputSerializer, CalculationResultSerializer
from .functions import calcular_potencia_dados


class CalculatePumpPowerView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = CalculationInputSerializer(data=request.data)
        if serializer.is_valid():
            data = serializer.validated_data

            print(data)
            resultados = calcular_potencia_dados(data)
            msg = "Cálculo realizado com sucesso!"

            resultado = {
                "sucesso": True,
                "mensagem": msg,
                "received_data": data,
                "potencia_estimada": resultados["potencia"],
                "altura_manometrica": resultados["altura_manometrica"],
                "vazao": resultados["vazao"],
                "velocidade_succao": resultados["velocidade_succao"],
                "reynolds_succao": resultados["reynolds_succao"],
                "tipo_fluxo_succao": resultados["tipo_fluxo_succao"],
                "fator_atrito_succao": resultados["fator_atrito_succao"],
                "perda_carga_continua_succao": resultados["hf_continua_succao"],
                "perda_carga_localizada_succao": resultados[
                    "hf_localizada_succao"
                ],
                "perda_carga_total_succao": resultados["hf_total_succao"],
                "velocidade_recalque": resultados["velocidade_recalque"],
                "reynolds_recalque": resultados["reynolds_recalque"],
                "tipo_fluxo_recalque": resultados["tipo_fluxo_recalque"],
                "fator_atrito_recalque": resultados["fator_atrito_recalque"],
                "perda_carga_continua_recalque": resultados[
                    "hf_continua_recalque"
                ],
                "perda_carga_localizada_recalque": resultados[
                    "hf_localizada_recalque"
                ],
                "perda_carga_total_recalque": resultados["hf_total_recalque"],
                "perda_carga_total": resultados["hf_total_succao"]
                + resultados["hf_total_recalque"],
            }
            result_serializer = CalculationResultSerializer(data=resultado)
            result_serializer.is_valid(raise_exception=True)
            return Response(result_serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
