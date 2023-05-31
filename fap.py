import pygame, sys, random 
def create_pipe():
    random_pipe_pos=random.choice(pipe_height)
    bot_pipe=pipe_surface.get_rect(midtop=(500,random_pipe_pos))
    top_pipe=pipe_surface.get_rect(midtop=(500,random_pipe_pos-680))
    return bot_pipe, top_pipe
def draw_floor():
     screen.blit(floor,(floor_x_pos,650))
     screen.blit(floor,(floor_x_pos+432,650))
def move_pipe(pipes):
    for pipe in pipes:
        pipe.centerx-=5
    return pipes
def draw_pipe(pipes):
    for pipe in pipes:
        if pipe.bottom>=600:
            screen.blit(pipe_surface, pipe)
        else:
            flip_pipe=pygame.transform.flip(pipe_surface, False, True)
            screen.blit(flip_pipe, pipe)
def check_vacham(pipes):
    for pipe in pipes:
        if bird_rect.colliderect(pipe):
            hit_sound.play()
            return False
    if bird_rect.top<=-75 or bird_rect.bottom>=650:    
        return False
    return True
def rotate_bird(bird1):
    new_bird=pygame.transform.rotozoom(bird1, -bird_movement*3, 1)
    return new_bird
def bird_animation():
    new_bird=bird_list[bird_index]
    new_bird_rect=new_bird.get_rect(center=(100, bird_rect.centery))
    return new_bird, new_bird_rect 
def score_display(game_state):
    if game_state == 'main game':
        score_surface = game_font.render(str(int(score)), True, (255,255,255))
        score_rect = score_surface.get_rect(center=(216,100))
        screen.blit(score_surface, score_rect)
    if game_state == 'game_over':
        score_surface = game_font.render(f'Score: {int(score)}', True, (255,255,255))
        score_rect = score_surface.get_rect(center=(216,100))
        screen.blit(score_surface, score_rect)

        high_score_surface = game_font.render(f'High Score: {int(high_score)}', True, (255,255,255))
        high_score_rect = high_score_surface.get_rect(center=(216,630))
        screen.blit(high_score_surface, high_score_rect)
def update_score(score, high_score):
    if score>high_score:
        high_score=score
    return high_score
pygame.mixer.pre_init(frequency=44100, size=-16, channels=2,buffer=512)
pygame.init()
screen= pygame.display.set_mode((432, 768))
clock = pygame.time.Clock()
game_font=pygame.font.Font('C:/Users/MSI-VN/Desktop/gamepy/data/04B_19.TTF',40)
#cacbientrochoi
gravity=0.25
bird_movement = 0
game_active=True
score=0
high_score=0
#chenbg
bg=pygame.image.load('C:/Users/MSI-VN/Desktop/gamepy/data/assets/background-night.png')
bg1=pygame.image.load('C:/Users/MSI-VN/Desktop/gamepy/data/assets/night.png')
bg2=pygame.image.load('C:/Users/MSI-VN/Desktop/gamepy/data/assets/snow.webp')
bg=pygame.transform.scale2x(bg)
lbg=[bg1,bg2,bg]
#chensan
floor=pygame.image.load('C:/Users/MSI-VN/Desktop/gamepy/data/assets/floor.png')
floor=pygame.transform.scale2x(floor)   
floor_x_pos = 0
#createbird
#bird=pygame.image.load('C:/Users/MSI-VN/Desktop/gamepy/data/assets/yellowbird-midflap.png')
#bird= pygame.transform.scale2x(bird)
bird_down=pygame.image.load('C:/Users/MSI-VN/Desktop/gamepy/data/assets/yellowbird-downflap.png')
bird_mid=pygame.image.load('C:/Users/MSI-VN/Desktop/gamepy/data/assets/yellowbird-midflap.png')
bird_up=pygame.image.load('C:/Users/MSI-VN/Desktop/gamepy/data/assets/yellowbird-upflap.png')
bird_down_blue=pygame.image.load('C:/Users/MSI-VN/Desktop/gamepy/data/assets/blue.png')
bird_mid_blue=pygame.image.load('C:/Users/MSI-VN/Desktop/gamepy/data/assets/blue.png')
bird_up_blue=pygame.image.load('C:/Users/MSI-VN/Desktop/gamepy/data/assets/blue.png')
bird_down_red=pygame.image.load('C:/Users/MSI-VN/Desktop/gamepy/data/assets/red.png')
bird_mid_red=pygame.image.load('C:/Users/MSI-VN/Desktop/gamepy/data/assets/red.png')
bird_up_red=pygame.image.load('C:/Users/MSI-VN/Desktop/gamepy/data/assets/red.png')
bird_over_rect= bird_mid.get_rect(center=(116,284))
birdblue_over_rect= bird_mid_blue.get_rect(center=(216,284))
birdred_over_rect= bird_mid_red.get_rect(center=(316,284))
bird_list_blue=[bird_down, bird_mid, bird_up]
bird_list=[bird_down_blue, bird_mid_blue, bird_up_blue]
bird_list_red=[bird_down_red, bird_mid_red, bird_up_red]
bird_index=0
bird=bird_list[bird_index]
bird_blue=bird_list_blue[bird_index]
bird_red=bird_list_red[bird_index]
bird_rect_blue=bird.get_rect(center=(100,384))
bird_rect=bird_blue.get_rect(center=(100,384))
bird_rect_red=bird_red.get_rect(center=(100,384))
#createtimerforbird
birdflap=pygame.USEREVENT+1
pygame.time.set_timer(birdflap,200)
#createpipe
pipe_surface=pygame.image.load('C:/Users/MSI-VN/Desktop/gamepy/data/assets/pipe-green.png')
pipe_surface= pygame.transform.scale2x(pipe_surface)
pipe_list=[]
#createtimer
spawnpipe=pygame.USEREVENT
pygame.time.set_timer(spawnpipe, 1500)
pipe_height=[200,300,400]
#createscreenend
game_over_surface = pygame.image.load('C:/Users/MSI-VN/Desktop/gamepy/data/assets/message.png')
game_over_rect= game_over_surface.get_rect(center=(216,484))
#Sound
flap_sound = pygame.mixer.Sound('C:/Users/MSI-VN/Desktop/gamepy/data/sound/sfx_wing.wav')
hit_sound = pygame.mixer.Sound('C:/Users/MSI-VN/Desktop/gamepy/data/sound/sfx_hit.wav')
score_sound = pygame.mixer.Sound('C:/Users/MSI-VN/Desktop/gamepy/data/sound/sfx_point.wav')
score_sound_countdown = 100
while True:
    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type==pygame.KEYDOWN:
            if event.key==pygame.K_SPACE and game_active:
                bird_movement=0 
                bird_movement=-7
                flap_sound.play()
            if event.type==pygame.KEYDOWN and game_active==False:
                game_active=True
                pipe_list.clear()
                bird_rect.center=(100,384)
                bird_movement=0
                score = 0
        if event.type==spawnpipe:
            pipe_list.extend(create_pipe())
            if bird_index<2:
                bird_index+=1
            else:
                bird_index=0
            bird, bird_rect=bird_animation()
    screen.blit(bg1,(0,0))
    if game_active:
        #chim
        bird_movement+=gravity
        rotated_bird=rotate_bird(bird)
        bird_rect.centery+=bird_movement
        screen.blit(rotated_bird, bird_rect)
        game_active=check_vacham(pipe_list)
        #ong
        pipe_list=move_pipe(pipe_list) 
        draw_pipe(pipe_list)
        score+=0.01
        score_display('main game')
        score_sound_countdown-=1
        if score_sound_countdown <= 0:
            score_sound.play()
            score_sound_countdown =100
        
    else:
        screen.blit(game_over_surface, game_over_rect)
        screen.blit(bird_mid, bird_over_rect)
        screen.blit(bird_mid_blue, birdblue_over_rect)
        screen.blit(bird_mid_red, birdred_over_rect)
        high_score=update_score(score,high_score )
        score_display('game_over')
    #san 
    floor_x_pos-=1
    draw_floor()
    if floor_x_pos<=-432:
        floor_x_pos=0
    pygame.display.update()
    clock.tick(120)