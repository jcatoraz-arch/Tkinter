import pygame
import os
import json
import tkinter as tk
from tkinter import messagebox

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

formacion_azul = "4-4-2"
formacion_rojo = "4-4-2"
menu_formaciones_azul = False
menu_formaciones_rojo = False

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

def load_teams():
    try:
        with open(os.path.join(ruta_base, "teams.json"), "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return {
            "Borussia Dortmund": {
                "formation": "4-4-2",
                "players": ["Ter Stegen", "Pique", "Ramos", "Varane", "Alba", "Busquets", "Pedri", "De Jong", "Dembele", "Messi", "Suarez"]
            },
            "Porto": {
                "formation": "4-4-2",
                "players": ["Casillas", "Carvajal", "Pepe", "Ramos", "Marcelo", "Modric", "Kroos", "Casemiro", "Bale", "Benzema", "Ronaldo"]
            },
            "Estudiantes de Rio Cuarto": {
                "formation": "4-4-2",
                "players": ["Buffon", "Abate", "Barzagli", "Bonucci", "Evra", "Pirlo", "Verratti", "Marchisio", "Robinho", "Balotelli", "Cassano"]
            },
            "Cambaceres": {
                "formation": "4-4-2",
                "players": ["Neuer", "Lahm", "Boateng", "Hummels", "Alaba", "Schweinsteiger", "Khedira", "Muller", "Robben", "Gotze", "Lewandowski"]
            }
        }

def save_teams():
    with open(os.path.join(ruta_base, "teams.json"), "w") as f:
        json.dump(teams_data, f, indent=4)

teams_data = load_teams()
current_team = None
current_team_red = None
current_team_color = None

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

equipo1, _ = obtener_formacion(formacion_azul)
_, equipo2 = obtener_formacion(formacion_rojo)
originales1 = equipo1.copy()
originales2 = equipo2.copy()

# Listas de posiciones independientes para cada equipo
posiciones_azul = posiciones_base.copy()
posiciones_rojo = posiciones_base.copy()

boton_formacion_azul = pygame.Rect(10,10,200,40)
boton_formacion_rojo = pygame.Rect(ANCHO - 210,10,200,40)
boton_equipos = pygame.Rect(10, ALTO - 50, 200, 40)
boton_equipos_rojo = pygame.Rect(ANCHO - 210, ALTO - 50, 200, 40)
boton_guardar = pygame.Rect(10, mitad - 20, 30, 30)
menu_equipos_abierto = False
menu_equipos_rojo_abierto = False

jugador_seleccionado = None
offset_x = 0
offset_y = 0
last_collided_azul = None
last_collided_rojo = None
selected_player = None

def guardar_formacion():
    data = {
        "equipo1": equipo1,
        "equipo2": equipo2
    }
    with open("formacion_guardada.json","w") as f:
        json.dump(data,f)


def guardar_cambios_equipo():

    # guardar equipo azul
    if current_team:
        teams_data[current_team]["players"] = posiciones_azul.copy()
        teams_data[current_team]["formation"] = formacion_azul

    # guardar equipo rojo
    if current_team_red:
        teams_data[current_team_red]["players"] = posiciones_rojo.copy()
        teams_data[current_team_red]["formation"] = formacion_rojo

    save_teams()

def confirmar_guardado():

    root = tk.Tk()
    root.withdraw()

    respuesta = messagebox.askyesno(
        "Confirmar guardado",
        "¿Estas seguro que deseas guardar la formación de este plantel?"
    )

    root.destroy()

    return respuesta
def dibujar_boton(rect, texto):

    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()

    color = (40,40,40)

    if rect.collidepoint(mouse):
        color = (80,80,80)

    if rect.collidepoint(mouse) and click[0]:
        color = (20,20,20)

    pygame.draw.rect(pantalla, color, rect)
    pygame.draw.rect(pantalla, (255,255,255), rect, 2)

    texto_render = font.render(texto, True, (255,255,255))
    text_rect = texto_render.get_rect(center=rect.center)
    pantalla.blit(texto_render, text_rect)

running = True

while running:

    clock.tick(60)

    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = event.pos

            if boton_formacion_azul.collidepoint(event.pos):
                menu_formaciones_azul = not menu_formaciones_azul
                menu_formaciones_rojo = False

            if boton_formacion_rojo.collidepoint(event.pos):
                menu_formaciones_rojo = not menu_formaciones_rojo
                menu_formaciones_azul = False

            if boton_equipos.collidepoint(event.pos):
                menu_equipos_abierto = not menu_equipos_abierto

            if boton_equipos_rojo.collidepoint(event.pos):
                menu_equipos_rojo_abierto = not menu_equipos_rojo_abierto

            if boton_guardar.collidepoint(event.pos):
                if confirmar_guardado():
                    guardar_cambios_equipo()

            if menu_formaciones_azul:
                for i,f in enumerate(formaciones):
                    rect = pygame.Rect(10,50+i*40,200,35)
                    if rect.collidepoint(event.pos):
                        formacion_azul = f
                        equipo1, _ = obtener_formacion(f)
                        originales1 = equipo1.copy()
                        posiciones_azul = teams_data[current_team]["players"].copy() if current_team else posiciones_base.copy()
                        menu_formaciones_azul = False
                        if current_team_color == 'azul' and current_team:
                            teams_data[current_team]["formation"] = f
                            save_teams()

            if menu_formaciones_rojo:
                for i,f in enumerate(formaciones):
                    rect = pygame.Rect(ANCHO - 210,50+i*40,200,35)
                    if rect.collidepoint(event.pos):
                        formacion_rojo = f
                        _, equipo2 = obtener_formacion(f)
                        originales2 = equipo2.copy()
                        posiciones_rojo = teams_data[current_team_red]["players"].copy() if current_team_red else posiciones_base.copy()
                        menu_formaciones_rojo = False
                        if current_team_color == 'rojo' and current_team_red:
                            teams_data[current_team_red]["formation"] = f
                            save_teams()

            if menu_equipos_abierto:
                for i, team in enumerate(teams_data.keys()):
                    rect = pygame.Rect(10, ALTO - 50 - 40*(i+1), 200, 35)
                    if rect.collidepoint(event.pos):
                        current_team = team
                        current_team_color = 'azul'
                        formacion_azul = teams_data[team]["formation"]
                        equipo1, _ = obtener_formacion(formacion_azul)
                        originales1, _ = posiciones_originales(formacion_azul)
                        posiciones_azul = teams_data[team]["players"].copy()
                        posiciones_rojo = teams_data[current_team_red]["players"].copy() if current_team_red else posiciones_base.copy()
                        menu_equipos_abierto = False

            if menu_equipos_rojo_abierto:
                for i, team in enumerate(teams_data.keys()):
                    rect = pygame.Rect(ANCHO - 210, ALTO - 50 - 40*(i+1), 200, 35)
                    if rect.collidepoint(event.pos):
                        current_team_red = team
                        current_team_color = 'rojo'
                        formacion_rojo = teams_data[team]["formation"]
                        _, equipo2 = obtener_formacion(formacion_rojo)
                        originales2 = equipo2.copy()
                        posiciones_rojo = teams_data[team]["players"].copy()
                        posiciones_azul = teams_data[current_team]["players"].copy() if current_team else posiciones_base.copy()
                        menu_equipos_rojo_abierto = False

            # Player selection logic
            clicked_player = None
            clicked_team = None
            clicked_index = None

            for i, pos in enumerate(equipo1):
                rect = pygame.Rect(pos[0], pos[1], 45, 45)
                if rect.collidepoint(mouse_x, mouse_y):
                    clicked_player = pos
                    clicked_team = "azul"
                    clicked_index = i
                    break

            if clicked_player is None:
                for i, pos in enumerate(equipo2):
                    rect = pygame.Rect(pos[0], pos[1], 45, 45)
                    if rect.collidepoint(mouse_x, mouse_y):
                        clicked_player = pos
                        clicked_team = "rojo"
                        clicked_index = i
                        break

            if clicked_player is not None:

                # primera selección
                if selected_player is None:
                    selected_player = (clicked_team, clicked_index)

                else:
                    selected_team, selected_index = selected_player

                    # SOLO intercambiar si es el mismo equipo
                    if selected_team == clicked_team:

                        if selected_team == "azul":
                            posiciones_azul[selected_index], posiciones_azul[clicked_index] = (
                                posiciones_azul[clicked_index],
                                posiciones_azul[selected_index]
                            )

                        elif selected_team == "rojo":
                            posiciones_rojo[selected_index], posiciones_rojo[clicked_index] = (
                                posiciones_rojo[clicked_index],
                                posiciones_rojo[selected_index]
                            )

                    # deseleccionar siempre
                    selected_player = None



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
        text_rect = texto.get_rect(center=(pos[0]+22.5, pos[1]-12))
        pantalla.blit(texto,text_rect)

    # Highlight selected player
    if selected_player:
        equipo, idx = selected_player
        pos = equipo1[idx] if equipo == "azul" else equipo2[idx]
        pygame.draw.circle(pantalla, (255, 255, 0), (pos[0] + 22, pos[1] + 22), 30, 3)

    dibujar_boton(boton_formacion_azul,"Formacion Azul: "+formacion_azul)
    dibujar_boton(boton_formacion_rojo,"Formacion Rojo: "+formacion_rojo)

    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()

    color_guardar = (120,120,0)

    if boton_guardar.collidepoint(mouse):
        color_guardar = (170,170,0)

    if boton_guardar.collidepoint(mouse) and click[0]:
        color_guardar = (80,80,0)

    dibujar_boton(boton_guardar,"G")
    dibujar_boton(boton_equipos,"Equipo Azul: " + (current_team if current_team else "Ninguno"))
    dibujar_boton(boton_equipos_rojo,"Equipo Rojo: " + (current_team_red if current_team_red else "Ninguno"))

    if menu_formaciones_azul:
        for i,f in enumerate(formaciones):
            rect = pygame.Rect(10,50+i*40,200,35)
            pygame.draw.rect(pantalla,(60,60,60),rect)
            texto = font.render(f,True,(255,255,255))
            text_rect = texto.get_rect(center=rect.center)
            pantalla.blit(texto,text_rect)

    if menu_formaciones_rojo:
        for i,f in enumerate(formaciones):
            rect = pygame.Rect(ANCHO - 210,50+i*40,200,35)
            pygame.draw.rect(pantalla,(60,60,60),rect)
            texto = font.render(f,True,(255,255,255))
            text_rect = texto.get_rect(center=rect.center)
            pantalla.blit(texto,text_rect)

    if menu_equipos_abierto:
        for i, team in enumerate(teams_data.keys()):
            rect = pygame.Rect(10, ALTO - 50 - 40*(i+1), 200, 35)
            pygame.draw.rect(pantalla,(60,60,60),rect)
            texto = font.render(team, True, (255,255,255))
            text_rect = texto.get_rect(center=rect.center)
            pantalla.blit(texto,text_rect)

    if menu_equipos_rojo_abierto:
        for i, team in enumerate(teams_data.keys()):
            rect = pygame.Rect(ANCHO - 210, ALTO - 50 - 40*(i+1), 200, 35)
            pygame.draw.rect(pantalla,(60,60,60),rect)
            texto = font.render(team, True, (255,255,255))
            text_rect = texto.get_rect(center=rect.center)
            pantalla.blit(texto,text_rect)

    pygame.display.flip()

pygame.quit()