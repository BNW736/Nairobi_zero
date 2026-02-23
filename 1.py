import pygame as pg
import random
import gymnasium as gym
import numpy as np
from stable_baselines3 import PPO
import numpy as np
import time


class NairobiCityEnv(
    gym.Env,
):
    # It defines the environment
    def __init__(self, render_mode=False):
        self.number_of_players = 2
        self.render_mode = render_mode 
        self.WIDTH = 1800
        self.HEIGHT = 800
        self.PLAYER_SIZE = 20
        self.ROAD_WIDTH = 100
        self.HALF_ROAD = self.ROAD_WIDTH // 2
        self.MOVEMENT_SPEED = 5
        self.fps=60
        self.timer = 0.0
        self.state = 0
        # COLORS
        self.BLACK = (0, 0, 0)
        self.WHITE = (255, 255, 255)
        self.YELLOW = (255, 255, 0)
        self.GREEN = (0, 255, 0)
        self.RED = (255, 0, 0)
        self.BLUE = (0, 0, 255)
        self.ROAD_GRAY = (50, 50, 50)
        # DURATION
        self.durations = [3.0, 1.0, 4.0]
        
        # ROAD LOCATIONS (The Centers)
        self.VERTICAL_ROADS_X = [300, 600, 900, 1200, 1500]
        self.HORIZONTAL_ROADS_Y = [200, 400, 600]
        self.CENTER_POINT = {"x": self.WIDTH // 2, "y": self.HEIGHT // 2}
        self.clock = pg.time.Clock()
        self.dt = 1.0 / self.fps 
        self.action_space = gym.spaces.MultiDiscrete([4] * self.number_of_players)
        self.number = self.number_of_players * 2
        self.observation_space = gym.spaces.Box(
            low=0,
            high=max(self.WIDTH, self.HEIGHT),
            shape=(self.number,),
            dtype=np.float64,
        )
        if self.render_mode == True:
            self.screen = pg.display.set_mode((self.WIDTH, self.HEIGHT))
            pg.display.set_caption("Nairobi City ")

    def check_on_road(self, player_x, player_y):
        for road_x in self.VERTICAL_ROADS_X:
            distance = abs(player_x - road_x)
            if distance < self.HALF_ROAD:
                return True

        # B. Check Horizontal Roads (Distance from Y center)
        for road_y in self.HORIZONTAL_ROADS_Y:
            distance = abs(player_y - road_y)
            if distance < self.HALF_ROAD:
                return True

        dist_circle = np.sqrt(
            (player_x - self.CENTER_POINT["x"]) ** 2
            + (player_y - self.CENTER_POINT["y"]) ** 2
        )
        if dist_circle < 100:
            return True  # Safe!

        # If all checks fail, you are OFF ROAD
        return False

    def reset(self, seed=None, options=None):
        # Create 5 players
        self.players = []
        for i in range(self.number_of_players):
            self.players.append(
                {
                    "id": i + 1,
                    "x": (i + 1) * (self.WIDTH // 3),
                    "y": self.HEIGHT // 3,  # Start them in the middle
                    "color": self.GREEN,
                    "finished": False,
                }
            )

        self.traffic_lights_x = []
        for road_x in self.VERTICAL_ROADS_X:
            self.traffic_lights_x.append(
                {"x": road_x, "state": random.randint(0, 2), "timer": 0.0}
            )
        self.traffic_lights_y = []
        for road_y in self.HORIZONTAL_ROADS_Y:
            self.traffic_lights_y.append(
                {"y": road_y, "state": random.randint(1, 2), "timer": 0.0}
            )
        all_coords = []
        for p in self.players:
            all_coords.extend([p["x"], p["y"]])
        obs = np.array(all_coords, dtype=np.float64)
        info = {}
        return obs, info

    def step(self, action):
        reward = 0
        
        for i, player in enumerate(self.players):
            self.timer=self.timer+self.dt
            # Skip if finished
            if player["finished"]:
                reward = reward + 20
                continue

            move = action[i]

            if move == 0:
                player["x"] -= self.MOVEMENT_SPEED
            if move == 1:
                player["x"] += self.MOVEMENT_SPEED
            if move == 2:
                player["y"] -= self.MOVEMENT_SPEED
            if move == 3:
                player["y"] += self.MOVEMENT_SPEED

            # Screen Boundary Checks (Keep inside window)
            player["x"] = np.clip(player["x"], 0, self.WIDTH - self.PLAYER_SIZE)
            player["y"] = np.clip(player["y"], 0, self.HEIGHT - self.PLAYER_SIZE)

            # --- THE PENALTY CHECK ---

            dist_to_center = np.sqrt(
                (player["x"] - self.CENTER_POINT["x"]) ** 2
                + (player["y"] - self.CENTER_POINT["y"]) ** 2
            )

            if dist_to_center < 50:
                player["finished"] = True
                player["color"] = self.BLUE
                print(f"Player {player['id']} Reached City Center!")
                reward = reward + 100
            elif self.check_on_road(player["x"], player["y"]):
                player["color"] = self.GREEN
                reward = reward + 30
                reward -= 0.1 + (0.1 * dist_to_center)
    
            else:
                player["color"] = self.RED
                reward = reward - 30
                reward -= 0.1 + (0.1 * dist_to_center)
                
            for light in self.traffic_lights_x:
                light["timer"] += self.dt
                if light["timer"] >= self.durations[light["state"]]:
                    light["timer"] = 0.0
                    light["state"] = (light["state"] + 1) % 3
                """if light["state"] == 0: 
                    light_color = self.GREEN
                elif light["state"] == 1:
                    light_color = self.YELLOW
                else: 
                    light_color = self.RED"""
               

            for light in self.traffic_lights_y:
                light["timer"] += self.dt
                if light["timer"] >= self.durations[light["state"]]:
                    light["timer"] = 0.0
                    light["state"] = (light["state"] + 1) % 3
                """if light["state"] == 0: 
                    light_color = self.GREEN
                elif light["state"] == 1:
                    light_color = self.YELLOW
                else: 
                    light_color = self.RED"""
            all_coords=[]
            for p in self.players:
                all_coords.extend([p["x"], p["y"]])
            obs = np.array(all_coords, dtype=np.float64)

      
        # 5. Global Termination Check
        terminated = all(p["finished"] for p in self.players)
        truncated = False

        return obs, reward, terminated, truncated, {}

    def render(self, seed=None, options=None):
        self.screen.fill(self.GREEN)

        # Draw Roads
        for y in self.HORIZONTAL_ROADS_Y:
            pg.draw.line(
                self.screen, self.BLACK, (0, y), (self.WIDTH, y), self.ROAD_WIDTH
            )
            pg.draw.line(
                self.screen, self.WHITE, (0, y), (self.WIDTH, y), self.ROAD_WIDTH // 12
            )

        for x in self.VERTICAL_ROADS_X:
            pg.draw.line(
                self.screen, self.BLACK, (x, 0), (x, self.HEIGHT), self.ROAD_WIDTH
            )
            pg.draw.line(
                self.screen, self.WHITE, (x, 0), (x, self.HEIGHT), self.ROAD_WIDTH // 12
            )

        # Draw X traffic lights
        for light in self.traffic_lights_x:
            if light["state"] == 0: 
                light_color = self.GREEN
            elif light["state"] == 1:
                light_color = self.YELLOW
            else: 
                light_color = self.RED

            left_line_x = light["x"] - 50
            right_line_x = light["x"] + 50
            pg.draw.line(self.screen, light_color, (left_line_x, 0), (left_line_x, self.HEIGHT), 10)
            pg.draw.line(self.screen, light_color, (right_line_x, 0), (right_line_x, self.HEIGHT), 10)
    
        # Draw Y traffic lights
        for light in self.traffic_lights_y:
            if light["state"] == 0: 
                light_color = self.GREEN
            elif light["state"] == 1:
                light_color = self.YELLOW
            else: 
                light_color = self.RED

            left_line_y = light["y"] - 50
            right_line_y = light["y"] + 50
            pg.draw.line(self.screen, light_color, (0, left_line_y), (self.WIDTH, left_line_y), 10)
            pg.draw.line(self.screen, light_color, (0, right_line_y), (self.WIDTH, right_line_y), 10)

        pg.draw.circle(self.screen, self.YELLOW, (self.CENTER_POINT["x"], self.CENTER_POINT["y"]), 100)
        pg.draw.circle(self.screen, self.BLACK, (self.CENTER_POINT["x"], self.CENTER_POINT["y"]), 80)
        # Draw Center Roundabout
        pg.draw.circle(
            self.screen,
            self.YELLOW,
            (self.CENTER_POINT["x"], self.CENTER_POINT["y"]),
            100,
        )
        pg.draw.circle(
            self.screen,
            self.BLACK,
            (self.CENTER_POINT["x"], self.CENTER_POINT["y"]),
            80,
        )
        # Draw Players
        for player in self.players:
            pg.draw.rect(
                self.screen,
                player["color"],
                (player["x"], player["y"], self.PLAYER_SIZE, self.PLAYER_SIZE),
            )

        pg.display.flip()
        self.clock.tick(self.fps) 
        
        
# Train without rendering
env = NairobiCityEnv()
obs, _ = env.reset()
model = PPO("MlpPolicy", env, verbose=1, learning_rate=0.003, ent_coef=0)
model.learn(total_timesteps=1)
model.save("goal")


print("Environment Ready! Playing...")


play_env = NairobiCityEnv(render_mode=True)
obs, _ = play_env.reset()

for _ in range(10000):
    action, _ = model.predict(obs)
    obs, reward, terminated, truncated, info = play_env.step(action)
    play_env.render()
    if terminated:
        print("Game Finished! Resetting...")
        obs, _ = play_env.reset()
    time.sleep(0.05)

play_env.close()
