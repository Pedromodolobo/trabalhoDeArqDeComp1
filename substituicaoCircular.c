#include <stdio.h>
#include <stdlib.h>

/*
 * Trabalho 1 - Arquitetura de Computadores
 * Exercicio 2: SUBSTITUICAO ROTATIVA ("circular")  ->  arquivo "Code 2"
 *
 * Etapa 1: ler a mensagem em binario (codigo ASCII em binario) e
 *          converter cada token para o caractere correspondente.
 * Etapa 2: descriptografar usando uma cifra de substituicao ROTATIVA.
 *
 * Modelo da cifra:
 *   Existe um alfabeto de substituicao fixo, mas ele gira uma casa a
 *   cada letra processada. Contando cada letra da mensagem a partir
 *   de 0 (espacos NAO contam), a k-esima letra cifrada e decifrada por:
 *
 *       claro = (TABELA[cifrado] - k) mod 26
 *
 *   onde TABELA[cifrado] e o valor estatico da substituicao.
 *
 *   Chave estatica descoberta (cifrado -> valor):
 *       A B C D E F G H I J K L M N O P Q R S T U V W X Y Z
 *       R J V M N E T K F D Z X G W S L A U Q O I H C P Y B
 *
 * Uso: ./substituicaoCircular "Code 2"
 */

/* Converte uma string de '0' e '1' para o valor inteiro (ASCII). */
int binarioParaInt(const char *bin)
{
    int valor = 0;

    for (int i = 0; bin[i] != '\0'; i++) {
        valor = valor * 2 + (bin[i] - '0');
    }

    return valor;
}

/*
 * Alfabeto de substituicao estatico.
 * Posicao 0 = 'A', posicao 1 = 'B', ..., posicao 25 = 'Z'.
 */
static const char TABELA[] = "RJVMNETKFDZXGWSLAUQOIHCPYB";

/* Decifra um caractere na posicao k (k conta apenas letras). */
char decifrar(char c, int k)
{
    if (c >= 'A' && c <= 'Z') {
        int valor = TABELA[c - 'A'] - 'A';
        int claro = (valor - k) % 26;

        if (claro < 0) {
            claro += 26;
        }

        return (char)(claro + 'A');
    }

    return c; /* mantem espacos e pontuacao */
}

int main(int argc, char *argv[])
{
    const char *nomeArquivo = (argc > 1) ? argv[1] : "Code 2";
    FILE *arq = fopen(nomeArquivo, "r");

    if (arq == NULL) {
        fprintf(stderr, "Erro: nao foi possivel abrir \"%s\"\n", nomeArquivo);
        return 1;
    }

    char token[64];
    int k = 0; /* indice da letra (rotacao), nao conta espacos */

    printf("Mensagem decifrada:\n\n");

    while (fscanf(arq, "%63s", token) == 1) {
        char caractere = (char)binarioParaInt(token);

        if (caractere >= 'A' && caractere <= 'Z') {
            putchar(decifrar(caractere, k));
            k++; /* so letras fazem o alfabeto girar */
        } else {
            putchar(caractere);
        }
    }

    putchar('\n');
    fclose(arq);
    return 0;
}
