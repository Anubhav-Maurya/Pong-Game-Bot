#   🎮 Pong Game: Player vs AI Bot  

A Python-based **Pong game** where a player competes against an AI-powered bot. The AI bot uses **trajectory prediction** to anticipate the ball's movement and respond effectively.  

## 🚀 Features  
- **Single-player mode**: Play against an intelligent AI bot.  
- **AI Trajectory Prediction**: The bot predicts the ball’s future position and moves accordingly.    
- **Game Win Condition**: First to reach the winning score wins the match.  
- **Simple UI with Pygame**: Classic Pong-style visuals with a responsive interface.  

## 🧠 AI Bot Mechanism  
The AI bot is a **rule-based agent** that performs three key tasks:  
1. **Perception**: Detects ball position and movement.  
2. **Prediction**: Calculates the expected trajectory of the ball.  
3. **Action**: Moves the paddle to intercept the ball optimally.  

## 📜 Installation & Setup  
### 1️⃣ Clone the Repository  
```bash
git clone https://github.com/Anubhav-Maurya/Pong-Game-Bot.git
cd Pong-Game-Bot
  
### 2️⃣ Install Dependencies
Make sure Python is installed, then install the required libraries:
```bash
pip install pygame

### 3️⃣ Run the Game
```bash
python pong.py

### 🖥️ Run the Executable (Windows)
Download the .exe file from the Releases section or create one using:
```bash
pyinstaller --onefile pong.py
Then, run the .exe file from the dist/ folder.
