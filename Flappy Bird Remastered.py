#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pygame, sys, random


# In[2]:


def floor_loop():
    screen.blit(floor,(floor_x,500))
    screen.blit(floor,(floor_x + 576,500))

def create_pipe():
    random_pipe_pos = random.randint(200,400)
    bottom_pipe = pipe_surface.get_rect(midtop = (700,random_pipe_pos))
    top_pipe = pipe_surface.get_rect(midbottom = (700,random_pipe_pos-250))
    return bottom_pipe, top_pipe

def move_pipes(pipes):
    for pipe in pipes:
        pipe.centerx -= 5
        if pipe.midright[0] <= -100:
            pipes.pop(0)
    return pipes

def draw_pipes(pipes):
    for pipe in pipes:
        if pipe.bottom >= 576:
            screen.blit(pipe_surface, pipe)
        else:
            flip_pipe = pygame.transform.flip(pipe_surface,False,True)
            screen.blit(flip_pipe, pipe)

def check_collision(pipes):
    for pipe in pipes:
        if bird_rect.colliderect(pipe):
            return False
    if bird_rect.top<= -100 or bird_rect.bottom >= 500:
        return False
    
    return True

def rotate_bird(bird):
    new_bird = pygame.transform.rotozoom(bird, -bird_movement*3 , 1)
    return new_bird

def bird_animation():
    new_bird = bird_frames[bird_index]
    new_bird_rect = new_bird.get_rect(center=(100,bird_rect.centery))
    return new_bird, new_bird_rect

def score_display(game_state):
    if game_state == "main_game":
        score_surface = game_font.render(str(int(score)), True, (255,255,255))
        score_rect = score_surface.get_rect(center = (288,100))
        screen.blit(score_surface, score_rect)
    if game_state == "game_over":
        score_surface = game_font.render(f'Score: {int(score)}', True, (255,255,255))
        score_rect = score_surface.get_rect(center = (288,50))
        screen.blit(score_surface, score_rect)
        
        high_score_surface = game_font.render(f'High Score: {int(high_score)}', True, (255,255,255))
        high_score_rect = high_score_surface.get_rect(center = (288,480))
        screen.blit(high_score_surface, high_score_rect)
                                                             
def update_score(score, high_score):
    if score > high_score:
        high_score = score
    return high_score

pygame.init()
screen = pygame.display.set_mode((576,576))
clock = pygame.time.Clock() #Frame rates
game_font = pygame.font.Font(r"C:\Users\User\Desktop\04B_19__.TTF",40)


#Game Variables
gravity = 0.1
bird_movement = 0
game_active = True
score = 0
high_score = 0

bg_surface = pygame.image.load(r"C:\Users\User\Desktop\background-day.png").convert()
bg_surface = pygame.transform.scale(bg_surface, (576,625)) #Scales background

#Floor intialization
floor = pygame.image.load(r"C:\Users\User\Desktop\base.png").convert()
floor = pygame.transform.scale2x(floor)
floor_x = 0

#Bird initialization

bird_downflap = pygame.transform.scale2x(pygame.image.load(r"C:\Users\User\Desktop\yellowbird-downflap.png").convert_alpha())
bird_midflap = pygame.transform.scale2x(pygame.image.load(r"C:\Users\User\Desktop\yellowbird-midflap.png").convert_alpha())
bird_upflap = pygame.transform.scale2x(pygame.image.load(r"C:\Users\User\Desktop\yellowbird-upflap.png").convert_alpha())
bird_frames = [bird_downflap, bird_midflap, bird_upflap]
bird_index = 0
bird_surface = bird_frames[bird_index]
bird_rect = bird_surface.get_rect(center=(100, 256))

BIRDFLAP = pygame.USEREVENT + 1
pygame.time.set_timer(BIRDFLAP, 200)

#Pipe initialization
pipe_surface = pygame.image.load(r"C:\Users\User\Desktop\pipe-green.png").convert()
pipe_surface = pygame.transform.scale2x(pipe_surface)
pipe_list = []

#Spawn Pipe Event
SPAWNPIPE = pygame.USEREVENT
pygame.time.set_timer(SPAWNPIPE, random.randint(500,1000))

#Game Over Event
game_over_surface = pygame.transform.scale(pygame.image.load(r"C:\Users\User\Desktop\message.png").convert_alpha(), (288,288))
game_over_rect = game_over_surface.get_rect(center = (288,288))


while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and game_active:
                bird_movement = 0
                bird_movement -= 5
            if event.key == pygame.K_SPACE and game_active == False:
                game_active = True 
                pipe_list.clear()
                bird_rect.center =  (100,256)
                bird_movement = 0
                score = 0
        if event.type == SPAWNPIPE:
            pipe_list.extend(create_pipe())
            
        if event.type == BIRDFLAP:
            if bird_index < 2:
                bird_index += 1
            else:
                bird_index = 0
                
            bird_surface, bird_rect = bird_animation()
    screen.blit(bg_surface,(0,0))
    
    if game_active:
        #Bird
        bird_movement += gravity
        rotated_bird = rotate_bird(bird_surface)
        bird_rect.centery += bird_movement
        screen.blit(rotated_bird,bird_rect)
        game_active = check_collision(pipe_list)
        
        #Pipes
        pipe_list = move_pipes(pipe_list)
        draw_pipes(pipe_list)
        
        #Score
        score_display("main_game")
        for pipe in pipe_list:
            if bird_rect.centerx == pipe.centerx:
                score += 0.5
                score_display("main_game")
    else:
        screen.blit(game_over_surface, game_over_rect)
        high_score = update_score(score, high_score)
        score_display("game_over")
    
    #Floor
    floor_x -=1
    floor_loop()
    if floor_x <= -576:
        floor_x = 0
    
    pygame.display.update()
    clock.tick(120)

