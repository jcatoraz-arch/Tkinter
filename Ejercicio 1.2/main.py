import pygame
import os
import json

pygame.init()

ANCHO = 500
ALTO = 700

pantalla = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("Formaciones FIFA")

clock = pygame.time.Clock()

ruta_base = os.path.dirname(os.path.abspath(__file__))
ruta_assets = os.path.join(ruta_base, "assets")

cancha = pygame.image.load(os.path.join(ruta_assets,"cancha.png"))
jugador_rojo = pygame.image.load(os.path.join(ruta_assets,"jugador.png"))
jugador_azul = pygame.image.load(os.path.join(ruta_assets,"jugador2.png"))

cancha = pygame.transform.scale(cancha,(ANCHO,ALTO))
jugador_rojo = pygame.transform.scale(jugador_rojo,(45,45))
jugador_azul = pygame.transform.scale(jugador_azul,(45,45))

font = pygame.font.SysFont(None,24)

mitad = ALTO // 2

formacion_actual = "4-4-2"
menu_abierto = False

formaciones = [
    "4-4-2",
    "4-3-3",
    "3-5-2",
    "4-2-3-1",
    "5-3-2",
    "4-1-2-1-2"
]

posiciones_base = [
    "POR",
    "LI","DFC","DFC","LD",
    "MI","MC","MC","MD",
    "DC","DC"
]

def obtener_formacion(nombre):
    # Defino coordenadas predeterminadas de equipo1 (azul)
    if nombre == "4-4-2":
        equipo1 = [
            (230, mitad + 220),
            (80, mitad + 140),(180, mitad + 140),(280, mitad + 140),(380, mitad + 140),
            (80, mitad + 70),(180, mitad + 70),(280, mitad + 70),(380, mitad + 70),
            (180, mitad + 10),(280, mitad + 10)
        ]
    elif nombre == "4-3-3":
        equipo1 = [
            (230, mitad + 220),
            (80, mitad + 140),(180, mitad + 140),(280, mitad + 140),(380, mitad + 140),
            (120, mitad + 70),(230, mitad + 70),(340, mitad + 70),
            (80, mitad + 10),(230, mitad + 10),(380, mitad + 10)
        ]
    elif nombre == "3-5-2":
        equipo1 = [
            (230, mitad + 220),
            (120, mitad + 150),(230, mitad + 150),(340, mitad + 150),
            (80, mitad + 90),(160, mitad + 90),(230, mitad + 90),(300, mitad + 90),(380, mitad + 90),
            (180, mitad + 20),(280, mitad + 20)
        ]
    elif nombre == "4-2-3-1":
        equipo1 = [
            (230, mitad + 220),
            (80, mitad + 150),(180, mitad + 150),(280, mitad + 150),(380, mitad + 150),
            (150, mitad + 90),(310, mitad + 90),
            (80, mitad + 40),(230, mitad + 40),(380, mitad + 40),
            (230, mitad - 10)
        ]
    elif nombre == "5-3-2":
        equipo1 = [
            (230, mitad + 220),
            (60, mitad + 150),(140, mitad + 150),(230, mitad + 150),(320, mitad + 150),(400, mitad + 150),
            (140, mitad + 80),(230, mitad + 80),(320, mitad + 80),
            (180, mitad + 20),(280, mitad + 20)
        ]
    elif nombre == "4-1-2-1-2":
        equipo1 = [
            (230, mitad + 220),
            (80, mitad + 150),(180, mitad + 150),(280, mitad + 150),(380, mitad + 150),
            (230, mitad + 110),
            (140, mitad + 70),(320, mitad + 70),
            (230, mitad + 40),
            (180, mitad - 10),(280, mitad - 10)
        ]

    # Equipo2 (rojo) = espejo y 60px más arriba
    equipo2 = [(x, ALTO - y - 60) for (x,y) in equipo1]

    return equipo1, equipo2

def posiciones_originales(nombre):
    eq1, eq2 = obtener_formacion(nombre)
    return eq1.copy(), eq2.copy()

equipo1, equipo2 = obtener_formacion(formacion_actual)
originales1, originales2 = posiciones_originales(formacion_actual)

# Listas de posiciones independientes para cada equipo
posiciones_azul = posiciones_base.copy()
posiciones_rojo = posiciones_base.copy()

boton_formacion = pygame.Rect(10,10,200,40)

jugador_seleccionado = None
offset_x = 0
offset_y = 0

def guardar_formacion():
    data = {
        "equipo1": equipo1,
        "equipo2": equipo2
    }
    with open("formacion_guardada.json","w") as f:
        json.dump(data,f)

running = True

while running:

    clock.tick(60)

    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = event.pos

            if boton_formacion.collidepoint(event.pos):
                menu_abierto = not menu_abierto

            if menu_abierto:
                for i,f in enumerate(formaciones):
                    rect = pygame.Rect(10,50+i*40,200,35)
                    if rect.collidepoint(event.pos):
                        formacion_actual = f
                        equipo1, equipo2 = obtener_formacion(f)
                        originales1, originales2 = posiciones_originales(f)
                        posiciones_azul = posiciones_base.copy()
                        posiciones_rojo = posiciones_base.copy()
                        menu_abierto = False

            # Selección de jugadores azules
            for i,pos in enumerate(equipo1):
                rect = pygame.Rect(pos[0],pos[1],45,45)
                if rect.collidepoint(mouse_x,mouse_y):
                    jugador_seleccionado = ("azul",i)
                    offset_x = mouse_x - pos[0]
                    offset_y = mouse_y - pos[1]

            # Selección de jugadores rojos
            for i,pos in enumerate(equipo2):
                rect = pygame.Rect(pos[0],pos[1],45,45)
                if rect.collidepoint(mouse_x,mouse_y):
                    jugador_seleccionado = ("rojo",i)
                    offset_x = mouse_x - pos[0]
                    offset_y = mouse_y - pos[1]

        if event.type == pygame.MOUSEBUTTONUP:
            if jugador_seleccionado:
                equipo, indice = jugador_seleccionado
                mouse_rect = pygame.Rect(0,0,45,45)

                if equipo == "azul":
                    for i,pos in enumerate(equipo1):
                        if i != indice:
                            rect = pygame.Rect(pos[0],pos[1],45,45)
                            if rect.colliderect(mouse_rect.move(equipo1[indice])):
                                # Intercambiamos roles y volvemos a posiciones originales
                                equipo1[indice], equipo1[i] = originales1[i], originales1[indice]
                                posiciones_azul[indice], posiciones_azul[i] = posiciones_azul[i], posiciones_azul[indice]

                if equipo == "rojo":
                    for i,pos in enumerate(equipo2):
                        if i != indice:
                            rect = pygame.Rect(pos[0],pos[1],45,45)
                            if rect.colliderect(mouse_rect.move(equipo2[indice])):
                                equipo2[indice], equipo2[i] = originales2[i], originales2[indice]
                                posiciones_rojo[indice], posiciones_rojo[i] = posiciones_rojo[i], posiciones_rojo[indice]

                # Actualizamos coordenadas originales después del intercambio
                originales1 = equipo1.copy()
                originales2 = equipo2.copy()

            jugador_seleccionado = None

        if event.type == pygame.MOUSEMOTION:
            if jugador_seleccionado:
                mouse_x,mouse_y = event.pos
                equipo,indice = jugador_seleccionado
                if equipo == "azul":
                    equipo1[indice] = (mouse_x-offset_x,mouse_y-offset_y)
                if equipo == "rojo":
                    equipo2[indice] = (mouse_x-offset_x,mouse_y-offset_y)

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_s:
                guardar_formacion()

    pantalla.blit(cancha,(0,0))

    # Dibujamos jugadores azules
    for i,pos in enumerate(equipo1):
        pantalla.blit(jugador_azul,pos)
        texto = font.render(posiciones_azul[i],True,(255,255,255))
        pantalla.blit(texto,(pos[0],pos[1]-18))

    # Dibujamos jugadores rojos
    for i,pos in enumerate(equipo2):
        pantalla.blit(jugador_rojo,pos)
        texto = font.render(posiciones_rojo[i],True,(255,255,255))
        pantalla.blit(texto,(pos[0],pos[1]-18))

    pygame.draw.rect(pantalla,(20,20,20),boton_formacion)
    texto = font.render("Formacion: "+formacion_actual,True,(255,255,255))
    pantalla.blit(texto,(20,20))

    if menu_abierto:
        for i,f in enumerate(formaciones):
            rect = pygame.Rect(10,50+i*40,200,35)
            pygame.draw.rect(pantalla,(60,60,60),rect)
            texto = font.render(f,True,(255,255,255))
            pantalla.blit(texto,(60,60+i*40))

    pygame.display.flip()

pygame.quit()