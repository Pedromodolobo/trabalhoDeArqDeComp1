#!/usr/bin/env python3
"""
Quebra de cifra de SUBSTITUICAO HOMOGENEA por escalada (hill climbing),
usando a metrica de quad-grams.  Exercicio 1 -> arquivo "Code 1".

Ideia: a chave e uma permutacao das 26 letras (26! possibilidades).
Partimos de chaves aleatorias, trocamos duas letras da chave e aceitamos
a troca se o quad-gram score do texto resultante melhorar.  Repetimos
com varios reinicios para escapar de maximos locais.

Uso:
    python3 quebra_homogenea.py "Code 1" [quadgrams.txt]
"""

import math
import random
import sys
import os

ALFA = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"


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


def criar_avaliador(quad, total, piso):
    def avaliar(texto):
        letras = "".join(c for c in texto.upper() if "A" <= c <= "Z")
        soma = 0.0
        for i in range(len(letras) - 3):
            g = letras[i:i + 4]
            v = quad.get(g)
            soma += math.log10(v / total) if v else piso
        return soma
    return avaliar


def decifrar(texto, chave):
    """chave[c] = letra clara correspondente a letra cifrada c."""
    saida = []
    for c in texto:
        if "A" <= c <= "Z":
            saida.append(chave[ord(c) - 65])
        else:
            saida.append(c)
    return "".join(saida)


def quebrar(cifrado, avaliar, reinicios=25, iteracoes=1500):
    melhor = (None, None)
    for _ in range(reinicios):
        chave = list(ALFA)
        random.shuffle(chave)
        atual = avaliar(decifrar(cifrado, chave))
        for _ in range(iteracoes):
            a, b = random.sample(range(26), 2)
            chave[a], chave[b] = chave[b], chave[a]
            novo = avaliar(decifrar(cifrado, chave))
            if novo > atual:
                atual = novo
            else:
                chave[a], chave[b] = chave[b], chave[a]
        if melhor[0] is None or atual > melhor[0]:
            melhor = (atual, chave[:])
    return melhor


def main():
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)

    caminho = sys.argv[1]
    quad_path = sys.argv[2] if len(sys.argv) > 2 else "quadgrams.txt"
    if not os.path.exists(quad_path):
        quad_path = os.path.join(os.path.dirname(__file__), "quadgrams.txt")

    random.seed(1)
    quad, total = carregar_quadgrams(quad_path)
    piso = math.log10(0.01 / total)
    avaliar = criar_avaliador(quad, total, piso)

    cifrado = carregar_binario(caminho)
    score, chave = quebrar(cifrado, avaliar)
    claro = decifrar(cifrado, chave)

    n = sum(c.isalpha() for c in claro)
    print("Chave (cifrado -> claro):")
    print("  ", ALFA)
    print("  ", "".join(chave))
    print(f"Score: {score:.1f}  ({score / n:.2f} por letra)")
    print("\nMensagem:\n")
    print(claro)


if __name__ == "__main__":
    main()
