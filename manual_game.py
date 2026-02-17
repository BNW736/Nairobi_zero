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
timer=0.0
state=0

# COLORS
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
YELLOW = (255, 255, 0)
GREEN = (0, 255, 0)      
RED = (255, 0, 0)       
BLUE = (0, 0, 255)       
ROAD_GRAY = (50, 50, 50)
#DURATION
durations = [3.0, 1.0, 4.0]

# ROAD LOCATIONS (The Centers)
VERTICAL_ROADS_X = [300, 600, 900, 1200, 1500]
HORIZONTAL_ROADS_Y = [200, 400, 600]
CENTER_POINT = {"x": WIDTH // 2, "y": HEIGHT // 2} 

def check_on_road(player_x, player_y):
    for road_x in VERTICAL_ROADS_X:
        distance = abs(player_x - road_x)
        if distance < HALF_ROAD:
            return True  

    # B. Check Horizontal Roads (Distance from Y center)
    for road_y in HORIZONTAL_ROADS_Y:
        distance = abs(player_y - road_y)
        if distance < HALF_ROAD:
            return True  

    dist_circle = np.sqrt((player_x - CENTER_POINT["x"])**2 + (player_y - CENTER_POINT["y"])**2)
    if dist_circle < 100:
        return True # Safe!

    # If all checks fail, you are OFF ROAD
    return False

# --- 3. INITIALIZATION ---
pg.init()
screen = pg.display.set_mode((WIDTH, HEIGHT))
pg.display.set_caption("Nairobi_Zero")
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

traffic_lights_x = []

for road_x in VERTICAL_ROADS_X:
    traffic_lights_x.append({
        "x": road_x,
        "state": random.randint(0, 2), 
        "timer": 0.0
    })
traffic_lights_y=[]
for road_y in HORIZONTAL_ROADS_Y:
    traffic_lights_y.append({
        "y": road_y,
        "state": random.randint(1, 2), 
        "timer": 0.0
    })

running = True
while running:
 
    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False

    dt = clock.tick(FPS) / 1000.0  #0.016 seconds TO SEE TIME BETTER
    timer += dt
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
        
        if dist_to_center < 50:
            player["finished"] = True
            player["color"] = BLUE
            print(f"Player {player['id']} Reached City Center!")
        
        # 2. Are we on the road?
        elif check_on_road(player["x"], player["y"]):
            player["color"] = GREEN  
        else:
            player["color"] = RED   

    # --- DRAWING ---
    screen.fill(GREEN)

    # Draw Roads
    for y in HORIZONTAL_ROADS_Y:
        pg.draw.line(screen, BLACK, (0, y), (WIDTH, y), ROAD_WIDTH)
        pg.draw.line(screen, WHITE, (0, y), (WIDTH, y), ROAD_WIDTH // 12)
        

    for x in VERTICAL_ROADS_X:
        pg.draw.line(screen, BLACK, (x, 0), (x, HEIGHT), ROAD_WIDTH)
        pg.draw.line(screen, WHITE, (x, 0), (x, HEIGHT), ROAD_WIDTH // 12)
        
    
    for light in traffic_lights_x:
        light["timer"] += dt
        
      
        if light["timer"] >= durations[light["state"]]:
            light["timer"] = 0.0
            light["state"] = (light["state"] + 1) % 3

        # 2. DETERMINE COLOR FOR THIS LIGHT
        if light["state"] == 0:
            light_color = GREEN
        elif light["state"] == 1:
            light_color = YELLOW
        else:
            light_color = RED

       
        left_line_x = light["x"] - 50
        right_line_x = light["x"] + 50
        
        # Draw Left Boundary
        pg.draw.line(screen, light_color, (left_line_x, 0), (left_line_x, HEIGHT), 10)
        # Draw Right Boundary
        pg.draw.line(screen, light_color, (right_line_x, 0), (right_line_x, HEIGHT), 10)
    
    for light in traffic_lights_y:
        light["timer"] += dt
        
      
        if light["timer"] >= durations[light["state"]]:
            light["timer"] = 0.0
            light["state"] = (light["state"] + 1) % 3

        # 2. DETERMINE COLOR FOR THIS LIGHT
        if light["state"] == 0:
            light_color = GREEN
        elif light["state"] == 1:
            light_color = YELLOW
        else:
            light_color = RED

        # 3. DRAW THE LINES (Dynamic Math)
        # Road width is 100. So boundaries are Center - 50 and Center + 50.
        left_line_y = light["y"] - 50
        right_line_y = light["y"] + 50
        
        # Draw Left Boundary
        pg.draw.line(screen, light_color, (0, left_line_y), (WIDTH, left_line_y), 10)
        # Draw Right Boundary
        pg.draw.line(screen, light_color, (0, right_line_y), (WIDTH, right_line_y), 10)
    # Draw Center Roundabout
    pg.draw.circle(screen, YELLOW, (CENTER_POINT["x"], CENTER_POINT["y"]), 100)
    pg.draw.circle(screen, BLACK, (CENTER_POINT["x"], CENTER_POINT["y"]), 80)
    # Draw Players
    for player in players:
        pg.draw.rect(screen, player["color"], (player["x"], player["y"], PLAYER_SIZE, PLAYER_SIZE))
        
    pg.display.flip()
    clock.tick(FPS)

pg.quit()