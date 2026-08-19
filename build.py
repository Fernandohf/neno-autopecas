# -*- coding: utf-8 -*-
"""Gera as 6 páginas da landing da Neno Autopeças a partir de um único template."""
import os, json, html
from urllib.parse import quote

SAIDA = os.path.dirname(os.path.abspath(__file__))

# ---------------------------------------------------------------- dados fixos
DOMINIO = "https://fernandohf.github.io/neno-autopecas"   # provisório: GitHub Pages. Trocar pelo domínio próprio quando definido.
ZAP_NUM = "5584999675667"
ZAP_VIS = "(84) 99967-5667"
FIXO_TEL = "+558433512392"
FIXO_VIS = "(84) 3351-2392"
ENDERECO = "Av. Senador Dinarte Mariz, 632 — São Benedito"
CIDADE_UF = "Pau dos Ferros - RN, 59900-000"
INSTAGRAM = "https://www.instagram.com/nenopecaspdf/"
FACEBOOK = "https://www.facebook.com/nenoautopecaspdf"

# coordenadas exatas do pino do Perfil da Empresa no Google
LAT, LNG = -6.1180038, -38.2055928

# link curto do Perfil da Empresa (mesmo do Google Maps)
PERFIL_GOOGLE = "https://maps.app.goo.gl/zBPvgLzxWstUExD79"

ROTA = ("https://www.google.com/maps/dir/?api=1&destination="
        "Neno+Autope%C3%A7as%2C+Av.+Senador+Dinarte+Mariz%2C+632%2C+"
        "Pau+dos+Ferros+-+RN%2C+59900-000")
MAPA_EMBED = ("https://www.google.com/maps?q=Av.+Senador+Dinarte+Mariz%2C+632%2C"
              "+Pau+dos+Ferros+-+RN&amp;hl=pt-BR&amp;z=17&amp;output=embed")

# ------------------------------------------------------- nota do Google (real)
# Conferida no Perfil da Empresa. Atualize os dois números quando mudarem —
# eles alimentam o selo do topo, o rótulo do hero e o JSON-LD (aggregateRating).
NOTA = "4,9"
NOTA_NUM = "4.9"
QTD_AVALIACOES = 34

# Avaliações reais copiadas do Perfil da Empresa no Google, em HTML estático.
# Nenhum widget externo: cada script de fora custa perto de meio segundo no 4G.
AVALIACOES = [
    dict(nome="Marina Paiva Pinto", nota=5, quando="ago. 2026",
         texto="Atendimento muito bom, recomendo."),
    dict(nome="Renata Fernandes", nota=5, quando="ago. 2026",
         texto="Excelente. Ótimo trabalho e atendimento."),
    dict(nome="Hugo Adelino", nota=5, quando="abr. 2021",
         texto="Ótimo atendimento, loja clássica e muito boa!"),
    dict(nome="Mônica Maria", nota=5, quando="mar. 2019",
         texto="Ótimo atendimento e qualidade nos serviços."),
]

# ------------------------------------------------------------------- galeria
# Fotos reais da loja (as mesmas do Perfil da Empresa no Google).
GALERIA = [
    dict(src="fachada-noite.webp", w=880, h=586, classe="larga",
         alt="Fachada da Neno Autopeças com o letreiro aceso à noite, em Pau dos Ferros",
         legenda="A fachada na Av. Senador Dinarte Mariz, 632."),
    dict(src="balcao.webp", w=880, h=586, classe="",
         alt="Balcão de atendimento da Neno Autopeças com prateleiras de peças ao fundo",
         legenda="O balcão: você aponta, a gente pega na prateleira."),
    dict(src="estoque.webp", w=880, h=586, classe="",
         alt="Corredor de prateleiras cheias de caixas de peças na Neno Autopeças",
         legenda="Corredor de estoque — é daqui que sai a peça de hoje."),
    dict(src="atendimento.webp", w=880, h=586, classe="",
         alt="Atendente da Neno Autopeças no balcão, ao lado das caixas etiquetadas por modelo",
         legenda="Caixa etiquetada por modelo: acha rápido, entrega rápido."),
    dict(src="produtos.webp", w=880, h=495, classe="",
         alt="Fluido de freio Bosch DOT 3 e outros produtos no expositor da loja",
         legenda="Marca na mão antes de você decidir."),
]

CIDADES = ["São Francisco do Oeste", "Marcelino Vieira", "Rafael Fernandes", "Encanto",
           "Portalegre", "José da Penha", "Doutor Severiano", "Água Nova", "Luís Gomes",
           "São Miguel", "Alexandria", "Martins", "Pilões", "Serrinha dos Pintos",
           "Tenente Ananias", "Major Sales"]

MODELOS = ["Palio", "Gol", "Uno", "Weekend", "Siena", "Celta", "Corsa", "Fiorino", "Elba",
           "Onix", "Strada", "Doblô", "Argo", "Fox", "Crossfox", "Prisma", "Cobalt", "Hilux"]

MONTADORAS = ["Fiat", "GM / Chevrolet", "Volkswagen", "Ford", "Mercedes-Benz"]

PESADA = ["Mercedes-Benz 1113", "GM A10", "GM C10", "GM D10", "GM D20", "GM C20",
          "GM C40", "Ford F1000", "Ford Cargo", "Trator"]

# ------------------------------------------------------------------ famílias
FAMILIAS = [
    dict(key="embreagem", anchor="embreagem", nome="Embreagem",
         itens=["Kit de embreagem", "Cilindro mestre de embreagem", "Cilindro auxiliar de embreagem"],
         zap="Preciso de peça de embreagem"),
    dict(key="suspensao", anchor="suspensao", nome="Suspensão e direção",
         itens=["Amortecedor", "Suporte de amortecedor", "Pivô de suspensão", "Bandeja",
                "Terminal de direção", "Bieleta", "Rolamento de roda", "Cubo de roda",
                "Junta homocinética", "Base e coxim do motor"],
         zap="Preciso de peça de suspensão"),
    dict(key="freio", anchor="freio", nome="Freio",
         itens=["Pastilha de freio", "Tambor de freio", "Disco de freio",
                "Cilindro mestre de freio", "Sapata", "Lona"],
         zap="Preciso de peça de freio"),
    dict(key="arrefecimento", anchor="arrefecimento", nome="Arrefecimento",
         itens=["Radiador", "Eletroventilador", "Bomba d'água", "Válvula termostática",
                "Mangote de radiador"],
         zap="Preciso de peça de arrefecimento"),
    dict(key="linha-pesada", anchor="linha-pesada", nome="Linha pesada e antiga",
         itens=["Mercedes-Benz 1113", "GM A10, C10, D10, D20, C20 e C40",
                "Ford F1000 e Ford Cargo", "Peça de trator",
                "Freio, suspensão, embreagem e arrefecimento dessas linhas"],
         zap="Preciso de peça de linha pesada"),
]

# ------------------------------------------------------------------ variantes
VARIANTES = [
    dict(
        slug="index", destaque=None,
        titulo="Autopeças em Pau dos Ferros | Peça no balcão hoje — Neno Autopeças",
        desc=("Autopeças em Pau dos Ferros com estoque no balcão: freio, suspensão, embreagem, "
              "radiador e linha pesada. Chame no WhatsApp " + ZAP_VIS + " e leve a peça hoje."),
        h1="Autopeças em Pau dos Ferros",
        lead=("Você chega, diz o carro e o ano, e sai com a peça na mão. Loja física na "
              "Av. Senador Dinarte Mariz, com prateleira cheia pra quem não pode parar o carro "
              "esperando 7 a 15 dias de frete."),
        zap="Preciso de uma peça",
    ),
    dict(
        slug="embreagem", destaque="embreagem",
        titulo="Kit de embreagem em Pau dos Ferros | Tem no balcão — Neno Autopeças",
        desc=("Kit de embreagem, cilindro mestre e cilindro auxiliar em Pau dos Ferros. "
              "Conferimos a aplicação pelo modelo e ano. WhatsApp " + ZAP_VIS + ", leve hoje."),
        h1="Kit de embreagem em Pau dos Ferros",
        lead=("Embreagem patinando, pedal duro, barulho quando pisa? Manda o modelo e o ano no "
              "WhatsApp que a gente confere a aplicação do kit e responde na hora se tem aqui. "
              "Tendo, é hoje — sem esperar encomenda."),
        zap="Preciso de kit de embreagem",
    ),
    dict(
        slug="suspensao", destaque="suspensao",
        titulo="Amortecedor e suspensão em Pau dos Ferros | Neno Autopeças",
        desc=("Amortecedor, pivô, bandeja, terminal, bieleta e rolamento de roda em Pau dos "
              "Ferros. Estoque no balcão. Chame no WhatsApp " + ZAP_VIS + "."),
        h1="Amortecedor e suspensão em Pau dos Ferros",
        lead=("Batendo em lombada, carro jogando na curva, zoada de rolamento? Diz o carro e o "
              "ano que a gente vê amortecedor, pivô, bandeja, terminal e o resto da lista. "
              "O que estiver na prateleira você leva hoje."),
        zap="Preciso de amortecedor / peça de suspensão",
    ),
    dict(
        slug="freio", destaque="freio",
        titulo="Pastilha, tambor e disco de freio em Pau dos Ferros | Neno Autopeças",
        desc=("Pastilha, tambor, disco, sapata, lona e cilindro mestre de freio em Pau dos "
              "Ferros. Peça no balcão hoje. WhatsApp " + ZAP_VIS + "."),
        h1="Pastilha, tambor e disco de freio em Pau dos Ferros",
        lead=("Freio chiando, pedal baixo, disco riscado? Fala o modelo e o ano que a gente "
              "confere pastilha, tambor, disco e sapata na hora. Freio não é peça pra esperar "
              "15 dias de frete — tem aqui, você leva hoje."),
        zap="Preciso de peça de freio (pastilha, tambor ou disco)",
    ),
    dict(
        slug="arrefecimento", destaque="arrefecimento",
        titulo="Radiador, eletroventilador e bomba d'água em Pau dos Ferros — Neno Autopeças",
        desc=("Radiador, eletroventilador, bomba d'água, válvula termostática e mangote em "
              "Pau dos Ferros. Tem no balcão hoje. WhatsApp " + ZAP_VIS + "."),
        h1="Radiador, eletroventilador e bomba d'água em Pau dos Ferros",
        lead=("Carro fervendo, marca d'água no chão, ventoinha que não liga? Radiador, "
              "eletroventilador, bomba d'água, válvula e mangote a gente confere pelo modelo e "
              "ano e responde na hora se tem no balcão."),
        zap="Preciso de peça de arrefecimento (radiador, ventoinha ou bomba d'água)",
    ),
    dict(
        slug="linha-pesada", destaque="linha-pesada",
        titulo="Peças MB 1113, D20, C10, F1000 e trator em Pau dos Ferros — Neno Autopeças",
        desc=("Peças para Mercedes 1113, D20, C10, C20, F1000, Ford Cargo e trator em Pau dos "
              "Ferros. Linha pesada e antiga no balcão. WhatsApp " + ZAP_VIS + "."),
        h1="Peças MB 1113, D20, C10, F1000 e trator em Pau dos Ferros",
        lead=("1113, D20, C10, F1000, Cargo e trator: é aqui que ainda tem. Essa linha quase "
              "ninguém segura em estoque e na internet o prazo passa de 15 dias. Manda o que "
              "você precisa no WhatsApp que a gente procura na prateleira e te manda a foto."),
        zap="Preciso de peça de linha pesada/antiga",
    ),
]

# ------------------------------------------------------------------ ícones SVG
def _ic(d, vb="0 0 24 24", extra=""):
    return '<svg viewBox="%s" aria-hidden="true"><path%s d="%s"/></svg>' % (vb, extra, d)

IC_ZAP = _ic('M12.04 2C6.58 2 2.13 6.45 2.13 11.91c0 1.75.46 3.45 1.32 4.95L2 22l5.25-1.38a9.9 '
             '9.9 0 0 0 4.79 1.22h.01c5.46 0 9.91-4.45 9.91-9.91 0-2.65-1.03-5.14-2.9-7.01A9.82 '
             '9.82 0 0 0 12.04 2Zm5.8 14.13c-.25.69-1.44 1.32-1.98 1.37-.53.05-1.02.24-3.44-.72'
             '-2.9-1.14-4.74-4.1-4.88-4.29-.14-.19-1.16-1.54-1.16-2.94 0-1.4.73-2.09.99-2.37.26'
             '-.29.57-.36.76-.36.19 0 .38 0 .55.01.18.01.41-.07.64.49.24.58.81 2 .88 2.14.07.14'
             '.12.31.02.5-.09.19-.14.31-.28.48-.14.17-.29.37-.42.5-.14.14-.28.29-.12.57.16.29.72 '
             '1.19 1.55 1.93 1.07.95 1.97 1.25 2.25 1.39.28.14.44.12.6-.07.17-.19.69-.81.88-1.09'
             '.19-.29.37-.24.62-.14.25.09 1.61.76 1.89.9.28.14.46.21.53.33.07.12.07.69-.18 1.37Z')

IC_TEL = _ic('M6.62 10.79a15.05 15.05 0 0 0 6.59 6.59l2.2-2.2a1 1 0 0 1 1.03-.24c1.12.37 2.33.57 '
             '3.56.57a1 1 0 0 1 1 1V20a1 1 0 0 1-1 1C10.4 21 3 13.6 3 4a1 1 0 0 1 1-1h3.5a1 1 0 0 '
             '1 1 1c0 1.24.2 2.44.57 3.57a1 1 0 0 1-.25 1.02l-2.2 2.2Z')

IC_MAP = _ic('M12 2a7 7 0 0 0-7 7c0 5.25 7 13 7 13s7-7.75 7-13a7 7 0 0 0-7-7Zm0 9.5A2.5 2.5 0 1 1 '
             '12 6.5a2.5 2.5 0 0 1 0 5Z')

IC_RELOGIO = _ic('M12 2a10 10 0 1 0 0 20 10 10 0 0 0 0-20Zm1 10.6V6h-2v7.6l5.2 3.1 1-1.7-4.2-2.4Z',
                 extra=' fill-rule="evenodd"')

IC_ESCUDO = _ic('M12 2 4 5v6.2c0 5 3.4 9.4 8 10.8 4.6-1.4 8-5.8 8-10.8V5l-8-3Zm-1 14.2-4-4 '
                '1.4-1.4 2.6 2.6 5-5L17.4 10 11 16.2Z')

IC_CAIXA = _ic('M12 2 2 6.6v10.8L12 22l10-4.6V6.6L12 2Zm0 2.3 6.6 3-6.6 3-6.6-3 6.6-3ZM4 8.6l7 '
               '3.2v7.4l-7-3.2V8.6Zm9 10.6v-7.4l7-3.2v7.4l-7 3.2Z')

IC_CARTAO = _ic('M3 5h18a2 2 0 0 1 2 2v1H1V7a2 2 0 0 1 2-2Zm-2 5h22v7a2 2 0 0 1-2 2H3a2 2 0 0 '
                '1-2-2v-7Zm3 4v2h6v-2H4Z')

IC_ESTRELA = _ic('m12 17.3-6.2 3.7 1.7-7L2 9.2l7.2-.6L12 2l2.8 6.6 7.2.6-5.5 4.8 1.7 7L12 17.3Z')

IC_INSTA = _ic('M12 2.2c3.2 0 3.6 0 4.9.07 1.2.05 1.8.25 2.2.42.6.22 1 .48 1.4.9.4.4.7.8.9 '
               '1.4.2.4.4 1 .4 2.2.1 1.3.1 1.7.1 4.9s0 3.6-.1 4.9c0 1.2-.2 1.8-.4 2.2-.2.6-.5 '
               '1-.9 1.4-.4.4-.8.7-1.4.9-.4.2-1 .4-2.2.4-1.3.1-1.7.1-4.9.1s-3.6 0-4.9-.1c-1.2 '
               '0-1.8-.2-2.2-.4-.6-.2-1-.5-1.4-.9-.4-.4-.7-.8-.9-1.4-.2-.4-.4-1-.4-2.2C2.2 15.6 '
               '2.2 15.2 2.2 12s0-3.6.1-4.9c0-1.2.2-1.8.4-2.2.2-.6.5-1 .9-1.4.4-.4.8-.7 1.4-.9.4'
               '-.2 1-.4 2.2-.4C8.4 2.2 8.8 2.2 12 2.2Zm0 1.8c-3.1 0-3.5 0-4.8.07-1.1.05-1.7.24'
               '-2.1.4-.5.2-.9.44-1.3.83-.4.4-.63.8-.83 1.3-.16.4-.35 1-.4 2.1C2.53 8.5 2.5 8.9 '
               '2.5 12s0 3.5.07 4.8c.05 1.1.24 1.7.4 2.1.2.5.44.9.83 1.3.4.4.8.63 1.3.83.4.16 1 '
               '.35 2.1.4 1.3.07 1.7.07 4.8.07s3.5 0 4.8-.07c1.1-.05 1.7-.24 2.1-.4.5-.2.9-.44 '
               '1.3-.83.4-.4.63-.8.83-1.3.16-.4.35-1 .4-2.1.07-1.3.07-1.7.07-4.8s0-3.5-.07-4.8c'
               '-.05-1.1-.24-1.7-.4-2.1a3.5 3.5 0 0 0-.83-1.3 3.5 3.5 0 0 0-1.3-.83c-.4-.16-1'
               '-.35-2.1-.4C15.5 4 15.1 4 12 4Zm0 3a5 5 0 1 1 0 10 5 5 0 0 1 0-10Zm0 1.8a3.2 3.2 '
               '0 1 0 0 6.4 3.2 3.2 0 0 0 0-6.4Zm5.2-3.1a1.17 1.17 0 1 1 0 2.34 1.17 1.17 0 0 1 '
               '0-2.34Z')

IC_FACE = _ic('M22 12a10 10 0 1 0-11.56 9.88v-6.99H7.9V12h2.54V9.8c0-2.5 1.5-3.89 3.77-3.89 1.09 '
              '0 2.24.2 2.24.2v2.46h-1.26c-1.24 0-1.63.77-1.63 1.56V12h2.78l-.45 2.89h-2.33v6.99A10 '
              '10 0 0 0 22 12Z')

# ícone da marca: o vetor oficial do logo (carro, motor com raio, disco de
# freio e porca laranja), extraído do SVG horizontal da agência e reescalado
# para o viewBox 160×81,5. Vai inline no HTML — nenhuma requisição extra.
CARRO_TRACO = (
    "M129.6 81.5c-.3 0-.6-.1-.9-.1-1.2-.1-2.4-.3-3.5-.7-.9-.3-1.8-.6-2.6-1.1-1.4-.6-2.6-1.5"
    "-3.8-2.4-1.2-1.2-2.3-2.4-3.3-3.9-1-1.5-1.7-3.2-2.2-4.9-.2-1-.5-2.1-.5-3.2-.1-.9-.1-1.9"
    " 0-2.8 0-1.4.3-2.7.7-4 .3-.9.6-1.8 1.1-2.7.6-1.3 1.5-2.6 2.5-3.7 1.5-1.7 3.2-3.1 5.2-4"
    ".2 1.7-.8 3.5-1.4 5.4-1.7 1.2-.2 2.4-.3 3.7-.2 2.3 0 4.5.6 6.6 1.5 1.6.8 3 1.7 4.3 2.9"
    " 1.7 1.5 3.1 3.2 4.1 5.2.5 1 1 2.1 1.3 3.2 0 .1 0 .1 0 .2.1 0 .2 0 .3 0 .8 0 1.5 0 2.3"
    " 0 1.1 0 2.2.1 3.4.1.1 0 .2 0 .3 0 .1-.1.2-.3.2-.4.3-.8.5-1.6.5-2.5.1-.5.1-1 .2-1.6 0-"
    ".5 0-.9 0-1.4 0-1.2-.1-2.3-.3-3.4-.4-1.8-1-3.6-1.8-5.3-.6-1.2-1.3-2.3-2-3.4-.4-.6-.8-1"
    ".2-1.1-1.8-.2-.5-.3-1-.5-1.6-.1-.7-.3-1.3-.3-2 0-.7 0-1.4 0-2 0 0 0 0 0-.1 0-1.2.1-2.5"
    " 0-3.8 0-.7 0-1.4-.1-2-.1-.4-.2-.8-.4-1.2-.4-1.3-1-2.5-1.7-3.7-.8-1.5-1.7-2.9-2.7-4.3-"
    ".9-1.4-1.9-2.6-2.9-3.9-.8-1.1-1.6-2.1-2.2-3.4-.1-.1-.1-.3-.2-.5-.2-.4-.3-.7-.4-1-.1-.1"
    "-.2-.2-.3-.3-.7-.3-1.4-.5-2.2-.7-1.2-.2-2.5-.5-3.8-.6-1.7-.3-3.5-.5-5.2-.8-1.2-.1-2.5-"
    ".3-3.7-.4-1.6-.2-3.2-.4-4.9-.6-.9-.1-1.8-.2-2.7-.3-1-.1-2.1-.1-3.1-.2-.8-.1-1.7-.2-2.5"
    "-.2-.8-.1-1.5-.1-2.3-.1-1-.1-2-.1-3.1-.2-.4 0-.8 0-1.2 0-1.4 0-2.8 0-4.2 0-.9 0-1.8.1-"
    "2.6.1-.7 0-1.4 0-2.1.1-.8 0-1.6.1-2.5.1-.7.1-1.5.2-2.3.3-.7 0-1.3.1-1.9.2-1.3.2-2.7.4-"
    "3.9.6-1.9.3-3.8.6-5.6 1-1.9.5-3.8.9-5.7 1.5-2.3.6-4.5 1.3-6.7 2.1-1.9.7-3.8 1.4-5.6 2."
    "3-2 .8-4 1.7-6 2.6-1.5.7-3.1 1.5-4.6 2.2-1.7.8-3.3 1.6-5 2.4-1.3.6-2.7 1.3-4.1 2-1.6.8"
    "-3.3 1.5-5 2.2-1 .5-2.1.9-3.2 1.2-1.6.4-3.2.8-4.7 1.3-2.4.6-4.7 1.4-7 2.3-1.7.6-3.4 1."
    "3-5 2.3-.9.4-1.7 1-2.5 1.6-.8.7-1.5 1.5-2.2 2.4-.9 1-1.6 2.2-2.2 3.5-.2.5-.4 1.2-.6 1."
    "8-.5 1-.9 1.9-1.4 2.9-.2.5-.4 1-.6 1.5-.1.3-.1.6-.2.9 0 .5-.1 1-.1 1.4-.1.9-.1 1.7-.2 "
    "2.5 0 .8-.1 1.5-.1 2.3 0 .6 0 1.2 0 1.8 0 1.3.3 2.5.8 3.6.2.4.4.8.6 1.2.1.3.4.5.7.7.6."
    "3 1.1.5 1.7.7.2 0 .4.1.7.1 1 0 1.9 0 2.9 0 .1 0 .1 0 .2 0 .7 0 1.5 0 2.3 0 .2 0 .4-.1."
    "7-.1.1-.4.2-.8.3-1.2.3-1.4.7-2.7 1.4-4 .7-1.4 1.5-2.6 2.5-3.7 1.4-1.7 3-3 4.9-4 .7-.4 "
    "1.4-.7 2.2-1 1.7-.6 3.4.5 3.6 2.2.1 1.3-.7 2.4-1.8 2.8-1.5.6-2.9 1.5-4.1 2.6-1.1 1.1-2"
    " 2.3-2.6 3.6-.6 1.2-1 2.4-1.1 3.7-.1.5-.1 1-.1 1.5-.1 2.1.4 4.2 1.4 6.1.5 1 1.2 2 2 2."
    "8 1 1.1 2.2 2 3.6 2.6 1.3.7 2.7 1.1 4.2 1.2 2.3.2 4.5-.1 6.5-1.1 1.3-.5 2.4-1.3 3.4-2."
    "2 1.1-1.1 2-2.4 2.7-3.8.1-.2.2-.5.3-.8.4-.9 1.1-1.5 2.1-1.7 1.5-.3 2.7.7 3 2 0 .1.1.3."
    "1.5 0 .4-.1.8-.2 1.1-.7 1.9-1.7 3.5-2.9 5-1.6 1.8-3.4 3.3-5.5 4.4-1.7.9-3.5 1.5-5.4 1."
    "8-.5.1-.9.1-1.4.2-.2 0-.4 0-.5 0-.6 0-1.3 0-1.9 0-.2 0-.3 0-.5 0-.5-.1-1-.1-1.4-.2-2.1"
    "-.3-4-1-5.8-2-1.9-1.1-3.6-2.5-5-4.2-1.1-1.2-1.9-2.5-2.6-3.9-.5-1.1-.9-2.2-1.1-3.4-.1-."
    "4-.2-.9-.3-1.4-.1 0-.1 0-.2 0-.4 0-.8 0-1.1 0-.5 0-.9 0-1.4 0-.9 0-1.9 0-2.9 0-.2 0-.5"
    " 0-.7-.1-1 0-2-.3-2.9-.5-1.8-.6-3.2-1.6-4.3-3.1-.5-.6-.9-1.3-1.2-2.1-.3-.7-.5-1.4-.7-2"
    ".2-.2-.9-.4-1.7-.5-2.7-.1-.2-.1-.5-.2-.7 0-.6 0-1.2 0-1.9.1-.1.1-.2.1-.3 0-.2.1-.4.1-."
    "6.1-1 .2-1.9.2-2.8.1-.8.2-1.6.2-2.4.1-1 .2-1.9.4-2.9.2-.7.4-1.4.8-2 .7-1.3 1.2-2.6 1.7"
    "-3.9.3-.7.6-1.4.9-2 .4-1 1-1.8 1.6-2.6.8-1.3 1.8-2.4 2.9-3.4.9-.8 1.8-1.4 2.7-2 1.5-1."
    "1 3.1-1.9 4.8-2.6 1.9-.8 3.8-1.4 5.7-2 1.9-.6 3.9-1.2 5.8-1.7 1.8-.5 3.5-1 5.2-1.7 2.2"
    "-.9 4.3-2 6.5-3 1.2-.6 2.4-1.2 3.7-1.8 2.2-1 4.5-2.1 6.7-3.2 1.7-.7 3.3-1.5 5-2.2 1.7-"
    ".8 3.4-1.5 5.1-2.2 1.6-.6 3.1-1.2 4.7-1.8 1.8-.7 3.6-1.2 5.5-1.7 1.2-.3 2.3-.6 3.5-.9 "
    "1-.3 2-.5 3.1-.7 1.2-.3 2.4-.6 3.6-.8 1.2-.2 2.4-.4 3.5-.6.9-.1 1.8-.3 2.7-.4 1.3-.2 2"
    ".5-.3 3.8-.5 1.2-.1 2.3-.2 3.5-.3.7 0 1.3 0 2 0 .3 0 .6 0 .8 0 .1 0 .2-.1.2-.1 2.7 0 5"
    ".3 0 8 0 .4 0 .8 0 1.2 0 1 .1 2.1.1 3.1.2 1 0 2 .1 3 .1 1.3.2 2.5.3 3.8.4.9.1 1.8.3 2."
    "7.4 1.2.1 2.4.2 3.6.4.8.1 1.7.2 2.6.3 1.1.1 2.2.3 3.3.4.8.1 1.6.2 2.4.3 1.5.2 3 .4 4.5"
    ".7 1 .2 2 .4 3 .7 1.1.2 2.2.6 3.1 1.3.9.6 1.5 1.5 2 2.4.2.4.2.7.4 1.1.5.9 1 1.8 1.7 2."
    "6 1.2 1.5 2.4 3.1 3.5 4.8 1 1.5 2 3 2.8 4.6.9 1.7 1.7 3.4 2.1 5.2.2 1.1.4 2.2.4 3.2.1."
    "8 0 1.6 0 2.4 0 .7-.1 1.5-.1 2.2 0 .5.1 1 .1 1.5 0 .6.1 1.2.4 1.7.3.6.7 1.1 1 1.7.7 1 "
    "1.4 2.1 1.9 3.2.7 1.2 1.2 2.6 1.6 3.9.2.8.4 1.6.6 2.4.1.7.1 1.4.2 2.1 0 .7 0 1.3 0 2 0"
    " .4 0 .7 0 1.1 0 .1.1.1.1.2 0 1.1 0 2.3 0 3.5-.1.2 0 .4-.1.6-.1.6-.2 1.2-.4 1.8-.2 1.2"
    "-.6 2.4-1.4 3.4-.4.4-.8.8-1.4 1-.8.4-1.7.5-2.5.5-1.2 0-2.3 0-3.4-.1-.6 0-1.2 0-1.8 0-."
    "2 0-.4 0-.6 0 0 .2 0 .4-.1.6 0 .4 0 .8-.1 1.2-.1 1.1-.4 2.3-.7 3.3-.5 1.6-1.3 3.1-2.2 "
    "4.5-.9 1.3-1.9 2.4-3.1 3.4-1.2 1-2.5 1.9-3.9 2.6-1.3.6-2.7 1.1-4.1 1.3-.7.2-1.5.3-2.2."
    "4-.2 0-.3 0-.5 0-.6 0-1.3 0-1.9 0zm9.9-26.6c-.3-.2-.5-.4-.7-.6-.9-.9-1.9-1.5-3-2-1.8-."
    "8-3.6-1.2-5.6-1.1-.9 0-1.8.1-2.7.3-2.3.6-4.3 1.8-6 3.5-1 1.1-1.8 2.3-2.4 3.6-.7 1.6-1."
    "1 3.3-1.1 5.1 0 .7.1 1.3.2 2 .2 1.2.5 2.3 1 3.3.7 1.4 1.6 2.7 2.7 3.7 1.1 1.1 2.3 1.9 "
    "3.7 2.5 1.9.8 3.9 1.1 5.9 1 1.5-.2 3-.5 4.4-1.2 1.6-.8 2.9-1.8 4.1-3.1.9-1 1.6-2.2 2.1"
    "-3.5.7-1.6 1-3.3.9-5 0-1.1-.1-2.1-.4-3.1-.6-2-1.6-3.8-3.1-5.4z",
    "M59.3 45.5c-.5.8-1.2 1.3-2.2 1.3-.7 0-1.3-.2-1.8-.7-.6-.5-.9-1.1-.9-1.8 0-4 0-8 0-12 0"
    "-1 .7-2 1.8-2.3 1-.3 1.9-.1 2.7.6.5.5.7 1.1.7 1.8.1 1 0 2 0 3 0 .1 0 .2 0 .3.9 0 1.8 0"
    " 2.7 0 0-.1 0-.2 0-.2 0-1.1 0-2.1 0-3.1-.1-1.1.8-2.2 2-2.5.1 0 .3 0 .5 0 .8 0 1.6 0 2."
    "4 0 .2 0 .3-.1.5-.2 1.4-.9 2.9-1.8 4.4-2.7 1.7-1.1 3.5-2.2 5.3-3.3.2-.1.5-.3.7-.5.5-.3"
    ".9-.4 1.5-.4 1.5 0 3.1 0 4.6 0 .1 0 .2 0 .3 0 0-.9 0-1.7 0-2.6-.1 0-.2 0-.3 0-1.6 0-3."
    "1 0-4.7 0-1.4 0-2.5-1.2-2.5-2.6 0-.7.2-1.3.7-1.8.4-.5 1-.8 1.8-.8 2.8 0 5.7 0 8.6 0 2."
    "2 0 4.4 0 6.6 0 1.2-.1 2.3.8 2.5 2.1.2.9 0 1.7-.7 2.3-.4.5-1 .8-1.8.8-1.5 0-3.1 0-4.6 "
    "0-.1 0-.2 0-.4 0 0 .8 0 1.7 0 2.6.1 0 .3 0 .4 0 4.2 0 8.4 0 12.6 0 1.1 0 2.3.8 2.5 2.1"
    ".1.2.1.3.1.4 0 3.4 0 6.7 0 10.1 0 .1 0 .2 0 .3.8 0 1.7 0 2.6 0 0-.1 0-.2 0-.3 0-1 0-2 "
    "0-3-.1-1 .7-2.2 1.9-2.5.9-.2 1.8 0 2.5.7.5.5.8 1.1.8 1.8 0 3.9 0 7.9 0 11.8 0 1.4-1.2 "
    "2.6-2.6 2.6-.7 0-1.3-.2-1.8-.7-.5-.5-.8-1-.8-1.8 0-1 0-2 0-3.1 0-.1 0-.1 0-.2-.9 0-1.8"
    " 0-2.6 0 0 .1 0 .1 0 .2 0 1 0 2 0 3 0 .9-.4 1.6-1.2 2.2-1 .7-2 1.4-3 2.1-1.5 1-3 2.1-4"
    ".6 3.2-.1.1-.3.2-.5.3-.4.3-.8.4-1.3.4-7.3 0-14.7 0-22.1 0-.9 0-1.6-.4-2.1-1.2-1-1.4-1."
    "9-2.8-2.9-4.2-.1-.2-.2-.2-.4-.2-.8 0-1.6 0-2.4 0-1.4 0-2.5-1.2-2.5-2.5 0-1.1 0-2.1 0-3"
    ".2 0 0 0-.1 0-.1-.9 0-1.8 0-2.7 0 0 .1 0 .1 0 .2 0 1 0 2 .1 3 0 .5-.2.9-.4 1.3zm30.8-8"
    ".1c.1-.2.3-.4.5-.6-.9 0-1.7 0-2.5 0-.8 0-1.6 0-2.5 0 1.9-2.5 3.7-5 5.5-7.5-1.9 0-3.8 0"
    "-5.7 0-1.9 3.1-3.9 6.3-5.8 9.4 1.6 0 3.2 0 4.7 0-.6 1.4-1.2 2.8-1.8 4.1-.6 1.4-1.2 2.8"
    "-1.8 4.2.1 0 .1 0 .1 0 .1-.1.2-.2.3-.3.3-.4.7-.7 1-1.1.5-.5 1-1 1.5-1.5.8-.8 1.5-1.6 2"
    ".3-2.5.5-.5 1-1 1.5-1.5.9-.9 1.8-1.8 2.7-2.7z",
)

CARRO_LARANJA = (
    "M47.8 63.7c-.4 0-.8 0-1.2 0-1.1 0-2-.8-2.2-1.9-.4-1.9-1.2-3.6-2.5-5.1-1.6-1.9-3.7-3.2-"
    "6.2-3.6-.7-.2-1.3-.5-1.7-1.2-.2-.3-.2-.6-.2-1 0-1.7 0-3.5 0-5.2-.1-.9.7-1.9 1.6-2.1.5-"
    ".1.9-.1 1.4 0 2.3.3 4.5 1.1 6.5 2.2 1.5.7 2.8 1.7 4.1 2.8 1.3 1.2 2.4 2.5 3.3 4 1.3 1."
    "8 2.2 3.8 2.7 6 .2.8.3 1.5.5 2.3 0 .1 0 .3 0 .4 0 1.2-.9 2.2-1.9 2.3-.1.1-.2.1-.3.1-1."
    "3 0-2.6 0-3.9 0z",
    "M39.4 68.7c-.7.8-1.5 1.4-2.4 1.8-1 .4-2 .7-3 .7-1.2 0-2.3-.1-3.3-.6-2.3-1.1-3.8-2.9-4."
    "4-5.5-.1-.5 0-1-.1-1.6 0-1 .2-1.9.6-2.8 1.1-2.4 3-3.9 5.6-4.4 2.4-.5 4.6.1 6.4 1.8 1.3"
    " 1.1 2.1 2.6 2.4 4.3.3 2-.1 3.8-1.2 5.5-.2.3-.4.5-.6.8zm-3.8-3.1c.7-.7.9-1.5.8-2.4-.2-"
    "1.3-1.5-2.3-2.8-2.2-1.5.1-2.9 1.6-2.4 3.3.5 2.1 3 2.7 4.4 1.3z",
    "M127.2 70.6c-.5.1-.8-.2-1.1-.6-.3-.5-.6-1.1-.9-1.6-.8-1.3-1.6-2.7-2.4-4-.2-.5-.2-1 0-1"
    ".5.6-.9 1.1-1.8 1.7-2.8.5-.8 1-1.7 1.5-2.6.1-.2.3-.4.5-.6.1-.1.3-.2.6-.2 1.4 0 2.8 0 4"
    ".3 0 .8 0 1.7 0 2.6 0 .3 0 .6.2.8.5.3.4.6.9.9 1.4.8 1.5 1.7 2.9 2.5 4.4.1.1.2.3.2.4.1."
    "3 0 .6-.1.8-.5.8-.9 1.6-1.4 2.3-.6 1.1-1.2 2.2-1.9 3.3-.1.2-.2.4-.4.6-.1.1-.4.2-.6.2-2"
    ".2 0-4.5 0-6.8 0zm.8-6.2c0 0 0 .1.1.2.4 1.1 1.5 1.9 2.8 1.7 1.4-.2 2.5-1.5 2.2-3.1-.2-"
    "1.4-1.5-2.4-2.9-2.2-1.5.2-2.6 1.7-2.2 3.4z",
)


def marca_svg(escuro=False):
    traco = "#ffffff" if escuro else "#2c3448"
    laranja = "#ff9538" if escuro else "#ed7a16"
    return (
        '<svg viewBox="0 0 160 81.5" aria-hidden="true">'
        + "".join('<path fill="%s" d="%s"/>' % (traco, d) for d in CARRO_TRACO)
        + "".join('<path fill="%s" d="%s"/>' % (laranja, d) for d in CARRO_LARANJA)
        + '</svg>'
    )


def marca(escuro=False, tag="span"):
    return ('<%s class="marca">%s<span class="marca-nome"><b>NENO</b><i>AUTOPEÇAS</i></span></%s>'
            % (tag, marca_svg(escuro), tag))


# favicon: o mesmo vetor do ícone dentro de um quadrado marinho. Virou arquivo
# (assets/icone.svg, gerado no fim deste script) porque o desenho oficial é
# detalhado demais para caber como data: URI no <head> de cada página.
FAVICON = "assets/icone.svg"


def icone_quadrado(lado=64, raio=14, fundo="#2c3448"):
    """Ícone quadrado — favicon e apple-touch: carro branco sobre marinho."""
    esc = lado / 160.0 * .9
    dx = (lado - 160 * esc) / 2.0
    dy = (lado - 81.5 * esc) / 2.0
    return (
        '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 %g %g" width="%g" height="%g">'
        '<rect width="%g" height="%g" rx="%g" fill="%s"/>'
        '<g transform="translate(%.2f,%.2f) scale(%.4f)">'
        % (lado, lado, lado, lado, lado, lado, raio, fundo, dx, dy, esc)
        + "".join('<path fill="#ffffff" d="%s"/>' % d for d in CARRO_TRACO)
        + "".join('<path fill="#ff9538" d="%s"/>' % d for d in CARRO_LARANJA)
        + '</g></svg>'
    )


def estrelas(n=5):
    return '<span class="estrelas" aria-hidden="true">%s</span>' % ("★" * n + "☆" * (5 - n))


def zap_url(msg):
    return "https://wa.me/%s?text=%s" % (
        ZAP_NUM, quote("Olá! Vim pelo Google. " + msg + " para: (modelo e ano do carro)"))


def zap_oficina():
    return "https://wa.me/%s?text=%s" % (ZAP_NUM, quote(
        "Olá! Falo por uma OFICINA MECÂNICA de (cidade). "
        "Quero saber a condição para oficina e entrar na lista de disponibilidade."))


# ------------------------------------------------------------------- JSON-LD
def jsonld(v):
    dados = {
        "@context": "https://schema.org",
        "@type": "AutoPartsStore",
        "@id": DOMINIO + "/#loja",
        "name": "Neno Autopeças",
        "legalName": "Neno Autopeças Ltda",
        "url": DOMINIO + "/" + (v["slug"] + ".html" if v["slug"] != "index" else ""),
        "telephone": ["+55 84 3351-2392", "+55 84 99967-5667"],
        "image": [DOMINIO + "/assets/fachada.webp",
                  DOMINIO + "/assets/hero-fachada.webp",
                  DOMINIO + "/assets/balcao.webp"],
        "logo": DOMINIO + "/assets/fachada.webp",
        "priceRange": "$$",
        "currenciesAccepted": "BRL",
        "paymentAccepted": "Dinheiro, Cartão de crédito, Cartão de débito, Aproximação (NFC)",
        "address": {
            "@type": "PostalAddress",
            "streetAddress": "Av. Senador Dinarte Mariz, 632",
            "addressLocality": "Pau dos Ferros",
            "addressRegion": "RN",
            "postalCode": "59900-000",
            "addressCountry": "BR",
        },
        # coordenadas exatas do pino do Perfil da Empresa no Google
        "geo": {"@type": "GeoCoordinates", "latitude": LAT, "longitude": LNG},
        "hasMap": PERFIL_GOOGLE,
        "openingHoursSpecification": [
            {"@type": "OpeningHoursSpecification",
             "dayOfWeek": ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"],
             "opens": "07:00", "closes": "11:30"},
            {"@type": "OpeningHoursSpecification",
             "dayOfWeek": ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"],
             "opens": "13:00", "closes": "17:00"},
            {"@type": "OpeningHoursSpecification",
             "dayOfWeek": ["Saturday"], "opens": "07:00", "closes": "12:00"},
        ],
        "aggregateRating": {
            "@type": "AggregateRating",
            "ratingValue": NOTA_NUM,
            "reviewCount": QTD_AVALIACOES,
            "bestRating": "5",
            "worstRating": "1",
        },
        "review": [
            {"@type": "Review",
             "author": {"@type": "Person", "name": a["nome"]},
             "reviewRating": {"@type": "Rating", "ratingValue": str(a["nota"]), "bestRating": "5"},
             "reviewBody": a["texto"]}
            for a in AVALIACOES
        ],
        "areaServed": [{"@type": "City", "name": c, "addressRegion": "RN"}
                       for c in ["Pau dos Ferros"] + CIDADES],
        "sameAs": [FACEBOOK, INSTAGRAM],
    }
    return json.dumps(dados, ensure_ascii=False, indent=1)


def jsonld_faq():
    dados = {
        "@context": "https://schema.org",
        "@type": "FAQPage",
        "mainEntity": [
            {"@type": "Question", "name": p,
             "acceptedAnswer": {"@type": "Answer", "text": r}}
            for p, r in FAQ
        ],
    }
    return json.dumps(dados, ensure_ascii=False, indent=1)


# ------------------------------------------------------------------- blocos
def bloco_familia(f, destaque):
    aberto = " open" if destaque == f["key"] else ""
    classe = "familia familia-destaque" if destaque == f["key"] else "familia"
    itens = "\n".join("      <li>%s</li>" % html.escape(i) for i in f["itens"])
    return f"""    <details class="{classe}" id="{f['anchor']}"{aberto}>
     <summary>{html.escape(f['nome'])}</summary>
     <div class="familia-corpo">
      <ul class="lista-pecas">
{itens}
      </ul>
      <a class="btn btn-zap" href="{zap_url(f['zap'])}" data-cta="whatsapp" rel="noopener">{IC_ZAP} Perguntar se tem — {html.escape(f['nome'].lower())}</a>
     </div>
    </details>"""


def catalogo(destaque):
    ordem = FAMILIAS[:]
    if destaque:
        ordem.sort(key=lambda f: 0 if f["key"] == destaque else 1)
    return "\n".join(bloco_familia(f, destaque) for f in ordem)


FAQ = [
    ("Vocês têm a peça do meu carro?",
     "Manda no WhatsApp o modelo, o ano e o motor — de preferência uma foto do documento ou da "
     "peça velha. A gente confere a aplicação e responde se tem aqui, junto com a foto da peça na "
     "prateleira. Se não tiver, a gente fala na hora, sem enrolar."),
    ("Entregam em outra cidade?",
     "Fazemos entrega. Para as cidades do Alto Oeste a gente combina o envio no WhatsApp — muita "
     "gente também manda buscar com quem vem a Pau dos Ferros no mesmo dia. O combinado sai por "
     "escrito antes de você pagar."),
    ("É peça original ou paralela?",
     "Trabalhamos com as duas. A gente diz qual é qual antes de vender, com a marca na mão, e o "
     "preço muda conforme a escolha. Quem decide é você — só não vendemos peça sem dizer o que é."),
    ("Tem garantia?",
     "Tem. Toda peça sai com nota e com a garantia do fabricante. Deu problema dentro do prazo, "
     "traz na loja com a nota que a gente resolve no balcão."),
    ("Quais as formas de pagamento?",
     "Dinheiro, cartão de crédito e de débito (VISA e MasterCard) e pagamento por aproximação no "
     "celular. Não é preciso agendar nada: chega e é atendido."),
    ("Atendem oficina com condição diferente?",
     "Sim. Oficina mecânica tem condição própria, atendimento prioritário no balcão e entra na "
     "lista de disponibilidade que mandamos às terças e sextas. Chame no WhatsApp dizendo que é "
     "oficina."),
]


def faq_html():
    out = []
    for p, r in FAQ:
        out.append(f"""    <details class="faq">
     <summary>{html.escape(p)}</summary>
     <div class="faq-resp"><p>{html.escape(r)}</p></div>
    </details>""")
    return "\n".join(out)


def chips(itens, extra=""):
    lis = "\n".join("     <li>%s</li>" % html.escape(i) for i in itens)
    return f'    <ul class="chips {extra}">\n{lis}\n    </ul>'


def galeria_html():
    out = []
    for g in GALERIA:
        cls = (' class="%s"' % g["classe"]) if g["classe"] else ""
        out.append(f"""    <figure{cls}>
     <img src="assets/{g['src']}" width="{g['w']}" height="{g['h']}" loading="lazy" decoding="async"
          alt="{html.escape(g['alt'])}">
     <figcaption>{html.escape(g['legenda'])}</figcaption>
    </figure>""")
    return "\n".join(out)


def avaliacoes_html():
    out = []
    for a in AVALIACOES:
        inicial = a["nome"].strip()[0].upper()
        out.append(f"""    <figure class="avaliacao">
     {estrelas(a['nota'])}
     <blockquote>“{html.escape(a['texto'])}”</blockquote>
     <figcaption>
      <span class="inicial" aria-hidden="true">{inicial}</span>
      <span><span class="quem">{html.escape(a['nome'])}</span><br><span class="quando">{a['nota']} de 5 · {a['quando']}</span></span>
     </figcaption>
    </figure>""")
    return "\n".join(out)


def tiras_html():
    itens = [
        (IC_RELOGIO, "Estoque no balcão: leva hoje"),
        (IC_ESTRELA, "%s no Google · %d avaliações" % (NOTA, QTD_AVALIACOES)),
        (IC_ESCUDO, "Nota fiscal e garantia do fabricante"),
        (IC_CARTAO, "Dinheiro, cartão e aproximação"),
    ]
    lis = "\n".join("    <li>%s <span>%s</span></li>" % (ic, html.escape(t)) for ic, t in itens)
    return '   <ul class="tiras">\n%s\n   </ul>' % lis


# ------------------------------------------------------------------ template
def pagina(v):
    canonical = DOMINIO + "/" + ("" if v["slug"] == "index" else v["slug"] + ".html")
    zap = zap_url(v["zap"])
    return f"""<!DOCTYPE html>
<html lang="pt-BR">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{html.escape(v['titulo'])}</title>
<meta name="description" content="{html.escape(v['desc'])}">
<link rel="canonical" href="{canonical}">
<meta name="robots" content="index, follow, max-image-preview:large">
<meta name="theme-color" content="#2c3448">
<meta name="geo.region" content="BR-RN">
<meta name="geo.placename" content="Pau dos Ferros">
<meta name="geo.position" content="{LAT};{LNG}">
<meta name="ICBM" content="{LAT}, {LNG}">
<meta property="og:type" content="business.business">
<meta property="og:locale" content="pt_BR">
<meta property="og:site_name" content="Neno Autopeças">
<meta property="og:title" content="{html.escape(v['titulo'])}">
<meta property="og:description" content="{html.escape(v['desc'])}">
<meta property="og:url" content="{canonical}">
<meta property="og:image" content="{DOMINIO}/assets/fachada.webp">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta name="twitter:card" content="summary_large_image">
<link rel="icon" href="{FAVICON}">
<link rel="apple-touch-icon" href="assets/icone-180.png">
<link rel="preload" as="image" href="assets/hero-fachada.webp" fetchpriority="high">
<link rel="stylesheet" href="styles.css">

<!-- =====================================================================
     GOOGLE ADS — TAG DE CONVERSÃO (placeholder)
     1) Descomente o bloco abaixo e troque AW-XXXXXXXXX pelo ID da conta.
     2) Em Ferramentas > Conversões, crie 3 ações de conversão
        (WhatsApp, Ligar, Ver rota) e cole cada rótulo no objeto
        NENO_CONVERSOES no fim desta página.
<script async src="https://www.googletagmanager.com/gtag/js?id=AW-XXXXXXXXX"></script>
<script>
  window.dataLayer = window.dataLayer || [];
  function gtag(){{dataLayer.push(arguments);}}
  gtag('js', new Date());
  gtag('config', 'AW-XXXXXXXXX');
</script>
     ===================================================================== -->

<script type="application/ld+json">
{jsonld(v)}
</script>
<script type="application/ld+json">
{jsonld_faq()}
</script>
</head>
<body data-grupo="{v['slug']}">
<a class="pular" href="#conteudo">Pular para o conteúdo</a>

<!-- 1. BARRA FIXA DE AÇÃO — rodapé no mobile, topo no desktop -->
<nav class="barra" aria-label="Contato rápido">
 <div class="barra-grade">
  <a class="btn btn-zap" href="{zap}" data-cta="whatsapp" rel="noopener">{IC_ZAP} WhatsApp</a>
  <a class="btn btn-ligar" href="tel:{FIXO_TEL}" data-cta="ligar">{IC_TEL} Ligar</a>
  <a class="btn btn-rota" href="{ROTA}" data-cta="rota" target="_blank" rel="noopener">{IC_MAP} Rota</a>
 </div>
</nav>

<header class="topo">
 <div class="env">
  {marca()}
  <div class="topo-lado">
   <a class="nota-google" href="{PERFIL_GOOGLE}" target="_blank" rel="noopener"
      aria-label="Nota {NOTA} de 5 no Google, {QTD_AVALIACOES} avaliações">
    <span class="nota">{NOTA}</span>{estrelas()}<span class="qtd">({QTD_AVALIACOES})</span>
   </a>
   <a class="topo-tel" href="tel:{FIXO_TEL}" data-cta="ligar">{IC_TEL} {FIXO_VIS}</a>
  </div>
 </div>
</header>

<main id="conteudo">

<!-- 2. HERO -->
<section class="hero">
 <div class="env">
  <div class="hero-texto">
   <p class="selo" id="selo-horario" aria-live="polite"><span class="ponto"></span><span id="selo-texto">Confira o horário abaixo</span></p>
   <h1>{html.escape(v['h1'])}</h1>
   <p class="promessa"><strong>Tem no balcão hoje.</strong> {html.escape(v['lead'])}</p>
   <div class="pilha">
    <a class="btn btn-zap btn-grande" href="{zap}" data-cta="whatsapp" rel="noopener">{IC_ZAP} Chamar no WhatsApp</a>
    <a class="btn btn-ligar btn-grande" href="tel:{FIXO_TEL}" data-cta="ligar">{IC_TEL} Ligar agora</a>
    <a class="btn btn-rota btn-grande" href="{ROTA}" data-cta="rota" target="_blank" rel="noopener">{IC_MAP} Ver rota até a loja</a>
   </div>
  </div>
  <div class="hero-figura">
   <img class="hero-foto" src="assets/hero-fachada.webp" width="1040" height="585"
        alt="Fachada da Neno Autopeças na Av. Senador Dinarte Mariz, em Pau dos Ferros, com a loja aberta e o balcão à vista"
        fetchpriority="high" decoding="async">
   <p class="hero-etiqueta">{estrelas()}<span>{NOTA} no Google<small>{QTD_AVALIACOES} avaliações</small></span></p>
  </div>
 </div>
 <div class="env env-tiras">
{tiras_html()}
 </div>
</section>

<!-- 3. FAIXA DE PROVA -->
<section class="provas" aria-label="A loja em números">
 <div class="env">
  <div class="provas-grade">
   <div><div class="prova-num">+30 mil</div><div class="prova-txt">peças vendidas no balcão</div></div>
   <div><div class="prova-num">+7 mil</div><div class="prova-txt">itens diferentes já atendidos</div></div>
   <div><div class="prova-num">{NOTA} ★</div><div class="prova-txt">no Google, com {QTD_AVALIACOES} avaliações</div></div>
   <div><div class="prova-num">Alto Oeste</div><div class="prova-txt">atendemos a região toda, num raio de 60 km</div></div>
  </div>
 </div>
</section>

<!-- 4. TEM NA HORA -->
<section>
 <div class="env">
  <div class="cabeca-sec revelar">
   <span class="olho">Por que aqui</span>
   <h2>Tem na hora</h2>
   <p class="apoio">A diferença não é o preço da internet. É o carro voltar a rodar hoje.</p>
  </div>
  <div class="cartoes">
   <div class="cartao revelar">
    <div class="cartao-icone">{IC_CAIXA}</div>
    <h3>Estoque no balcão, não encomenda</h3>
    <ul class="contraste">
     <li><span class="sim">✓</span><span><strong>Aqui:</strong> você vem, confere a peça na mão e leva hoje.</span></li>
     <li><span class="nao">✕</span><span><strong>Site:</strong> 7 a 15 dias de frete com o carro parado.</span></li>
    </ul>
   </div>
   <div class="cartao revelar">
    <div class="cartao-icone">{IC_ESCUDO}</div>
    <h3>Conferimos a aplicação antes de vender</h3>
    <p>Diz o modelo, o ano e o motor que a gente checa se a peça serve mesmo no seu carro. Peça
       errada volta pro estoque, não pro seu prejuízo.</p>
   </div>
   <div class="cartao revelar">
    <div class="cartao-icone">{IC_ZAP}</div>
    <h3>Foto da peça antes de você sair de casa</h3>
    <p>Se você mora em outra cidade, a gente manda pelo WhatsApp a foto da peça na prateleira.
       Você só pega a estrada depois de ver que tem.</p>
   </div>
  </div>
 </div>
</section>

<!-- 5. CATÁLOGO POR FAMÍLIA -->
<section class="sec-cinza">
 <div class="env">
  <div class="cabeca-sec revelar">
   <span class="olho">O que tem na prateleira</span>
   <h2>Catálogo por família</h2>
   <p class="apoio">Toque na família para ver a lista. Não achou o item? Pergunte no WhatsApp — a
      prateleira é maior que a lista.</p>
  </div>
{catalogo(v['destaque'])}
 </div>
</section>

<!-- 6. MODELOS ATENDIDOS -->
<section>
 <div class="env">
  <div class="cabeca-sec revelar">
   <span class="olho">Serve no seu carro?</span>
   <h2>Modelos que a gente atende todo dia</h2>
  </div>
{chips(MODELOS)}
  <h3>Montadoras</h3>
{chips(MONTADORAS, "montadoras")}
  <p class="apoio pequeno">Não está na lista? Manda o modelo e o ano no WhatsApp mesmo assim.
     Boa parte das peças serve em mais de um carro.</p>
 </div>
</section>

<!-- 7. LINHA PESADA E ANTIGA -->
<section class="pesada" id="linha-pesada-destaque">
 <div class="env">
  <div class="pesada-grade">
   <div>
    <span class="olho">Quase ninguém tem</span>
    <h2>Linha pesada e antiga</h2>
    <p class="destaque-frase">1113, D20, C10, F1000, Cargo e trator: peça dessas você não acha
       pronta em marketplace — e quando acha, o prazo passa de 15 dias.</p>
    <p>A gente segura essa linha em estoque justamente porque é o que ninguém mais segura. Freio,
       suspensão, embreagem e arrefecimento dessas máquinas saem do balcão no mesmo dia.</p>
{chips(PESADA)}
    <div class="pilha">
     <a class="btn btn-zap btn-grande" href="{zap_url('Preciso de peça de linha pesada/antiga')}" data-cta="whatsapp" rel="noopener">{IC_ZAP} Perguntar sobre linha pesada</a>
    </div>
   </div>
   <img class="pesada-foto" src="assets/linha-pesada.webp" width="880" height="586" loading="lazy" decoding="async"
        alt="Depósito da Neno Autopeças com tambores de freio, molas e caixas de peças de linha pesada">
  </div>
 </div>
</section>

<!-- 8. OFICINAS MECÂNICAS -->
<section>
 <div class="env">
  <div class="oficina revelar">
   <span class="olho">Para oficina mecânica</span>
   <h2>Condição de oficina</h2>
   <ul>
    <li><span><strong>Condição própria para oficina</strong> — preço diferente do balcão, combinado direto com a gente.</span></li>
    <li><span><strong>Lista de disponibilidade às terças e sextas</strong> — você recebe no WhatsApp o que entrou e o que está na prateleira.</span></li>
    <li><span><strong>Atendimento prioritário</strong> — carro no elevador não espera fila.</span></li>
   </ul>
   <a class="btn btn-zap btn-grande" href="{zap_oficina()}" data-cta="whatsapp" rel="noopener">{IC_ZAP} Falar como oficina</a>
  </div>
 </div>
</section>

<!-- 9. A LOJA POR DENTRO -->
<section class="sec-cinza">
 <div class="env">
  <div class="cabeca-sec revelar">
   <span class="olho">A loja por dentro</span>
   <h2>Não é depósito de foto bonita: é a prateleira mesmo</h2>
   <p class="apoio">Fotos da loja na Av. Senador Dinarte Mariz, as mesmas do nosso Perfil da
      Empresa no Google.</p>
  </div>
  <div class="galeria">
{galeria_html()}
  </div>
 </div>
</section>

<!-- 10. AVALIAÇÕES DO GOOGLE -->
<section>
 <div class="env">
  <div class="cabeca-sec revelar">
   <span class="olho">Quem já comprou</span>
   <h2>Avaliações no Google</h2>
  </div>
  <div class="nota-bloco revelar">
   <div class="nota-grande">
    <span class="nota-valor">{NOTA}</span>
    <span class="nota-lado">{estrelas()}<small>{QTD_AVALIACOES} avaliações no Google</small></span>
   </div>
   <p class="apoio pequeno">Comentários copiados do nosso Perfil da Empresa.
      <a href="{PERFIL_GOOGLE}" target="_blank" rel="noopener">Ver todas no Google</a>.</p>
  </div>
  <div class="avaliacoes">
{avaliacoes_html()}
  </div>
 </div>
</section>

<!-- 11. COMO CHEGAR -->
<section class="sec-cinza">
 <div class="env">
  <div class="cabeca-sec revelar">
   <span class="olho">Onde fica</span>
   <h2>Como chegar</h2>
  </div>
  <div class="chegar-grade">
   <div>
    <div class="endereco-cartao">
     <p><strong>{ENDERECO}</strong><br>{CIDADE_UF}</p>
     <p class="apoio pequeno">Avenida principal de Pau dos Ferros. Estacionamento gratuito na porta
        e Wi-Fi na loja. Entrada e atendimento acessíveis para cadeira de rodas.</p>
     <table class="horarios">
      <caption>Horário de funcionamento</caption>
      <tbody>
       <tr><th scope="row">Segunda a sexta</th><td>07:00–11:30 e 13:00–17:00</td></tr>
       <tr><th scope="row">Sábado</th><td>07:00–12:00</td></tr>
       <tr><th scope="row">Domingo</th><td>Fechado</td></tr>
      </tbody>
     </table>
     <a class="btn btn-rota btn-grande" href="{ROTA}" data-cta="rota" target="_blank" rel="noopener">{IC_MAP} Abrir rota no Google Maps</a>
    </div>
   </div>
   <div class="mapa-caixa" id="mapa-caixa" data-src="{MAPA_EMBED}">
    <div>
     <p class="pequeno apoio">O mapa só carrega quando você pedir — assim a página abre rápido no 4G.</p>
     <button type="button" class="btn btn-escuro" id="btn-mapa">Carregar o mapa</button>
    </div>
   </div>
  </div>

  <h3>Cidades que atendemos</h3>
  <ul class="cidades">
   <li>Pau dos Ferros</li>
{chr(10).join('   <li>%s</li>' % html.escape(c) for c in CIDADES)}
  </ul>
 </div>
</section>

<!-- 12. FAQ -->
<section>
 <div class="env">
  <div class="cabeca-sec revelar">
   <span class="olho">Perguntas que chegam todo dia</span>
   <h2>Dúvidas</h2>
  </div>
  <div class="faq-grade">
{faq_html()}
  </div>
 </div>
</section>

</main>

<!-- 13. RODAPÉ -->
<footer class="rodape">
 <div class="env">
  <div class="rodape-blocos">
   <div>
    {marca(escuro=True)}
    <p>Neno Autopeças Ltda<br>{ENDERECO}<br>{CIDADE_UF}</p>
    <ul class="rodape-links">
     <li><a href="{INSTAGRAM}" rel="noopener" target="_blank">{IC_INSTA} Instagram</a></li>
     <li><a href="{FACEBOOK}" rel="noopener" target="_blank">{IC_FACE} Facebook</a></li>
     <li><a href="{PERFIL_GOOGLE}" rel="noopener" target="_blank">{IC_MAP} Google</a></li>
    </ul>
   </div>
   <div>
    <h3>Contato</h3>
    <p>WhatsApp <a href="{zap}" data-cta="whatsapp" rel="noopener">{ZAP_VIS}</a><br>
       Fixo <a href="tel:{FIXO_TEL}" data-cta="ligar">{FIXO_VIS}</a></p>
    <h3>Horário</h3>
    <p>Seg a sex 07:00–11:30 e 13:00–17:00<br>Sábado 07:00–12:00<br>Domingo fechado</p>
   </div>
   <div>
    <div class="nao-trabalhamos">
     <h3>O que não trabalhamos</h3>
     <p>Pra não fazer você perder viagem: não vendemos pneu, bateria, para-brisa, escapamento
        completo, motor ou câmbio completo, som e multimídia, nem acessório de tuning.</p>
    </div>
   </div>
  </div>
  <p class="rodape-fim">© <span id="ano">2026</span> Neno Autopeças Ltda · {ENDERECO}, {CIDADE_UF} ·
     Loja física de autopeças em Pau dos Ferros, atendendo o Alto Oeste potiguar.</p>
 </div>
</footer>

<script>
(function () {{
  "use strict";

  document.documentElement.className += ' js';

  /* ---------------------------------------------------------------
     A) CONVERSÕES DO GOOGLE ADS
     Troque os rótulos abaixo pelos das 3 ações de conversão criadas
     na conta. Formato: 'AW-XXXXXXXXX/YYYYYYYY'.
     --------------------------------------------------------------- */
  var NENO_CONVERSOES = {{
    whatsapp: 'AW-XXXXXXXXX/YYYYYYYY',  /* conversão "Clique no WhatsApp" */
    ligar:    'AW-XXXXXXXXX/YYYYYYYY',  /* conversão "Clique para ligar"  */
    rota:     'AW-XXXXXXXXX/YYYYYYYY'   /* conversão "Clique em ver rota" */
  }};

  var grupo = document.body.getAttribute('data-grupo') || 'index';

  document.addEventListener('click', function (ev) {{
    var alvo = ev.target.closest ? ev.target.closest('[data-cta]') : null;
    if (!alvo) return;
    var acao = alvo.getAttribute('data-cta');
    if (!NENO_CONVERSOES[acao]) return;

    if (typeof window.gtag === 'function') {{
      window.gtag('event', 'conversion', {{
        send_to: NENO_CONVERSOES[acao],
        value: 1.0,
        currency: 'BRL',
        transaction_id: ''
      }});
      window.gtag('event', 'contato_' + acao, {{ metodo: acao, grupo_anuncio: grupo }});
    }}
    if (window.dataLayer) {{
      window.dataLayer.push({{ event: 'contato', metodo: acao, grupo_anuncio: grupo }});
    }}
  }}, true);

  /* ---------------------------------------------------------------
     B) SELO "ABERTO AGORA / ABRE ÀS HH:MM"
     Horário: seg-sex 07:00-11:30 e 13:00-17:00 | sáb 07:00-12:00.
     Calculado no fuso da loja (America/Fortaleza), não no do celular.
     --------------------------------------------------------------- */
  var GRADE = {{
    0: [],
    1: [[420, 690], [780, 1020]],
    2: [[420, 690], [780, 1020]],
    3: [[420, 690], [780, 1020]],
    4: [[420, 690], [780, 1020]],
    5: [[420, 690], [780, 1020]],
    6: [[420, 720]]
  }};
  var NOMES = ['domingo', 'segunda', 'terça', 'quarta', 'quinta', 'sexta', 'sábado'];

  function hhmm(m) {{
    var h = Math.floor(m / 60), i = m % 60;
    return (h < 10 ? '0' : '') + h + ':' + (i < 10 ? '0' : '') + i;
  }}

  function agoraNaLoja() {{
    try {{
      var p = new Intl.DateTimeFormat('en-US', {{
        timeZone: 'America/Fortaleza', weekday: 'short',
        hour: '2-digit', minute: '2-digit', hourCycle: 'h23'
      }}).formatToParts(new Date());
      var v = {{}};
      for (var i = 0; i < p.length; i++) v[p[i].type] = p[i].value;
      var dias = {{ Sun: 0, Mon: 1, Tue: 2, Wed: 3, Thu: 4, Fri: 5, Sat: 6 }};
      return {{ dia: dias[v.weekday], min: parseInt(v.hour, 10) * 60 + parseInt(v.minute, 10) }};
    }} catch (e) {{
      var d = new Date();
      return {{ dia: d.getDay(), min: d.getHours() * 60 + d.getMinutes() }};
    }}
  }}

  function situacao() {{
    var n = agoraNaLoja(), faixas = GRADE[n.dia] || [], i;
    for (i = 0; i < faixas.length; i++) {{
      if (n.min >= faixas[i][0] && n.min < faixas[i][1]) {{
        return {{ aberto: true, texto: 'Aberto agora · fecha às ' + hhmm(faixas[i][1]) }};
      }}
    }}
    for (i = 0; i < faixas.length; i++) {{
      if (n.min < faixas[i][0]) {{
        return {{ aberto: false, texto: 'Fechado agora · abre às ' + hhmm(faixas[i][0]) }};
      }}
    }}
    for (var d = 1; d <= 7; d++) {{
      var prox = (n.dia + d) % 7, f = GRADE[prox] || [];
      if (f.length) {{
        return {{
          aberto: false,
          texto: 'Fechado agora · abre ' + (d === 1 ? 'amanhã' : NOMES[prox]) + ' às ' + hhmm(f[0][0])
        }};
      }}
    }}
    return {{ aberto: false, texto: 'Confira o horário abaixo' }};
  }}

  function pintaSelo() {{
    var caixa = document.getElementById('selo-horario');
    var texto = document.getElementById('selo-texto');
    if (!caixa || !texto) return;
    var s = situacao();
    texto.textContent = s.texto;
    caixa.className = 'selo ' + (s.aberto ? 'aberto' : 'fechado');
  }}
  pintaSelo();
  setInterval(pintaSelo, 60000);

  /* ---------------------------------------------------------------
     C) MAPA SÓ APÓS CLIQUE (nada de iframe no carregamento)
     --------------------------------------------------------------- */
  var btnMapa = document.getElementById('btn-mapa');
  if (btnMapa) {{
    btnMapa.addEventListener('click', function () {{
      var caixa = document.getElementById('mapa-caixa');
      var f = document.createElement('iframe');
      f.src = caixa.getAttribute('data-src');
      f.width = '100%';
      f.height = '340';
      f.loading = 'lazy';
      f.title = 'Mapa da Neno Autopeças, Av. Senador Dinarte Mariz, 632, Pau dos Ferros';
      f.setAttribute('referrerpolicy', 'no-referrer-when-downgrade');
      caixa.innerHTML = '';
      caixa.className = 'mapa-caixa carregado';
      caixa.appendChild(f);
    }});
  }}

  /* ---------------------------------------------------------------
     D) No desktop, abre todas as famílias do catálogo
     --------------------------------------------------------------- */
  if (window.matchMedia && window.matchMedia('(min-width: 900px)').matches) {{
    var fam = document.querySelectorAll('details.familia');
    for (var k = 0; k < fam.length; k++) fam[k].open = true;
  }}

  /* Abre a família correspondente quando a URL vem com #âncora */
  if (location.hash) {{
    var alvoHash = document.querySelector('details' + location.hash);
    if (alvoHash) alvoHash.open = true;
  }}

  /* ---------------------------------------------------------------
     E) REVELAÇÃO SUAVE AO ROLAR — puro enfeite, degrada sozinho.
        Sem IntersectionObserver (ou com "reduzir movimento"), tudo
        aparece normalmente.
     --------------------------------------------------------------- */
  var reduzir = window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  var alvos = document.querySelectorAll('.revelar');
  if (!reduzir && 'IntersectionObserver' in window) {{
    var obs = new IntersectionObserver(function (linhas) {{
      for (var i = 0; i < linhas.length; i++) {{
        if (linhas[i].isIntersecting) {{
          linhas[i].target.className += ' visivel';
          obs.unobserve(linhas[i].target);
        }}
      }}
    }}, {{ rootMargin: '0px 0px -8% 0px', threshold: .08 }});
    for (var j = 0; j < alvos.length; j++) obs.observe(alvos[j]);
  }} else {{
    for (var m = 0; m < alvos.length; m++) alvos[m].className += ' visivel';
  }}

  var ano = document.getElementById('ano');
  if (ano) ano.textContent = new Date().getFullYear();
}})();
</script>
</body>
</html>
"""


with open(os.path.join(SAIDA, "assets", "icone.svg"), "w", encoding="utf-8") as fh:
    fh.write(icone_quadrado())

for v in VARIANTES:
    caminho = os.path.join(SAIDA, v["slug"] + ".html")
    with open(caminho, "w", encoding="utf-8") as fh:
        fh.write(pagina(v))
    print(v["slug"] + ".html", os.path.getsize(caminho), "bytes")
