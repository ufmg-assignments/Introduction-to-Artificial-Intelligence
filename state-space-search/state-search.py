import heapq
import sys

class Estado:
    
    def __init__(self, conf):
        
        self.configuracao = conf
        self.pai = None
        self.custo_total_avaliacao = 0
        self.custo_real = 0
        self.representacao = self.representar_configuracao()
        
    def representar_configuracao(self):
        
        representacao = ""
        for i in range(len(self.configuracao)-1):
            representacao += str(self.configuracao[i]) + " "
        representacao += str(self.configuracao[-1])
        
        return representacao
    
    def expandir_estado(self, modo):
        
        if modo == "real":
            r, h = 1, 0
        elif modo == "a_estrela":
            r, h = 1, 1
        elif modo == "guloso":
            r, h = 0, 1
        
        estados_possiveis = []
        
        for i in range(len(self.configuracao)):
            for j in range(i+1, len(self.configuracao)):
                if self.configuracao[j] < self.configuracao[i]:
                    
                    nova_configuracao = self.configuracao.copy()
                    nova_configuracao[j], nova_configuracao[i] = nova_configuracao[i], nova_configuracao[j]
                    novo_estado = Estado(nova_configuracao)
                    
                    if abs(j-i) == 1:
                        novo_estado.custo_total_avaliacao = r*(self.custo_real + 2) + h*novo_estado.calcular_heuristica()
                        novo_estado.custo_real = self.custo_real + 2
                        
                    else:
                        novo_estado.custo_total_avaliacao = r*(self.custo_real + 4) + h*novo_estado.calcular_heuristica()
                        novo_estado.custo_real = self.custo_real + 4
                    
                    estados_possiveis.append(novo_estado)
    
        return estados_possiveis
                
    def __lt__(self, outro_estado):
        
        return self.custo_total_avaliacao < outro_estado.custo_total_avaliacao
                
    def calcular_heuristica(self):
        
        heur = 0
        
        for i in range(len(self.configuracao)):
            if abs(self.configuracao[i] - (i+1)) ==1:
                heur += 2
            elif abs(self.configuracao[i] - (i+1)) > 1:
                heur += 4
                
        return heur
        
        
    def eh_solucao(self):
        
        for i in range(len(self.configuracao)-1):
            if self.configuracao[i+1] < self.configuracao[i]:
                return False
        
        return True
        
        
def bfs(configuracao_inicial):
    
    estado_inicial = Estado(configuracao_inicial)
    
    num_expandidos = 0
    caminho = ""
    
    if estado_inicial.eh_solucao():
        return 0, 0, estado_inicial.representacao
    
    fronteira = [estado_inicial]
    fronteira_repr = {estado_inicial.representacao}
    explorados = set()
    
    while len(fronteira) > 0:
        
        no_atual = fronteira.pop(0)
        explorados.add(no_atual.representacao)
        fronteira_repr.remove(no_atual.representacao)
        num_expandidos += 1
        
        for estado in no_atual.expandir_estado("real"):
            estado.pai = no_atual
            if estado.representacao not in explorados and estado.representacao not in fronteira_repr:
                if estado.eh_solucao():
                    no_aux = estado
                    while no_aux.pai != None:
                        caminho =  "\n" + no_aux.representacao + caminho
                        no_aux = no_aux.pai
                    caminho = no_aux.representacao + caminho
                        
                    return estado.custo_real, num_expandidos, caminho
                
                fronteira.append(estado)
                fronteira_repr.add(estado.representacao)
                
def ids(configuracao_inicial):

    num_expandidos = 0
    caminho = ""
    
    nivel_maximo = 0
    while True:

        estado_inicial = Estado(configuracao_inicial)
        stack = [(estado_inicial, 0)]
        explorados = set()
        
        while stack:
            estado, nivel = stack.pop()
            num_expandidos +=1
            
            if estado.eh_solucao():
                
                no_aux = estado
                while no_aux.pai != None:
                    caminho =  "\n" + no_aux.representacao + caminho
                    no_aux = no_aux.pai
                caminho = no_aux.representacao + caminho
                
                return estado.custo_real, num_expandidos, caminho
            
            elif nivel < nivel_maximo:
                nos_filhos = estado.expandir_estado("real")
                for filho in reversed(nos_filhos):
                    if filho.representacao not in explorados:
                        filho.pai = estado
                        stack.append((filho, nivel + 1))
                        explorados.add(filho.representacao)
        
        nivel_maximo +=1
        
        
def busca_geral(configuracao_inicial, modo):
    
    estado_inicial = Estado(configuracao_inicial)
    
    num_expandidos = 0
    caminho = ""
   
    fronteira = []
    fronteira_repr = {}
    explorados = set()
    
    heapq.heappush(fronteira, estado_inicial)
    fronteira_repr[estado_inicial.representacao] = estado_inicial
    
    while len(fronteira) > 0:
        
        no_atual = heapq.heappop(fronteira)
        del fronteira_repr[no_atual.representacao]
        
        if no_atual.eh_solucao():
            num_expandidos += 1
            
            no_aux = no_atual
            while no_aux.pai != None:
                caminho =  "\n" + no_aux.representacao + caminho
                no_aux = no_aux.pai
            caminho = no_aux.representacao + caminho
            
            
            return no_atual.custo_real, num_expandidos, caminho
        
        explorados.add(no_atual.representacao)
        num_expandidos += 1
        
        for estado in no_atual.expandir_estado(modo):
            
            rep = estado.representacao
            
            if rep not in explorados and rep not in fronteira_repr:
                estado.pai = no_atual
                heapq.heappush(fronteira, estado)
                fronteira_repr[rep] = estado
            elif rep in fronteira_repr: 
                if estado.custo_total_avaliacao < fronteira_repr[rep].custo_total_avaliacao:
                    fronteira_repr[rep].pai = no_atual
                    fronteira_repr[rep].custo_total_avaliacao = estado.custo_total_avaliacao
                    fronteira_repr[rep].custo_real = estado.custo_real
                    heapq.heapify(fronteira)
                    
if __name__ == "__main__":

    algoritmo = sys.argv[1]
    n = int(sys.argv[2])
    configuracao_inicial = [int(e) for e in sys.argv[3:n+3]]
    imprimir_vetores = "PRINT" == sys.argv[-1]

    if algoritmo == "B":
        custo, num_expansoes, caminho = bfs(configuracao_inicial)
    elif algoritmo == "I":
        custo, num_expansoes, caminho = ids(configuracao_inicial)
    elif algoritmo == "U":
        custo, num_expansoes, caminho = busca_geral(configuracao_inicial, "real")
    elif algoritmo == "A":
        custo, num_expansoes, caminho = busca_geral(configuracao_inicial, "a_estrela")
    elif algoritmo == "G":
        custo, num_expansoes, caminho = busca_geral(configuracao_inicial, "guloso")

    print(str(custo) + " " + str(num_expansoes))
                                                 
    if imprimir_vetores:
        print(caminho)
