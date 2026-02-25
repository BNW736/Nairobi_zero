import pygame as pg
import random
import gymnasium as gym
import numpy as np
from stable_baselines3 import PPO
import numpy as np
import time

"""This project is a learning and proof-of-concept initiative designed
to explore a smarter way to reduce traffic congestion in Nairobi.
The idea is that once a vehicle enters a designated control zone,
an AI system temporarily takes control of the car and autonomously navigates it
to its destination. The AI would optimize routing, coordinate with other vehicles, 
and avoid collisions and traffic bottlenecks, with the goal of improving traffic flow, reducing 
congestion, and enhancing road safety"""
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
        #identifying what the bot can see
        self.action_space = gym.spaces.MultiDiscrete([4] * self.number_of_players)
        self.num_lights = len(self.VERTICAL_ROADS_X) + len(self.HORIZONTAL_ROADS_Y)
        self.obs_size = (self.number_of_players * 2) + self.num_lights
        
        self.observation_space = gym.spaces.Box(
            low=0,
            high=1.0,
            shape=(self.obs_size,),
            dtype=np.float32,
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
        """This is the player charateristics and the road in the environment"""
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
        
        obs = self._get_obs()
        info = {}
        return obs, info
    
    def update_lights(self):
        # Update timers and states for X-axis roads to change the colors
        for light in self.traffic_lights_x:
            light["timer"] += self.dt
            current_state = light["state"]
            # Check if it's time to change the color based on self.durations
            if light["timer"] >= self.durations[current_state]:
                light["timer"] = 0.0 # Reset timer
                light["state"] = (current_state + 1) % 3 # Cycle: 0 (Green) -> 1 (Yellow) -> 2 (Red)

        # Update timers and states for Y-axis roads
        for light in self.traffic_lights_y:
            light["timer"] += self.dt
            current_state = light["state"]
            if light["timer"] >= self.durations[current_state]:
                light["timer"] = 0.0
                light["state"] = (current_state + 1) % 3
    #With some help from  ai 
    def _get_obs(self):
        """THIS is the ods the ai see in the environment"""
        obs_list = []
        # 1. Normalize player coordinates (divide by screen dimensions)
        for p in self.players:
            obs_list.extend([p["x"] / self.WIDTH, p["y"] / self.HEIGHT])
            
        # 2. Normalize traffic light states (divide by max state, which is 2)
        for light_x in self.traffic_lights_x:
            obs_list.append(light_x["state"] / 2.0)
        for light_y in self.traffic_lights_y:
            obs_list.append(light_y["state"] / 2.0)
            
        # 3. Cast to float32 (PyTorch prefers float32 over float64)
        return np.array(obs_list, dtype=np.float32)
                
    def step(self, action):
        """This is the step that tell the ai what it can do and the penatly for speciftic movements and 
        the goal of the game"""
        #To loop the color
        self.update_lights()
        reward = 0
        
        for i, player in enumerate(self.players):
            self.timer=self.timer+self.dt
            # Skip if finished
            if player["finished"]:
                reward = reward + 20
                continue
            #The actions the ai can make
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

            # Check Red Light Violations BEFORE the road check
            red_light_penalty = 0
            
            # Check if crossing vertical roads on a red light
            for light_x in self.traffic_lights_x:
                if light_x["state"] == 2 and abs(player["x"] - light_x["x"]) < self.HALF_ROAD:
                    red_light_penalty -= 20 # Strong penalty for running a red
                    
            # Check if crossing horizontal roads on a red light
            for light_y in self.traffic_lights_y:
                if light_y["state"] == 2 and abs(player["y"] - light_y["y"]) < self.HALF_ROAD:
                    red_light_penalty -= 20 

            # Apply the standard rewards and the new penalty
            if dist_to_center < 50:
                player["finished"] = True
                player["color"] = self.BLUE
                print(f"Player {player['id']} Reached City Center!")
                reward = reward + 100
                
            elif self.check_on_road(player["x"], player["y"]):
                player["color"] = self.GREEN
                reward = reward + 30 + red_light_penalty # Add the penalty here!
                reward -= 0.1 + (0.1 * dist_to_center)
                
            else:
                player["color"] = self.RED
                reward = reward - 30 + red_light_penalty # And here!
                reward -= 0.1 + (0.1 * dist_to_center)
            
        # Get the updated observation using our new helper method
        obs = self._get_obs()

        # 5. Global Termination Check
        terminated = all(p["finished"] for p in self.players)
        truncated = False

        return obs, reward, terminated, truncated, {}

    def render(self, seed=None, options=None):
        """Green is the back ground to represent grass and the lines the road """
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
        for light_x in self.traffic_lights_x:
            # Determine color based on this specific light's state
            if light_x["state"] == 0: 
                light_color_x = self.GREEN
            elif light_x["state"] == 1:
                light_color_x = self.YELLOW
            else: 
                light_color_x = self.RED

            left_line_x = light_x["x"] - 50
            right_line_x = light_x["x"] + 50
            pg.draw.line(self.screen, light_color_x, (left_line_x, 0), (left_line_x, self.HEIGHT), 10)
            pg.draw.line(self.screen, light_color_x, (right_line_x, 0), (right_line_x, self.HEIGHT), 10)
        # Draw Y traffic lights
        for light_y in self.traffic_lights_y:
            if light_y["state"] == 0: 
                light_color = self.GREEN
            elif light_y["state"] == 1:
                light_color = self.YELLOW
            else: 
                light_color = self.RED

            left_line_y = light_y["y"] - 50
            right_line_y = light_y["y"] + 50
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
model = PPO("MlpPolicy", env, verbose=1, learning_rate=0.0003)
#increase it to give the ai more time to learn
model.learn(total_timesteps=500000)
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
