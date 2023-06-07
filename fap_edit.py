import pygame
from sys import exit
import random

pygame.init()
clock = pygame.time.Clock()

# Window
win_height = 720
win_width = 551
window = pygame.display.set_mode((win_width, win_height))

# Images

bird_images = [pygame.image.load("C:/Users/MSI-VN/Desktop/gamepy/data/assetss/yellowbird-downflap.png"),
               pygame.image.load("C:/Users/MSI-VN/Desktop/gamepy/data/assetss/yellowbird-midflap.png"),
               pygame.image.load("C:/Users/MSI-VN/Desktop/gamepy/data/assetss/yellowbird-upflap.png")]
birdblue= [pygame.image.load('C:/Users/MSI-VN/Desktop/gamepy/data/assets/blue.png'),
               pygame.image.load('C:/Users/MSI-VN/Desktop/gamepy/data/assets/blue.png'),
               pygame.image.load('C:/Users/MSI-VN/Desktop/gamepy/data/assets/blue.png')]
birdred= [pygame.image.load('C:/Users/MSI-VN/Desktop/gamepy/data/assets/red.png'),
               pygame.image.load('C:/Users/MSI-VN/Desktop/gamepy/data/assets/red.png'),
               pygame.image.load('C:/Users/MSI-VN/Desktop/gamepy/data/assets/red.png')]
skyline_image = pygame.image.load("C:/Users/MSI-VN/Desktop/gamepy/data/assetss/background.png")
ground_image = pygame.image.load("C:/Users/MSI-VN/Desktop/gamepy/data/assetss/ground.png")
top_pipe_image = pygame.image.load("C:/Users/MSI-VN/Desktop/gamepy/data/assetss/pipe_top.png")
bottom_pipe_image = pygame.image.load("C:/Users/MSI-VN/Desktop/gamepy/data/assetss/pipe_bottom.png")
game_over_image = pygame.image.load("C:/Users/MSI-VN/Desktop/gamepy/data/assetss/game_over.png")
start_image = pygame.image.load('C:/Users/MSI-VN/Desktop/gamepy/data/assetss/start.png')
coin_image=pygame.image.load('C:/Users/MSI-VN/Desktop/gamepy/data/assetss/coin.png')
#boss_image=pygame.image.load('C:/Users/MSI-VN/Desktop/gamepy/data/assetss/boss.png')
coin_image = pygame.transform.scale(coin_image, (50, 40))
#boss_image = pygame.transform.scale(boss_image, (50, 40))
start_image= pygame.transform.scale2x(start_image)
# Game
scroll_speed = 2
bird_start_position = (100, 250)
score = 0
high_score=0
font = pygame.font.Font('C:/Users/MSI-VN/Desktop/gamepy/data/04B_19.TTF',26)
game_stopped = True

def update_score(score, high_score):
        if score>high_score:
            high_score=score
        return high_score
class Bird(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        if use_birdblue:
            self.image = birdblue[0]
        elif use_birdred:
            self.image = birdred[0]
        else:
            self.image = bird_images[0]
        self.rect = self.image.get_rect()
        self.rect.center = bird_start_position
        self.image_index = 0
        self.vel = 0
        self.flap = False
        self.alive = True

    def update(self, user_input):
        # Animate Bird
        if self.alive:
            self.image_index += 1
        if self.image_index >= 30:
            self.image_index = 0
        if use_birdblue:
            self.image = birdblue[self.image_index // 10]
        elif use_birdred:
            self.image = birdred[self.image_index // 10]
        else:
            self.image = bird_images[self.image_index // 10]

        # Gravity and Flap
        self.vel += 0.5
        if self.vel > 7:
            self.vel = 7
        if self.rect.y < 500:
            self.rect.y += int(self.vel)
        if self.vel == 0:
            self.flap = False

        # Rotate Bird
        self.image = pygame.transform.rotate(self.image, self.vel * -7)

        # User Input
        if user_input[pygame.K_SPACE] and not self.flap and self.rect.y > 0 and self.alive:
            self.flap = True
            self.vel = -7


class Pipe(pygame.sprite.Sprite):
    def __init__(self, x, y, image, pipe_type):
        pygame.sprite.Sprite.__init__(self)
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = x, y
        self.enter, self.exit, self.passed = False, False, False
        self.pipe_type = pipe_type

    def update(self):
        # Move Pipe
        self.rect.x -= scroll_speed
        if self.rect.x <= -win_width:
            self.kill()

        # Score
        global score
        if self.pipe_type == 'bottom':
            if bird_start_position[0] > self.rect.topleft[0] and not self.passed:
                self.enter = True
            if bird_start_position[0] > self.rect.topright[0] and not self.passed:
                self.exit = True
            if self.enter and self.exit and not self.passed:
                self.passed = True
                score += 1

class Coin(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = coin_image
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = x, y

    def update(self):
        # Move coin
        self.rect.x -= scroll_speed
        if self.rect.x <= -win_width:
            self.kill()

# class Boss(pygame.sprite.Sprite):
#     def __init__(self, x, y):
#         pygame.sprite.Sprite.__init__(self)
#         self.image = boss_image
#         self.rect = self.image.get_rect()
#         self.rect.x, self.rect.y = x, y

#     def update(self):
#         # Move boss
#         self.rect.x -= scroll_speed
#         if self.rect.x <= -win_width:
#             self.kill()

class Ground(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = ground_image
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = x, y

    def update(self):
        # Move Ground
        self.rect.x -= scroll_speed
        if self.rect.x <= -win_width:
            self.kill()


def quit_game():
    # Exit Game
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()


# Game Main Method
pipe_coordinates = []
coin_x = random.randint(0, 600)
coin_y = random.randint(0, 450)
# boss_x = random.randint(0, 600)
# boss_y = random.randint(0, 450)
def main():
    global score
    global high_score
    global pipe_coordinates, coin_x, coin_y
    # Instantiate Bird
    bird = pygame.sprite.GroupSingle()
    bird.add(Bird())

    # Setup Pipes
    pipe_timer = 0
    pipes = pygame.sprite.Group()

    # Instantiate Initial Ground
    x_pos_ground, y_pos_ground = 0, 520
    ground = pygame.sprite.Group()
    ground.add(Ground(x_pos_ground, y_pos_ground))
    # Instantiate coin
    coin = pygame.sprite.Group()
    while any(abs(coin_x - pipe_x) < 100 and abs(coin_y - pipe_y) < 200 for pipe_x, pipe_y in pipe_coordinates):
        coin_x = random.randint(0, 600)
        coin_y = random.randint(0, 450)
    pipe_coordinates.append((coin_x, coin_y))
    coin.add(Coin(coin_x, coin_y))
    # Instantiate boss
    # boss = pygame.sprite.Group()
    # boss_spawned = False  # Trạng thái xuất hiện của boss
    # while any(abs(boss_x - pipe_x) < 100 and abs(boss_y - pipe_y) < 200 for pipe_x, pipe_y in pipe_coordinates):
    #     boss_x = random.randint(0, 600)
    #     boss_y = random.randint(0, 450)
    # pipe_coordinates.append((boss_x, boss_y))
    #boss.add(Boss(boss_x, boss_y))

    run = True
    while run:
        # Quit
        quit_game()

        # Reset Frame
        window.fill((0, 0, 0))

        # User Input
        user_input = pygame.key.get_pressed()

        # Draw Background
        window.blit(skyline_image, (0, 0))

        # Spawn Ground
        if len(ground) <= 2:
            ground.add(Ground(win_width, y_pos_ground))
            while any(abs(coin_x - pipe_x) < 100 and abs(coin_y - pipe_y) < 200 for pipe_x, pipe_y in pipe_coordinates):
                coin_x = random.randint(0, 600)
                coin_y = random.randint(0, 450)
            pipe_coordinates.append((coin_x, coin_y))
            coin.add(Coin(coin_x, coin_y))

            # if not boss_spawned:  # Kiểm tra xem đã xuất hiện boss chưa
            #     while any(abs(boss_x - pipe_x) < 100 and abs(boss_y - pipe_y) < 200 for pipe_x, pipe_y in pipe_coordinates):
            #         boss_x = random.randint(0, 600)
            #         boss_y = random.randint(0, 450)
            #     pipe_coordinates.append((boss_x, boss_y))
            #     boss.add(Boss(boss_x, boss_y))
            #     boss_spawned = True
        # Draw - Pipes, Ground and Bird and Coin
        pipes.draw(window)
        ground.draw(window)
        bird.draw(window)
        coin.draw(window)
        #boss.draw(window)
        # Show Score
        score_text = font.render(f'Score: {int(score)}', True, (255,255,255))
        window.blit(score_text, (20, 20))

        # Update - Pipes, Ground and Bird
        if bird.sprite.alive:
            pipes.update()
            ground.update()
            coin.update()
            #boss.update()
        bird.update(user_input)

        # Collision Detection
        collision_pipes = pygame.sprite.spritecollide(bird.sprites()[0], pipes, False)
        collision_ground = pygame.sprite.spritecollide(bird.sprites()[0], ground, False)
        #collision_boss = pygame.sprite.spritecollide(bird.sprites()[0], boss, False)
        collision_coin = pygame.sprite.spritecollide(bird.sprites()[0], coin, True)
        if collision_coin:
            score+=1
        if collision_pipes or collision_ground: #or collision_boss:
            bird.sprite.alive = False
            if collision_ground:
                window.blit(game_over_image, (win_width // 2 - game_over_image.get_width() // 2,
                                              win_height // 2 - game_over_image.get_height() // 2))
                high_score=update_score(score,high_score )
                high_score_surface = font.render(f'High Score: {int(high_score)}', True, (255,255,255))
                window.blit(high_score_surface, (190,270))
                if user_input[pygame.K_r]:
                    score = 0
                    break
        # Spawn Pipes
        if pipe_timer <= 0 and bird.sprite.alive:
            x_top, x_bottom = 550, 550
            y_top = random.randint(-600, -480)
            y_bottom = y_top + random.randint(130, 150) + bottom_pipe_image.get_height()
            pipes.add(Pipe(x_top, y_top, top_pipe_image, 'top'))
            pipes.add(Pipe(x_bottom, y_bottom, bottom_pipe_image, 'bottom'))
            pipe_timer = random.randint(180, 250)
        pipe_timer -= 1

        clock.tick(60)
        pygame.display.update()
use_birdblue = False
use_birdred = False
# Menu
def menu():
    global game_stopped, use_birdblue, use_birdred
    while game_stopped:
        quit_game()

        # Draw Menu
        window.fill((0, 0, 0))
        window.blit(skyline_image, (0, 0))
        window.blit(ground_image, Ground(0, 520))
        window.blit(bird_images[0], (150, 250))
        window.blit(birdblue[0], (260, 250))
        window.blit(birdred[0], (370, 250))
        window.blit(start_image, (win_width // 2 - start_image.get_width() // 2,
                                  win_height // 2 - start_image.get_height() // 2))

        # User Input
        user_input = pygame.key.get_pressed()
        if user_input[pygame.K_1]:
            use_birdblue = False
            use_birdred = False
            main()
        elif user_input[pygame.K_2]:
            use_birdblue = True
            use_birdred = False
            main()
        elif user_input[pygame.K_3]:
            use_birdred = True
            use_birdblue = False
            main()
        pygame.display.update()


menu()