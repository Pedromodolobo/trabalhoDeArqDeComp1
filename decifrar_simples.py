#!/usr/bin/env python3
"""
Decifra cifra de substituição SIMPLES (homogênea) a partir de arquivo binário.
Arquivo: Code 1
Formato: tokens binários (ASCII) separados por espaços, '100000' representa espaço.

Uso:
    python3 decifrar_simples.py Code1
    (ou python3 decifrar_simples.py "Code 1")
"""

import sys

# Chave descoberta: cifrado -> claro
ALFA_CIF = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
ALFA_CLR = "DVHYZQFWRPLJSIEXMGCAUTOBKN"
MAPA = dict(zip(ALFA_CIF, ALFA_CLR))


def binario_para_char(token):
    return chr(int(token, 2))


def decifrar_char(c):
    if 'A' <= c <= 'Z':
        return MAPA.get(c, c)
    return c


def main():
    if len(sys.argv) < 2:
        nome = "Code 1"
    else:
        nome = sys.argv[1]
    try:
        with open(nome, 'r') as f:
            for linha in f:
                if not linha:
                    continue
                # divide por whitespace
                for token in linha.rstrip().split():
                    if not token:
                        continue
                    c = binario_para_char(token)
                    print(decifrar_char(c), end='')
            print()
    except FileNotFoundError:
        print(f"Erro: arquivo '{nome}' não encontrado.", file=sys.stderr)
        sys.exit(1)
    except ValueError:
        print(f"Erro: token binário inválido em '{nome}'.", file=sys.stderr)
        sys.exit(1)


if __name__ == '__main__':
    main()
