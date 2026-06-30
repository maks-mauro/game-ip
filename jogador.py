# arquivo jogador modificado para a biblioteca pygame - teste

import pygame

class Personagem(pygame.sprite.Sprite): 
    HP_MAX      = 200
    MP_MAX      = 8 
    SPEED_BASE  = 50

    def __init__(self, nome, x, y): 
        super().__init__() 
        
        self.image = pygame.Surface((50, 80))
        self.image.fill((0, 128, 255)) 
        self.rect = self.image.get_rect() 
        self.rect.topleft = (x, y) 
        
        self.nome         = nome
        self.hp           = self.HP_MAX
        self.mp           = 4 
        self.speed        = self.SPEED_BASE
        self.defesa_atual = 0
        
        self.paralisia = 0
        self.envenenamento = 0
        self.lentidao = 0
        self.imune_paralisia = 0
        self.imune_envenenamento = 0

    @property 
    def vivo(self):  
        return self.hp > 0

    @property
    def hp_pct(self): 
        return self.hp / self.HP_MAX

    @property
    def mp_pct(self): 
        return self.mp / self.MP_MAX

    def receber_dano(self, dano): 
        self.hp = max(0, self.hp - dano)

    def curar(self, valor): 
        antes = self.hp
        self.hp = min(self.HP_MAX, self.hp + valor)
        return self.hp - antes
        
    def recuperar_mp(self, valor):
        self.mp = min(self.MP_MAX, self.mp + valor)

    def processar_efeitos(self): 
        msgs = []
        
        if self.envenenamento > 0:
            dano = 5
            self.receber_dano(dano)
            msgs.append(f"☠️ {self.nome} sofreu {dano} de dano por envenenamento!")
            self.envenenamento -= 1
            
            
        if self.lentidao > 0: self.lentidao -= 1
        if self.imune_paralisia > 0: self.imune_paralisia -= 1
        if self.imune_envenenamento > 0: self.imune_envenenamento -= 1
            
        return msgs

    def status_str(self): 
        status = []
        if self.paralisia > 0: status.append(f"Paralisado({self.paralisia})")
        if self.envenenamento > 0: status.append(f"Envenenado({self.envenenamento})")
        if self.lentidao > 0: status.append(f"Lento({self.lentidao})")
        if self.imune_paralisia > 0: status.append(f"ImuneRaio({self.imune_paralisia})")
        if self.imune_envenenamento > 0: status.append(f"ImuneMetal({self.imune_envenenamento})")
        return ", ".join(status) if status else "—" 

    def update(self):
        if not self.vivo:
            self.image.fill((100, 100, 100)) 

   