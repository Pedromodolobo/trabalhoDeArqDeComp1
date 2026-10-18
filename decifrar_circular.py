#!/usr/bin/env python3
"""
Decifra cifra de substituição CIRCULAR (rotativa) a partir de arquivo binário.
Arquivo: Code 2
Modelo: alfabeto estático F + rotação k por letra (espaços não contam).
claro[k] = (F[cifrado[k]] - k) mod 26

Uso:
    python3 decifrar_circular.py Code2
    (ou python3 decifrar_circular.py "Code 2")
"""

import sys

# Alfabeto estático descoberto (cifrado -> valor)
TABELA = "RJVMNETKFDZXGWSLAUQOIHCPYB"  # A..Z -> índice 0..25


def binario_para_char(token):
    return chr(int(token, 2))


def decifrar_char(c, k):
    if 'A' <= c <= 'Z':
        valor = ord(TABELA[ord(c) - ord('A')]) - ord('A')
        claro = (valor - k) % 26
        return chr(claro + ord('A'))
    return c


def main():
    if len(sys.argv) < 2:
        nome = "Code 2"
    else:
        nome = sys.argv[1]
    try:
        k = 0  # conta apenas letras
        with open(nome, 'r') as f:
            for linha in f:
                if not linha:
                    continue
                for token in linha.rstrip().split():
                    if not token:
                        continue
                    c = binario_para_char(token)
                    if 'A' <= c <= 'Z':
                        print(decifrar_char(c, k), end='')
                        k += 1
                    else:
                        print(c, end='')
            print()
    except FileNotFoundError:
        print(f"Erro: arquivo '{nome}' não encontrado.", file=sys.stderr)
        sys.exit(1)
    except ValueError:
        print(f"Erro: token binário inválido em '{nome}'.", file=sys.stderr)
        sys.exit(1)


if __name__ == '__main__':
    main()
