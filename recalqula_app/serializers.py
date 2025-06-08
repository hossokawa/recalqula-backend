from rest_framework import serializers


class AcessorioSerializer(serializers.Serializer):
    idAcessorio = serializers.CharField(max_length=255)
    quantidade = serializers.IntegerField(min_value=1)


class CalculationInputSerializer(serializers.Serializer):
    diametroSuccao = serializers.FloatField()
    comprimentoSuccao = serializers.FloatField()
    materialSuccao = serializers.CharField(max_length=255)
    alturaSuccao = serializers.FloatField()
    acessoriosSuccao = serializers.ListField(child=AcessorioSerializer())

    diametroRecalque = serializers.FloatField()
    comprimentoRecalque = serializers.FloatField()
    materialRecalque = serializers.CharField(max_length=255)
    alturaRecalque = serializers.FloatField()
    acessoriosRecalque = serializers.ListField(child=AcessorioSerializer())

    fluido = serializers.CharField(max_length=255)
    viscosidadeFluido = serializers.FloatField()
    densidadeFluido = serializers.FloatField()
    vazao = serializers.FloatField()
    unidadeVazao = serializers.CharField(max_length=255)


class CalculationResultSerializer(serializers.Serializer):
    sucesso = serializers.BooleanField()
    potencia_estimada = serializers.FloatField()
    mensagem = serializers.CharField(max_length=255)
    received_data = serializers.JSONField()  # To show the received data
