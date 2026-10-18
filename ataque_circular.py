#!/usr/bin/env python3
"""
Ataque à cifra de substituição CIRCULAR (rotativa) usando quad-grams e hill-climbing.
Modelo: claro[k] = (F[cifrado[k]] - k) mod 26, k conta só letras.
Busca F (permutação fixa) e passo k adequado maximizando score.

Uso:
    python3 ataque_circular.py "Code 2" [quadgrams.txt]
"""

import math
import os
import random
import sys

ALFA = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
PASSOS = [1, 3, 5, 7, 9, 11, 15, 17, 19, 21, 23, 25]


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


def letras_e_valores(cifrado):
    idx = []
    valores = []
    for i, c in enumerate(cifrado):
        if 'A' <= c <= 'Z':
            idx.append(i)
            valores.append(ord(c) - ord('A'))
    return idx, valores


def criar_avaliador(quad, total, piso):
    def avaliar(seq_letras):
        soma = 0.0
        for i in range(len(seq_letras) - 3):
            g = seq_letras[i] + seq_letras[i + 1] + seq_letras[i + 2] + seq_letras[i + 3]
            v = quad.get(g)
            if v:
                soma += math.log10(v / total)
            else:
                soma += piso
        return soma
    return avaliar


def aplicar_com_F(cifrado, F, passo):
    idx, valores = letras_e_valores(cifrado)
    saida = list(cifrado)
    for k, pos in enumerate(idx):
        v = F[valores[k]]
        claro_v = (v - passo * k) % 26
        saida[pos] = chr(claro_v + ord('A'))
    return "".join(saida)


def quebrar_caso(cifrado, avaliar, passo, reinicios=4, iteracoes=3000, semente=7):
    random.seed(semente + passo)
    idx, valores = letras_e_valores(cifrado)
    n = len(valores)

    def avalia_seq(F):
        seq = []
        for k in range(n):
            v = F[valores[k]]
            cv = (v - passo * k) % 26
            seq.append(chr(cv + ord('A')))
        return avaliar(seq)

    melhor_score = None
    melhor_F = None
    for _ in range(reinicios):
        F = list(range(26))
        random.shuffle(F)
        atual = avalia_seq(F)
        for _ in range(iteracoes):
            a, b = random.sample(range(26), 2)
            F[a], F[b] = F[b], F[a]
            novo = avalia_seq(F)
            if novo > atual:
                atual = novo
            else:
                F[a], F[b] = F[b], F[a]
        if melhor_score is None or atual > melhor_score:
            melhor_score = atual
            melhor_F = F[:]
    return melhor_score, melhor_F


def main():
    if len(sys.argv) < 2:
        print("Uso: python3 ataque_circular.py <arquivo_binario> [quadgrams.txt]")
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
        nletras = sum(1 for c in cifrado.upper() if 'A' <= c <= 'Z')
        melhor_score = None
        melhor_passo = None
        melhor_F = None
        print("Testando passos de rotação (score por letra, maior melhor):")
        for passo in PASSOS:
            score, F = quebrar_caso(cifrado, avaliar, passo)
            por_letra = score / nletras if nletras else score
            print(f"  passo={passo:2d}  score={score:9.1f}  por letra={por_letra:.2f}")
            if melhor_score is None or score > melhor_score:
                melhor_score = score
                melhor_passo = passo
                melhor_F = F
        claro = aplicar_com_F(cifrado, melhor_F, melhor_passo)
        print(f"\nMelhor passo: {melhor_passo}")
        print("Alfabeto estático F (cifrado -> valor):")
        print("  ", ALFA)
        print("  ", "".join(ALFA[c] for c in melhor_F))
        print("\nMensagem:\n")
        print(claro)
    except FileNotFoundError as e:
        print(f"Erro: arquivo não encontrado - {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == '__main__':
    main()
