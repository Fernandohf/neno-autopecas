# Landing pages — Neno Autopeças

6 páginas HTML estáticas compartilhando um único `styles.css`. Sem framework,
sem CDN, sem Google Fonts, sem biblioteca. É só subir a pasta inteira para a
hospedagem (Hostinger, Netlify, Vercel, GitHub Pages — qualquer uma serve).

```
index.html          Autopeças em Pau dos Ferros  (grupo genérico)
embreagem.html      Kit de embreagem
suspensao.html      Amortecedor e suspensão
freio.html          Pastilha, tambor e disco de freio
arrefecimento.html  Radiador, eletroventilador e bomba d'água
linha-pesada.html   MB 1113, D20, C10, F1000 e trator
styles.css          CSS compartilhado pelas 6
assets/             fotos reais da loja + ícone
build.py            gerador (edite aqui e rode `python build.py` para refazer as 6)
```

## ANTES DE PUBLICAR — só faltam 2 coisas

### 1. Trocar o domínio
Em `build.py`, a variável `DOMINIO`. Depois rode `python build.py`. Ela alimenta
o `canonical`, o `og:url` e o JSON-LD.

### 2. Colar o snippet do Google Ads
No `<head>` de cada página tem um bloco comentado. Descomente, troque
`AW-XXXXXXXXX` pelo ID da conta e, no script do rodapé, preencha os três rótulos:

```js
var NENO_CONVERSOES = {
  whatsapp: 'AW-XXXXXXXXX/YYYYYYYY',
  ligar:    'AW-XXXXXXXXX/YYYYYYYY',
  rota:     'AW-XXXXXXXXX/YYYYYYYY'
};
```

Crie **três ações de conversão separadas** no Ads (Clique no WhatsApp, Clique
para ligar, Clique em ver rota). Todo elemento com `data-cta="..."` dispara
sozinho — inclusive os botões dentro do catálogo e do rodapé. Com R$ 500/mês e
margem de R$ 53, separar as três é o que vai dizer qual grupo paga a conta.

> Os dois pontos acima são o que sobrou. Imagens, logo, cor da marca, pino do
> mapa e avaliações **já estão prontos e com dado real** — veja abaixo de onde
> cada um veio.

## O que mudou nesta revisão

### Fotos reais no lugar dos placeholders
As imagens coloridas de "SUBSTITUIR" sumiram. Em `assets/` agora estão as fotos
do próprio **Perfil da Empresa da loja no Google** (o mesmo link do Maps),
recortadas, tratadas e convertidas para WebP:

| arquivo | o que é | tamanho | onde aparece |
| --- | --- | --- | --- |
| `hero-fachada.webp` | fachada com o letreiro novo e a loja aberta | 1040 × 585 | hero |
| `fachada-noite.webp` | letreiro aceso à noite | 880 × 586 | galeria (foto grande) |
| `balcao.webp` | balcão por dentro | 880 × 586 | galeria |
| `estoque.webp` | corredor de prateleiras | 880 × 586 | galeria |
| `atendimento.webp` | atendente ao lado das caixas etiquetadas | 880 × 586 | galeria |
| `produtos.webp` | fluido de freio e produtos no expositor | 880 × 495 | galeria |
| `linha-pesada.webp` | depósito com tambores e caixas | 880 × 586 | bloco escuro |
| `fachada.webp` | foto de capa | 1200 × 630 | `og:image` (WhatsApp/Facebook) |
| `icone-180.png` | ícone da marca | 180 × 180 | `apple-touch-icon` |

Para trocar qualquer uma, **mantenha o nome do arquivo** e, se a proporção mudar,
corrija o `width`/`height` no `build.py` (a lista `GALERIA` e o `<img>` do hero).
Esses números existem para o navegador reservar o espaço e não empurrar a página
durante o carregamento — número errado piora o CLS.

Para converter JPG → WebP: `cwebp -q 50 foto.jpg -o assets/hero-fachada.webp`.
Alvo: hero abaixo de 60 KB, as da galeria abaixo de 50 KB.

### Logo de verdade, sem arquivo
O `logo-horizontal.svg` de placeholder foi apagado. A assinatura agora é
**desenhada inline no HTML**: o ícone (carro, motor com raio, disco de freio e
porca laranja) é um SVG gerado pela função `marca_svg()` do `build.py`, e o
"NENOAUTOPEÇAS" é texto com a fonte do sistema. Vantagem: zero requisição, e a
versão clara/escura sai da mesma fonte (o rodapé usa `marca(escuro=True)`).

O favicon é o mesmo desenho embutido como `data:` URI no `<head>` — também sem
requisição de rede.

Se um dia chegar o SVG oficial da agência, troque o corpo de `marca_svg()`.

### Uma cor de laranja só, tirada da fachada
Os três laranjas divergentes acabaram. As cores foram **amostradas da foto da
fachada**: o letreiro é `#2c3448` (azul-marinho) e o portão/letras é `#ed7a16`.
No topo do `styles.css`:

| variável | valor | uso |
| --- | --- | --- |
| `--laranja` | `#ed7a16` | preenchimento (botão, selo, faixa) — 7,2:1 com texto preto |
| `--laranja-texto` | `#a34500` | texto e link sobre branco — 5,4:1 (AA) |
| `--marinho` | `#2c3448` | topo escuro, rodapé, chips de montadora — 11,4:1 com branco |

O laranja claro **nunca** é usado como texto sobre branco (reprova em 2,9:1).

### Pino do mapa exato
O `geo` do JSON-LD estava com a coordenada aproximada do centro da cidade. Agora
usa o pino real do Perfil da Empresa: **-6.1180038, -38.2055928** (constantes
`LAT`/`LNG` no `build.py`). Elas também alimentam as metatags `geo.position` e
`ICBM`.

### Avaliações reais do Google
A caixa "espaço reservado" virou uma seção de verdade, em **HTML estático**
(nenhum widget externo — cada script de fora custa perto de meio segundo no 4G):

- nota **4,9** com **34 avaliações**, no selo do topo, no rótulo do hero, na
  faixa de números e na seção;
- 4 comentários reais, com nome e data, copiados do Perfil da Empresa;
- `aggregateRating` + `review` no JSON-LD, para a estrelinha aparecer no
  resultado do Google.

Tudo fica em `NOTA`, `QTD_AVALIACOES` e `AVALIACOES`, no topo do `build.py`.
**Reveja de tempos em tempos**: se a nota mudar no Google e não mudar aqui, o
`aggregateRating` fica mentindo — e isso o Google pune.

### Cara mais moderna
- Hero em duas colunas com a foto da fachada, sombra alta e etiqueta flutuante
  com a nota do Google.
- Tira de 4 garantias logo abaixo do hero (leva hoje · 4,9 no Google · nota e
  garantia · formas de pagamento).
- Cartões com ícone, faixa lateral em degradê e elevação no hover.
- Galeria da loja em mosaico (foto grande + 4 menores), com legenda sobre
  degradê e zoom suave no hover.
- Catálogo, FAQ e blocos escuros repaginados; a família da variante fica com o
  cabeçalho laranja sólido, impossível de não ver.
- Seta que gira no `<details>`, selo "Aberto agora" com pulso, revelação suave
  ao rolar (`IntersectionObserver`).
- **Tudo isso degrada sozinho**: sem JS, o conteúdo aparece normal; com
  `prefers-reduced-motion: reduce`, toda animação e transição é desligada.

## O que já estava pronto e continua

- Barra fixa de ação com WhatsApp, Ligar e Rota — rodapé no celular, topo no
  desktop. Nunca sai da tela.
- Selo "Aberto agora · fecha às 17:00" / "Fechado agora · abre às 07:00",
  calculado em JS no fuso da loja (America/Fortaleza), não no do celular do
  visitante. Atualiza a cada minuto. O horário bate com o do Perfil da Empresa.
- Mensagem do WhatsApp pré-preenchida e **diferente por página** e por família do
  catálogo. A do bloco de oficina se identifica como oficina, separada das outras.
- Catálogo em 5 famílias com âncoras `#embreagem`, `#suspensao`, `#freio`,
  `#arrefecimento`, `#linha-pesada`. Na variante correspondente, a família aparece
  primeiro e já aberta. No desktop todas abrem sozinhas.
- JSON-LD `AutoPartsStore` com telefone, endereço, horário em duas faixas,
  geo, `areaServed` com as 17 cidades — mais um `FAQPage` com as 6 perguntas.
- Mapa do Google só carrega depois do clique — nenhum iframe no load.
- Zero requisição externa no carregamento. Font-stack do sistema.
- Sem popup, sem intersticial, sem carrossel, sem contagem regressiva.

## Números conferidos

| | |
| --- | --- |
| HTML por página | ~52 KB (12 KB com gzip) |
| CSS (uma vez, fica em cache) | 28 KB (7 KB com gzip) |
| Foto do hero | 59 KB |
| **Carga inicial completa** | **~78 KB com gzip** (limite pedido: 200 KB) |
| Todas as imagens somadas | 376 KB (as da galeria só carregam ao rolar) |
| Botões abaixo de 48 px de altura | 0 |
| Erros de JS no console | 0 |
| Requisições externas no load | 0 |
| Rolagem horizontal em 360/390/414 px | nenhuma |

## Como refazer as páginas

Todo o texto está em `build.py` (dicionários `VARIANTES`, `FAMILIAS`, `FAQ`,
`AVALIACOES`, `GALERIA`). Edite lá e rode:

```bash
python build.py
```

Isso reescreve os 6 HTML. Não edite os HTML na mão se pretende rodar o gerador de
novo — eles são substituídos.

## Sobre o que não foi inventado

O texto não promete nada que não estava na ficha da loja: não fala em preço, não
fala em faturamento, não promete prazo de entrega fechado, não cita marca de peça
que não foi informada. Onde a ficha era omissa (formas de pagamento além do
cartão, entrega para outras cidades), a resposta do FAQ ficou no que a ficha
confirma — "faz entrega" e "combina no WhatsApp". **Leia as 6 respostas do FAQ
antes de publicar** e ajuste o que não bater com a rotina da loja.

Os números da faixa escura (+30 mil peças, +7 mil itens, Alto Oeste) vieram da
ficha da loja e não foram conferidos aqui — se algum não se sustentar, tire.
A nota 4,9 e as 34 avaliações, essas sim, saíram do Perfil da Empresa no Google.
