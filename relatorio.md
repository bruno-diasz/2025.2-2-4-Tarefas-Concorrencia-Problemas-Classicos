# Solução do Problema do Jantar dos Filósofos 

**Disciplina**: Sistemas Operacionais  
**Semestre**: 2025.2  
**Avaliação**: 4ª atividade avaliativa do bimestre  

---

## 1. Contexto Inicial do Trabalho (Introdução)

O Problema do Jantar dos Filósofos é um problema clássico de sincronização e concorrência em sistemas operacionais. Este problema ilustra de forma clara os desafios enfrentados ao gerenciar recursos compartilhados entre múltiplos processos ou threads concorrentes.

### 1.1 Descrição do Problema

O cenário consiste em:
- **5 filósofos** sentados ao redor de uma mesa redonda
- **5 talheres** dispostos na mesa, um entre cada par de filósofos adjacentes
- Cada filósofo alterna entre duas atividades: **pensar** e **comer**
- Para comer, um filósofo precisa de **dois talheres** simultaneamente (o da esquerda e o da direita)
- Após terminar de comer, o filósofo devolve ambos os talheres à mesa

### 1.2 Desafios do Problema

Os principais desafios de concorrência são:

1. **Deadlock (Impasse)**: Se todos os filósofos pegarem o talher da esquerda ao mesmo tempo, ninguém conseguirá pegar o talher da direita, resultando em um travamento permanente onde todos ficam esperando indefinidamente.

2. **Starvation (Inanição)**: Um filósofo pode ficar esperando por recursos indefinidamente enquanto outros filósofos conseguem comer repetidamente.

3. **Condição de Corrida**: Acesso concorrente aos mesmos recursos (talheres) pode levar a estados inconsistentes.

4. **Exclusão Mútua**: Garantir que dois filósofos vizinhos não tentem usar o mesmo talher ao mesmo tempo.

### 1.3 Objetivo do Trabalho

Implementar uma solução em Python utilizando threads que atenda aos seguintes requisitos:

- ✅ Processamento dos filósofos usando threads em um único processo
- ✅ 5 filósofos sentados à mesa
- ✅ Cada filósofo deve pegar 2 talheres antes de comer
- ✅ Após comer, devolver os talheres à mesa
- ✅ Filósofos vizinhos não podem comer simultaneamente
- ✅ Filósofos não se comunicam entre si
- ✅ Sem coordenador central

A solução deve **prevenir deadlock** e garantir que todos os filósofos consigam comer.

---

## 2. Descrevendo a Solução em Python para o Jantar dos Filósofos

### 2.1 Implementando o Algoritmo

#### 2.1.1 Qual o Algoritmo Utilizado

Foi utilizado o **Algoritmo de Dijkstra para Ordenação de Recursos** (Resource Hierarchy Solution).

**Princípio do Algoritmo:**

O algoritmo se baseia na técnica de **ordenação hierárquica de recursos**, onde:

1. **Numeração dos Recursos**: Cada talher recebe um identificador único (ID) de 0 a 4
2. **Regra de Aquisição Ordenada**: Cada filósofo deve **sempre** adquirir primeiro o talher com o **menor ID**, e só depois adquirir o talher com o **maior ID**
3. **Quebra da Circularidade**: Esta regra simples quebra a condição circular necessária para que ocorra deadlock

**Como funciona na prática:**

Considere a disposição dos filósofos e talheres:

```
        Talher 0
    F0          F4
Talher 1      Talher 4
    F1          F3
        F2
    Talher 2  Talher 3
```

- **Filósofo 0**: tem acesso aos talheres 0 e 1 → pega 0 primeiro, depois 1 ✅
- **Filósofo 1**: tem acesso aos talheres 1 e 2 → pega 1 primeiro, depois 2 ✅
- **Filósofo 2**: tem acesso aos talheres 2 e 3 → pega 2 primeiro, depois 3 ✅
- **Filósofo 3**: tem acesso aos talheres 3 e 4 → pega 3 primeiro, depois 4 ✅
- **Filósofo 4**: tem acesso aos talheres 4 e 0 → pega **0 primeiro**, depois 4 ✅ **(Quebra o ciclo!)**

**Por que funciona:**

A chave está no **Filósofo 4**. Ao invés de seguir a regra "pegar esquerda primeiro" (que seria o talher 4), ele segue a regra de Dijkstra e pega o talher 0 primeiro.

Isso significa que:
- Se todos os filósofos tentarem pegar seus talheres simultaneamente
- Os filósofos 0 e 4 vão **competir** pelo talher 0
- Um deles conseguirá (por exemplo, o Filósofo 0)
- O Filósofo 4 **ficará esperando**
- **NÃO forma um ciclo circular de espera** = **SEM DEADLOCK**

#### 2.1.2 Implementação do Algoritmo em Python

**Estrutura de Classes:**

```python
class Filosofo(threading.Thread):
    def __init__(self, philosopher_id, talher_esquerdo, talher_direito, 
                 id_talher_esq, id_talher_dir, max_refeicoes=3):
        # Cada filósofo é uma thread independente
        # Armazena os locks dos talheres E seus IDs numéricos
```

**Implementação do Algoritmo de Dijkstra:**

```python
def pegar_talheres(self):
    """
    Implementa o ALGORITMO DE DIJKSTRA
    """
    # Determina qual talher tem menor ID
    if self.id_talher_esq < self.id_talher_dir:
        primeiro_talher = self.talher_esquerdo
        segundo_talher = self.talher_direito
        primeiro_id = self.id_talher_esq
        segundo_id = self.id_talher_dir
    else:
        # Inverte a ordem: pega direito primeiro!
        primeiro_talher = self.talher_direito
        segundo_talher = self.talher_esquerdo
        primeiro_id = self.id_talher_dir
        segundo_id = self.id_talher_esq
    
    # Adquire locks na ordem: menor ID primeiro
    primeiro_talher.acquire()  # Bloqueia até conseguir
    segundo_talher.acquire()   # Bloqueia até conseguir
```

**Ciclo de Vida do Filósofo:**

```python
def run(self):
    while self.refeicoes < self.max_refeicoes:
        self.pensar()           # Tempo aleatório pensando
        self.pegar_talheres()   # Adquire locks (Dijkstra)
        try:
            self.comer()        # Tempo aleatório comendo
        finally:
            self.devolver_talheres()  # Libera locks sempre
```

**Uso de Locks (threading.Lock):**

- `Lock.acquire()`: Bloqueia até conseguir acesso exclusivo ao recurso
- `Lock.release()`: Libera o recurso para outros
- Garante **exclusão mútua** no acesso aos talheres

---

### 2.2 Tratando Impasse (Deadlock)

#### 2.2.1 Qual a Estratégia de Tratamento de Impasses

A estratégia utilizada é **PREVENÇÃO DE DEADLOCK** através da quebra de uma das quatro condições necessárias para deadlock (Condições de Coffman):

**As 4 Condições para Deadlock:**
1. ✅ Exclusão Mútua: Recursos não compartilháveis (talheres)
2. ✅ Posse e Espera: Filósofo segura um talher e espera outro
3. ✅ Não Preempção: Recursos não podem ser retirados à força
4. ❌ **Espera Circular**: ESTA É QUEBRADA PELO ALGORITMO

**Como o Algoritmo de Dijkstra quebra a Espera Circular:**

Sem ordenação (DEADLOCK possível):
```
F0 → talher 0 → espera talher 1
F1 → talher 1 → espera talher 2
F2 → talher 2 → espera talher 3
F3 → talher 3 → espera talher 4
F4 → talher 4 → espera talher 0  ← CICLO FECHADO!
```

Com ordenação de Dijkstra (SEM DEADLOCK):
```
F0 → talher 0 → espera talher 1
F1 → talher 1 → espera talher 2
F2 → talher 2 → espera talher 3
F3 → talher 3 → espera talher 4
F4 → espera talher 0 → (sem talher 4!)  ← CICLO QUEBRADO!
```

O Filósofo 4 **não segura o talher 4** enquanto espera o talher 0, quebrando a circularidade.

#### 2.2.2 Implementação do Tratamento de Impasse em Python

**1. Numeração dos Recursos:**

```python
# Cria talheres numerados de 0 a 4
talheres = [threading.Lock() for _ in range(5)]

for i in range(5):
    id_talher_esq = i
    id_talher_dir = (i + 1) % 5  # Circular: 0,1,2,3,4,0...
```

**2. Ordenação na Aquisição:**

```python
def pegar_talheres(self):
    # Comparação: qual ID é menor?
    if self.id_talher_esq < self.id_talher_dir:
        # Ordem natural: esquerda -> direita
        primeiro_talher = self.talher_esquerdo
        segundo_talher = self.talher_direito
    else:
        # Ordem invertida: direita -> esquerda
        # Isso acontece APENAS para o Filósofo 4!
        primeiro_talher = self.talher_direito
        segundo_talher = self.talher_esquerdo
    
    # Sempre adquire na ordem: menor ID primeiro
    primeiro_talher.acquire()
    segundo_talher.acquire()
```

**3. Garantia de Liberação (try/finally):**

```python
def run(self):
    self.pegar_talheres()
    try:
        self.comer()
    finally:
        # SEMPRE libera os talheres, mesmo se houver exceção
        self.devolver_talheres()
```

O `finally` garante que os recursos são liberados mesmo em caso de erro, evitando **resource leaks**.

---

## 3. Executar o Código e Descrever Comportamento Observado

### 3.1 Comando de Execução

```bash
python3 src/jantar_filosofos.py
```

### 3.2 Saída Esperada

```
================================================================================
🍽️  JANTAR DOS FILÓSOFOS - ALGORITMO DE DIJKSTRA
================================================================================

📋 Configuração:
   • Filósofos: 5
   • Talheres: 5
   • Refeições por filósofo: 3

🎯 Algoritmo: Dijkstra (Ordenação de Recursos)
   • Regra: Sempre pegar o talher de MENOR ID primeiro
   • Objetivo: Prevenir deadlock quebrando a circularidade

================================================================================

👤 Filósofo 0 sentou à mesa (talheres disponíveis: 0, 1)
👤 Filósofo 1 sentou à mesa (talheres disponíveis: 1, 2)
👤 Filósofo 2 sentou à mesa (talheres disponíveis: 2, 3)
👤 Filósofo 3 sentou à mesa (talheres disponíveis: 3, 4)
👤 Filósofo 4 sentou à mesa (talheres disponíveis: 4, 0)
🤔 Filósofo 0 está pensando... (0.32s)
🤔 Filósofo 2 está pensando... (0.15s)
🤔 Filósofo 1 está pensando... (0.41s)
🤔 Filósofo 4 está pensando... (0.28s)
🤔 Filósofo 3 está pensando... (0.19s)
🍴 Filósofo 2 tentando pegar talher 2...
✅ Filósofo 2 pegou talher 2
🍴 Filósofo 2 tentando pegar talher 3...
✅ Filósofo 2 pegou talher 3
🍝 Filósofo 2 está COMENDO (refeição 1/3) - 0.54s
🍴 Filósofo 3 tentando pegar talher 3...
🍴 Filósofo 4 tentando pegar talher 0...
✅ Filósofo 4 pegou talher 0
🍴 Filósofo 4 tentando pegar talher 4...
✅ Filósofo 4 pegou talher 4
🍝 Filósofo 4 está COMENDO (refeição 1/3) - 0.59s
🍴 Filósofo 0 tentando pegar talher 0...
🔄 Filósofo 2 devolvendo talheres 2 e 3
✅ Filósofo 2 devolveu os talheres
✅ Filósofo 3 pegou talher 3
🍴 Filósofo 3 tentando pegar talher 4...
...
(output continua até todos comerem 3 vezes)
...

================================================================================
✅ JANTAR DOS FILÓSOFOS FINALIZADO COM SUCESSO!
================================================================================
⏱️  Tempo total de execução: 12.45 segundos
📊 Total de refeições realizadas: 15
🎉 Nenhum deadlock ocorreu - Algoritmo de Dijkstra funcionou!
================================================================================
```

### 3.3 Comportamento Observado

**Pontos Importantes Observados:**

1. **Threads Concorrentes**: 
   - Todos os 5 filósofos iniciam pensando simultaneamente
   - Os tempos são aleatórios, simulando comportamento real
   - A ordem de execução varia a cada execução

2. **Aquisição Ordenada de Recursos**:
   - Filósofo 4 **sempre** tenta pegar o talher 0 primeiro (menor ID)
   - Isso pode criar espera, mas **nunca deadlock**
   - Outros filósofos pegam em ordem natural (0→1, 1→2, etc.)

3. **Concorrência Visível**:
   - Enquanto um filósofo come, outros pensam ou esperam
   - Filósofos vizinhos **nunca** comem simultaneamente (exclusão mútua funciona)
   - Talheres são compartilhados sem conflitos

4. **Ausência de Deadlock**:
   - Em todas as execuções, o programa termina com sucesso
   - Todos os filósofos completam suas 3 refeições
   - Tempo total varia (10-15 segundos tipicamente) devido à aleatoriedade

5. **Garantia de Progresso**:
   - Nenhum filósofo fica bloqueado indefinidamente (sem starvation)
   - O `try/finally` garante que talheres são sempre liberados

---

## 4. Considerações Finais

### 4.1 Eficácia da Solução

A implementação do Algoritmo de Dijkstra para o Problema do Jantar dos Filósofos demonstrou ser **extremamente eficaz** na prevenção de deadlock. Durante todos os testes realizados, nenhum caso de impasse foi observado, e todos os filósofos conseguiram completar suas refeições com sucesso.

### 4.2 Vantagens do Algoritmo

1. **Simplicidade**: A regra de ordenação é simples e fácil de implementar
2. **Determinístico**: Sempre funciona, não depende de sorte ou timing
3. **Sem Coordenação Central**: Cada filósofo toma decisões independentemente
4. **Eficiente**: Não há overhead significativo de sincronização adicional

### 4.3 Desvantagens e Limitações

1. **Escalabilidade**: Requer conhecimento prévio de todos os recursos (numeração)
2. **Rigidez**: Todos os processos devem seguir a mesma regra de ordenação
3. **Desempenho**: Pode haver alguma perda de paralelismo (ex: Filósofo 4 esperando mais)

### 4.4 Conceitos de Sistemas Operacionais Demonstrados

Este trabalho permitiu explorar praticamente diversos conceitos fundamentais:

- **Threads e Concorrência**: Múltiplas threads executando simultaneamente
- **Locks e Exclusão Mútua**: Uso de `threading.Lock()` para proteger recursos
- **Sincronização**: Coordenação entre threads sem comunicação direta
- **Deadlock**: Compreensão das condições e técnicas de prevenção
- **Condições de Coffman**: Identificação e quebra de condições necessárias
- **Resource Ordering**: Técnica prática de prevenção de deadlock

### 4.5 Aprendizados

A implementação prática deste problema clássico proporcionou uma compreensão profunda de como problemas de sincronização podem ser resolvidos através de algoritmos elegantes e simples. O Algoritmo de Dijkstra demonstra que, muitas vezes, a solução para problemas complexos de concorrência está em estabelecer regras simples e consistentes que quebram as condições necessárias para situações indesejadas como deadlock.

### 4.6 Aplicações no Mundo Real

Este tipo de problema e solução é fundamental em:
- Sistemas de gerenciamento de banco de dados (lock ordering)
- Sistemas operacionais modernos (alocação de recursos)
- Aplicações multithread (sincronização de acesso)
- Sistemas distribuídos (coordenação de processos)

---

**Referências:**

- Dijkstra, E. W. (1965). "Solution of a problem in concurrent programming control"
- Tanenbaum, A. S. "Modern Operating Systems"
- Silberschatz, Galvin, Gagne. "Operating System Concepts"
