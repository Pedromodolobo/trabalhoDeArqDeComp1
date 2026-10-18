#!/usr/bin/env python3
"""
Quebra de cifra de SUBSTITUICAO ROTATIVA, usando a metrica de quad-grams.
Exercicio 2 -> arquivo "Code 2".

Modelo da cifra:
    O alfabeto de substituicao gira uma casa a cada letra (espacos nao
    contam).  Sendo k o indice da letra (0,1,2,...) e S um alfabeto de
    substituicao fixo, o texto cifrado e obtido por
        cifrado[k] = S[ (claro[k] + k) mod 26 ]
    Portanto, para decifrar precisamos descobrir S.  Reescrevendo com
    F = inverso(S):
        claro[k] = ( F[cifrado[k]] - k ) mod 26

Estrategia:
    1) Detectar o giro: testamos alguns passos de rotacao e, para cada um,
       otimizamos F por escalada (trocas de letras) maximizando o score
       de quad-grams do texto claro.
    2) O passo que produzir texto com qualidade de idioma (perto de -4
       por letra em ingles) e o correto.

Uso:
    python3 quebra_rotativa.py "Code 2" [quadgrams.txt]
"""

import math
import random
import sys
import os

ALFA = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
PASSOS = [1, 3, 5, 7, 9, 11, 15, 17, 19, 21, 23, 25]  # coprimos com 26


def carregar_binario(caminho):
    with open(caminho) as arq:
        return "".join(chr(int(t, 2)) for t in arq.read().split())


def carregar_quadgrams(caminho):
    quad, total = {}, 0
    with open(caminho) as arq:
        for linha in arq:
            p = linha.split()
            if len(p) == 2:
                quad[p[0]] = int(p[1])
                total += int(p[1])
    return quad, total


def letras_e_pos(cifrado):
    """Devolve a lista de indices das letras e seus valores 0..25."""
    idx = [i for i, c in enumerate(cifrado) if "A" <= c <= "Z"]
    valores = [ord(cifrado[i]) - 65 for i in idx]
    return idx, valores


def criar_avaliador(quad, total, piso):
    def avaliar(lista):
        soma = 0.0
        for i in range(len(lista) - 3):
            g = lista[i] + lista[i + 1] + lista[i + 2] + lista[i + 3]
            v = quad.get(g)
            soma += math.log10(v / total) if v else piso
        return soma
    return avaliar


def quebrar_caso(cifrado, avaliar, passo, reinicios, iteracoes):
    idx, valores = letras_e_pos(cifrado)
    n = len(valores)

    def avalia(F):
        seq = [chr((F[valores[k]] - passo * k) % 26 + 65) for k in range(n)]
        return avaliar(seq)

    melhor = (None, None)
    for _ in range(reinicios):
        F = list(range(26))
        random.shuffle(F)
        atual = avalia(F)
        for _ in range(iteracoes):
            a, b = random.sample(range(26), 2)
            F[a], F[b] = F[b], F[a]
            novo = avalia(F)
            if novo > atual:
                atual = novo
            else:
                F[a], F[b] = F[b], F[a]
        if melhor[0] is None or atual > melhor[0]:
            melhor = (atual, F[:])
    return melhor


def aplicar(cifrado, F, passo):
    idx, valores = letras_e_pos(cifrado)
    saida = list(cifrado)
    for k, pos in enumerate(idx):
        saida[pos] = chr((F[valores[k]] - passo * k) % 26 + 65)
    return "".join(saida)


def main():
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)

    caminho = sys.argv[1]
    quad_path = sys.argv[2] if len(sys.argv) > 2 else "quadgrams.txt"
    if not os.path.exists(quad_path):
        quad_path = os.path.join(os.path.dirname(__file__), "quadgrams.txt")

    random.seed(7)
    quad, total = carregar_quadgrams(quad_path)
    piso = math.log10(0.01 / total)
    avaliar = criar_avaliador(quad, total, piso)

    cifrado = carregar_binario(caminho)
    n = sum(c.isalpha() for c in cifrado)

    print("Testando passos de rotacao (score por letra, mais alto = melhor):")
    melhor = (None, None, None)
    for passo in PASSOS:
        score, F = quebrar_caso(cifrado, avaliar, passo, reinicios=4,
                                iteracoes=3000)
        por_letra = score / n
        print(f"  passo={passo:2d}  score={score:9.1f}  por letra={por_letra:.2f}")
        if melhor[0] is None or score > melhor[0]:
            melhor = (score, passo, F)

    _, passo, F = melhor
    claro = aplicar(cifrado, F, passo)
    print(f"\nMelhor passo de rotacao: {passo}")
    print("Alfabeto estatico F (cifrado -> valor; texto = valor - passo*k):")
    print("  ", ALFA)
    print("  ", "".join(ALFA[F[c]] for c in range(26)))
    print("\nMensagem:\n")
    print(claro)


if __name__ == "__main__":
    main()
