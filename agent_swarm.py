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
        self.size = 30
        self.yellow = (255, 255, 0)
        self.size_line = 100
        self.movemenet = 50
        self.render_mode = render_mode
        self.finished_players = [False] * self.number_of_players
        # The number of actions the agent is to take
        self.action_space = gym.spaces.MultiDiscrete([4] * self.number_of_players)
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
        self.finished_players = [False] * self.number_of_players
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
        total_reward = 0
        
        # Loop through EVERY player to apply their specific action
        for i in range(self.number_of_players):
            
            # 1. Skip if this player is already finished
            if self.finished_players[i]:
                continue
            
            # 2. Get the specific move for player 'i' from the action list
            move_type = action[i]

            if move_type == 0:
                self.players[i]["x"] -= self.movemenet
            elif move_type == 1:
                self.players[i]["x"] += self.movemenet
            elif move_type == 2: 
                self.players[i]["y"] -= self.movemenet
            elif move_type == 3: 
                self.players[i]["y"] += self.movemenet

            # Boundary checks
            self.players[i]["x"] = np.clip(self.players[i]["x"], 0, self.width - self.size)
            self.players[i]["y"] = np.clip(self.players[i]["y"], 0, self.height - self.size)

            # 4. Check Win Condition for THIS player
            px, py = self.players[i]["x"], self.players[i]["y"]
            cx, cy = self.circle["x"], self.circle["y"]
            dist = np.sqrt((px - cx)**2 + (py - cy)**2)
            
            hit_radius = self.size + self.size_line

            if dist < hit_radius:
                self.finished_players[i] = True
                total_reward += 100 
            else:
                total_reward -= (0.1 + (0.01 * dist))

        # 5. Global Termination Check
        terminated = all(self.finished_players)
        truncated = False
        
        return self._get_obs(), total_reward, terminated, truncated, {}

    def _get_obs(self):
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
model = PPO("MlpPolicy", env, verbose=1,learning_rate=0.003,ent_coef=0)
model.learn(total_timesteps=50000)
model.save("goal")

print("Environment Ready! Playing...")


play_env = NairobiCityEnv(number_of_players=number_of_players, render_mode=True)
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