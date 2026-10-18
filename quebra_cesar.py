#!/usr/bin/env python3
"""
Quebra de cifra de Cesar por forca bruta, usando a metrica de quad-grams.

Uso:
    python3 quebra_cesar.py "Code 2" [quadgrams.txt]

A mensagem de entrada esta em binario (codigo ASCII em binario).
"""

import math
import sys
import os


def carregar_binario(caminho):
    """Le tokens binarios separados por espaco e devolve o texto (ASCII)."""
    with open(caminho) as arq:
        return "".join(chr(int(token, 2)) for token in arq.read().split())


def carregar_quadgrams(caminho):
    """Le a tabela 'QUAD count' e devolve (dicionario, total)."""
    quad = {}
    total = 0
    with open(caminho) as arq:
        for linha in arq:
            partes = linha.split()
            if len(partes) == 2:
                quad[partes[0]] = int(partes[1])
                total += int(partes[1])
    return quad, total


def pontuar(texto, quad, total, piso):
    """Soma de log10(P(quad-grama)); quanto maior, mais parecido com o idioma."""
    letras = "".join(c for c in texto.upper() if "A" <= c <= "Z")
    soma = 0.0
    for i in range(len(letras) - 3):
        grama = letras[i:i + 4]
        valor = quad.get(grama)
        soma += math.log10(valor / total) if valor else piso
    return soma


def deslocar(texto, k):
    """Aplica Cesar com deslocamento -k (decifra)."""
    saida = []
    for c in texto:
        if "A" <= c <= "Z":
            saida.append(chr((ord(c) - 65 - k) % 26 + 65))
        else:
            saida.append(c)
    return "".join(saida)


def main():
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)

    caminho = sys.argv[1]
    quad_path = sys.argv[2] if len(sys.argv) > 2 else "quadgrams.txt"
    if not os.path.exists(quad_path):
        quad_path = os.path.join(os.path.dirname(__file__), "quadgrams.txt")

    quad, total = carregar_quadgrams(quad_path)
    piso = math.log10(0.01 / total)
    cifrado = carregar_binario(caminho)

    resultados = []
    for k in range(26):
        claro = deslocar(cifrado, k)
        resultados.append((pontuar(claro, quad, total, piso), k, claro))
    resultados.sort(reverse=True)

    print("Ranking dos 26 deslocamentos (melhor primeiro):\n")
    for score, k, claro in resultados:
        print(f"  shift={k:2d}  score={score:9.1f}  {claro[:60]}")

    melhor_score, melhor_k, melhor = resultados[0]
    print("\nMelhor deslocamento:", melhor_k)
    print("Mensagem:", melhor)


if __name__ == "__main__":
    main()
