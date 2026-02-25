# Project Nairobi_Zero: Learning Traffic AI
## 👋 About This Project
**Nairobi_Zero** is my attempt to build a traffic simulation for Nairobi using Python and Artificial Intelligence.

I wanted to see if I could train a computer (AI Agent) to control cars and traffic flow, instead of just programming them manually.

The goal is to eventually simulate real Nairobi intersections to see if AI can reduce traffic jams. For now, it is a simulation of agents learning to find a target.

## 🎮 What I Built
I created three different stages to learn how Reinforcement Learning works:

### 1. Manual Mode (`manual_game.py`)
* **What it is:** A simple game where you control 5 squares (cars) using the keyboard.
* **Why I built it:** To test the "physics" and make sure the cars stay on the road boundaries.
* **Controls:**
    * Keys `1, 2, 3, 4, 5` select the car.
    * `Arrow Keys` move the selected car.

### 2. Duo Agent (`agent_duo.py`)
* **The Goal:** I trained an AI to control **two cars at the same time**.
* **The Challenge:** The AI gets points (rewards) when the two cars are close to each other.
* **Result:** The AI learned to make the cars "hold hands" and move together.

### 3. The Swarm (`agent_swarm.py`)
* **The Goal:** This is the main project. It controls **many cars** at once.
* **The Logic:**
    * The cars spawn at random places.
    * They have to find the "City Center" (Yellow Circle) in the middle.
    * If they reach the center, they get +100 points.
    * If they take too long, they lose points.
* **Tech Used:** I used `Stable-Baselines3` (PPO Algorithm) to train the brain.

---



