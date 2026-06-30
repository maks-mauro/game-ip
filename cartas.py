# arquivo cartas modificado para pygame - teste

import pygame

# Define a classe CartaComponente que herda de pygame.sprite.Sprite.
class CartaComponente(pygame.sprite.Sprite): 
    
    def __init__(self, nome, categoria, valor, descricao, cor, x=0, y=0):
        super().__init__()
        
        # Define os atributos lógicos da carta que serão usados na batalha.
        self.nome = nome
        self.categoria = categoria 
        self.valor = valor         
        self.descricao = descricao
        self.cor = cor

        # Cria uma superfície gráfica (um retângulo) para a carta com largura 150 e altura 220.
        self.image = pygame.Surface((150, 220))
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y) 
        self.image.fill(self.cor)


def resolver_magia(usuario, alvo, acao, forma, elemento, estado):
    combo = (acao, forma, elemento)
    msg = ""
    
    # --- COMBINAÇÕES DE ATAQUE ---
    if combo == ("ataque", "triangulo", "raio"):
        dano = max(0, 75 - alvo.defesa_atual)
        alvo.receber_dano(dano) 
        msg = f"{usuario.nome} usou Descarga elétrica! (-{dano} HP)"
    elif combo == ("ataque", "quadrado", "raio"):
        dano = max(0, 50 - alvo.defesa_atual)
        alvo.receber_dano(dano)
        msg = f"{usuario.nome} usou Matriz Estática! (-{dano} HP)"
    elif combo == ("ataque", "circulo", "raio"):
        dano = max(0, 30 - alvo.defesa_atual)
        alvo.receber_dano(dano)
        # Aplica a Paralisia no alvo. Durará 1 turno pulado.
        if alvo.imune_paralisia == 0: alvo.paralisia = 1
        msg = f"{usuario.nome} usou Zona De Alta-Tensão! (-{dano} HP, Paralisia)"

    elif combo == ("ataque", "triangulo", "metal"):
        dano = max(0, 60 - alvo.defesa_atual)
        alvo.receber_dano(dano)
        msg = f"{usuario.nome} usou Lança Imparável! (-{dano} HP)"
    elif combo == ("ataque", "quadrado", "metal"):
        dano = max(0, 40 - alvo.defesa_atual)
        alvo.receber_dano(dano)
        msg = f"{usuario.nome} usou Esmagamento de Aço! (-{dano} HP)"
    elif combo == ("ataque", "circulo", "metal"):
        dano = max(0, 25 - alvo.defesa_atual)
        alvo.receber_dano(dano)
        # Aplica Envenenamento. Este status agora causa dano e durará exatos 3 turnos.
        if alvo.imune_envenenamento == 0: alvo.envenenamento = 3
        msg = f"{usuario.nome} usou Chuva de estilhaços! (-{dano} HP, Envenenamento)"

    elif combo == ("ataque", "triangulo", "borracha"):
        dano = max(0, 50 - alvo.defesa_atual)
        alvo.receber_dano(dano)
        msg = f"{usuario.nome} usou Impacto Elástico! (-{dano} HP)"
    elif combo == ("ataque", "quadrado", "borracha"):
        dano = max(0, 35 - alvo.defesa_atual)
        alvo.receber_dano(dano)
        msg = f"{usuario.nome} usou Disparo Elástico! (-{dano} HP)"
    elif combo == ("ataque", "circulo", "borracha"):
        dano = max(0, 15 - alvo.defesa_atual)
        alvo.receber_dano(dano)
        alvo.lentidao = 3
        msg = f"{usuario.nome} usou Tempestade Ricochete! (-{dano} HP, Lentidão)"

    # --- COMBINAÇÕES DE DEFESA ---
    elif combo == ("defesa", "triangulo", "raio"):
        usuario.defesa_atual = 45 
        msg = f"{usuario.nome} usou Barreira de Luz! (+50 Defesa)"
    elif combo == ("defesa", "quadrado", "raio"):
        usuario.defesa_atual = 30
        msg = f"{usuario.nome} usou Grade Eletrostática! (+30 Defesa)"
    elif combo == ("defesa", "circulo", "raio"):
        usuario.defesa_atual = 15
        usuario.lentidao = 0
        msg = f"{usuario.nome} usou Corrente de Dispersão! (+15 Defesa, Cancela Lentidão)"
        
    elif combo == ("defesa", "triangulo", "metal"):
        usuario.defesa_atual = 70
        msg = f"{usuario.nome} usou Escudo intransponível! (+50 Defesa)"
    elif combo == ("defesa", "quadrado", "metal"):
        usuario.defesa_atual = 50
        msg = f"{usuario.nome} usou Muralha de Aço! (+30 Defesa)"
    elif combo == ("defesa", "circulo", "metal"):
        usuario.defesa_atual = 30
        usuario.imune_envenenamento = 3 
        msg = f"{usuario.nome} usou Grade de Isolamento! (+15 Defesa, imune a envenenamento por 3 turnos)"

    elif combo == ("defesa", "triangulo", "borracha"):
        usuario.defesa_atual = 55
        msg = f"{usuario.nome} usou Absorção de Impacto! (+50 Defesa)"
    elif combo == ("defesa", "quadrado", "borracha"):
        usuario.defesa_atual = 35
        msg = f"{usuario.nome} usou Barreira Elástica! (+30 Defesa)"
    elif combo == ("defesa", "circulo", "borracha"):
        usuario.defesa_atual = 20
        usuario.paralisia = 0 
        msg = f"{usuario.nome} usou Domo de borracha! (+15 Defesa, Cancela Paralisia)"

    # --- COMBINAÇÕES DE CURA ---
    elif combo == ("cura", "triangulo", "raio"):
        ganho = usuario.curar(45) 
        msg = f"{usuario.nome} usou Pulso Vital! (+{ganho} HP)"
    elif combo == ("cura", "quadrado", "raio"):
        ganho = usuario.curar(30)
        msg = f"{usuario.nome} usou Descarga Estática! (+{ganho} HP)"
    elif combo == ("cura", "circulo", "raio"):
        ganho = usuario.curar(15)
        usuario.imune_paralisia = 3 
        msg = f"{usuario.nome} usou Carga de Regeneração! (+{ganho} HP, Imune Paralisia)"

    elif combo == ("cura", "triangulo", "metal"):
        ganho = usuario.curar(50)
        msg = f"{usuario.nome} usou Toque de Restauro Metálico! (+{ganho} HP)"
    elif combo == ("cura", "quadrado", "metal"):
        ganho = usuario.curar(40)
        msg = f"{usuario.nome} usou Forja Celular! (+{ganho} HP)"
    elif combo == ("cura", "circulo", "metal"):
        ganho = usuario.curar(20)
        usuario.imune_envenenamento = 3 
        msg = f"{usuario.nome} usou Sutura de Mercúrio! (+{ganho} HP, Imune Envenenamento)"

    elif combo == ("cura", "triangulo", "borracha"):
        ganho = usuario.curar(70)
        msg = f"{usuario.nome} usou Retorno de Vitalidade! (+{ganho} HP)"
    elif combo == ("cura", "quadrado", "borracha"):
        ganho = usuario.curar(50)
        msg = f"{usuario.nome} usou fricção Curativa! (+{ganho} HP)"
    elif combo == ("cura", "circulo", "borracha"):
        ganho = usuario.curar(30)
        usuario.imune_envenenamento = 3 
        msg = f"{usuario.nome} usou Forma Restauradora! (+{ganho} HP, Imune Envenenamento)"

    alvo.defesa_atual = 0 
    
    return msg, True

# DECKS PARA CADA FASE
def obter_deck_acao():
    return [
        CartaComponente("Ataque", "acao", "ataque", "Inicia um ataque", (180, 50, 50)),
        CartaComponente("Defesa", "acao", "defesa", "Inicia uma defesa", (50, 50, 180)),
        CartaComponente("Utilitários", "acao", "utilitarios", "Aba de itens e curas", (50, 150, 50)),
        CartaComponente("Fuga", "fuga", "fuga", "Fugir imediatamente", (100, 100, 100))
    ]

def obter_deck_utilitarios():
    return [
        CartaComponente("Cura", "utilitario", "cura", "Magias de Cura", (50, 150, 50)),
        CartaComponente("Inventário", "utilitario", "inventario", "Abre inventário (em breve)", (150, 100, 50)),
        CartaComponente("Voltar", "voltar", "voltar", "Voltar etapa", (100, 100, 100))
    ]

def obter_deck_forma():
    return [
        CartaComponente("Triângulo", "forma", "triangulo", "Focado / 6 MP", (120, 50, 150)),
        CartaComponente("Quadrado", "forma", "quadrado", "Mediano / 4 MP", (120, 50, 150)),
        CartaComponente("Círculo", "forma", "circulo", "Área-Efeitos / 2 MP", (120, 50, 150)),
        CartaComponente("Voltar", "voltar", "voltar", "Voltar etapa", (100, 100, 100)) 
    ]

def obter_deck_elemento():
    return [
        CartaComponente("Raio", "elemento", "raio", "Alto Dano", (220, 80, 20)),
        CartaComponente("Metal", "elemento", "metal", "Alta Defesa", (200, 180, 20)),
        CartaComponente("Borracha", "elemento", "borracha", "Alta Cura", (20, 120, 220)),
        CartaComponente("Voltar", "voltar", "voltar", "Voltar etapa", (100, 100, 100)) 
    ]