import pygame as pg
import random

import numpy as np


width = 1800
height = 800
size = 20
size_line = 100
movemenet = 3
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

    # Draw roads in Nairobi city style
        yellow = (255, 255, 0)
        white = (255, 255, 255)

    # Horizontal roads
        pg.draw.line(screen, white, (0, 200), (width, 200), size_line)
        pg.draw.line(screen, Black, (0, 200), (width, 200), size_line//10)
        pg.draw.line(screen, white, (0, 400), (width, 400), size_line)
        pg.draw.line(screen, Black, (0, 400), (width, 400), size_line//10)
        pg.draw.line(screen, white, (0, 600), (width, 600), size_line)
        pg.draw.line(screen, Black, (0, 600), (width, 600), size_line//10)

    # Vertical roads
        pg.draw.line(screen, white, (300, 0), (300, height), size_line)
        pg.draw.line(screen, Black, (300, 0), (300, height), size_line//10)
        pg.draw.line(screen, white, (600, 0), (600, height), size_line)
        pg.draw.line(screen, Black, (600, 0), (600, height), size_line//10)
        pg.draw.line(screen, white, (900, 0), (900, height), size_line)
        pg.draw.line(screen, Black, (900, 0), (900, height), size_line//10)
        pg.draw.line(screen, white, (1200, 0), (1200, height), size_line)
        pg.draw.line(screen, Black, (1200, 0), (1200, height), size_line//10)
        pg.draw.line(screen, white, (1500, 0), (1500, height), size_line)
        pg.draw.line(screen, Black, (1500, 0), (1500, height), size_line//10)
        circl={
            "x":width//2,
            "y":height//2
        }

    # Diagonal roads for city character
        pg.draw.circle(screen, yellow, (circl["x"], circl["y"]), size_line * 1, size_line // 1)
           
        for player in players:
            p1,p2=player ["x"],player["y"]
            c1,c2=circl["x"],circl["y"]
            dic=np.sqrt((p1-c1)**2+(p2-c2)**2)
            hit_radius = size + size_line
            if dic< hit_radius:
                print("yes")
                
            
           
    # Draw all players in a loop
        for player in players:
            pg.draw.rect(screen, player["color"], (player["x"], player["y"], size, size))

        pg.display.flip()

pg.quit()
