import pygame, sys, time, random
import time
# ... (Snake Eater code, same as before) ...

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


#init pygame!!
pygame.init()

#display-is obieqtis gaketeba zomaze
screen = pygame.display.set_mode((920, 800))
pygame.display.set_caption("My platformer Game")

#suratis chatvirtva!
background_img = pygame.image.load("start_screen.png")

#gilakis gaketeba zomaze da suratis mimagreba!
start_btn_img = pygame.image.load("start_button.png")
start_btn_img2 = pygame.image.load("start_button.png")
snake_image = pygame.image.load("start_button.png")
next_screen_img = pygame.image.load("map_N1.jpeg")
end_screen_img = pygame.image.load("end_screen.jpeg")
win_screen_img = pygame.image.load("win_screen.jpeg")
snake_image = pygame.transform.scale(snake_image, (10, 10))
background_img = pygame.transform.scale(background_img, (920, 800))
next_screen_img = pygame.transform.scale(next_screen_img, (SCREEN_WIDTH, SCREEN_HEIGHT))
end_screen_img = pygame.transform.scale(end_screen_img, (SCREEN_WIDTH, SCREEN_HEIGHT))
end_screen_rect = end_screen_img.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
win_screen_img = pygame.transform.scale(win_screen_img, (SCREEN_WIDTH, SCREEN_HEIGHT))
win_screen_rect = win_screen_img.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))

button_width = 200
button_height = 100
start_btn_img2 = pygame.transform.scale(start_btn_img2, (button_width, button_height))
start_btn_img = pygame.transform.scale(start_btn_img, (button_width, button_height))
start_btn_rect = start_btn_img.get_rect()
start_btn_rect2 = start_btn_img2.get_rect()
start_btn_rect2.center = (300, 400)

start_btn_rect.center = (500, 400)


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

# Difficulty settings
# Easy      ->  10
# Medium    ->  25
# Hard      ->  40
# Harder    ->  60
# Impossible->  120
difficulty = 25

# Window size
frame_size_x = 920
frame_size_y = 800

# Checks for errors encountered
check_errors = pygame.init()
if check_errors[1] > 0:
    print(f'[!] Had {check_errors[1]} errors when initializing game, exiting...')
    sys.exit(-1)
else:
    print('[+] Game successfully initialized')

# Initialize game window
pygame.display.set_caption('My Platformer Game')
game_window = pygame.display.set_mode((frame_size_x, frame_size_y))

# Colors (R, G, B)
black = pygame.Color(0, 0, 0)
white = pygame.Color(255, 255, 255)
red = pygame.Color(255, 0, 0)
green = pygame.Color(0, 255, 0)
blue = pygame.Color(0, 0, 255)

# FPS (frames per second) controller
fps_controller = pygame.time.Clock()

# Game variables
snake_pos = [100, 50]
snake_body = [[100, 50], [100-10, 50], [100-(2*10), 50]]
food_pos = [random.randrange(1, (frame_size_x//10)) * 10, random.randrange(1, (frame_size_y//10)) * 10]
food_spawn = True
direction = 'RIGHT'
change_to = direction
score = 0

# Game Over
def game_over():
    my_font = pygame.font.SysFont('times new roman', 90)
    game_over_surface = my_font.render('YOU DIED', True, red)
    game_over_rect = game_over_surface.get_rect()
    game_over_rect.midtop = (frame_size_x/2, frame_size_y/4)
    game_window.fill(black)
    game_window.blit(game_over_surface, game_over_rect)
    show_score(0, red, 'times', 20)
    pygame.display.flip()
    time.sleep(3)
    pygame.quit()
    sys.exit()

# Score
def show_score(choice, color, font, size):
    score_font = pygame.font.SysFont(font, size)
    score_surface = score_font.render('Score : ' + str(score), True, color)
    score_rect = score_surface.get_rect()
    if choice == 1:
        score_rect.midtop = (frame_size_x/10, 15)
    else:
        score_rect.midtop = (frame_size_x/2, frame_size_y/1.25)
    game_window.blit(score_surface, score_rect)

gameon = False
second_game = False
running_platformer = True

while gameon or running_platformer or second_game:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running_platformer = False
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
                # Start button clicked, switch to Snake Eater game
                gameon = True
                running_platformer = False
            elif start_btn_rect2.collidepoint(mouse_pos):
                second_game = True
                running_platformer = False
        # Whenever a key is pressed down
        elif event.type == pygame.KEYDOWN:
            # W -> Up; S -> Down; A -> Left; D -> Right
            if event.key == pygame.K_UP or event.key == ord('w'):
                change_to = 'UP'
            if event.key == pygame.K_DOWN or event.key == ord('s'):
                change_to = 'DOWN'
            if event.key == pygame.K_LEFT or event.key == ord('a'):
                change_to = 'LEFT'
            if event.key == pygame.K_RIGHT or event.key == ord('d'):
                change_to = 'RIGHT'
            # Esc -> Create event to quit the game
            if event.key == pygame.K_ESCAPE:
                pygame.event.post(pygame.event.Event(pygame.QUIT))
    if running_platformer:
        # Display the platformer start screen
        screen.blit(background_img, (0, 0))
        screen.blit(start_btn_img, start_btn_rect)
        screen.blit(start_btn_img2, start_btn_rect2)

        pygame.display.flip()
    elif second_game:

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
        print("hero")
    else:
        # Making sure the snake cannot move in the opposite direction instantaneously
        if change_to == 'UP' and direction != 'DOWN':
            direction = 'UP'
        if change_to == 'DOWN' and direction != 'UP':
            direction = 'DOWN'
        if change_to == 'LEFT' and direction != 'RIGHT':
            direction = 'LEFT'
        if change_to == 'RIGHT' and direction != 'LEFT':
            direction = 'RIGHT'

        # Moving the snake
        if direction == 'UP':
            snake_pos[1] -= 10
        if direction == 'DOWN':
            snake_pos[1] += 10
        if direction == 'LEFT':
            snake_pos[0] -= 10
        if direction == 'RIGHT':
            snake_pos[0] += 10

        # Snake body growing mechanism
        snake_body.insert(0, list(snake_pos))
        if snake_pos[0] == food_pos[0] and snake_pos[1] == food_pos[1]:
            score += 1
            food_spawn = False
        else:
            snake_body.pop()

        # Spawning food on the screen
        if not food_spawn:
            food_pos = [random.randrange(1, (frame_size_x//10)) * 10, random.randrange(1, (frame_size_y//10)) * 10]
        food_spawn = True

        # GFX
        game_window.fill(black)
        for pos in snake_body:
            # Snake body
            # .draw.rect(play_surface, color, xy-coordinate)
            # xy-coordinate -> .Rect(x, y, size_x, size_y)
            pygame.draw.rect(game_window, green, pygame.Rect(pos[0], pos[1], 10, 10))

        # Snake food
        pygame.draw.rect(game_window, white, pygame.Rect(food_pos[0], food_pos[1], 10, 10))

        # Game Over conditions
        # Getting out of bounds
        if snake_pos[0] < 0 or snake_pos[0] > frame_size_x-10:
            game_over()
        if snake_pos[1] < 0 or snake_pos[1] > frame_size_y-10:
            game_over()
        # Touching the snake body
        for block in snake_body[1:]:
            if snake_pos[0] == block[0] and snake_pos[1] == block[1]:
                game_over()

        show_score(1, white, 'consolas', 20)
        # Refresh game screen
        pygame.display.update()
        # Refresh rate
        fps_controller.tick(difficulty)


pygame.quit()

# Main logic
running = True

        

    

pygame.quit()