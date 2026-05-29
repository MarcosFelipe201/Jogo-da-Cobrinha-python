import pygame
import random
import sys
import math

pygame.init()
pygame.mixer.init(frequency=44100, size=-16, channels=1, buffer=512)

#  TEMAS VISUAIS
TEMAS = {
    "Selva": {
        "fundo":         (15,  35,  15),
        "grade":         (25,  55,  25),
        "parede":        (150, 255, 50),
        "parede_brilho": (200, 255, 100),
        "cobra":         (0,  255, 128),
        "cobra_sombra":  (0,  150,  80),
        "cobra_brilho":  (150, 255, 200),
        "pontos":        (255, 100, 200),
    },
    "Noite": {
        "fundo":         (20,   0,  40),
        "grade":         (40,   0,  70),
        "parede":        (0,  255, 255),
        "parede_brilho": (150, 255, 255),
        "cobra":         (255,  0, 255),
        "cobra_sombra":  (150,  0, 150),
        "cobra_brilho":  (255, 150, 255),
        "pontos":        (0,  255, 150),
    },
    "Deserto": {
        "fundo":         (60,  10,  10),
        "grade":         (80,  20,  20),
        "parede":        (255, 100,  0),
        "parede_brilho": (255, 150, 50),
        "cobra":         (255,  50,  0),
        "cobra_sombra":  (150,  20,  0),
        "cobra_brilho":  (255, 120, 80),
        "pontos":        (255, 200,  0),
    },
    "Gelo": {
        "fundo":         (0,   20,  60),
        "grade":         (10,  40,  90),
        "parede":        (100, 255, 200),
        "parede_brilho": (180, 255, 230),
        "cobra":         (50, 150, 255),
        "cobra_sombra":  (20,  80, 180),
        "cobra_brilho":  (150, 200, 255),
        "pontos":        (255, 255, 255),
    },
}

#  PERSONAGENS
PERSONAGENS = ["Cobra", "Lagarta", "Dragão", "Alien"]

#  DIFICULDADES
DIFICULDADES = {
    "Fácil":   {"velocidade": 8,  "obstaculos": 0},
    "Médio":   {"velocidade": 12, "obstaculos": 3},
    "Difícil": {"velocidade": 17, "obstaculos": 6},
    "Insano":  {"velocidade": 24, "obstaculos": 10},
}

#  JANELA / CONSTANTES
ESPESSURA_PAREDE = 10
LARGURA          = 640
ALTURA           = 480
TAMANHO_BLOCO    = 20

AREA_X1      = ESPESSURA_PAREDE
AREA_Y1      = ESPESSURA_PAREDE
AREA_X2      = LARGURA - ESPESSURA_PAREDE
AREA_Y2      = ALTURA  - ESPESSURA_PAREDE
AREA_LARGURA = AREA_X2 - AREA_X1
AREA_ALTURA  = AREA_Y2 - AREA_Y1

tela    = pygame.display.set_mode((LARGURA, ALTURA))
relogio = pygame.time.Clock()
pygame.display.set_caption("🐍 Cobrinha Supreme")

fonte_titulo = pygame.font.SysFont("bahnschrift", 48, bold=True)
fonte_grande = pygame.font.SysFont("bahnschrift", 32, bold=True)
fonte_media  = pygame.font.SysFont("bahnschrift", 22)
fonte_pequena= pygame.font.SysFont("bahnschrift", 17)

#  IMAGENS (cabeças dos personagens desenhadas em pygame)
def criar_cabeca(personagem, cor_cobra, cor_sombra):
    surf = pygame.Surface((TAMANHO_BLOCO, TAMANHO_BLOCO), pygame.SRCALPHA)
    B = TAMANHO_BLOCO
    cx, cy = B // 2, B // 2

    if personagem == "Lagarta":
        pygame.draw.circle(surf, cor_sombra, (cx, cy), B//2)
        pygame.draw.circle(surf, (150, 50, 200), (cx, cy), B//2 - 2)
        pygame.draw.circle(surf, (255,255,255), (cx-3, cy-3), 2)
        pygame.draw.circle(surf, (255,255,255), (cx+3, cy-3), 2)
        pygame.draw.line(surf, (255,100,255), (cx-3, 1), (cx-5, -2), 1)
        pygame.draw.line(surf, (255,100,255), (cx+3, 1), (cx+5, -2), 1)

    elif personagem == "Dragão":
        pts = [(cx, 0), (B, cy+4), (cx+2, B), (cx-2, B), (0, cy+4)]
        pygame.draw.polygon(surf, cor_sombra, pts)
        pts2 = [(cx, 2), (B-2, cy+4), (cx+1, B-2), (cx-1, B-2), (2, cy+4)]
        pygame.draw.polygon(surf, (100, 255, 100), pts2)
        pygame.draw.circle(surf, (255,0,0), (cx-3, cy-1), 2)
        pygame.draw.circle(surf, (255,0,0), (cx+3, cy-1), 2)

    elif personagem == "Alien":
        pygame.draw.rect(surf, cor_sombra, (1, 3, B-2, B-4), border_radius=4)
        pygame.draw.rect(surf, (255, 50, 50), (2, 4, B-4, B-6), border_radius=3)
        for ex, ey in [(3,6),(B-5,6),(cx-1,5)]:
            pygame.draw.circle(surf, (0,255,255), (ex, ey), 2)
        for ax in [2, 5, B-6, B-3]:
            pygame.draw.line(surf, (200,0,50), (ax, B-4), (ax, B), 1)

    else:  # Cobra padrão
        pygame.draw.circle(surf, cor_sombra, (cx, cy), B//2)
        pygame.draw.circle(surf, cor_cobra, (cx, cy), B//2 - 2)
        pygame.draw.circle(surf, (0,0,0), (cx-3, cy-2), 3)
        pygame.draw.circle(surf, (0,0,0), (cx+3, cy-2), 3)
        pygame.draw.circle(surf, (255,0,0), (cx-3, cy-2), 1)
        pygame.draw.circle(surf, (255,0,0), (cx+3, cy-2), 1)
        pygame.draw.line(surf, (50,220,50), (cx, cy+3), (cx+3, cy+5), 2)

    return surf

def criar_comida():
    surf = pygame.Surface((TAMANHO_BLOCO, TAMANHO_BLOCO), pygame.SRCALPHA)
    B = TAMANHO_BLOCO
    pygame.draw.circle(surf, (100, 0, 200), (B//2, B//2+1), B//2-1)
    pygame.draw.circle(surf, (150, 50, 255), (B//2-2, B//2-2), B//4)
    pygame.draw.line(surf, (0, 255, 255), (B//2+1, 2), (B//2+3, -1), 2)
    return surf

#  SOM PROCEDURAL
import numpy as np

def gerar_som(freq=440, duracao=0.08, volume=0.3, forma="square"):
    sample_rate = 44100
    n = int(sample_rate * duracao)
    t = np.linspace(0, duracao, n, False)
    if forma == "square":
        onda = np.sign(np.sin(2 * np.pi * freq * t))
    elif forma == "triangle":
        onda = 2 * np.abs(2 * (t * freq - np.floor(t * freq + 0.5))) - 1
    else:
        onda = np.sin(2 * np.pi * freq * t)
    fade = np.linspace(1, 0, n)
    onda = (onda * fade * volume * 32767).astype(np.int16)
    stereo = np.column_stack([onda, onda])
    return pygame.sndarray.make_sound(stereo)

try:
    SOM_COMER   = gerar_som(freq=800, duracao=0.15, volume=0.4, forma="triangle")
    SOM_MORTE   = gerar_som(freq=100, duracao=0.45, volume=0.6, forma="square")
    SOM_NIVEL   = gerar_som(freq=1200, duracao=0.30, volume=0.4, forma="sine")
    SONS_OK     = True
except Exception:
    SONS_OK = False

def tocar(som):
    if SONS_OK:
        try: som.play()
        except: pass

#  PARTÍCULAS
particulas = []

def adicionar_particulas(x, y, cor):
    for _ in range(15):
        angulo = random.uniform(0, 2*math.pi)
        vel    = random.uniform(2, 6)
        particulas.append({
            "x": x + TAMANHO_BLOCO//2,
            "y": y + TAMANHO_BLOCO//2,
            "vx": math.cos(angulo)*vel,
            "vy": math.sin(angulo)*vel,
            "vida": 30,
            "cor": cor,
            "raio": random.randint(3, 7),
        })

def atualizar_particulas():
    mortas = []
    for p in particulas:
        p["x"]    += p["vx"]
        p["y"]    += p["vy"]
        p["vida"] -= 1
        p["vy"]   += 0.05
        alpha = int(255 * p["vida"] / 30)
        r,g,b = p["cor"]
        pygame.draw.circle(tela, (min(r,255),min(g,255),min(b,255)),
                           (int(p["x"]), int(p["y"])), p["raio"])
        if p["vida"] <= 0:
            mortas.append(p)
    for p in mortas:
        particulas.remove(p)

#  RECORDES (em memória)
recordes = {d: 0 for d in DIFICULDADES}

#  FUNÇÕES AUXILIARES DE DESENHO
def desenhar_grade(tema):
    for x in range(AREA_X1, AREA_X2, TAMANHO_BLOCO):
        pygame.draw.line(tela, tema["grade"], (x, AREA_Y1), (x, AREA_Y2))
    for y in range(AREA_Y1, AREA_Y2, TAMANHO_BLOCO):
        pygame.draw.line(tela, tema["grade"], (AREA_X1, y), (AREA_X2, y))

def desenhar_paredes(tema):
    EP = ESPESSURA_PAREDE
    pygame.draw.rect(tela, tema["parede"], (0, 0, LARGURA, EP))
    pygame.draw.rect(tela, tema["parede"], (0, ALTURA-EP, LARGURA, EP))
    pygame.draw.rect(tela, tema["parede"], (0, 0, EP, ALTURA))
    pygame.draw.rect(tela, tema["parede"], (LARGURA-EP, 0, EP, ALTURA))
    pygame.draw.rect(tela, tema["parede_brilho"], (0, 0, LARGURA, EP), 2)
    pygame.draw.rect(tela, tema["parede_brilho"], (0, ALTURA-EP, LARGURA, EP), 2)
    pygame.draw.rect(tela, tema["parede_brilho"], (0, 0, EP, ALTURA), 2)
    pygame.draw.rect(tela, tema["parede_brilho"], (LARGURA-EP, 0, EP, ALTURA), 2)

def desenhar_obstaculos(obstaculos, tema):
    for ox, oy in obstaculos:
        pygame.draw.rect(tela, tema["parede"], (ox, oy, TAMANHO_BLOCO, TAMANHO_BLOCO), border_radius=3)
        pygame.draw.rect(tela, tema["parede_brilho"], (ox, oy, TAMANHO_BLOCO, TAMANHO_BLOCO), 2, border_radius=3)

def desenhar_segmento(x, y, tema):
    cx = x + TAMANHO_BLOCO // 2
    cy = y + TAMANHO_BLOCO // 2
    r  = TAMANHO_BLOCO // 2
    pygame.draw.circle(tela, tema["cobra_sombra"], (cx, cy), r)
    pygame.draw.circle(tela, tema["cobra"],        (cx, cy), r-2)
    pygame.draw.circle(tela, tema["cobra_brilho"], (cx-2, cy-2), max(2, r//3))

def desenhar_cobra(lista_cobra, direcao, img_cabeca, tema):
    for bloco in lista_cobra[:-1]:
        desenhar_segmento(bloco[0], bloco[1], tema)
    if lista_cobra:
        cab = lista_cobra[-1]
        angulos = {"direita":0, "esquerda":180, "cima":270, "baixo":90}
        img_rot = pygame.transform.rotate(img_cabeca, angulos.get(direcao, 0))
        tela.blit(img_rot, [cab[0], cab[1]])

def texto_centro(msg, cor, y, fonte=None):
    f = fonte or fonte_media
    s = f.render(msg, True, cor)
    r = s.get_rect(center=(LARGURA//2, y))
    tela.blit(s, r)

def caixa_opcao(rect, texto, selecionado, cor_sel, cor_text):
    cor_fundo = cor_sel if selecionado else (50, 50, 50)
    cor_borda = cor_sel if selecionado else (100, 100, 100)
    pygame.draw.rect(tela, cor_fundo, rect, border_radius=8)
    pygame.draw.rect(tela, cor_borda, rect, 2, border_radius=8)
    s = fonte_media.render(texto, True, cor_text if selecionado else (200,200,200))
    r = s.get_rect(center=rect.center)
    tela.blit(s, r)

#  MENU PRINCIPAL
def menu_principal():
    tema_idx        = 0
    personagem_idx  = 0
    dificuldade_idx = 1
    nomes_temas     = list(TEMAS.keys())
    nomes_dif       = list(DIFICULDADES.keys())
    tick            = 0

    while True:
        tick += 1
        tema_nome = nomes_temas[tema_idx]
        tema      = TEMAS[tema_nome]
        tela.fill(tema["fundo"])
        desenhar_grade(tema)
        desenhar_paredes(tema)

        # título animado
        escala = 1 + 0.025 * math.cos(tick * 0.08)
        titulo_surf = fonte_titulo.render("🐍 COBRINHA", True, tema["pontos"])
        w = int(titulo_surf.get_width() * escala)
        h = int(titulo_surf.get_height() * escala)
        titulo_surf = pygame.transform.scale(titulo_surf, (w, h))
        tela.blit(titulo_surf, titulo_surf.get_rect(center=(LARGURA//2, 70)))

        # subtítulo
        texto_centro("SUPREME EDITION", (200,200,200), 115, fonte_pequena)

        # ---- SEÇÃO: PERSONAGEM ----
        texto_centro("PERSONAGEM", tema["pontos"], 155, fonte_pequena)
        lp = len(PERSONAGENS)
        for i, p in enumerate(PERSONAGENS):
            col = i % 2
            row = i // 2
            rx = 160 + col * 180
            ry = 168 + row * 42
            rect = pygame.Rect(rx, ry, 160, 34)
            caixa_opcao(rect, p, i == personagem_idx, tema["cobra"], (0,0,0) if tema_nome=="Gelo" else (255,255,255))

        # ---- SEÇÃO: TEMA ----
        texto_centro("TEMA VISUAL", tema["pontos"], 262, fonte_pequena)
        for i, tn in enumerate(nomes_temas):
            col = i % 2
            row = i // 2
            rx = 160 + col * 180
            ry = 275 + row * 42
            rect = pygame.Rect(rx, ry, 160, 34)
            caixa_opcao(rect, tn, i == tema_idx, tema["cobra"], (0,0,0) if tema_nome=="Gelo" else (255,255,255))

        # ---- SEÇÃO: DIFICULDADE ----
        texto_centro("DIFICULDADE", tema["pontos"], 370, fonte_pequena)
        for i, d in enumerate(nomes_dif):
            rx = 60 + i * 132
            rect = pygame.Rect(rx, 382, 122, 34)
            caixa_opcao(rect, d, i == dificuldade_idx, tema["cobra"], (0,0,0) if tema_nome=="Gelo" else (255,255,255))

        # recordes
        dif_nome = nomes_dif[dificuldade_idx]
        rec = recordes[dif_nome]
        texto_centro(f"🏆 Recorde ({dif_nome}): {rec}", (255,220,80), 430, fonte_pequena)

        # botão jogar
        cor_btn = (
            int(150 + 100*math.cos(tick*0.1)),
            int(50 + 50*math.sin(tick*0.1)),
            150
        )
        btn = pygame.Rect(LARGURA//2 - 110, 448, 220, 20)
        pygame.draw.rect(tela, cor_btn, btn, border_radius=6)
        s = fonte_media.render("▶  JOGAR  [ENTER]", True, (255,255,255))
        tela.blit(s, s.get_rect(center=btn.center))

        pygame.display.flip()
        relogio.tick(60)

        for ev in pygame.event.get():
            if ev.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            if ev.type == pygame.KEYDOWN:
                if ev.key in (pygame.K_RETURN, pygame.K_SPACE):
                    return (nomes_temas[tema_idx],
                            PERSONAGENS[personagem_idx],
                            nomes_dif[dificuldade_idx])
                if ev.key == pygame.K_ESCAPE:
                    pygame.quit(); sys.exit()
            if ev.type == pygame.MOUSEBUTTONDOWN:
                mx, my = ev.pos
                # personagem
                for i, p in enumerate(PERSONAGENS):
                    col = i % 2; row = i // 2
                    rx = 160 + col*180; ry = 168 + row*42
                    if pygame.Rect(rx, ry, 160, 34).collidepoint(mx, my):
                        personagem_idx = i
                # tema
                for i, tn in enumerate(nomes_temas):
                    col = i % 2; row = i // 2
                    rx = 160 + col*180; ry = 275 + row*42
                    if pygame.Rect(rx, ry, 160, 34).collidepoint(mx, my):
                        tema_idx = i
                # dificuldade
                for i, d in enumerate(nomes_dif):
                    rx = 60 + i*132
                    if pygame.Rect(rx, 382, 122, 34).collidepoint(mx, my):
                        dificuldade_idx = i
                # jogar
                if btn.collidepoint(mx, my):
                    return (nomes_temas[tema_idx],
                            PERSONAGENS[personagem_idx],
                            nomes_dif[dificuldade_idx])

#  LOOP DO JOGO
def gerar_obstaculos(n, lista_cobra, comida_x, comida_y):
    cols = AREA_LARGURA // TAMANHO_BLOCO
    rows = AREA_ALTURA  // TAMANHO_BLOCO
    obs  = []
    tentativas = 0
    while len(obs) < n and tentativas < 500:
        tentativas += 1
        ox = random.randint(0, cols-1)*TAMANHO_BLOCO + AREA_X1
        oy = random.randint(0, rows-1)*TAMANHO_BLOCO + AREA_Y1
        if [ox, oy] in lista_cobra: continue
        if ox == comida_x and oy == comida_y: continue
        if abs(ox - lista_cobra[-1][0]) < TAMANHO_BLOCO*4 and \
           abs(oy - lista_cobra[-1][1]) < TAMANHO_BLOCO*4: continue
        obs.append((ox, oy))
    return obs

def loop_jogo(tema_nome, personagem, dificuldade_nome):
    global recordes
    tema      = TEMAS[tema_nome]
    cfg       = DIFICULDADES[dificuldade_nome]
    velocidade= cfg["velocidade"]
    n_obs     = cfg["obstaculos"]

    img_cabeca = criar_cabeca(personagem, tema["cobra"], tema["cobra_sombra"])
    img_comida = criar_comida()

    x = AREA_X1 + (AREA_LARGURA//2 // TAMANHO_BLOCO) * TAMANHO_BLOCO
    y = AREA_Y1  + (AREA_ALTURA //2 // TAMANHO_BLOCO) * TAMANHO_BLOCO

    x_mudanca = 0; y_mudanca = 0; direcao = "direita"
    lista_cobra = [[x, y]]
    comprimento = 1

    def nova_comida():
        cols = AREA_LARGURA // TAMANHO_BLOCO
        rows = AREA_ALTURA  // TAMANHO_BLOCO
        while True:
            cx = random.randint(0, cols-1)*TAMANHO_BLOCO + AREA_X1
            cy = random.randint(0, rows-1)*TAMANHO_BLOCO + AREA_Y1
            if [cx,cy] not in lista_cobra:
                return cx, cy

    comida_x, comida_y = nova_comida()
    obstaculos = gerar_obstaculos(n_obs, lista_cobra, comida_x, comida_y)

    particulas.clear()
    fim = False; morreu = False
    flash = 0  # frames de flash na morte

    while not fim:

        # GAME OVER
        if morreu:
            pontuacao = comprimento - 1
            if pontuacao > recordes[dificuldade_nome]:
                recordes[dificuldade_nome] = pontuacao
                novo_recorde = True
            else:
                novo_recorde = False

            esperando = True
            while esperando:
                tela.fill(tema["fundo"])
                desenhar_grade(tema)
                desenhar_paredes(tema)
                # sobreposição escura
                overlay = pygame.Surface((LARGURA, ALTURA), pygame.SRCALPHA)
                overlay.fill((0,0,0,140))
                tela.blit(overlay, (0,0))

                texto_centro("FIM DE JOGO ", (220,20,60), ALTURA//2-70, fonte_grande)
                texto_centro(f"Pontuação: {pontuacao}", tema["pontos"], ALTURA//2-20, fonte_grande)
                if novo_recorde:
                    texto_centro("NOVO RECORDE!", (255,220,80), ALTURA//2+25, fonte_media)
                texto_centro(f"Recorde ({dificuldade_nome}): {recordes[dificuldade_nome]}",
                             (200,200,200), ALTURA//2+55, fonte_pequena)
                texto_centro("[ C ] Continuar   [ M ] Menu   [ S ] Sair",
                             (255,255,255), ALTURA//2+90, fonte_pequena)
                pygame.display.flip()
                relogio.tick(30)

                for ev in pygame.event.get():
                    if ev.type == pygame.QUIT:
                        pygame.quit(); sys.exit()
                    if ev.type == pygame.KEYDOWN:
                        if ev.key == pygame.K_c:
                            loop_jogo(tema_nome, personagem, dificuldade_nome)
                            return
                        if ev.key == pygame.K_m:
                            esperando = False; fim = True
                        if ev.key == pygame.K_s:
                            pygame.quit(); sys.exit()
                    if ev.type == pygame.MOUSEBUTTONDOWN:
                        mx,my = ev.pos
                        esperando = False; fim = True
            continue

        # EVENTOS 
        for ev in pygame.event.get():
            if ev.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            if ev.type == pygame.KEYDOWN:
                if ev.key == pygame.K_LEFT  and direcao != "direita":
                    x_mudanca=-TAMANHO_BLOCO; y_mudanca=0; direcao="esquerda"
                elif ev.key == pygame.K_RIGHT and direcao != "esquerda":
                    x_mudanca=TAMANHO_BLOCO;  y_mudanca=0; direcao="direita"
                elif ev.key == pygame.K_UP    and direcao != "baixo":
                    y_mudanca=-TAMANHO_BLOCO; x_mudanca=0; direcao="cima"
                elif ev.key == pygame.K_DOWN  and direcao != "cima":
                    y_mudanca=TAMANHO_BLOCO;  x_mudanca=0; direcao="baixo"
                elif ev.key == pygame.K_ESCAPE:
                    fim = True
                # WASD
                elif ev.key == pygame.K_a and direcao != "direita":
                    x_mudanca=-TAMANHO_BLOCO; y_mudanca=0; direcao="esquerda"
                elif ev.key == pygame.K_d and direcao != "esquerda":
                    x_mudanca=TAMANHO_BLOCO;  y_mudanca=0; direcao="direita"
                elif ev.key == pygame.K_w and direcao != "baixo":
                    y_mudanca=-TAMANHO_BLOCO; x_mudanca=0; direcao="cima"
                elif ev.key == pygame.K_s and direcao != "cima":
                    y_mudanca=TAMANHO_BLOCO;  x_mudanca=0; direcao="baixo"

        # MOVER
        x += x_mudanca
        y += y_mudanca

        # COLISÃO PAREDE
        if x < AREA_X1 or x >= AREA_X2 or y < AREA_Y1 or y >= AREA_Y2:
            tocar(SOM_MORTE)
            morreu = True; continue

        # COLISÃO OBSTÁCULO
        if (x,y) in obstaculos:
            tocar(SOM_MORTE)
            morreu = True; continue

        # CORPO
        cabeca = [x, y]
        lista_cobra.append(cabeca)
        if len(lista_cobra) > comprimento:
            del lista_cobra[0]

        # COLISÃO PRÓPRIO CORPO
        if cabeca in lista_cobra[:-1]:
            tocar(SOM_MORTE)
            morreu = True; continue

        # DESENHAR
        tela.fill(tema["fundo"])
        desenhar_grade(tema)
        desenhar_paredes(tema)
        desenhar_obstaculos(obstaculos, tema)
        tela.blit(img_comida, [comida_x, comida_y])
        atualizar_particulas()
        desenhar_cobra(lista_cobra, direcao, img_cabeca, tema)

        # pontuação e dificuldade no HUD
        pontos_txt = fonte_media.render(f"🍎 {comprimento-1}", True, tema["pontos"])
        tela.blit(pontos_txt, (AREA_X1+5, AREA_Y1+4))
        dif_txt = fonte_pequena.render(dificuldade_nome, True, (200,200,200))
        tela.blit(dif_txt, (LARGURA - dif_txt.get_width() - AREA_X1 - 5, AREA_Y1+5))

        pygame.display.flip()

        # COMER
        if x == comida_x and y == comida_y:
            tocar(SOM_COMER)
            adicionar_particulas(comida_x, comida_y, (100,255,255))
            comprimento += 1
            comida_x, comida_y = nova_comida()
            if dificuldade_nome != "Fácil" and (comprimento-1) % 5 == 0 and comprimento > 1:
                tocar(SOM_NIVEL)
                novos = gerar_obstaculos(1, lista_cobra, comida_x, comida_y)
                obstaculos.extend(novos)

        relogio.tick(velocidade)

#  PONTO DE ENTRADA
if __name__ == "__main__":
    while True:
        tema_nome, personagem, dificuldade = menu_principal()
        loop_jogo(tema_nome, personagem, dificuldade)
