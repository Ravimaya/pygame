import pygame
import engine

import pygame
from pygame import mixer

def drawText(t, x, y):
    text_surface = font.render(t, True, MUSTARD, DARK_GREY)
    text_rectangle = text_surface.get_rect()
    text_rectangle.topleft = (x, y)
    screen.blit(text_surface, text_rectangle)

# constant variables
SCREEN_SIZE = (700,500)
DARK_GREY = (50,50,50)
MUSTARD =  (209,206,25)

# init
pygame.init()
screen = pygame.display.set_mode(SCREEN_SIZE)
pygame.display.set_caption('Rik\'s Platform Game')
clock = pygame.time.Clock()
font = pygame.font.Font(pygame.font.get_default_font(), 24)

# game states = playing // win // lose
game_state = 'playing' 

# player
pygame_image = pygame.image.load("C:\\Users\\user\\Desktop\\pygame\\images\\vita_00.png")
player_x = 300

player_y = 0
player_speed = 0
player_acceleration = 0.2

player_width = 55
player_height = 55

player_direction = 'right'

# platforms
platforms = [
    # middle
   pygame.Rect(100,300,400,50),
   # left
   pygame.Rect(100,250,50,50),
   # right
   pygame.Rect(450,250,50,50)
]

# coins
coin_image = pygame.image.load("C:\\Users\\user\\Desktop\\pygame\\images\\coin_0.png")
coin_animation = engine.Animation([
    pygame.image.load("C:\\Users\\user\\Desktop\\pygame\\images\\coin_0.png"),
    pygame.image.load("C:\\Users\\user\\Desktop\\pygame\\images\\coin_1.png"),
    pygame.image.load("C:\\Users\\user\\Desktop\\pygame\\images\\coin_2.png"),
    pygame.image.load("C:\\Users\\user\\Desktop\\pygame\\images\\coin_3.png"),
    pygame.image.load("C:\\Users\\user\\Desktop\\pygame\\images\\coin_4.png"),
    pygame.image.load("C:\\Users\\user\\Desktop\\pygame\\images\\coin_5.png")
]) 
coins = [
    pygame.Rect(100,200,21,22),
    pygame.Rect(210,250,21,22)
]

score = 0

# enemies
enemy_image = pygame.image.load("C:\\Users\\user\\Desktop\\pygame\\images\\spiky_monster.png")
enemies = [
    pygame.Rect(150,260,50,39)  
]

lives = 3
heart_image = pygame.image.load("C:\\Users\\user\\Desktop\\pygame\\images\\heart.png")

running = True
while running:
    
    # check for quit
    for event in pygame.event.get():
        print(event)
        if event.type == pygame.QUIT:
            running = False
            
    if game_state == 'playing':        
               
        new_player_x = player_x
        new_player_y = player_y
            
        # player input
        keys = pygame.key.get_pressed()
        # a=left
        if keys[pygame.K_a]:
            new_player_x -= 2
            player_direction = 'left'
            player_state = 'left'
        # d=right
        if keys[pygame.K_d]:
            new_player_x += 2
            player_direction = 'right'
            player_state = 'right'
        if not keys[pygame.K_a] and not keys[pygame.K_d]:
            player_state = 'idle' 
        # w=jump 
        if keys[pygame.K_w]:
            player_speed = -5
            jump_Sound = mixer.Sound("C:\\Users\\user\\Desktop\\pygame\\sounds\\01_Jump_v2.ogg")
            jump_Sound.play()
    
    
    if game_state == 'playing':

       # update coin animation
        coin_animation.update()
    
       # horizontal movement
    
        new_player_rect = pygame.Rect(new_player_x,player_y,player_width,player_height)
        x_collision = False
    
       #...check against every platform
        for p in platforms:
            if p.colliderect(new_player_rect):
                x_collision = True
                break
    
        if x_collision == False:
            player_x = new_player_x
        
        # vertical movement
    
        player_speed += player_acceleration
        new_player_y += player_speed
    
        new_player_rect = pygame.Rect(player_x,new_player_y,player_width,player_height)
        y_collision = False
        player_on_ground = False
    
        #...check against every platform
        for p in platforms:
            if p.colliderect(new_player_rect):
                y_collision = True
                player_speed = 0
                # if the platform is below the player
                if p[1] > new_player_y:
                    # stick the player to the platform
                    player_y = p[1] - player_height
                    player_on_ground = True
                break
    
        print(player_on_ground)
    
        if y_collision == False:
            player_y = new_player_y
      
        # see if any coins have been collected
        player_rect = pygame.Rect(player_x, player_y, player_width, player_height)
        for c in coins:
            if c.colliderect(player_rect):
                coins.remove(c)
                score += 1
                coin_Sound = mixer.Sound("C:\\Users\\user\\Desktop\\pygame\\sounds\\01_Coin Pickup_v2.ogg")
                coin_Sound.play()
                # win if the score is 2
                if score >= 2:
                    game_state = 'win'
                    
            
        # see if any player has hit an enemy
        for e in enemies:
            if e.colliderect(player_rect):
                lives -= 1
                enemy_Sound = mixer.Sound("C:\\Users\\user\\Desktop\\pygame\\sounds\\04_Death_v2.ogg")
                enemy_Sound.play()
                # reset player position
                player_x = 300
                player_y = 0
                player_speed = 0 
                # change the game state
                # if no lives remaining
                if lives <= 0:
                    game_state = 'lose'     
                             
    # background
    screen.fill(DARK_GREY)
    
    # platforms
    for p in platforms:
        pygame.draw.rect(screen, MUSTARD, p)
        
    # coins
    for c in coins:
        #screen.blit(coin_image, (c.x, c.y))
         coin_animation.draw(screen, c.x, c.y)
        
    # enemies
    for e in enemies:
        screen.blit(enemy_image, (e.x, e.y))
        
    # player
    if player_direction == 'right':
        screen.blit(pygame_image, (player_x, player_y))
    elif player_direction == 'left':
        screen.blit(pygame.transform.flip(pygame_image, True, False), (player_x, player_y))
    
    
    # score
    screen.blit(coin_image, (10, 10))
    drawText(str(score), 50, 10)
    
    # lives
    for l in range(lives):
        screen.blit(heart_image, (200 + (l*50), 0)) 
            
    if game_state == 'win':
       drawText('You win!', 50, 50)
    if game_state == 'lose':
       drawText('You lose!', 50, 50)
    
    # present screen
    pygame.display.flip()
    
    clock.tick(60)
      
# quit
pygame.quit()