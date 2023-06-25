import pygame
from sys import exit
import random
pygame.init()
clock = pygame.time.Clock()
# Dựng cửa sổ khung hình
win_height = 720
win_width = 551
window = pygame.display.set_mode((win_width, win_height))
# Thêm hình ảnh cho các đối tượng
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
coin_image = pygame.transform.scale(coin_image, (50, 40))
start_image= pygame.transform.scale2x(start_image)

flap_sound = pygame.mixer.Sound('C:/Users/MSI-VN/Desktop/gamepy/data/sound/sfx_wing.wav')
hit_sound = pygame.mixer.Sound('C:/Users/MSI-VN/Desktop/gamepy/data/sound/sfx_hit.wav')
score_sound = pygame.mixer.Sound('C:/Users/MSI-VN/Desktop/gamepy/data/sound/sfx_point.wav')

sur_image=pygame.image.load("C:/Users/MSI-VN/Desktop/gamepy/data/assetss/tao.png")
sur_image = pygame.transform.scale(sur_image, (40, 40))

bom_image=pygame.image.load('C:/Users/MSI-VN/Desktop/gamepy/data/assetss/dan.png')
bom_image = pygame.transform.scale(bom_image, (60, 140))

boss_image=pygame.image.load('C:/Users/MSI-VN/Desktop/gamepy/data/assetss/sr.png')
boss_image = pygame.transform.scale(boss_image, (60, 50))
# Các biến tính toán
scroll_speed = 2
bird_start_position = (100, 250)
score = 0
coin_score = 0
high_score=0
font = pygame.font.Font('C:/Users/MSI-VN/Desktop/gamepy/data/04B_19.TTF',26)
game_stopped = True
sur=0
# hàm tính điểm cao (high score)
def update_score(score, high_score):
        if score>high_score:
            high_score=score
        return high_score
# Lớp đối tượng chim
class Bird(pygame.sprite.Sprite):
    def __init__(self):
        #thiết lập các biến giá trị
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
        # Thiết lập đập cánh
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
            flap_sound.play()
#Lớp ống
class Pipe(pygame.sprite.Sprite):
    def __init__(self, x, y, image, pipe_type):
        #thiết lập các biến giá trị
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
                score_sound.play()
                score += 1    
#Lớp đồng tiền           
class Coin(pygame.sprite.Sprite):
    def __init__(self, x, y):
        #thiết lập các biến giá trị
        pygame.sprite.Sprite.__init__(self)
        self.image = coin_image
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = x, y
    def update(self):
        # Move coin
        self.rect.x -= scroll_speed
        if self.rect.x <= -win_width:
            self.kill()
class SRV(pygame.sprite.Sprite):
    def __init__(self, x, y):
        #thiết lập các biến giá trị
        pygame.sprite.Sprite.__init__(self)
        self.image = sur_image
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = x, y
    def update(self):
        # Move chướng ngại vật
        self.rect.x -= scroll_speed
        if self.rect.x <= -win_width:
            self.kill()
#Lớp viên đạn bắn ra
class Bom(pygame.sprite.Sprite):
    def __init__(self, x, y):
        #thiết lập các biến giá trị
        pygame.sprite.Sprite.__init__(self)
        self.image = bom_image
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = x, y
    def update(self):
        # Move Bom
        self.rect.x += 4
        if self.rect.x >= win_width:
            self.kill()
#Lớp chướng ngại vật
class Boss(pygame.sprite.Sprite):
    def __init__(self, x, y):
        #thiết lập các biến giá trị
        pygame.sprite.Sprite.__init__(self)
        self.image = boss_image
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = x, y
    def update(self):
        # Move Boss
        self.rect.x -= scroll_speed
        if self.rect.x <= -win_width:
            self.kill()
    def remove(self):
        self.rect.x += 2
        if self.rect.x >= win_width:
            self.kill()
#Lớp sàn
class Ground(pygame.sprite.Sprite):
    def __init__(self, x, y):
        #thiết lập các biến giá trị
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
# Hàm chính của game
def main():
    global score, sur, coin_score
    global high_score
    # Instantiate Bird
    bird = pygame.sprite.GroupSingle()
    bird.add(Bird())
    # Setup Pipes
    pipe_timer = 0
    boss_timer=0
    pipes = pygame.sprite.Group()
    # Instantiate Initial Ground
    x_pos_ground, y_pos_ground = 0, 520
    ground = pygame.sprite.Group()
    ground.add(Ground(x_pos_ground, y_pos_ground))
    # Instantiate coin, boom, boss, sur
    coin = pygame.sprite.Group()
    boom = pygame.sprite.Group()
    boss=pygame.sprite.Group()
    surr = pygame.sprite.Group()
    surr1 = pygame.sprite.Group()
    surr2 = pygame.sprite.Group()
    
    surr.add(SRV(5, 470))
    surr1.add(SRV(55, 470))
    surr2.add(SRV(105, 470))
    run = True
    state_play=True
    while run:
        # Quit
        quit_game()
        # Reset Frame
        window.fill((0, 0, 0))
        # User Input
        user_input = pygame.key.get_pressed()
        # Draw Background
        window.blit(skyline_image, (0, 0))
        # Draw - Pipes, Ground and Bird and Coin and Boss and Boom and SUR (chướng ngại vật)
        pipes.draw(window)
        ground.draw(window)
        bird.draw(window)
        coin.draw(window)
        boss.draw(window)
        boom.draw(window)
        if sur==2:
            surr.draw(window)
            surr1.draw(window)
            surr2.draw(window)
        elif sur==1:
            surr.draw(window)
            surr1.draw(window)
        elif sur==0:
            surr.draw(window)
        #timespawn
        if len(ground) <= 2:
            ground.add(Ground(win_width, y_pos_ground))
            coin.add(Coin(random.randint(100, 400), random.randint(0, 450)))
        if boss_timer <= 0 and bird.sprite.alive:   
            x_boss=random.randint(400, 900)
            y_boss=random.randint(150, 400)
            boss.add(Boss(x_boss,y_boss))
            boss_timer = random.randint(200, 250)
        boss_timer-=0.5
        # Show Score
        score_text = font.render(f'Score: {int(score)}', True, (255,255,255))
        coin_score_text = font.render(f'Coin: {int(coin_score)}', True, (255,255,255))
        window.blit(score_text, (20, 20))
        window.blit(coin_score_text, (20, 50))
        # Update - Pipes, Ground and Bird
        if bird.sprite.alive:
            pipes.update()
            ground.update()
            coin.update()
            boss.update()
            boom.update()
            if user_input[pygame.K_p]:
                boom.add(Bom(0, y_boss))
        bird.update(user_input)
        # Collision Detection
        collision_pipes = pygame.sprite.spritecollide(bird.sprites()[0], pipes, False)
        collision_ground = pygame.sprite.spritecollide(bird.sprites()[0], ground, False)
        collision_coin = pygame.sprite.spritecollide(bird.sprites()[0], coin, True)
        collision_boss = pygame.sprite.spritecollide(bird.sprites()[0], boss, False)
        collision_sprites = pygame.sprite.groupcollide(boss, boom, False, False)
        if collision_sprites:
            boss.remove(boss)
        if collision_coin:
            score_sound.play()
            coin_score+=1
            if sur<2:
                if coin_score%3==0:
                    sur+=1
        if collision_pipes or collision_ground or collision_boss:
            if sur==0:
                if state_play==True:
                    hit_sound.play()
                    state_play=False
                bird.sprite.alive = False
                if collision_ground:
                    window.blit(game_over_image, (win_width // 2 - game_over_image.get_width() // 2,
                                                win_height // 2 - game_over_image.get_height() // 2))
                    high_score=update_score(score,high_score )
                    high_score_surface = font.render(f'High Score: {int(high_score)}', True, (255,255,255))
                    window.blit(high_score_surface, (190,270))
                    surr.update()
                    if user_input[pygame.K_r]:
                        score = 0
                        coin_score = 0
                        break
            else:
                sur-=1
                main()
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