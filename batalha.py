# arquivo de batalha em pygame - teste

from jogador import Personagem
from inimigos import CPU
# Importando novos decks (sem a necessidade de renderização aqui)
from cartas import obter_deck_acao, obter_deck_utilitarios, obter_deck_forma, obter_deck_elemento, resolver_magia

# PREPARAÇÃO PARA O INVENTÁRIO (Desabilitado até a criação do arquivo)
try:
    import inventario # Quando o arquivo inventario.py for criado, isso funcionará
    SISTEMA_INVENTARIO_ATIVO = True
except ImportError:
    SISTEMA_INVENTARIO_ATIVO = False

_ESPERA   = "espera"
_ANIMANDO = "animando"
_FIM      = "fim"

class Batalha:
    LOG_MAX   = 7 # quantidade maxima de mensagens na tela
    DELAY_FPS = 38 # Cria um intervalo de tempo, medido em quadros (frames), entre as ações automáticas de um turno.

    def __init__(self, nome_jogador): 
        # Os personagens nascem na posição 0,0 pois o arquivo render.py agora se encarrega de posicioná-los dinamicamente de acordo com a resolução.
        self.jogador   = Personagem(nome_jogador, x=0, y=0)
        self.cpu       = CPU(nome="Computador", x=0, y=0)
        self.log       = ["⚔️  Batalha iniciada!", "Escolha sua AÇÃO (Ataque, Defesa, Utilitários, Fuga)."]
        self.turno     = 1
        self.resultado = None
        self._estado   = _ESPERA
        self._fila     = []
        self._timer    = 0
        
        # Sistema de Fases Dinâmicas para suportar os menus de utilitários e submenus
        self.estado_menu = "acao" # Estados possíveis: "acao", "utilitarios", "forma", "elemento", "inventario"
        self.idx_carta = 0
        self.escolha_acao = None
        self.escolha_forma = None
        self.escolha_elemento = None
        self.custo_mp = {"triangulo": 6, "quadrado": 4, "circulo": 2}

    @property
    def aguardando_input(self):
        return self._estado == _ESPERA

    @property
    def encerrada(self):
        return self._estado == _FIM

    @property
    def deck_atual(self):
        # Decks agora mudam de forma dinâmica conforme a aba
        if self.estado_menu == "acao":
            return obter_deck_acao()
        elif self.estado_menu == "utilitarios":
            return obter_deck_utilitarios()
        elif self.estado_menu == "forma":
            return obter_deck_forma()
        elif self.estado_menu == "elemento":
            return obter_deck_elemento()
        # O retorno do deck do inventário será configurado futuramente aqui
        return []

    def input(self, acao):
        if self._estado != _ESPERA:
            return
        if acao == "esquerda":
            if self.deck_atual:
                self.idx_carta = (self.idx_carta - 1) % len(self.deck_atual)
        elif acao == "direita":
            if self.deck_atual:
                self.idx_carta = (self.idx_carta + 1) % len(self.deck_atual)
        elif acao == "usar":
            if self.deck_atual:
                self._processar_selecao(self.deck_atual[self.idx_carta])

    def _processar_selecao(self, carta):
        if carta.categoria == "fuga":
            self._encerrar("fuga")
            return
            
        if carta.categoria == "voltar":
            # Lógica para voltar as etapas de menus de Utilitários ou Forma
            if self.estado_menu == "utilitarios":
                self.estado_menu = "acao"
            elif self.estado_menu == "forma":
                if self.escolha_acao == "cura":
                    self.estado_menu = "utilitarios" # Volta pro sub-menu se veio da cura
                else:
                    self.estado_menu = "acao"
            elif self.estado_menu == "elemento":
                self.estado_menu = "forma"
            elif self.estado_menu == "inventario":
                self.estado_menu = "utilitarios" # Preparado para quando o inventário existir
            self.idx_carta = 0
            return

        if self.estado_menu == "acao":
            # Se usar Utilitários, redireciona o menu sem travar a Ação principal ainda
            if carta.valor == "utilitarios":
                self.estado_menu = "utilitarios"
            else:
                self.escolha_acao = carta.valor
                self.estado_menu = "forma"
            self.idx_carta = 0
            
        elif self.estado_menu == "utilitarios":
            # Tratamento do menu de Utilitários (Inventário e Cura) com suporte flexível
            if carta.valor == "inventario":
                if SISTEMA_INVENTARIO_ATIVO:
                    self.estado_menu = "inventario" # Vai para a nova fase se o arquivo existir
                else:
                    self._log("🎒 Arquivo inventario.py ainda não implementado!")
                    self.estado_menu = "acao" # Volta pro menu inicial sem consumir o turno
            elif carta.valor == "cura":
                self.escolha_acao = "cura" # Define a ação pra rodar o combo mágico depois
                self.estado_menu = "forma"
            self.idx_carta = 0

        elif self.estado_menu == "forma":
            custo = self.custo_mp[carta.valor]
            if self.jogador.mp < custo:
                self._log(f"MP Insuficiente! Requer {custo} MP. (Você tem {self.jogador.mp})")
            else:
                self.escolha_forma = carta.valor
                self.estado_menu = "elemento"
                self.idx_carta = 0
                
        elif self.estado_menu == "elemento":
            self.escolha_elemento = carta.valor
            self.jogador.mp -= self.custo_mp[self.escolha_forma]
            self._montar_turno()
            
        elif self.estado_menu == "inventario":
            # Espaço reservado para lidar com o uso de itens do inventário no futuro
            pass

    def tick(self):
        if self._estado != _ANIMANDO:
            return
        self._timer -= 1
        if self._timer <= 0:
            self._executar_proxima()

    def _montar_turno(self):
        self.jogador.defesa_atual = 0
        self.cpu.defesa_atual     = 0
        self.cpu.escolher_combo()
        self._fila = [
            ("efeitos",      self.jogador, None),
            ("efeitos",      self.cpu,     None),
            ("jogador_usa",  self.jogador, self.cpu),
            ("cpu_usa",      self.cpu,     self.jogador),
            ("fim_turno",    None,         None),
        ]
        self._estado = _ANIMANDO
        self._executar_proxima()

    def _executar_proxima(self):
        if not self._fila:
            return

        tipo, sujeito, alvo = self._fila.pop(0)
        estado_acao = {}

        if tipo == "efeitos":
            for msg in sujeito.processar_efeitos():
                self._log(msg)

        elif tipo == "jogador_usa":
            # A Paralisia atua não deixando o jogador agir e pulando o turno. É subtraída após agir seu efeito.
            if self.jogador.paralisia > 0:
                self._log(f"⚡ {self.jogador.nome} está paralisado e seu turno foi pulado!")
                self.jogador.paralisia -= 1 # Decai após pular o turno
            else:
                msg, _ = resolver_magia(self.jogador, self.cpu, self.escolha_acao, self.escolha_forma, self.escolha_elemento, estado_acao)
                self._log(msg)

        elif tipo == "cpu_usa":
            # CPU também tem o turno de ação pulado pela paralisia.
            if self.cpu.paralisia > 0:
                self._log(f"⚡ {self.cpu.nome} está paralisado e seu turno foi pulado!")
                self.cpu.paralisia -= 1 # Decai após pular o turno
            else:
                custo_cpu = self.custo_mp.get(self.cpu.escolha_forma, 0)
                if self.cpu.mp >= custo_cpu:
                    self.cpu.mp -= custo_cpu
                    msg, _ = resolver_magia(self.cpu, self.jogador, self.cpu.escolha_acao, self.cpu.escolha_forma, self.cpu.escolha_elemento, estado_acao)
                    self._log(f"[CPU] {msg}")
                else:
                    self._log(f"[CPU] {self.cpu.nome} tentou usar magia, mas estava sem MP!")

        elif tipo == "fim_turno":
            self.jogador.recuperar_mp(4)
            self.cpu.recuperar_mp(4)
            self.turno += 1
            self.estado_menu = "acao"
            self.idx_carta = 0
            
            if not self.jogador.vivo:
                self._encerrar("derrota"); return
            if not self.cpu.vivo:
                self._encerrar("vitoria"); return
                
            self._log(f"--- Turno {self.turno} Iniciado (+4 MP) ---")
            self._fila.clear()
            self._estado = _ESPERA
            return

        # Verifica morte imediata
        if tipo in ("jogador_usa", "cpu_usa", "efeitos"):
            if not self.jogador.vivo:
                self._encerrar("derrota"); return
            if not self.cpu.vivo:
                self._encerrar("vitoria"); return

        self._timer = self.DELAY_FPS if self._fila else 0
        if not self._fila:
            self._estado = _ESPERA

    def _encerrar(self, resultado):
        self.resultado = resultado
        self._log({
            "vitoria": "✦ VITÓRIA! Você derrotou o Chefão! ✦",
            "derrota": "✦ DERROTA! O Chefão venceu... ✦",
            "fuga":    "✦ Você fugiu da batalha. ✦",
        }[resultado])
        self._estado = _FIM

    def _log(self, msg):
        self.log.append(msg)
        if len(self.log) > self.LOG_MAX:
            self.log.pop(0)