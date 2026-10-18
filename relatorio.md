# Trabalho Prático 1 — Representação Numérica e Criptografia

**Disciplina:** Arquitetura de Computadores
**Tema:** quebra de cifras de substituição homogênea e rotativa

---

## 1. Introdução e modelo canônico

Um criptossistema clássico pode ser descrito pelo modelo canônico de cinco
elementos:

| Elemento | Descrição | Neste trabalho |
|---|---|---|
| Texto claro | mensagem original | inglês, em maiúsculas |
| Texto cifrado | mensagem ilegível | cadeia de letras/pontuação |
| Chave | segredo que parametriza o algoritmo | permutação do alfabeto |
| Algoritmo de cifragem | transforma claro → cifrado | substituição |
| Algoritmo de decifragem | transforma cifrado → claro | inverso |

Os anexos chegam em **binário**. Cada caractere foi convertido para o seu
**código ASCII** e depois para a representação binária; os caracteres são
separados por espaços e a barra (`100000`) representa o espaço. A primeira
etapa de qualquer programa é, portanto, ler cada token binário e recuperar o
caractere:

```python
texto = "".join(chr(int(token, 2)) for token in arquivo.read().split())
```

Cada mensagem é quebrada por **análise estatística do idioma**, e não por
tentativa de todas as chaves (a cifra de substituição tem `26! − 1 ≈ 4·10²⁶`
chaves, inviável de enumerar).

### 1.1 Métrica de N-gramas (quad-grams)

A qualidade de uma chave candidata é medida pela **estatística de
quad-grams**: a probabilidade de cada sequência de 4 letras aparecer em
textos estruturados do idioma. Para um texto `t` formado pelos quad-grams
`q_i`:

$$S(t) = \sum_{i} \log_{10}\!\left(\frac{c(q_i)}{N}\right)$$

onde `c(q_i)` é a contagem do quad-grama na tabela de referência e `N` é o
total. Quad-grams ausentes recebem um piso `log10(0.01/N)`. Quanto **maior**
(menos negativo) o score, mais parecido com o idioma. Como referência,
usamos a tabela canônica `quadgrams.txt` (389 373 quad-grams, ~4,2 bilhões de
ocorrências). Calibração obtida:

| Texto | Score por letra |
|---|---|
| Inglês real | ≈ **−4,14** |
| Texto aleatório | ≈ **−8,4** |

Essa separação clara é o que permite usar a métrica como função-objetivo.

---

## 2. Experimento 1 — Substituição **homogênea** (`Code 1`)

### 2.1 Identificação

O índice de coincidência (IC) mede a chance de duas letras ao acaso serem
iguais:

$$IC = \frac{\sum_i f_i(f_i-1)}{n(n-1)}$$

| Texto | Letras | IC |
|---|---|---|
| `Code 1` cifrado | 1697 | **0,0686** |
| inglês esperado | — | ≈ 0,066 |
| aleatório | — | ≈ 0,0385 |

O IC alto (≈ inglês) mostra que a **distribuição de frequências foi
preservada** → cifra **monoalfabética** (substituição homogênea). A letra mais
frequente do cifrado é `O` (14,2 %), que corresponde ao `E` do inglês.

### 2.2 Ataque

Como o espaço de chaves é gigantesco, usa-se **escalada (hill climbing)**:

1. começa-se de uma permutação aleatória (chave candidata);
2. trocam-se duas letras da chave;
3. mede-se o score de quad-grams do texto decifrado;
4. aceita-se a troca se o score melhorar;
5. repete-se com vários reinícios aleatórios.

Implementação: `quebra_homogenea.py`.

### 2.3 Resultado

Chave (cifrado → claro):

```
cifrado : ABCDEFGHIJKLMNOPQRSTUVWXYZ
claro   : DVHYZQFWRPLJSIEXMGCAUTOBKN
```

Score final: **−4,14 por letra** (qualidade de inglês real). O texto é o
trecho *Pale Blue Dot* de Carl Sagan:

> LOOK AGAIN AT THAT DOT. THAT'S HERE. THAT'S HOME. THAT'S US. ON IT EVERYONE
> YOU LOVE, EVERYONE YOU KNOW, EVERYONE YOU EVER HEARD OF, EVERY HUMAN BEING
> WHO EVER WAS, LIVED OUT THEIR LIVES. ... THE PALE BLUE DOT, THE ONLY HOME
> WE'VE EVER KNOWN.

---

## 3. Experimento 2 — Substituição **rotativa** (`Code 2`)

### 3.1 Identificação

| Texto | Letras | IC |
|---|---|---|
| `Code 2` cifrado | 370 | **0,0378** |

O IC é praticamente **uniforme** (igual ao aleatório), ou seja, a distribuição
foi "espalhada". Isso **descarta** tanto a substituição homogênea quanto um
César simples: a frequência de `Code 2` é quase plana (cada letra entre 2,4 % e
5,7 %), ao contrário de qualquer texto natural.

Conclusão: a chave **muda ao longo da mensagem** → cifra **polialfabética**
(a "substituição rotativa").

### 3.2 Descoberta do período

Calculando o IC médio **por coluna** para cada possível tamanho de chave,
aparece um pico em múltiplos de 26:

| Tamanho (L) | IC médio das colunas |
|---|---|
| 1 | 0,0378 |
| 13 | 0,0575 |
| **26** | **0,0703** |
| 39 | 0,0544 |
| **52** | **0,0694** |
| **78** | **0,0671** |

O valor alto em 26 (≈ inglês) e seus múltiplos indica que o alfabeto de
substituição **gira uma casa por letra** (período 26). Um César puro, um
Vigenère com palavra-chave e um César progressivo linear foram testados e
**descartados** (nenhum atinge score de idioma).

### 3.3 Modelo e ataque

O modelo que descreve os dados é: existe um alfabeto de substituição fixo `S`
que **gira** conforme a posição da letra. Sendo `k` o índice da letra (0,1,2,…;
espaços não contam):

$$cifrado[k] = S\big[(claro[k] + k) \bmod 26\big]
\qquad\Longrightarrow\qquad
claro[k] = \big(F[cifrado[k]] - k\big) \bmod 26$$

onde `F = S⁻¹` é a chave estática (uma permutação). O ataque é uma escalada
**sobre `F`** (trocar duas letras de `F`), pontuando o texto com quad-grams, e
testando alguns passos de rotação. O passo cujo texto atinge qualidade de
idioma é o correto.

Implementação: `quebra_rotativa.py`.

Score por passo de rotação (por letra):

| Passo | 1 | 3 | 5 | 7 | 11 | 15 | 25 |
|---|---|---|---|---|---|---|---|
| score/letra | **−4,13** | −6,58 | −6,60 | −6,61 | −6,46 | −6,37 | −6,44 |

O passo **1** se destaca (qualidade de inglês); os demais ficam perto de
"lixo estatístico".

### 3.4 Resultado

Chave estática `F` (cifrado → valor):

```
cifrado : ABCDEFGHIJKLMNOPQRSTUVWXYZ
F       : RJVMNETKFDZXGWSLAUQOIHCPYB
```

Score final: **−4,13 por letra**. Texto (também de Carl Sagan):

> THE DAY WE CEASE THE EXPLORATION OF THE COSMOS IS THE DAY WE THREATEN THE
> CONTINUING OF OUR SPECIES IN THAT BLEAK WORLD ARMS BEARING RESOURCE HUNGRY
> PEOPLE AND NATIONS WOULD BE PRONE TO ACT ON THEIR LOW CONTRACTED PREJUDICES
> AND WOULD HAVE SEEN THE LAST GASP OF HUMAN ENLIGHTENMENT UNTIL THE RISE OF
> A VISIONARY NEW CULTURE THAT ONCE AGAIN EMBRACES THE COSMIC PERSPECTIVE A
> PERSPECTIVE IN WHICH WE ARE ONE FITTING NEITHER ABOVE NOR BELOW BUT WITHIN

---

## 4. Métricas consolidadas

| | `Code 1` (homogênea) | `Code 2` (rotativa) |
|---|---|---|
| Letras | 1697 | 370 |
| IC do cifrado | 0,0686 (≈ idioma) | 0,0378 (≈ aleatório) |
| Diagnóstico | monoalfabética | polialfabética (rotação) |
| Período da chave | 1 (fixo) | 26 (gira 1 por letra) |
| Método | escalada sobre permutação | escalada sobre `F` + rotação |
| Score final (por letra) | **−4,14** | **−4,13** |
| Espaço de chaves | 26!−1 | 26 (passo) × 26! (alfabeto) |

---

## 5. Conclusão

O **índice de coincidência** foi a ferramenta que separou os dois casos:
valores próximos de 0,066 indicam uso de texto natural preservado
(monoalfabético); valores próximos de 0,038 indicam que a distribuição foi
"espalhada" (polialfabético). Nesse segundo caso, a análise por colunas
revelou o período 26 e levou ao modelo de **rotação do alfabeto de
substituição**. Em ambos os experimentos, a **estatística de quad-grams** foi
a função de qualidade que guiou a busca pela chave, atingindo textos com
score por letra equivalente ao de inglês real (≈ −4,1), o que confirma a
correção das chaves recuperadas.

---

## 6. Arquivos entregues

| Arquivo | Descrição |
|---|---|
| `quebra_cesar.py` | força bruta dos 25 deslocamentos de César (baseline genérico) |
| `quebra_homogenea.py` | quebra da substituição homogênea (`Code 1`) |
| `quebra_rotativa.py` | quebra da substituição rotativa (`Code 2`) |
| `substituicaoSimples.c` | decifragem homogênea em C (`Code 1`) |
| `substituicaoCircular.c` | decifragem rotativa em C (`Code 2`) |
| `quadgrams.txt` | tabela de referência de quad-grams do inglês |

### Como executar

```bash
# Python (quebra automática)
python3 quebra_homogenea.py "Code 1"
python3 quebra_rotativa.py  "Code 2"

# C (aplicando a chave recuperada)
gcc -O2 -o substituicaoSimples  substituicaoSimples.c  && ./substituicaoSimples  "Code 1"
gcc -O2 -o substituicaoCircular substituicaoCircular.c && ./substituicaoCircular "Code 2"
```
