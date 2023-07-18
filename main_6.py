import pygame
import time

SCREEN_WIDTH = 900
SCREEN_HEIGHT = 700
GRAVITY = 0.5
JUMP_FORCE = -1

class Hero(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height):
        super().__init__()
        self.image = pygame.image.load("character_design.png")
        self.image = pygame.transform.scale(self.image, (width, height))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.speed_x = 0
        self.speed_y = 0
        self.is_jumping = False

    def update(self):
        self.rect.x += self.speed_x

        if not self.is_jumping and self.rect.y < SCREEN_HEIGHT - self.rect.height:
            self.speed_y += GRAVITY
        self.rect.y += self.speed_y

    def jump(self):
        if not self.is_jumping:
            self.speed_y = JUMP_FORCE
            self.is_jumping = True
            self.speed_y += GRAVITY

    def handle_collision(self, platforms):
        for platform in platforms:
            if self.rect.colliderect(platform.rect) and self.speed_y >= 0:
                self.rect.y = platform.rect.y - self.rect.height
                self.is_jumping = False
                self.speed_y = 0

class Platform(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height):
        super().__init__()
        self.image = pygame.Surface((width, height))
        self.image.fill((0, 255, 0))  # Green color
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

pygame.init()

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("My platformer Game")

background_img = pygame.image.load("start_screen.png")
next_screen_img = pygame.image.load("map_N1.jpg")
end_screen_img = pygame.image.load("end_screen.jpg")
win_screen_img = pygame.image.load("win screen.jpg")
background_img = pygame.transform.scale(background_img, (SCREEN_WIDTH, SCREEN_HEIGHT))
next_screen_img = pygame.transform.scale(next_screen_img, (SCREEN_WIDTH, SCREEN_HEIGHT))
end_screen_img = pygame.transform.scale(end_screen_img, (SCREEN_WIDTH, SCREEN_HEIGHT))
end_screen_rect = end_screen_img.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
win_screen_img = pygame.transform.scale(win_screen_img, (SCREEN_WIDTH, SCREEN_HEIGHT))
win_screen_rect = win_screen_img.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))

start_btn_img = pygame.image.load("start_button.png")
button_width = 200
button_height = 100
start_btn_img = pygame.transform.scale(start_btn_img, (button_width, button_height))
start_btn_rect = start_btn_img.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))

hero = Hero(100, 485, 100, 100)
platforms = [
    Platform(0, 580, 230, 10),
    Platform(345, 520, 348, 10),
    Platform(420, 400, 138, 10),
    Platform(130, 365, 170, 10),
    Platform(690, 580, 115, 10),
    Platform(345, 240, 115, 10),
    Platform(0, 138, 230, 10),
    Platform(508, 165, 112, 10),
    Platform(731, 138, 200, 10),
]

all_sprites = pygame.sprite.Group()
all_sprites.add(hero)
all_sprites.add(*platforms)

running = True
game_started = False

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif hero.rect.y > 490:
            screen.blit(end_screen_img, end_screen_rect)
            pygame.display.flip()
            time.sleep(5)
            running = False
        elif hero.rect.y <= 40 and hero.rect.x >= 800:
            screen.blit(win_screen_img, win_screen_rect)
            pygame.display.flip()
            time.sleep(5)
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()
            if start_btn_rect.collidepoint(mouse_pos):
                game_started = True

    if game_started:
        screen.blit(next_screen_img, (0, 0))
        all_sprites.draw(screen)

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            hero.speed_x = -5
        elif keys[pygame.K_RIGHT]:
            hero.speed_x = 5
        else:
            hero.speed_x = 0

        if keys[pygame.K_SPACE]:
            hero.jump()
            # while hero.speed_y <= 0:
            #     hero.speed_y += GRAVITY
        if hero.is_jumping == True:
            hero.speed_y += 0.004


        hero.update()
        hero.handle_collision(platforms)

        screen.blit(hero.image, hero.rect)
        pygame.display.flip()
    else:
        screen.blit(background_img, (0, 0))
        screen.blit(start_btn_img, start_btn_rect)
        pygame.display.flip()

pygame.quit()
