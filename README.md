### Nairobi_Zero: Multi-Agent Traffic AI Simulation
**Nairobi_Zero** is a multi-agent Reinforcement Learning (RL) simulation built with Python, Pygame, and Gymnasium.

I created this project primarily as a hands-on way to learn more about Reinforcement Learning and how AI agents interact with custom-built environments. The overarching concept is a proof-of-concept initiative designed to explore a smarter way to reduce traffic congestion in Nairobi.

The idea is that once a vehicle enters a designated control zone, an AI system temporarily takes control of the car and autonomously navigates it to its destination. The AI is trained to optimize routing, coordinate with other vehicles, and avoid collisions and traffic bottlenecks, ultimately improving traffic flow and road safety.

## Features
**Custom Gymnasium Environment**: Built a custom gym.Env from scratch with continuous state monitoring, reward functions, and penalty constraints.

**Multi-Agent Control**: Trains a single model to output actions for multiple independent agents simultaneously using a MultiDiscrete action space.

**Dynamic Traffic Systems**: Features state-based traffic lights with variable timers that agents must learn to obey.

**Complex Reward Mechanics**: Agents are rewarded for reaching the center roundabout and penalized for going off-road, running red lights, or taking too long.

**Visual Rendering**: A Pygame visualizer that renders agents, dynamic road boundaries, and changing traffic lights in real-time to observe the AI's learning progress.

## Tech Stack
**Language**: Python

**Environment**: OpenAI Gymnasium

**RL Algorithm**: Proximal Policy Optimization (PPO) via Stable-Baselines3

**Rendering**: Pygame

**Math/Arrays**: NumPy

## Project Progression
This project was built iteratively to understand the core mechanics of RL before adding complexity:

**2-Player Sync**: Initial proof-of-concept to verify that Stable-Baselines3 could output commands for two separate squares to move towards each other.

**N-Player Goal Seeking**: Expanded the action space to handle a dynamic number of players (N), training them to navigate to a central target while avoiding boundaries.

**Environment Physics**: A manual Pygame sandbox used to code the road constraints, traffic light cycles, and collision detection without the AI overhead.

**Nairobi_Zero (Final)**: Merged the AI training with the complex environment. The observation space passes normalized coordinates and traffic light states to the PPO model, forcing it to learn traffic laws to maximize its reward.

## Installation & Setup
Clone the repository and navigate to the project folder.

## Install the required dependencies:

# Bash
**pip install pygame gymnasium stable-baselines3 numpy**
**Run the simulation**. The script will first train the PPO model for a set number of timesteps in headless mode, and then open the Pygame window to demonstrate the trained agents navigating the city.

## What the AI Learns (Observation & Action Space)
**Observation Space**: The agent "sees" the normalized X and Y coordinates of every vehicle, as well as the current state (Green, Yellow, Red) of every traffic light in the grid.

**Action Space**: For each vehicle, the model outputs a discrete action: 0 (Left), 1 (Right), 2 (Up), 3 (Down).

**Rewards & Penalties**: * +100 for reaching the center destination.

+30 for staying on the road.

-20 for running a red light.

-30 for driving off the road.

Continuous minor penalties based on distance to the goal to encourage speed.