from math import log10, pi


def calcular_fator_atrito(reynolds, rugosidade, diametro):
    if reynolds < 2000:
        return 64 / reynolds
    else:
        try:
            # Equação de Swamee-Jain
            return (
                0.25
                / (
                    log10(
                        ((rugosidade / diametro) / 3.7)
                        + (5.74 / (reynolds**0.9))
                    )
                )
                ** 2
            )
        except:
            return 0.02


def calcular_K_total_customizado(acessorios):
    tipos_pecas = {
        "valvula-gaveta-aberta": 0.2,
        "valvula-globo-aberta": 10,
        "valvula-retencao-aberta": 2.5,
        "valvula-borboleta-aberta": 0.3,
        "valvula-angulo-aberta": 5,
        "cotovelo-padrao-90": 0.9,
        "cotovelo-padrao-45": 0.4,
        "curva-padrao-90": 0.4,
        "curva-padrao-45": 0.2,
        "curva-padrao-22": 0.1,
        "te-passagem-direta": 0.6,
        "te-saida-lado": 1.3,
        "te-saida-bilateral": 1.8,
        "juncao": 0.4,
        "crivo": 0.75,
        "bocais": 2.75,
        "ampliacao-gradual": 0.3,
        "reducao-gradual": 0.15,
    }

    # K total começa com 1 por causa da saída da tubulação
    K_total = 1
    for item in acessorios:
        tipo = item["idAcessorio"]
        qtd = item["quantidade"]
        K = tipos_pecas.get(tipo, 0)
        K_total += qtd * K
    return K_total


def mapear_rugosidade_por_id(fluido):
    materiais = {
        "ferro-fundido": 0.26e-3,
        "pvc-plastico": 0.0015e-3,
        "cobre-bronze": 0.0015e-3,
        "concreto-liso": 0.3e-3,
        "aco-comercial": 0.045e-3,
        "ferro-galvanizado": 0.15e-3,
    }
    return materiais.get(fluido, 0.0015e-3)


def mapear_densidade_viscosidade_fluido(
    fluido_id, densidade_custom=None, viscosidade_custom=None
):
    fluidos = {
        "agua_20c": (998, 0.001002),
        "oleo_iso_vg46": (870, 0.041),
        "oleo_sae_30": (875, 0.29),
        "glicerina": (1260, 1.49),
        "oleo_vegetal": (920, 0.065),
    }
    if fluido_id == "outro":
        if densidade_custom is None or viscosidade_custom is None:
            raise ValueError(
                "Para a opção 'Outro', é necessário fornecer densidade e viscosidade personalizada."
            )
        return densidade_custom, viscosidade_custom
    return fluidos.get(fluido_id, (0, 0))


def converter_vazao_para_m3s(vazao, unidade):
    if unidade == "litro-segundo":
        return vazao / 1000  # 1000 L = 1 m³
    elif unidade == "metro-cubico-hora":
        return vazao / 3600  # 3600 s = 1 h
    elif unidade == "metro-cubico-segundo":
        return vazao
    else:
        raise ValueError(f"Unidade de vazão não reconhecida: {unidade}")


def converter_vazao_para_m3h(vazao_m3s):
    return vazao_m3s * 3600


def calcular_potencia_dados(data):
    densidade, viscosidade_dinamica = mapear_densidade_viscosidade_fluido(
        data["fluido"],
        data.get("densidadeFluido"),
        data.get("viscosidadeFluido"),
    )
    viscosidade_cinematica = viscosidade_dinamica / densidade
    unidade_vazao = data.get(
        "unidadeVazao", "metro-cubico-segundo"
    )  # padrão m³/s se não for fornecido
    vazao_m3s = converter_vazao_para_m3s(data["vazao"], unidade_vazao)
    peso_especifico = densidade * 9.81

    diam_suc = data["diametroSuccao"] / 1000
    comp_suc = data["comprimentoSuccao"]
    altura_suc = data["alturaSuccao"]
    rug_suc = mapear_rugosidade_por_id(data["materialSuccao"])
    K_suc = calcular_K_total_customizado(data["acessoriosSuccao"])

    diam_rec = data["diametroRecalque"] / 1000
    comp_rec = data["comprimentoRecalque"]
    altura_rec = data["alturaRecalque"]
    rug_rec = mapear_rugosidade_por_id(data["materialRecalque"])
    K_rec = calcular_K_total_customizado(data["acessoriosRecalque"])

    AREA_suc = pi * ((diam_suc / 2) ** 2)
    vel_suc = round(vazao_m3s / AREA_suc, 2)
    Re_suc = (vel_suc * diam_suc) / viscosidade_cinematica
    f_suc = calcular_fator_atrito(Re_suc, rug_suc, diam_suc)
    hf_suc_cont = f_suc * (comp_suc / diam_suc) * ((vel_suc**2) / (2 * 9.81))
    hf_suc_local = K_suc * ((vel_suc**2) / (2 * 9.81))
    hf_suc = hf_suc_cont + hf_suc_local

    AREA_rec = pi * ((diam_rec / 2) ** 2)
    vel_rec = vazao_m3s / AREA_rec
    Re_rec = (vel_rec * diam_rec) / viscosidade_cinematica
    f_rec = calcular_fator_atrito(Re_rec, rug_rec, diam_rec)
    hf_rec_cont = f_rec * (comp_rec / diam_rec) * ((vel_rec**2) / (2 * 9.81))
    hf_rec_local = K_rec * ((vel_rec**2) / (2 * 9.81))
    hf_rec = hf_rec_cont + hf_rec_local

    H = altura_rec + altura_suc + hf_suc + hf_rec
    pot_util = (peso_especifico * vazao_m3s * H) / 1000

    vazao_m3h = round(converter_vazao_para_m3h(vazao_m3s), 2)

    return {
        "potencia": round(pot_util, 2),
        "altura_manometrica": round(H, 4),
        "vazao": vazao_m3h,
        "velocidade_succao": vel_suc,
        "reynolds_succao": round(Re_suc, 2),
        "fator_atrito_succao": round(f_suc, 6),
        "tipo_fluxo_succao": "Laminar" if Re_suc < 2000 else "Turbulento",
        "hf_continua_succao": round(hf_suc_cont, 2),
        "hf_localizada_succao": round(hf_suc_local, 2),
        "hf_total_succao": round(hf_suc, 2),
        "velocidade_recalque": round(vel_rec, 2),
        "reynolds_recalque": round(Re_rec, 2),
        "fator_atrito_recalque": round(f_rec, 6),
        "tipo_fluxo_recalque": "Laminar" if Re_rec < 2000 else "Turbulento",
        "hf_continua_recalque": round(hf_rec_cont, 2),
        "hf_localizada_recalque": round(hf_rec_local, 2),
        "hf_total_recalque": round(hf_rec, 2),
    }
