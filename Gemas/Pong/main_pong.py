import pygame
import sys
import math
import random

# Allgemeine Einstellungen
WIDTH, HEIGHT = 800, 600
BALL_SPEED = 1.5
BALL_MAX_SPEED = 15
BALL_RANDOM_Y = 5
PADDLE_SPEED = 8
BALL_RADIUS = 10
PADDLE_WIDTH, PADDLE_HEIGHT = 15, 80
FPS = 60

# Farben
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Initialisierung von Pygame
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()
font = pygame.font.Font(None, 36)

# Ball Einstellungen
ball = pygame.Rect(WIDTH / 2, HEIGHT / 2, BALL_RADIUS * 2, BALL_RADIUS * 2)
ball_dx = BALL_SPEED
ball_dy = random.uniform(-BALL_RANDOM_Y, BALL_RANDOM_Y)  # Jetzt zufällig

# Paddle Einstellungen
paddle_left = pygame.Rect(0, HEIGHT / 2, PADDLE_WIDTH, PADDLE_HEIGHT)
paddle_right = pygame.Rect(WIDTH - PADDLE_WIDTH, HEIGHT / 2, PADDLE_WIDTH, PADDLE_HEIGHT)

# Score Einstellungen
score_left = 0
score_right = 0


def draw_objects():
    screen.fill(BLACK)
    pygame.draw.rect(screen, WHITE, paddle_left)
    pygame.draw.rect(screen, WHITE, paddle_right)
    pygame.draw.ellipse(screen, WHITE, ball)
    pygame.draw.aaline(screen, WHITE, (WIDTH / 2, 0), (WIDTH / 2, HEIGHT))

    score_text = font.render(f"{score_left} - {score_right}", True, WHITE)
    screen.blit(score_text, (WIDTH / 2 - score_text.get_width() / 2, 10))

    speed_text = font.render(f"Ball Speed: {math.sqrt(ball_dx**2 + ball_dy**2):.2f}", True, WHITE)
    screen.blit(speed_text, (10, 10))


def check_collision():
    global ball_dx, ball_dy, score_left, score_right

    if ball.left < 0:
        score_right += 1
        reset_ball()
        ball_dx = BALL_SPEED
        ball_dy = random.uniform(-BALL_RANDOM_Y, BALL_RANDOM_Y)  # Jetzt zufällig
    elif ball.right > WIDTH:
        score_left += 1
        reset_ball()
        ball_dx = -BALL_SPEED
        ball_dy = random.uniform(-BALL_RANDOM_Y, BALL_RANDOM_Y)  # Jetzt zufällig

    if ball.top < 0 or ball.bottom > HEIGHT:
        ball_dy *= -1

    if ball.colliderect(paddle_left):
        if ball_dx <= -BALL_MAX_SPEED:
            ball_dx = -BALL_MAX_SPEED
            ball_dx *= -1  # Increase speed by 5%
        else:
            ball_dx *= -1.25  # Increase speed by 5%

    elif ball.colliderect(paddle_right):

        if ball_dx >= BALL_MAX_SPEED:
            ball_dx = BALL_MAX_SPEED
            ball_dx *= -1  # Increase speed by 5%
        else:
            ball_dx *= -1.25  # Increase speed by 5%



def move_paddle():
    keys = pygame.key.get_pressed()

    if keys[pygame.K_w]:
        paddle_left.move_ip(0, -PADDLE_SPEED)
    if keys[pygame.K_s]:
        paddle_left.move_ip(0, PADDLE_SPEED)

    if keys[pygame.K_UP]:
        paddle_right.move_ip(0, -PADDLE_SPEED)
    if keys[pygame.K_DOWN]:
        paddle_right.move_ip(0, PADDLE_SPEED)

    if paddle_left.top < 0:
        paddle_left.top = 0
    if paddle_left.bottom > HEIGHT:
        paddle_left.bottom = HEIGHT
    if paddle_right.top < 0:
        paddle_right.top = 0
    if paddle_right.bottom > HEIGHT:
        paddle_right.bottom = HEIGHT


def reset_ball():
    ball.center = (WIDTH / 2, HEIGHT / 2)
    ball_dy = random.uniform(-BALL_RANDOM_Y, BALL_RANDOM_Y)  # Jetzt zufällig


def game_loop():
    global ball_dx, ball_dy

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        draw_objects()
        check_collision()
        move_paddle()

        ball.move_ip(ball_dx, ball_dy)

        pygame.display.flip()
        clock.tick(FPS)


if __name__ == "__main__":
    game_loop()
