# 2025.2-2-4-Tarefas-Concorrencia-Problemas-Classicos

Atividade avaliativa do 2o bimestre - Implementar solução para o Problema do jantar dos filósofos em python com thread

## Descrição do Problema

O Problema do Jantar dos Filósofos é um problema clássico de concorrência que ilustra os desafios de sincronização entre múltiplos processos que competem por recursos compartilhados.

### Requisitos da Implementação

1. ✅ O processamento dos filósofos devem ser threads em 1 único processo
2. ✅ São 5 filósofos sentados à mesa
3. ✅ Antes de comer, o filósofo deve pegar 2 talheres
4. ✅ Após comer, o filósofo devolve os talheres à mesa
5. ✅ Como os palitos são compartilhados, 2 filósofos vizinhos não podem comer ao mesmo tempo
6. ✅ Os filósofos não conversam entre si, nem conhecem os estados uns dos outros
7. ✅ Não há um coordenador central

## Solução Implementada

A solução utiliza:
- **Threading**: Cada filósofo é uma thread independente
- **Locks (Mutex)**: Cada talher é representado por um `threading.Lock()` para sincronização
- **Estratégia Anti-Deadlock**: Filósofos pares pegam primeiro o talher esquerdo, filósofos ímpares pegam primeiro o talher direito

### Prevenção de Deadlock

A principal técnica para evitar deadlock é alternar a ordem de aquisição dos recursos:
- Filósofos com ID par (0, 2, 4) pegam primeiro o talher esquerdo
- Filósofos com ID ímpar (1, 3) pegam primeiro o talher direito

Isso quebra uma das condições necessárias para deadlock (espera circular), garantindo que sempre haverá pelo menos um filósofo que consegue pegar ambos os talheres.

## Como Executar

```bash
python3 jantar_filosofos.py
```

## Estrutura do Código

- `jantar_filosofos.py`: Implementação completa do problema
  - Classe `Filosofo`: Representa cada filósofo como uma thread
  - Função `jantar_dos_filosofos()`: Função principal que configura e executa a simulação

## Comportamento Observado

Cada filósofo executa o seguinte ciclo:
1. **Pensar**: Simula o tempo pensando (0.1-0.5 segundos)
2. **Pegar talheres**: Adquire os dois locks (talheres) necessários
3. **Comer**: Simula o tempo comendo (0.2-0.6 segundos)
4. **Devolver talheres**: Libera os dois locks (talheres)

O programa termina quando cada filósofo completou 3 refeições.

## Exemplo de Saída

```
==================================================
Iniciando o Jantar dos Filósofos
==================================================
Filósofo 0 sentou-se à mesa
Filósofo 0 está pensando...
Filósofo 1 sentou-se à mesa
...
Filósofo 0 pegou o primeiro talher
Filósofo 0 pegou o segundo talher
Filósofo 0 está comendo (refeição 1/3)
...
==================================================
Jantar dos Filósofos finalizado!
==================================================
```

## Conceitos de Concorrência Demonstrados

- **Exclusão Mútua**: Uso de locks para garantir acesso exclusivo aos recursos (talheres)
- **Sincronização**: Coordenação entre threads sem comunicação direta
- **Prevenção de Deadlock**: Técnica de ordenação de recursos
- **Condição de Corrida**: Evitada através do uso adequado de locks
