Arquivos
prime-count.c: O programa recebe três valores — N, M e C — como argumentos na execução. Ele conta quantos números primos existem até N de forma concorrente, seguindo o modelo produtor/consumidor, utilizando um buffer de tamanho M e C consumidores.

Como Compilar
Para compilar o programa, use o gcc no terminal com o comando:

gcc -o prime-count.exe prime-count.c -Wall -lm

Como Executar
Depois de compilar, execute o programa da seguinte forma:

./prime-count N M C

Onde:
N = limite máximo para verificar números primos
M = tamanho do buffer
C = número de consumidores

