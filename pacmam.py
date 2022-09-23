import random
import pygame
import datetime

from abc import ABCMeta, abstractmethod

pygame.init()

screen = pygame.display.set_mode((800, 600), 0)
fonte = pygame.font.SysFont("arial", 24, True, False)

AMARELO = (255, 255, 0)
PRETO = (0, 0, 0)
AZUL = (0, 0, 255)
VERMELHO = (255, 0, 0)
BRANCO = (255, 255, 255)
CIANO = (0, 255, 255)
LARANJA = (255, 140, 0)
ROSA = (255, 15, 192)
VELOCIDADE = 1
ACIMA = 1
ABAIXO = 2
DIREITA = 3
ESQUERDA = 4
JOGANDO = "JOGANDO"
PAUSADO = "PAUSADO"
GAMEOVER = "GAMEOVER"
VITORIA = "VITORIA"


class ElementoJogo(metaclass=ABCMeta):
    @abstractmethod
    def pintar(self, tela):
        pass

    @abstractmethod
    def calcular_regras(self):
        pass

    @abstractmethod
    def processar_eventos(self, evtos):
        pass


class Movivel(metaclass=ABCMeta):
    @abstractmethod
    def aceitar_movimento(self):
        pass

    @abstractmethod
    def recusar_movimento(self, direcoes):
        pass

    @abstractmethod
    def esquina(self, direcoes):
        pass


class Cronometro:
    def __init__(self):
        self.start = True
        self.tempo = datetime.datetime.now()
        self.tempo_decorrido = datetime.timedelta(seconds=0)
        self.tempo_qd_parou = datetime.timedelta(seconds=0)
        self.tempo_zero = datetime.timedelta(seconds=0)

    def inicia_cronometro(self):
        self.tempo = datetime.datetime.now()

    def muda_estado_cronometro(self, estado):
        self.start = estado

    def conta_tempo(self):
        if self.start:
            if self.tempo_qd_parou > self.tempo_zero:
                self.tempo = datetime.datetime.now() - self.tempo_qd_parou
                self.tempo_qd_parou = self.tempo_zero
            self.tempo_decorrido = datetime.datetime.now() - self.tempo
        else:
            self.tempo_qd_parou = self.tempo_decorrido
        return int(self.tempo_decorrido.total_seconds())


class Cenario(ElementoJogo):
    def __init__(self, tamanho, pac):
        super().__init__()
        self.pacmam = pac
        self.moviveis = []
        self.tamanho = tamanho
        self.vidas = 3
        self.pontos = 0
        self.estado = JOGANDO  # JOGANDO / PAUSADO / 2-GameOver / 3-Vitória
        self.matriz = [
            [2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2],
            [2, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2],
            [2, 1, 2, 2, 2, 2, 1, 2, 2, 2, 2, 2, 1, 2, 2, 1, 2, 2, 2, 2, 2, 1, 2, 2, 2, 2, 1, 2],
            [2, 1, 2, 2, 2, 2, 1, 2, 2, 2, 2, 2, 1, 1, 1, 1, 2, 2, 2, 2, 2, 1, 2, 2, 2, 2, 1, 2],
            [2, 1, 2, 2, 2, 2, 1, 2, 2, 2, 2, 2, 1, 2, 2, 1, 2, 2, 2, 2, 2, 1, 2, 2, 2, 2, 1, 2],
            [2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2],
            [2, 1, 2, 2, 2, 2, 1, 2, 2, 1, 2, 2, 2, 2, 2, 2, 2, 2, 1, 2, 2, 1, 2, 2, 2, 2, 1, 2],
            [2, 1, 2, 2, 2, 2, 1, 2, 2, 1, 2, 2, 2, 2, 2, 2, 2, 2, 1, 2, 2, 1, 2, 2, 2, 2, 1, 2],
            [2, 1, 1, 1, 1, 1, 1, 2, 2, 1, 1, 1, 1, 2, 2, 1, 1, 1, 1, 2, 2, 1, 1, 1, 1, 1, 1, 2],
            [2, 2, 2, 1, 2, 2, 1, 2, 2, 2, 2, 2, 1, 2, 2, 1, 2, 2, 2, 2, 2, 1, 2, 2, 1, 2, 2, 2],
            [2, 2, 2, 1, 2, 2, 1, 2, 2, 2, 2, 2, 1, 2, 2, 1, 2, 2, 2, 2, 2, 1, 2, 2, 1, 2, 2, 2],
            [2, 1, 1, 1, 2, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 2, 1, 1, 1, 2],
            [2, 1, 2, 2, 2, 2, 1, 2, 2, 1, 2, 2, 0, 0, 0, 0, 2, 2, 1, 2, 2, 1, 2, 2, 2, 2, 1, 2],
            [2, 1, 2, 2, 2, 2, 1, 2, 2, 1, 2, 0, 0, 0, 0, 0, 0, 2, 1, 2, 2, 1, 2, 2, 2, 2, 1, 2],
            [2, 1, 1, 1, 1, 1, 1, 2, 2, 1, 2, 0, 0, 0, 0, 0, 0, 2, 1, 2, 2, 1, 1, 1, 1, 1, 1, 2],
            [2, 1, 2, 2, 2, 2, 1, 2, 2, 1, 2, 0, 0, 0, 0, 0, 0, 2, 1, 2, 2, 1, 2, 2, 2, 2, 1, 2],
            [2, 1, 2, 2, 2, 2, 1, 2, 2, 1, 2, 2, 2, 2, 2, 2, 2, 2, 1, 2, 2, 1, 2, 2, 2, 2, 1, 2],
            [2, 1, 1, 1, 2, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 2, 1, 1, 1, 2],
            [2, 2, 2, 1, 2, 2, 1, 2, 2, 2, 2, 2, 1, 2, 2, 1, 2, 2, 2, 2, 2, 1, 2, 2, 1, 2, 2, 2],
            [2, 2, 2, 1, 2, 2, 1, 2, 2, 2, 2, 2, 1, 2, 2, 1, 2, 2, 2, 2, 2, 1, 2, 2, 1, 2, 2, 2],
            [2, 1, 1, 1, 1, 1, 1, 2, 2, 1, 1, 1, 1, 2, 2, 1, 1, 1, 1, 2, 2, 1, 1, 1, 1, 1, 1, 2],
            [2, 1, 2, 2, 2, 2, 1, 2, 2, 1, 2, 2, 2, 2, 2, 2, 2, 2, 1, 2, 2, 1, 2, 2, 2, 2, 1, 2],
            [2, 1, 2, 2, 2, 2, 1, 2, 2, 1, 2, 2, 2, 2, 2, 2, 2, 2, 1, 2, 2, 1, 2, 2, 2, 2, 1, 2],
            [2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2],
            [2, 1, 2, 2, 2, 2, 1, 2, 2, 2, 2, 2, 1, 2, 2, 1, 2, 2, 2, 2, 2, 1, 2, 2, 2, 2, 1, 2],
            [2, 1, 2, 2, 2, 2, 1, 2, 2, 2, 2, 2, 1, 1, 1, 1, 2, 2, 2, 2, 2, 1, 2, 2, 2, 2, 1, 2],
            [2, 1, 2, 2, 2, 2, 1, 2, 2, 2, 2, 2, 1, 2, 2, 1, 2, 2, 2, 2, 2, 1, 2, 2, 2, 2, 1, 2],
            [2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2],
            [2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2]
        ]

    def adcionar_movivel(self, obj):
        self.moviveis.append(obj)

    def pintar_score(self, tela):
        pontos_x = 30 * self.tamanho
        img_pontos = fonte.render("Score: {}".format(self.pontos), True, AMARELO)
        img_vidas = fonte.render("Vidas: {}". format(self.vidas), True, AMARELO)
        tela.blit(img_pontos, (pontos_x, 50))
        tela.blit(img_vidas, (pontos_x, 100))

    def pintar_tempo(self, tela):
        tempo_x = 30 * self.tamanho
        img_tempo = fonte.render("Tempo: {}".format(cronometro.conta_tempo()), True, AMARELO)
        tela.blit(img_tempo, (tempo_x, 150))

    def pintar_linha(self, tela, numero_linha, linha):
        for numero_coluna, coluna in enumerate(linha):
            x = numero_coluna * self.tamanho
            y = numero_linha * self.tamanho
            half = self.tamanho // 2
            cor = PRETO

            if coluna == 2:
                cor = AZUL
            pygame.draw.rect(tela, cor, (x, y, self.tamanho, self.tamanho), 0)
            if coluna == 1:
                pygame.draw.circle(tela, AMARELO, (x + half, y + half), self.tamanho // 10, 0)

    def pintar(self, tela):
        if self.estado == JOGANDO:
            cronometro.muda_estado_cronometro(True)
            self.pintar_jogando(tela)
        elif self.estado == PAUSADO:
            cronometro.muda_estado_cronometro(False)
            self.pintar_jogando(tela)
            self.pintar_pausado(tela)
        elif self.estado == GAMEOVER:
            cronometro.muda_estado_cronometro(False)
            self.pintar_jogando(tela)
            self.pintar_gameover(tela)
        elif self.estado == VITORIA:
            cronometro.muda_estado_cronometro(False)
            self.pintar_jogando(tela)
            self.pintar_vitoria(tela)

    def pintar_texto_centro(self, tela, texto):
        texto_img = fonte.render(texto, True, AMARELO)
        texto_x = (tela.get_width() - texto_img.get_width()) // 2
        texto_y = (tela.get_height() - texto_img.get_height()) // 2
        tela.blit(texto_img, (texto_x, texto_y))

    def pintar_gameover(self, tela):
        self.pintar_texto_centro(tela, "G A M E  O V E R !")

    def pintar_pausado(self, tela):
        self.pintar_texto_centro(tela, "P A U S E !")

    def pintar_vitoria(self, tela):
        self.pintar_texto_centro(tela, "P A R A B É N S  V O C Ê  V E N C E U ! ! !")

    def pintar_jogando(self, tela):
        for numero_linha, linha in enumerate(self.matriz):
            self.pintar_linha(tela, numero_linha, linha)
        self.pintar_score(tela)
        self.pintar_tempo(tela)

    def get_direcoes(self, linha, coluna):
        direcoes = []
        if self.matriz[int(linha - 1)][int(coluna)] != 2:
            direcoes.append(ACIMA)
        if self.matriz[int(linha + 1)][int(coluna)] != 2:
            direcoes.append(ABAIXO)
        if self.matriz[int(linha)][int(coluna - 1)] != 2:
            direcoes.append(ESQUERDA)
        if self.matriz[int(linha)][int(coluna + 1)] != 2:
            direcoes.append(DIREITA)
        return direcoes

    def calcular_regras(self):
        if self.estado == JOGANDO:
            self.calcular_regras_jogando()
        elif self.estado == PAUSADO:
            self.calcular_regras_pausado()
        elif self.estado == GAMEOVER:
            self.calcular_regras_gameover()

    def calcular_regras_gameover(self):
        pass

    def calcular_regras_pausado(self):
        pass

    def calcular_regras_jogando(self):
        for movivel in self.moviveis:
            lin = int(movivel.linha)
            col = int(movivel.coluna)
            lin_intencao = int(movivel.linha_intencao)
            col_intencao = int(movivel.coluna_intencao)
            direcoes = self.get_direcoes(lin, col)
            if len(direcoes) >= 3:
                movivel.esquina(direcoes)
            if isinstance(movivel, Fantasma) and movivel.linha == self.pacmam.linha and \
               movivel.coluna == self.pacmam.coluna:
                self.vidas -= 1
                if self.vidas <= 0:
                    self.estado = GAMEOVER
                else:
                    self.pacmam.linha = 1
                    self.pacmam.coluna = 1
                    self.pacmam.lado = DIREITA
            else:
                if 0 <= col_intencao < 27 and 0 <= lin_intencao < 28 and \
                   self.matriz[lin_intencao][col_intencao] != 2:
                    movivel.aceitar_movimento()
                    if isinstance(movivel, Pacmam) and self.matriz[lin][col] == 1:
                        self.pontos += 1
                        self.matriz[lin][col] = 0
                        if self.pontos >= 305:
                            self.estado = VITORIA

                else:
                    movivel.recusar_movimento(direcoes)

    def processar_eventos(self, evts):
        for e in evts:
            if e.type == pygame.QUIT:
                exit()
            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_p:
                    if self.estado == JOGANDO:
                        self.estado = PAUSADO
                    else:
                        self.estado = JOGANDO


class Pacmam(ElementoJogo, Movivel):
    def __init__(self, tamanho):
        self.coluna = 1
        self.linha = 1
        self.centro_x = 30  # era 400
        self.centro_y = 30  # era 300
        self.tamanho = tamanho
        self.vel_x = 0
        self.vel_y = 0
        self.raio = self.tamanho // 2
        self.coluna_intencao = self.coluna
        self.linha_intencao = self.linha
        self.lado = DIREITA
        self.abertura_boca = 0
        self.velocidade_abertura_boca = 1

    def calcular_regras(self):
        self.coluna_intencao = self.coluna + self.vel_x
        self.linha_intencao = self.linha + self.vel_y
        self.centro_x = int(self.coluna * self.tamanho + self.raio)
        self.centro_y = int(self.linha * self.tamanho + self.raio)

    def processar_eventos_mouse(self, events_mouse):
        delay = 25
        for e in events_mouse:
            if e.type == pygame.MOUSEMOTION:
                mouse_x, mouse_y = e.pos
                self.coluna = (mouse_x - self.centro_x) / delay
                self.linha = (mouse_y - self.centro_y) / delay

    def processar_eventos(self, events):
        for e in events:
            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_RIGHT:
                    self.lado = DIREITA
                    self.vel_x = VELOCIDADE
                elif e.key == pygame.K_LEFT:
                    self.lado = ESQUERDA
                    self.vel_x = - VELOCIDADE
                elif e.key == pygame.K_UP:
                    self.lado = ACIMA
                    self.vel_y = - VELOCIDADE
                elif e.key == pygame.K_DOWN:
                    self.lado = ABAIXO
                    self.vel_y = VELOCIDADE

            elif e.type == pygame.KEYUP:
                if e.key == pygame.K_RIGHT:
                    self.vel_x = 0
                elif e.key == pygame.K_LEFT:
                    self.vel_x = 0
                elif e.key == pygame.K_UP:
                    self.vel_y = 0
                elif e.key == pygame.K_DOWN:
                    self.vel_y = 0

    def aceitar_movimento(self):
        self.linha = self.linha_intencao
        self.coluna = self.coluna_intencao

    def recusar_movimento(self, direcoes):
        self.linha_intencao = self.linha
        self.coluna_intencao = self.coluna

    def esquina(self, direcoes):
        pass

    def pintar(self, tela):
        self.abertura_boca += self.velocidade_abertura_boca
        if self.abertura_boca > self.raio:
            self.velocidade_abertura_boca = -1
        if self.abertura_boca <= 0:
            self.velocidade_abertura_boca = 1

        if self.lado == ACIMA:
            self.pintar_acima(tela)
        if self.lado == ABAIXO:
            self.pintar_abaixo(tela)
        if self.lado == DIREITA:
            self.pintar_direita(tela)
        if self.lado == ESQUERDA:
            self.pintar_esquerda(tela)

    def pintar_direita(self, tela):
        # desenho do corpo
        pygame.draw.circle(tela, AMARELO, (self.centro_x, self.centro_y), self.raio, 0)

        # desenho da boca
        canto_boca = (self.centro_x, self.centro_y)
        labio_superior = (self.centro_x + self.raio, self.centro_y - self.abertura_boca)
        labio_inferior = (self.centro_x + self.raio, self.centro_y + self.abertura_boca)
        pontos = [canto_boca, labio_superior, labio_inferior]
        pygame.draw.polygon(tela, PRETO, pontos, 0)

        # desenho do olho
        olho_x = int(self.centro_x + self.raio / 5)
        olho_y = int(self.centro_y - self.raio * 0.70)
        olho_raio = int(self.raio / 10)
        pygame.draw.circle(tela, PRETO, (olho_x, olho_y), olho_raio, 0)

    def pintar_esquerda(self, tela):
        pygame.draw.circle(tela, AMARELO, (self.centro_x, self.centro_y), self.raio, 0)

        canto_boca = (self.centro_x, self.centro_y)
        labio_superior = (self.centro_x - self.raio, self.centro_y - self.abertura_boca)
        labio_inferior = (self.centro_x - self.raio, self.centro_y + self.abertura_boca)
        lista_pontos = [canto_boca, labio_superior, labio_inferior]
        pygame.draw.polygon(tela, PRETO, lista_pontos, 0)

        olho_x = int(self.centro_x - self.raio / 5)
        olho_y = int(self.centro_y - self.raio * 0.70)
        olho_raio = int(self.raio / 10)
        pygame.draw.circle(tela, PRETO, (olho_x, olho_y), olho_raio, 0)

    def pintar_acima(self, tela):
        # desenho do corpo
        pygame.draw.circle(tela, AMARELO, (self.centro_x, self.centro_y), self.raio, 0)

        # desenho da boca
        canto_boca = (self.centro_x, self.centro_y)
        labio_superior = (self.centro_x - self.abertura_boca, self.centro_y - self.raio)
        labio_inferior = (self.centro_x + self.abertura_boca, self.centro_y - self.raio)
        pontos = [canto_boca, labio_superior, labio_inferior]
        pygame.draw.polygon(tela, PRETO, pontos, 0)

        # desenho do olho
        olho_x = int(self.centro_x - self.raio * 0.7)
        olho_y = int(self.centro_y - self.raio * 0.3)
        olho_raio = int(self.raio / 10)
        pygame.draw.circle(tela, PRETO, (olho_x, olho_y), olho_raio, 0)

    def pintar_abaixo(self, tela):
        # desenho do corpo
        pygame.draw.circle(tela, AMARELO, (self.centro_x, self.centro_y), self.raio, 0)

        # desenho da boca
        canto_boca = (self.centro_x, self.centro_y)
        labio_superior = (self.centro_x + self.abertura_boca, self.centro_y + self.raio)
        labio_inferior = (self.centro_x - self.abertura_boca, self.centro_y + self.raio)
        pontos = [canto_boca, labio_superior, labio_inferior]
        pygame.draw.polygon(tela, PRETO, pontos, 0)

        # desenho do olho
        olho_x = int(self.centro_x + self.raio * 0.7)
        olho_y = int(self.centro_y + self.raio * 0.3)
        olho_raio = int(self.raio / 10)
        pygame.draw.circle(tela, PRETO, (olho_x, olho_y), olho_raio, 0)


class Fantasma(ElementoJogo, Movivel):
    def __init__(self, cor, tamanho):
        self.coluna = 13.0
        self.linha = 13.0
        self.linha_intencao = self.linha
        self.coluna_intencao = self.coluna
        self.velocidade = 1
        self.direcao = ABAIXO
        self.tamanho = tamanho
        self.cor = cor

    def pintar(self, tela):
        fatia = self.tamanho // 8
        px = int(self.coluna * self.tamanho)
        py = int(self.linha * self.tamanho)
        contorno = [(px, py + self.tamanho),
                    (px + fatia * 2, py + fatia * 2),
                    (px + fatia * 3, py + fatia // 2),
                    (px + fatia * 4, py),
                    (px + fatia * 5, py),
                    (px + fatia * 6, py + fatia // 2),
                    (px + fatia * 7, py + fatia * 2),
                    (px + self.tamanho, py + self.tamanho),
                    (px + fatia * 7, py + fatia * 7),
                    (px + fatia * 6, py + self.tamanho),
                    (px + fatia * 4, py + fatia * 7),
                    (px + fatia * 3, py + self.tamanho),
                    (px + fatia * 2, py + fatia * 7),
                    (px, py + self.tamanho)]
        pygame.draw.polygon(tela, self.cor, contorno, 0)

        olho_raio_ext = fatia
        olho_raio_int = fatia // 2
        olho_e_x = int(px + fatia * 3)
        olho_e_y = int(py + fatia * 2.5)
        olho_d_x = int(px + fatia * 6)
        olho_d_y = int(py + fatia * 2.5)

        pygame.draw.circle(tela, BRANCO, (olho_e_x, olho_e_y), olho_raio_ext, 0)
        pygame.draw.circle(tela, PRETO, (olho_e_x, olho_e_y), olho_raio_int, 0)

        pygame.draw.circle(tela, BRANCO, (olho_d_x, olho_d_y), olho_raio_ext, 0)
        pygame.draw.circle(tela, PRETO, (olho_d_x, olho_d_y), olho_raio_int, 0)

    def calcular_regras(self):
        if self.direcao == ACIMA:
            self.linha_intencao -= self.velocidade
        elif self.direcao == ABAIXO:
            self.linha_intencao += self.velocidade
        elif self.direcao == ESQUERDA:
            self.coluna_intencao -= self.velocidade
        elif self.direcao == DIREITA:
            self.coluna_intencao += self.velocidade

    def mudar_direcao(self, direcoes):
        self.direcao = random.choice(direcoes)

    def esquina(self, direcoes):
        self.mudar_direcao(direcoes)

    def aceitar_movimento(self):
        self.linha = self.linha_intencao
        self.coluna = self.coluna_intencao

    def recusar_movimento(self, direcoes):
        self.linha_intencao = self.linha
        self.coluna_intencao = self.coluna
        self.mudar_direcao(direcoes)

    def processar_eventos(self, evts):
        pass


if __name__ == "__main__":
    size = 600 // 30
    pacmam = Pacmam(size)
    blinky = Fantasma(VERMELHO, size)
    inky = Fantasma(CIANO, size)
    clyde = Fantasma(LARANJA, size)
    pinky = Fantasma(ROSA, size)
    cenario = Cenario(size, pacmam)
    cronometro = Cronometro()
    cenario.adcionar_movivel(pacmam)
    cenario.adcionar_movivel(blinky)
    cenario.adcionar_movivel(inky)
    cenario.adcionar_movivel(clyde)
    cenario.adcionar_movivel(pinky)

    screen.fill(PRETO)
    cenario.pintar(screen)
    pacmam.pintar(screen)
    blinky.pintar(screen)
    inky.pintar(screen)
    clyde.pintar(screen)
    pinky.pintar(screen)
    pygame.display.update()

    rodar = False

    while True:
        # captura os eventos
        eventos = pygame.event.get()

        if not rodar:
            for e in eventos:
                if e.type == pygame.KEYDOWN:
                    if e.key == pygame.K_UP or\
                            e.key == pygame.K_DOWN or\
                            e.key == pygame.K_LEFT or\
                            e.key == pygame.K_RIGHT:
                        cronometro.inicia_cronometro()
                        rodar = True

        if rodar:
            # calcula as regras
            pacmam.calcular_regras()
            blinky.calcular_regras()
            inky.calcular_regras()
            clyde.calcular_regras()
            pinky.calcular_regras()
            cenario.calcular_regras()

            # pinta a tela
            screen.fill(PRETO)
            cenario.pintar(screen)
            pacmam.pintar(screen)
            blinky.pintar(screen)
            inky.pintar(screen)
            clyde.pintar(screen)
            pinky.pintar(screen)
            pygame.display.update()
            pygame.time.delay(100)

            # pacmam.processar_eventos_mouse(eventos)
            pacmam.processar_eventos(eventos)
            cenario.processar_eventos(eventos)
