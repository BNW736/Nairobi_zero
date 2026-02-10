#A simple example and capabilty of this technology to control two players at the same time in a simulated environment. The code defines a custom environment called "NairobiCityEnv" using the OpenAI Gymnasium library. The environment simulates a city where two players can move around. The agent can take actions to control the movement of both players simultaneously. The code includes methods for resetting the environment, taking steps based on actions, rendering the environment visually, and closing the environment when done. The main loop runs for a specified number of steps, randomly sampling actions and rendering the environment at each step.
#This code is a prof of concept that an agent can learn to control two players at the same time
import pygame as pg
import random
import gymnasium as gym
import numpy as np


class NairobiCityEnv(gym.Env):
#It defines the environment
    def __init__(self):
        self.width = 1800
        self.height = 800
        self.size = 20
        self.size_line = 40
        self.movemenet = 5
        self.metadata = {"render_modes": ["human", "rgb_array"], "render_fps": 30}
        pg.init()
        self.screen = pg.display.set_mode((self.width, self.height))
        pg.display.set_caption("Nairobi City Simulation")
        #The number of actions the agent is to take
        self.action_space = gym.spaces.Discrete(8)
        self.observation_space = gym.spaces.Box(low=0, high=max(self.width, self.height), shape=(4,), dtype=np.float32)
    def reset(self):
        #Specifies the initial state of the environmentand the players
        self.color = (0, 255, 0)
        self.color2=(0,0,255)
        self.players_x = np.array(230,dtype=np.float32)
        self.players_y = np.array(400,dtype=np.float32)
        self.players_x1 = np.array(400,dtype=np.float32)
        self.players_y1 = np.array(400,dtype=np.float32)
        obs = np.array([self.players_x, self.players_y, self.players_x1, self.players_y1], dtype=np.float32)
        info = {}
        return obs,info
    def step(self, action):
        #It defines the actions the agent can take and how the environment responds to those actions
        run=False
        for event in pg.event.get():
            if event.type == pg.QUIT:
                run=True
        if run:
            pg.quit()
            obs=np.array([self.players_x, self.players_y, self.players_x1, self.players_y1], dtype=np.float32)
            reward=0
            terminated=True
            truncated=False
            info={}
            return obs, reward, terminated, truncated, info
        
        if action == 0:  
            self.players_x = self.players_x - self.movemenet
        elif action == 1:  
            self.players_x = self.players_x + self.movemenet
        elif action == 2:  
            self.players_y = self.players_y - self.movemenet
        elif action == 3:  
            self.players_y = self.players_y + self.movemenet
        elif action == 4:  
            self.players_x1 = self.players_x1 - self.movemenet
        elif action == 5:  
            self.players_x1 = self.players_x1 + self.movemenet
        elif action == 6:  
            self.players_y1 = self.players_y1 - self.movemenet
        elif action == 7:  
            self.players_y1 = self.players_y1 + self.movemenet
        if self.players_x < 0:
            self.players_x = 0
        elif self.players_x > self.width - self.size:
            self.players_x = self.width - self.size
        if self.players_y < 0:
            self.players_y = 0
        elif self.players_y > self.height - self.size:
            self.players_y = self.height - self.size
        if self.players_x1 < 0:
            self.players_x1 = 0
        elif self.players_x1 > self.width - self.size:  
            self.players_x1 = self.width - self.size
        if self.players_y1 < 0:
            self.players_y1 = 0
        elif self.players_y1 > self.height - self.size:
            self.players_y1 = self.height - self.size
   
        obs = np.array([self.players_x, self.players_y, self.players_x1, self.players_y1], dtype=np.float32)
        reward = 0
        terminated = False
        truncated = False
        info = {}   
        return obs, reward, terminated, truncated, info
    def render(self):
        #It defines how the environment is visually represented to the agent and how the players are displayed on the screen
            self.screen.fill((0, 0, 0))
            pg.draw.rect(self.screen,self.color,(int(self.players_x), int(self.players_y), self.size, self.size))
            pg.draw.rect(self.screen,self.color2,(int(self.players_x1), int(self.players_y1), self.size, self.size))
            pg.display.update()
            clock = pg.time.Clock()
            clock.tick(self.metadata["render_fps"])
            
    def close(self):    
        pg.quit()
       
env = NairobiCityEnv()  # Initialize environment with a default action
obs, _ = env.reset()

print("Environment Ready!")
print("Initial State:", obs)

# number or run steps of random actions
for _ in range(500):
    action = env.action_space.sample()  # Pick random action
    obs, reward, terminated, truncated, info = env.step(action)
    env.render()  # View the game

    if terminated:
        obs, _ = env.reset()
    print("Action:", action, "State:", obs, "Reward:", reward, "Terminated:", terminated)
env.close()



