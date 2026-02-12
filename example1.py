# A simple example and capabilty of this technology to control many players at the same time to reach a goal
# This code is a prof of concept that an agent can learn to control many players at the same time
import pygame as pg
import random
import gymnasium as gym
import numpy as np
from stable_baselines3 import PPO
import numpy as np
import time


class NairobiCityEnv(gym.Env,):
    # It defines the environment
    def __init__(self,number_of_players, render_mode=False):
        print("Initializing Environment...")
        #The number of player you want 
        self.number_of_players = number_of_players
        self.width = 1800
        self.height = 800
        self.size = 20
        self.yellow = (255, 255, 0)
        self.size_line = 40
        self.movemenet = 5
        self.render_mode = render_mode
        self.finished_players = [False] * self.number_of_players
        # The number of actions the agent is to take
        actions_per_player = self.number_of_players * 4  # Each player has 4 possible actions
        self.action_space = gym.spaces.Discrete(actions_per_player)
        self.number=self.number_of_players * 2
        self.observation_space = gym.spaces.Box(
            low=0, high=max(self.width, self.height), shape=(self.number,), dtype=np.float64
        )
        #
        if self.render_mode == True:
            self.screen = pg.display.set_mode((self.width, self.height))
            pg.display.set_caption("Nairobi City Simulation")

    def reset(self, seed=None, options=None):
        # Specifies the initial state of the environmentand the players
        
        self.circle={"x":(self.width//2),"y":(self.height//2)}

        self.players = []
        for _ in range(self.number_of_players):
            self.players.append(
                {
                    "x":random.randint(0, self.width - self.size),
                    "y": random.randint(0, self.height - self.size),
                    "color": (
                        random.randint(100, 255),
                        random.randint(100, 255),
                        random.randint(100, 255),
                    ),
                }
            )
        
        all_coords = []
        for p in self.players:
            all_coords.extend([p["x"], p["y"]])
        obs = np.array(all_coords, dtype=np.float64)
        info = {}
        return obs, info

    def step(self, action):
        player_idx = action // 4 
        move_type = action % 4   

        # 1. CHECK IF THIS PLAYER IS ALREADY FINISHED
        # If they are already in the circle, ignore their moves!
        if self.finished_players[player_idx] == True:
            reward = 0 
            terminated = False
            truncated = False
            # Return old state, don't move them
            return self._get_obs(), reward, terminated, truncated, {}

        # 2. MOVE THE PLAYER (Standard Logic)
        if player_idx < self.number_of_players:
            if move_type == 0: self.players[player_idx]["x"] -= self.movemenet
            elif move_type == 1: self.players[player_idx]["x"] += self.movemenet
            elif move_type == 2: self.players[player_idx]["y"] -= self.movemenet
            elif move_type == 3: self.players[player_idx]["y"] += self.movemenet

            # Boundary checks
            self.players[player_idx]["x"] = np.clip(self.players[player_idx]["x"], 0, self.width - self.size)
            self.players[player_idx]["y"] = np.clip(self.players[player_idx]["y"], 0, self.height - self.size)

        # 3. CHECK WIN CONDITION FOR THIS PLAYER
        px, py = self.players[player_idx]["x"], self.players[player_idx]["y"]
        cx, cy = self.circle["x"], self.circle["y"]
        dist = np.sqrt((px - cx)**2 + (py - cy)**2)
        
        hit_radius = self.size + self.size_line

        if dist < hit_radius:
            self.finished_players[player_idx] = True # Mark this specific player as done!
            reward = 100 # Big bonus for arriving
        else:
            reward = -0.1 - (0.01 * dist) # Normal distance penalty

        # 4. CHECK IF *EVERYONE* IS FINISHED
        # The game only ends if ALL values in the list are True
        if all(self.finished_players):
            terminated = True
            print("EVERYONE MADE IT! Game Over.")
        else:
            terminated = False
            
        truncated = False
        obs = self._get_obs() # Helper function to get coords
        return obs, reward, terminated, truncated, {}

    # Helper to get observation (paste this inside your class)
    def _get_obs(self):
        #for better reading of the code
        all_coords = []
        for p in self.players:
            all_coords.extend([p["x"], p["y"]])
        return np.array(all_coords, dtype=np.float64)

    def render(self, seed=None, options=None):
        self.screen.fill((0, 0, 0))
        pg.draw.circle(self.screen,self.yellow,(self.circle["x"],self.circle["y"]),self.size_line,self.size_line)
        for player in self.players:
            pg.draw.rect(
                self.screen,
                player["color"],
                (player["x"], player["y"], self.size, self.size),
            )
        pg.display.update()

    def close(self):
        pg.quit()
number_of_players = int(input("Enter the number of players: "))
print(f"Number of Players: {number_of_players}")

# Train without rendering
env = NairobiCityEnv(number_of_players=number_of_players)
obs, _ = env.reset()
model = PPO("MlpPolicy", env, verbose=1)
model.learn(total_timesteps=1000000)

print("Environment Ready!")
print("Initial State:", obs)

# Play with rendering enabled
play_env = NairobiCityEnv(number_of_players=number_of_players, render_mode=True)
obs, _ = play_env.reset()
for _ in range(10000):
    action, _ = model.predict(obs)  # Model chooses action
    obs, reward, terminated, truncated, info = play_env.step(action)
    play_env.render()  # View the game

    if terminated:
        obs, _ = env.reset()
    print(
        "Action:", action, "State:", obs, "Reward:", reward, "Terminated:", terminated
    )
play_env.close()
