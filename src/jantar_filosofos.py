import threading
import time
import random


class Filosofo(threading.Thread):
    
    def __init__(self, philosopher_id, talher_esquerdo, talher_direito, id_talher_esq, id_talher_dir, max_refeicoes=3):
     
        super().__init__()
        self.philosopher_id = philosopher_id
        self.talher_esquerdo = talher_esquerdo
        self.talher_direito = talher_direito
        self.id_talher_esq = id_talher_esq
        self.id_talher_dir = id_talher_dir
        self.refeicoes = 0
        self.max_refeicoes = max_refeicoes
        
    def pensar(self):
        tempo = random.uniform(0.1, 0.5)
        print(f"🤔 Filósofo {self.philosopher_id} está pensando... ({tempo:.2f}s)")
        time.sleep(tempo)
        
    def pegar_talheres(self):
        
        # Determina qual talher tem menor ID 
        if self.id_talher_esq < self.id_talher_dir:
            primeiro_talher = self.talher_esquerdo
            segundo_talher = self.talher_direito
            primeiro_id = self.id_talher_esq
            segundo_id = self.id_talher_dir
        else:
            primeiro_talher = self.talher_direito
            segundo_talher = self.talher_esquerdo
            primeiro_id = self.id_talher_dir
            segundo_id = self.id_talher_esq
        
        # Pega primeiro o talher de menor ID
        print(f"🍴 Filósofo {self.philosopher_id} tentando pegar talher {primeiro_id}...")
        primeiro_talher.acquire()
        print(f"✅ Filósofo {self.philosopher_id} pegou talher {primeiro_id}")
        
        # Pega depois o talher de maior ID
        print(f"🍴 Filósofo {self.philosopher_id} tentando pegar talher {segundo_id}...")
        segundo_talher.acquire()
        print(f"✅ Filósofo {self.philosopher_id} pegou talher {segundo_id}")
        
    def comer(self):
        tempo = random.uniform(0.2, 0.6)
        print(f"🍝 Filósofo {self.philosopher_id} está COMENDO (refeição {self.refeicoes + 1}/{self.max_refeicoes}) - {tempo:.2f}s")
        time.sleep(tempo)
        self.refeicoes += 1
        
    def devolver_talheres(self):
        print(f"🔄 Filósofo {self.philosopher_id} devolvendo talheres {self.id_talher_esq} e {self.id_talher_dir}")
        self.talher_esquerdo.release()
        self.talher_direito.release()
        print(f"✅ Filósofo {self.philosopher_id} devolveu os talheres")
        
    def run(self):
        print(f"👤 Filósofo {self.philosopher_id} sentou à mesa (talheres disponíveis: {self.id_talher_esq}, {self.id_talher_dir})")
        
        while self.refeicoes < self.max_refeicoes:
            self.pensar()
            self.pegar_talheres()
            try:
                self.comer()
            finally:
                # Garante que os talheres são devolvidos mesmo se houver erro
                self.devolver_talheres()
        
        print(f"🚪 Filósofo {self.philosopher_id} terminou {self.max_refeicoes} refeições e saiu da mesa")


def jantar_dos_filosofos():
    NUM_FILOSOFOS = 5
    
    print("=" * 80)
    print("🍽️  JANTAR DOS FILÓSOFOS - ALGORITMO DE DIJKSTRA")
    print("=" * 80)
    print(f"\n📋 Configuração:")
    print(f"   • Filósofos: {NUM_FILOSOFOS}")
    print(f"   • Talheres: {NUM_FILOSOFOS}")
    print(f"   • Refeições por filósofo: 3")
    print(f"\n🎯 Algoritmo: Dijkstra (Ordenação de Recursos)")
    print(f"   • Regra: Sempre pegar o talher de MENOR ID primeiro")
    print(f"   • Objetivo: Prevenir deadlock quebrando a circularidade\n")
    print("=" * 80 + "\n")
    
    # Cria os talheres (locks) numerados de 0 a 4
    talheres = [threading.Lock() for _ in range(NUM_FILOSOFOS)]
    
    # Cria os filósofos como threads
    # Filósofo i tem acesso aos talheres i e (i+1) % NUM_FILOSOFOS
    filosofos = []
    for i in range(NUM_FILOSOFOS):
        id_talher_esq = i
        id_talher_dir = (i + 1) % NUM_FILOSOFOS
        
        talher_esquerdo = talheres[id_talher_esq]
        talher_direito = talheres[id_talher_dir]
        
        filosofo = Filosofo(
            philosopher_id=i,
            talher_esquerdo=talher_esquerdo,
            talher_direito=talher_direito,
            id_talher_esq=id_talher_esq,
            id_talher_dir=id_talher_dir,
            max_refeicoes=3
        )
        filosofos.append(filosofo)
    
    # Inicia todas as threads dos filósofos
    inicio = time.time()
    for filosofo in filosofos:
        filosofo.start()
    
    # Aguarda todas as threads terminarem
    for filosofo in filosofos:
        filosofo.join()
    
    tempo_total = time.time() - inicio
    
    print("\n" + "=" * 80)
    print("✅ JANTAR DOS FILÓSOFOS FINALIZADO COM SUCESSO!")
    print("=" * 80)
    print(f"⏱️  Tempo total de execução: {tempo_total:.2f} segundos")
    print(f"📊 Total de refeições realizadas: {NUM_FILOSOFOS * 3}")
    print(f"🎉 Nenhum deadlock ocorreu - funcionou!")
    print("=" * 80)


if __name__ == "__main__":
    jantar_dos_filosofos()
