#!/usr/bin/env python3
"""
Ataque à cifra de substituição SIMPLES (homogênea) usando quad-grams e hill-climbing.
Lê arquivo binário (Code 1) com tokens ASCII binários, busca melhor permutação
cifrado->claro maximizando score de quad-grams. Requer quadgrams.txt.

Uso:
    python3 ataque_simples.py "Code 1" [quadgrams.txt]
"""

import math
import os
import random
import sys

ALFA = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"


def carregar_binario(caminho):
    with open(caminho) as arq:
        return "".join(chr(int(t, 2)) for t in arq.read().split())


def carregar_quadgrams(caminho):
    quad = {}
    total = 0
    with open(caminho) as arq:
        for linha in arq:
            p = linha.rstrip().split()
            if len(p) == 2:
                quad[p[0].upper()] = int(p[1])
                total += int(p[1])
    return quad, total


def criar_avaliador(quad, total, piso):
    def avaliar(texto):
        letras = "".join(c for c in texto.upper() if 'A' <= c <= 'Z')
        soma = 0.0
        for i in range(len(letras) - 3):
            g = letras[i:i + 4]
            v = quad.get(g)
            if v:
                soma += math.log10(v / total)
            else:
                soma += piso
        return soma
    return avaliar


def decifrar_com_chave(texto, chave):
    saida = []
    for c in texto:
        if 'A' <= c <= 'Z':
            saida.append(chave[ord(c) - ord('A')])
        else:
            saida.append(c)
    return "".join(saida)


def atacar(cifrado, avaliar, reinicios=20, iteracoes=1500, semente=1):
    random.seed(semente)
    melhor_score = None
    melhor_chave = None
    for _ in range(reinicios):
        chave = list(ALFA)
        random.shuffle(chave)
        atual_score = avaliar(decifrar_com_chave(cifrado, chave))
        for _ in range(iteracoes):
            a, b = random.sample(range(26), 2)
            chave[a], chave[b] = chave[b], chave[a]
            novo_score = avaliar(decifrar_com_chave(cifrado, chave))
            if novo_score > atual_score:
                atual_score = novo_score
            else:
                chave[a], chave[b] = chave[b], chave[a]
        if melhor_score is None or atual_score > melhor_score:
            melhor_score = atual_score
            melhor_chave = chave[:]
    return melhor_score, melhor_chave


def main():
    if len(sys.argv) < 2:
        print("Uso: python3 ataque_simples.py <arquivo_binario> [quadgrams.txt]")
        sys.exit(1)
    caminho = sys.argv[1]
    quad_path = sys.argv[2] if len(sys.argv) > 2 else "quadgrams.txt"
    if not os.path.exists(quad_path):
        quad_path = os.path.join(os.path.dirname(__file__), "quadgrams.txt")
    try:
        quad, total = carregar_quadgrams(quad_path)
        piso = math.log10(0.01 / total) if total > 0 else -20
        avaliar = criar_avaliador(quad, total, piso)
        cifrado = carregar_binario(caminho)
        score, chave = atacar(cifrado, avaliar)
        claro = decifrar_com_chave(cifrado, chave)
        print("Chave (cifrado -> claro):")
        print("  ", ALFA)
        print("  ", "".join(chave))
        nletras = sum(1 for c in claro.upper() if 'A' <= c <= 'Z')
        print(f"Score: {score:.1f}  ({score/nletras:.2f} por letra)")
        print("\nMensagem:\n")
        print(claro)
    except FileNotFoundError as e:
        print(f"Erro: arquivo não encontrado - {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == '__main__':
    main()
