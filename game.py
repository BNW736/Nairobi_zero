import pygame as pg
import random

width = 1800
height = 800
size = 20
size_line = 10
movemenet = 8
Black = (0, 0, 0)

# Create 5 players with a loop
players = []
for i in range(5):
    players.append(
        {
            "x": (i + 1) * (width // 6),
            "y": height // 2,
            "color": (
                random.randint(100, 255),
                random.randint(100, 255),
                random.randint(100, 255),
            ),
        }
    )
pg.init()
screen = pg.display.set_mode((width, height))
running = True
while running:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False
    pg.draw.line(screen, (175, 55, 250), (width // 2, 0), (width // 2, height), size_line)
    key = pg.key.get_pressed()

    # Handle input for each player
    for i in range(5):
        if key[pg.K_1 + i]:  # Players 1-5 use keys 1-5
            if key[pg.K_LEFT]:
                players[i]["x"] = players[i]["x"] - movemenet
            if key[pg.K_RIGHT]:
                players[i]["x"] = players[i]["x"] + movemenet
            if key[pg.K_UP]:
                players[i]["y"] = players[i]["y"] - movemenet
            if key[pg.K_DOWN]:
                players[i]["y"] = players[i]["y"] + movemenet

            # Boundary checking for each player
            if players[i]["x"] > width - size:
                players[i]["x"] = width - size
            if players[i]["x"] < 0:
                players[i]["x"] = 0
            if players[i]["y"] > height - size:
                players[i]["y"] = height - size
            if players[i]["y"] < 0:
                players[i]["y"] = 0

    screen.fill(Black)

    # Draw all players in a loop
    for player in players:
        pg.draw.rect(screen, player["color"], (player["x"], player["y"], size, size))

    pg.display.flip()

pg.quit()
