#include <stdio.h>
#include <stdlib.h>

/*
 * Trabalho 1 - Arquitetura de Computadores
 *
 * Etapa 1: ler a mensagem binaria (codigo ASCII em binario) e
 *          converter cada token para o caractere correspondente.
 * Etapa 2: descriptografar a mensagem usando uma cifra de
 *          substituicao simples (mapeamento letra -> letra).
 *
 * Uso: ./substituicaoSimples "Code 1"
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
 * Tabela de descriptografia (substituicao simples).
 * A posicao 0 corresponde a 'A' do texto cifrado e assim por diante.
 *
 *   cifrado:  ABCDEFGHIJKLMNOPQRSTUVWXYZ
 *   claro  :  DVHYZQFWRPLJSIEXMGCAUTOBKN
 */
char decifrar(char c)
{
    static const char cifrado[] = "ABCDEFGHIJKLMNOPQRSTUVWXYZ";
    static const char claro[]   = "DVHYZQFWRPLJSIEXMGCAUTOBKN";

    for (int i = 0; cifrado[i] != '\0'; i++) {
        if (c == cifrado[i]) {
            return claro[i];
        }
    }

    return c; /* mantem espacos, pontuacao, etc. */
}

int main(int argc, char *argv[])
{
    const char *nomeArquivo = (argc > 1) ? argv[1] : "Code 1";
    FILE *arq = fopen(nomeArquivo, "r");

    if (arq == NULL) {
        fprintf(stderr, "Erro: nao foi possivel abrir \"%s\"\n", nomeArquivo);
        return 1;
    }

    char token[64];

    printf("Mensagem decifrada:\n\n");

    /* fscanf com "%63s" le apenas caracteres "nao brancos", ou seja,
       cada bloco de bits separado por espaco/quebra de linha. */
    while (fscanf(arq, "%63s", token) == 1) {
        char caractere = (char)binarioParaInt(token);
        putchar(decifrar(caractere));
    }

    putchar('\n');
    fclose(arq);
    return 0;
}
