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
    mensagem = serializers.CharField(max_length=255)
    received_data = serializers.JSONField()

    potencia_estimada = serializers.FloatField()
    altura_manometrica = serializers.FloatField()
    vazao = serializers.FloatField()

    velocidade_succao = serializers.FloatField()
    reynolds_succao = serializers.FloatField()
    fator_atrito_succao = serializers.FloatField()
    tipo_fluxo_succao = serializers.CharField(max_length=50)
    perda_carga_continua_succao = serializers.FloatField()
    perda_carga_localizada_succao = serializers.FloatField()
    perda_carga_total_succao = serializers.FloatField()

    velocidade_recalque = serializers.FloatField()
    reynolds_recalque = serializers.FloatField()
    fator_atrito_recalque = serializers.FloatField()
    tipo_fluxo_recalque = serializers.CharField(max_length=50)
    perda_carga_continua_recalque = serializers.FloatField()
    perda_carga_localizada_recalque = serializers.FloatField()
    perda_carga_total_recalque = serializers.FloatField()

    perda_carga_total = serializers.FloatField()
