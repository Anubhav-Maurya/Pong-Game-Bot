import pygame
import random
import sys
import math

# Initialize Pygame
pygame.init()

# Set up constants
WIDTH, HEIGHT = 800, 600
FPS = 60
WINNING_SCORE = 5

# Colors
BLACK = (0, 0, 0)
PURPLE = (0, 0, 255)
BLUE = (0, 0, 255)
WHITE = (255, 255, 255)
LIGHT_BLUE = (173, 216, 230)
GRAY = (169, 169, 169)

# Set up the game window
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pong Game: Player vs AI Bot")

# Fonts
title_font = pygame.font.Font(None, 64)
score_font = pygame.font.Font(None, 36)
menu_font = pygame.font.Font(None, 32)

class Paddle:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, 10, 100)
        self.speed = 5

    def move(self, up=True):
        if up:
            self.rect.y -= self.speed
        else:
            self.rect.y += self.speed
        self.rect.y = max(0, min(self.rect.y, HEIGHT - self.rect.height))

    def draw(self):
        pygame.draw.rect(screen, WHITE, self.rect)

class Ball:
    def __init__(self):
        self.reset()

    def reset(self):
        self.x = WIDTH // 2
        self.y = HEIGHT // 2
        self.speed_x = random.choice([-4, 4])
        self.speed_y = random.uniform(-3, 3)

    def move(self):
        self.x += self.speed_x
        self.y += self.speed_y

    def draw(self):
        pygame.draw.circle(screen, LIGHT_BLUE, (int(self.x), int(self.y)), 10)

# Trajectory Prediction Function
def predict_ball_y(ball):
    future_x = WIDTH - 60  # AI paddle x position
    time_to_reach_ai = (future_x - ball.x) / ball.speed_x

    predicted_y = ball.y + ball.speed_y * time_to_reach_ai

    # Simulate wall bounces during prediction
    while predicted_y < 0 or predicted_y > HEIGHT:
        if predicted_y < 0:
            predicted_y = -predicted_y
        elif predicted_y > HEIGHT:
            predicted_y = 2 * HEIGHT - predicted_y

    return predicted_y

class AIBot:
    def __init__(self, paddle):
        self.paddle = paddle
        self.speed = 10

    def move(self, ball):
        target_y = predict_ball_y(ball)
        if self.paddle.rect.centery < target_y:
            self.paddle.move(up=False)
        elif self.paddle.rect.centery > target_y:
            self.paddle.move(up=True)

def draw_dashed_line():
    dash_length = 10
    pygame.draw.rect(screen, BLUE, (0, 0, WIDTH, HEIGHT), 4)
    for y in range(0, HEIGHT, dash_length * 2):
        pygame.draw.line(screen, GRAY, (WIDTH // 2, y), (WIDTH // 2, y + dash_length))

def show_title_screen():
    screen.fill(PURPLE)
    title = title_font.render("Pong Game: Player vs AI Bot", True, WHITE)
    start_text = menu_font.render("Press SPACE to start", True, WHITE)
    quit_text = menu_font.render("Press Q to quit", True, WHITE)

    screen.blit(title, (WIDTH // 2 - title.get_width() // 2, HEIGHT // 4))
    screen.blit(start_text, (WIDTH // 2 - start_text.get_width() // 2, HEIGHT // 2))
    screen.blit(quit_text, (WIDTH // 2 - quit_text.get_width() // 2, HEIGHT // 2 + 50))

    pygame.display.flip()

    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    waiting = False
                elif event.key == pygame.K_q:
                    pygame.quit()
                    sys.exit()

def main():
    clock = pygame.time.Clock()
    player_paddle = Paddle(50, HEIGHT // 2 - 50)
    ai_paddle = Paddle(WIDTH - 60, HEIGHT // 2 - 50)
    ball = Ball()
    ai_bot = AIBot(ai_paddle)

    player_score = 0
    ai_score = 0

    show_title_screen()

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP]:
            player_paddle.move(up=True)
        if keys[pygame.K_DOWN]:
            player_paddle.move(up=False)

        ai_bot.move(ball)
        ball.move()

        # Ball collision with top and bottom
        if ball.y <= 10 or ball.y >= HEIGHT - 10:
            ball.speed_y *= -1

        # Ball collision with paddles
        if ball.x <= player_paddle.rect.right and player_paddle.rect.top <= ball.y <= player_paddle.rect.bottom:
            ball.speed_x *= -1.1
            ball.speed_y *= 1.1
        elif ball.x + 10 >= ai_paddle.rect.left and ai_paddle.rect.top <= ball.y <= ai_paddle.rect.bottom:
            ball.speed_x *= -1.1
            ball.speed_y *= 1.1

        # Score points
        if ball.x <= 0:
            ai_score += 1
            ball.reset()
        elif ball.x >= WIDTH:
            player_score += 1
            ball.reset()

        # Check for winner
        if player_score >= WINNING_SCORE or ai_score >= WINNING_SCORE:
            winner = "Player" if player_score >= WINNING_SCORE else "AI"
            winner_text = score_font.render(f"{winner} wins!", True, WHITE)
            screen.blit(winner_text, (WIDTH // 2 - winner_text.get_width() // 2, HEIGHT // 2))
            pygame.display.flip()
            pygame.time.wait(5000)
            running = False

        # Draw everything
        screen.fill(BLACK)
        draw_dashed_line()
        player_paddle.draw()
        ai_paddle.draw()
        ball.draw()

        # Draw scores
        player_text = score_font.render(f"Player:{player_score}", True, WHITE)
        ai_text = score_font.render(f"AI:{ai_score}", True, WHITE)
        screen.blit(player_text, (WIDTH // 4, 20))
        screen.blit(ai_text, (3 * WIDTH // 4 - ai_text.get_width(), 20))

        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()

if __name__ == "__main__":
    main()
