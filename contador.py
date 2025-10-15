

#include <pthread.h>
#include <stdio.h>
#include <stdlib.h>
#include <semaphore.h>
#include <math.h>
#include <time.h>

long long int *bufferCircular;
int indiceEntrada = 0;
int indiceSaida = 0;
int tamanhoBuffer;

sem_t semVazio;
sem_t semCheio;
sem_t semAcesso;

int *qtdPrimosConsumidor;
int numConsumidores;

//#define PRINT_THREAD_END  // 

int verificaPrimo(long long int numero) {
    if (numero <= 1) return 0;
    if (numero == 2) return 1;
    if (numero % 2 == 0) return 0;
    for (long long int j = 3; j * j <= numero; j += 2)
        if (numero % j == 0) return 0;
    return 1;
}

void *funcProdutor(void *arg) {
    long long int limite = (long long int) arg;

    for (int i = 1; i <= limite; i++) {
        sem_wait(&semVazio);
        sem_wait(&semAcesso);

        bufferCircular[indiceEntrada] = i;
        indiceEntrada = (indiceEntrada + 1) % tamanhoBuffer;

        sem_post(&semAcesso);
        sem_post(&semCheio);
    }

    // Insere sinais de término (-1) para cada consumidor
    for (int k = 0; k < numConsumidores; k++) {
        sem_wait(&semVazio);
        sem_wait(&semAcesso);

        bufferCircular[indiceEntrada] = -1;
        indiceEntrada = (indiceEntrada + 1) % tamanhoBuffer;

        sem_post(&semAcesso);
        sem_post(&semCheio);
    }

    pthread_exit(NULL);
}

void *funcConsumidor(void *arg) {
    long long int idConsumidor = (long long int) arg;
    int primosLocais = 0;

    while (1) {
        sem_wait(&semCheio);
        sem_wait(&semAcesso);

        long long int valor = bufferCircular[indiceSaida];
        indiceSaida = (indiceSaida + 1) % tamanhoBuffer;

        sem_post(&semAcesso);
        sem_post(&semVazio);

        if (valor == -1) break;
        if (verificaPrimo(valor))
            primosLocais++;
    }

    qtdPrimosConsumidor[idConsumidor] = primosLocais;

    #ifdef PRINT_THREAD_END
    printf("Consumidor %lld finalizou com %d primos.\n", idConsumidor + 1, primosLocais);
    #endif

    pthread_exit(NULL);
}

int main(int argc, char *argv[]) {
    if (argc < 4) {
        fprintf(stderr, "Uso: %s <N> <M> <C>\n", argv[0]);
        return 1;
    }

    long long int N = atoll(argv[1]);
    tamanhoBuffer = atoi(argv[2]);
    numConsumidores = atoi(argv[3]);

    bufferCircular = malloc(sizeof(long long int) * tamanhoBuffer);
    qtdPrimosConsumidor = calloc(numConsumidores, sizeof(int));

    sem_init(&semVazio, 0, tamanhoBuffer);
    sem_init(&semCheio, 0, 0);
    sem_init(&semAcesso, 0, 1);

    pthread_t threadProdutor;
    pthread_t *threadsConsumidor = malloc(sizeof(pthread_t) * numConsumidores);

    clock_t inicio = clock();

    pthread_create(&threadProdutor, NULL, funcProdutor, (void *) N);

    for (long long int i = 0; i < numConsumidores; i++) {
        pthread_create(&threadsConsumidor[i], NULL, funcConsumidor, (void *) i);
    }

    pthread_join(threadProdutor, NULL);
    for (long long int i = 0; i < numConsumidores; i++)
        pthread_join(threadsConsumidor[i], NULL);

    int totalPrimos = 0;
    int indiceVencedor = 0;
    for (long long int i = 0; i < numConsumidores; i++) {
        totalPrimos += qtdPrimosConsumidor[i];
        if (qtdPrimosConsumidor[i] > qtdPrimosConsumidor[indiceVencedor])
            indiceVencedor = i;
    }

    clock_t fim = clock();

    printf("Total de números primos encontrados: %d\n", totalPrimos);
    printf("Consumidor vencedor: %d\n", indiceVencedor + 1);
    printf("Tempo de execução: %.10f s\n", (double)(fim - inicio) / CLOCKS_PER_SEC);

    sem_destroy(&semVazio);
    sem_destroy(&semCheio);
    sem_destroy(&semAcesso);
    free(bufferCircular);
    free(qtdPrimosConsumidor);
    free(threadsConsumidor);

    return 0;
}
