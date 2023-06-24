import pygame
import sys
import random

# Spielkonstanten
GRAVITY = 0.25
FLAP_STRENGTH = 5
MIN_SPEED = -8
MAX_SPEED = 10
SPEED = 2
WIDTH, HEIGHT = 400, 600
PIPE_GAP = 200
OBSTACLE_WIDTH, OBSTACLE_HEIGHT = 30, 30

class Bird(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((30, 30))
        self.image.fill((255, 0, 0))
        self.rect = self.image.get_rect(center=(80, HEIGHT//2))
        self.speed = 0

    def flap(self):
        self.speed = -FLAP_STRENGTH

    def update(self):
        self.speed += GRAVITY
        self.speed = max(MIN_SPEED, self.speed)
        self.speed = min(MAX_SPEED, self.speed)
        self.rect.centery += self.speed

class Pipe(pygame.sprite.Sprite):
    def __init__(self, position, orientation):
        super().__init__()
        self.image = pygame.Surface((100, random.randint(50, 150)))
        self.image.fill((0, 255, 0))
        if orientation == "bottom":
            self.rect = self.image.get_rect(midbottom=position)
        else:
            self.rect = self.image.get_rect(midtop=position)

    def update(self):
        global score
        self.rect.x -= SPEED
        if self.rect.right < 0:
            self.kill()
            score += 1

def game_over_screen(screen, font, score, high_score):
    game_over_text = font.render("Game Over!", True, (255, 255, 255))
    score_text = font.render("Score: " + str(score), True, (255, 255, 255))
    high_score_text = font.render("High Score: " + str(high_score), True, (255, 255, 255))
    screen.blit(game_over_text, (WIDTH // 2 - game_over_text.get_width() // 2, HEIGHT // 2 - game_over_text.get_height() // 2))
    screen.blit(score_text, (WIDTH // 2 - score_text.get_width() // 2, HEIGHT // 2 - game_over_text.get_height() // 2 + 50))
    screen.blit(high_score_text, (WIDTH // 2 - high_score_text.get_width() // 2, HEIGHT // 2 - game_over_text.get_height() // 2 + 100))
    pygame.display.flip()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                return

def main( high_score):
    global score  # Deklariere die score Variable als global
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    clock = pygame.time.Clock()
    pygame.time.set_timer(pygame.USEREVENT, 2000)
    font = pygame.font.Font(None, 36)

    bird = Bird()
    all_sprites = pygame.sprite.Group(bird)
    pipes = pygame.sprite.Group()

    running = True
    score = 0

    def update_score():
        score_text = font.render("Score: " + str(score), True, (255, 255, 255))
        high_score_text = font.render("High Score: " + str(high_score), True, (255, 255, 255))
        screen.blit(score_text, (20, 20))
        screen.blit(high_score_text, (20, 60))

    while running:
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                    bird.flap()
                if event.type == pygame.USEREVENT:
                    pipe_height = random.randint(50, HEIGHT - 50)
                    pipes.add(Pipe((WIDTH + 100, pipe_height), "bottom"))
                    pipes.add(Pipe((WIDTH + 100, pipe_height - PIPE_GAP), "top"))

            all_sprites.update()
            pipes.update()

            for pipe in list(pipes):
                if pipe.rect.right < 0:
                    score += 1
                    pipes.remove(pipe)

            if pygame.sprite.spritecollide(bird, pipes, False) or bird.rect.top <= 0 or bird.rect.bottom >= HEIGHT:
                high_score = max(high_score, score)
                running = False

            screen.fill((0, 0, 0))
            all_sprites.draw(screen)
            pipes.draw(screen)
            update_score()
            pygame.display.flip()
            clock.tick(60)

        game_over_screen(screen, font, score, high_score)
        return  high_score

if __name__ == "__main__":
    high_score = 0
    while True:

        high_score = main( high_score)

