import pygame as pg
import random
import numpy as np

WIDTH = 1800
HEIGHT = 800
PLAYER_SIZE = 20
ROAD_WIDTH = 100
HALF_ROAD = ROAD_WIDTH // 2  
MOVEMENT_SPEED = 5
FPS = 60

# COLORS
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
YELLOW = (255, 255, 0)
GREEN = (0, 255, 0)      
RED = (255, 0, 0)       
BLUE = (0, 0, 255)       
ROAD_GRAY = (50, 50, 50)

# ROAD LOCATIONS (The Centers)
VERTICAL_ROADS_X = [300, 600, 900, 1200, 1500]
HORIZONTAL_ROADS_Y = [200, 400, 600]
CENTER_POINT = {"x": WIDTH // 2, "y": HEIGHT // 2} 

def check_on_road(player_x, player_y):
    for road_x in VERTICAL_ROADS_X:
        distance = abs(player_x - road_x)
        if distance < HALF_ROAD:
            return True  # Safe!

    # B. Check Horizontal Roads (Distance from Y center)
    for road_y in HORIZONTAL_ROADS_Y:
        distance = abs(player_y - road_y)
        if distance < HALF_ROAD:
            return True  # Safe!

    dist_circle = np.sqrt((player_x - CENTER_POINT["x"])**2 + (player_y - CENTER_POINT["y"])**2)
    if dist_circle < 100:
        return True # Safe!

    # If all checks fail, you are OFF ROAD
    return False

# --- 3. INITIALIZATION ---
pg.init()
screen = pg.display.set_mode((WIDTH, HEIGHT))
pg.display.set_caption("Nairobi_Zero: Manual Test (Red = Penalty)")
clock = pg.time.Clock()

# Create 5 players
players = []
for i in range(5):
    players.append({
        "id": i + 1,
        "x": (i + 1) * (WIDTH // 6),
        "y": HEIGHT // 2, # Start them in the middle
        "color": GREEN,
        "finished": False
    })


running = True
while running:
 
    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False

  
    keys = pg.key.get_pressed()

    for i, player in enumerate(players):
        # Skip if finished
        if player["finished"]:
            continue

        # Move logic (Press 1-5 + Arrows)
        if keys[pg.K_1 + i]: 
            if keys[pg.K_LEFT]:
                player["x"] -= MOVEMENT_SPEED
            if keys[pg.K_RIGHT]:
                player["x"] += MOVEMENT_SPEED
            if keys[pg.K_UP]:
                player["y"] -= MOVEMENT_SPEED
            if keys[pg.K_DOWN]:
                player["y"] += MOVEMENT_SPEED

        # Screen Boundary Checks (Keep inside window)
        player["x"] = np.clip(player["x"], 0, WIDTH - PLAYER_SIZE)
        player["y"] = np.clip(player["y"], 0, HEIGHT - PLAYER_SIZE)

        # --- THE PENALTY CHECK ---
        
        dist_to_center = np.sqrt((player["x"] - CENTER_POINT["x"])**2 + (player["y"] - CENTER_POINT["y"])**2)
        
        if dist_to_center < 50: # Close enough to center
            player["finished"] = True
            player["color"] = BLUE
            print(f"Player {player['id']} Reached City Center!")
        
        # 2. Are we on the road?
        elif check_on_road(player["x"], player["y"]):
            player["color"] = GREEN  # Safe
        else:
            player["color"] = RED    # PENALTY! (Off-road)

    # --- DRAWING ---
    screen.fill(BLACK)

    # Draw Roads
    for y in HORIZONTAL_ROADS_Y:
        pg.draw.line(screen, WHITE, (0, y), (WIDTH, y), ROAD_WIDTH)
        pg.draw.line(screen, ROAD_GRAY, (0, y), (WIDTH, y), ROAD_WIDTH // 10)

    for x in VERTICAL_ROADS_X:
        pg.draw.line(screen, WHITE, (x, 0), (x, HEIGHT), ROAD_WIDTH)
        pg.draw.line(screen, ROAD_GRAY, (x, 0), (x, HEIGHT), ROAD_WIDTH // 10)

    # Draw Center Roundabout
    pg.draw.circle(screen, YELLOW, (CENTER_POINT["x"], CENTER_POINT["y"]), 100)
    pg.draw.circle(screen, BLACK, (CENTER_POINT["x"], CENTER_POINT["y"]), 80) # Donut hole

    # Draw Players
    for player in players:
        pg.draw.rect(screen, player["color"], (player["x"], player["y"], PLAYER_SIZE, PLAYER_SIZE))
        
        # Draw ID number
        font = pg.font.SysFont(None, 24)
        img = font.render(str(player["id"]), True, BLACK if player["color"] == WHITE else WHITE)
        screen.blit(img, (player["x"], player["y"] - 20))

    pg.display.flip()
    clock.tick(FPS)

pg.quit()