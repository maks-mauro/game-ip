# arquivo render.py criado para separar a renderização de imagens - teste

import pygame
import sys
from batalha import Batalha

# Cores padrão importadas para a interface
COR_DESTAQUE = (255, 215, 0)
COR_TEXTO = (220, 220, 220)

def desenhar_carta(tela, carta, x, y, destacada, fonte_nome, fonte_desc):
    carta.rect.x = x
    carta.rect.y = y
    
    # Desenha o corpo da carta
    tela.blit(carta.image, carta.rect)
    
    # Renderiza o nome da carta
    texto_nome = fonte_nome.render(carta.nome, True, (255, 255, 255))
    tela.blit(texto_nome, (carta.rect.x + 10, carta.rect.y + 10))
    
    # Quebra de linhas para a descrição
    palavras = carta.descricao.split()
    linhas = []
    linha_atual = ""
    for p in palavras:
        if len(linha_atual) + len(p) < 18:
            linha_atual += p + " "
        else:
            linhas.append(linha_atual)
            linha_atual = p + " "
    linhas.append(linha_atual)

    # Desenha a descrição
    y_offset = 120
    for linha in linhas:
        texto_desc = fonte_desc.render(linha, True, (240, 240, 240))
        tela.blit(texto_desc, (carta.rect.x + 5, carta.rect.y + y_offset))
        y_offset += 20
        
    # Se a carta estiver selecionada, desenha a borda dourada nela
    if destacada:
        pygame.draw.rect(tela, COR_DESTAQUE, carta.rect, 4)

def desenhar_personagem(tela, personagem, fonte_status):
    # Desenha o personagem
    tela.blit(personagem.image, personagem.rect)
    
    # Pega a altura real da fonte para calcular um espaçamento perfeito
    altura_fonte = fonte_status.get_height()
    
    # Nome (Fica mais alto, 3.5 linhas acima do personagem)
    y_nome = personagem.rect.y - (altura_fonte * 3.5)
    texto_nome = fonte_status.render(personagem.nome, True, (255, 255, 255))
    tela.blit(texto_nome, (personagem.rect.x, y_nome))

    # Configurações das barras
    largura_barra = 60
    altura_barra = 12
    
    # Vida (HP) (Fica 2 linhas acima do personagem)
    cor_hp = (0, 255, 0) if personagem.hp_pct > 0.3 else (255, 0, 0)
    y_hp_barra = personagem.rect.y - (altura_fonte * 2)
    y_hp_texto = y_hp_barra - (altura_fonte // 4) # Ajuste fino para alinhar texto e barra
    
    pygame.draw.rect(tela, (255, 0, 0), (personagem.rect.x, y_hp_barra, largura_barra, altura_barra)) # Fundo
    pygame.draw.rect(tela, cor_hp, (personagem.rect.x, y_hp_barra, largura_barra * personagem.hp_pct, altura_barra)) # Vida atual

    texto_hp = fonte_status.render(f"HP: {personagem.hp}/{personagem.HP_MAX}", True, (255, 255, 255))
    tela.blit(texto_hp, (personagem.rect.x + largura_barra + 10, y_hp_texto))
    
    # Pontos Mágicos (MP) (Fica 1 linha acima do personagem)
    y_mp_barra = personagem.rect.y - altura_fonte
    y_mp_texto = y_mp_barra - (altura_fonte // 4)
    
    pygame.draw.rect(tela, (50, 50, 50), (personagem.rect.x, y_mp_barra, largura_barra, altura_barra)) # Fundo
    pygame.draw.rect(tela, (0, 150, 255), (personagem.rect.x, y_mp_barra, largura_barra * personagem.mp_pct, altura_barra)) # MP atual
    
    texto_mp = fonte_status.render(f"MP: {personagem.mp}", True, (255, 255, 255))
    tela.blit(texto_mp, (personagem.rect.x + largura_barra + 10, y_mp_texto))

    # Textos de Status (Ficam abaixo do personagem)
    texto_status = fonte_status.render(personagem.status_str(), True, (255, 255, 0))
    tela.blit(texto_status, (personagem.rect.x, personagem.rect.bottom + 5))

def renderizar_batalha(tela, batalha, largura, altura, fonte_log, fonte_carta):
    """Renderiza a cena completa da batalha, agregando todos os componentes visuais."""
    
    # Adaptação das posições dos personagens para serem dinâmicas (relativas à largura e altura atuais)
    batalha.jogador.rect.topleft = (largura * 0.20, altura * 0.40)
    batalha.cpu.rect.topleft = (largura * 0.75, altura * 0.40)

    # Desenha jogadores e HUDs
    desenhar_personagem(tela, batalha.jogador, fonte_log)
    desenhar_personagem(tela, batalha.cpu, fonte_log)

    # Desenha a Mão de Cartas
    if batalha.aguardando_input and batalha.deck_atual:
        # Espaçamento de cartas baseado na largura da tela
        espacamento = max(160, int(largura * 0.10))
        largura_carta = 150
        total_cartas = len(batalha.deck_atual)
        
        largura_total = (total_cartas - 1) * espacamento + largura_carta
        x_inicial = (largura - largura_total) // 2
        
        y_base = altura - 280
        y_selecionada = altura - 330
        
        # Desenha as não selecionadas por baixo
        for i, carta in enumerate(batalha.deck_atual):
            if i != batalha.idx_carta: 
                desenhar_carta(tela, carta, x_inicial + (i * espacamento), y_base, False, fonte_log, fonte_carta)
        
        # Desenha a selecionada destacada por cima
        if batalha.idx_carta < len(batalha.deck_atual):
            carta_atual = batalha.deck_atual[batalha.idx_carta]
            desenhar_carta(tela, carta_atual, x_inicial + (batalha.idx_carta * espacamento), y_selecionada, True, fonte_log, fonte_carta)

    # Textos da Interface alinhados de forma dinâmica
    texto_turno = fonte_log.render(f"Turno: {batalha.turno}", True, COR_DESTAQUE)
    tela.blit(texto_turno, ((largura // 2) - (texto_turno.get_width() // 2), 20))

    # Indicador dinâmico de estado de aba (Ação, Utilitários, Forma, Elemento, Inventário)
    if batalha.aguardando_input:
        if batalha.estado_menu == "inventario":
            fase_txt = "INVENTÁRIO (Pronto para implementação)"
        else:
            fase_txt = batalha.estado_menu.upper()
            
        texto_estado = fonte_log.render(f"Aba de {fase_txt}! (Setas escolher, ENTER usar)", True, (100, 255, 100))
    elif batalha.encerrada:
        texto_estado = fonte_log.render("Pressione ESC para sair", True, (255, 100, 100))
    else:
        texto_estado = fonte_log.render("Aguarde...", True, (200, 200, 200))
    tela.blit(texto_estado, (20, altura - 50))

    # Logs da batalha (centralizados no meio superior da tela dinamicamente)
    y_offset = altura * 0.12
    for i, msg in enumerate(batalha.log):
        opacidade = 255 if i == len(batalha.log) - 1 else 180
        surface_texto = fonte_log.render(msg, True, COR_TEXTO)
        surface_texto.set_alpha(opacidade)
        # Centralizando os logs com base na largura atual da janela
        tela.blit(surface_texto, ((largura // 2) - (surface_texto.get_width() // 2), y_offset))
        y_offset += 35


# CÓDIGO DE INTEGRAÇÃO COM O PYGAME FOI MOVIDO PARA CÁ
def iniciar_jogo():
    pygame.init()
    
    # Configurações de Tela adaptáveis
    # Iniciando com uma resolução razoável (1920x1080) mas com suporte a redimensionamento
    LARGURA_INICIAL, ALTURA_INICIAL = 1920, 1080
    tela = pygame.display.set_mode((LARGURA_INICIAL, ALTURA_INICIAL), pygame.RESIZABLE)
    pygame.display.set_caption("Batalha de Cartas Elementais")
    
    # Controle de FPS (Frames Por Segundo)
    relogio = pygame.time.Clock()
    FPS = 60 
    
    # Fontes e Cores
    try:
        fonte_log = pygame.font.SysFont("segoeuiemoji", 28) 
        fonte_carta_desc = pygame.font.SysFont("arial", 16)
    except:
        fonte_log = pygame.font.Font(None, 32)
        fonte_carta_desc = pygame.font.Font(None, 20)
        
    COR_FUNDO = (30, 30, 40)
    
    # Instancia a Batalha
    batalha = Batalha("Herói")

    rodando = True
    while rodando:
        # Pega as dimensões de forma responsiva a cada frame
        LARGURA, ALTURA = tela.get_size()
        
        # PROCESSAMENTO DE EVENTOS (Inputs)
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                rodando = False
            # Atualização no modo de janela se for redimensionada
            if evento.type == pygame.VIDEORESIZE:
                tela = pygame.display.set_mode((evento.w, evento.h), pygame.RESIZABLE)
            if evento.type == pygame.KEYDOWN:
                if batalha.aguardando_input:
                    if (evento.key == pygame.K_LEFT) or (evento.key == pygame.K_a):
                        batalha.input("esquerda")
                    elif (evento.key == pygame.K_RIGHT) or (evento.key == pygame.K_d):
                        batalha.input("direita")
                    elif evento.key in (pygame.K_RETURN, pygame.K_SPACE):
                        batalha.input("usar")
                elif batalha.encerrada:
                    if evento.key == pygame.K_ESCAPE:
                        rodando = False
        # ATUALIZAÇÃO DA LÓGICA (Tick)
        batalha.tick()
        # 3. RENDERIZAÇÃO
        tela.fill(COR_FUNDO)
        # Chama a função de renderização passando as dimensões atuais
        renderizar_batalha(tela, batalha, LARGURA, ALTURA, fonte_log, fonte_carta_desc)
        # Atualiza a janela
        pygame.display.flip()
        relogio.tick(FPS)
    pygame.quit()
    sys.exit()
if __name__ == "__main__":
    iniciar_jogo()