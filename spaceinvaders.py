import pygame
import random
import math
from pygame import mixer


# credits
# Icon :: Icons made by <a href="https://www.flaticon.com/authors/icongeek26" title="Icongeek26">Icongeek26</a> from <a href="https://www.flaticon.com/" title="Flaticon"> www.flaticon.com</a>
# Player : <div>Icons made by <a href="https://www.flaticon.com/authors/freepik" title="Freepik">Freepik</a> from <a href="https://www.flaticon.com/" title="Flaticon">www.flaticon.com</a></div>

class button():
    def __init__(self, color, x, y, width, height, text=''):
        self.color = color
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.text = text

    def draw(self, win, outline=None):
        # Call this method to draw the button on the screen
        if outline:
            pygame.draw.rect( win, outline, (self.x - 2, self.y - 2, self.width + 4, self.height + 4), 0 )

        pygame.draw.rect( win, self.color, (self.x, self.y, self.width, self.height), 0 )

        if self.text != '':
            font = pygame.font.SysFont( 'comicsans', 20 )
            text = font.render( self.text, 1, (0, 0, 0) )
            win.blit( text, (
            self.x + (self.width / 2 - text.get_width() / 2), self.y + (self.height / 2 - text.get_height() / 2)) )

    def isOver(self, pos):
        # Pos is the mouse position or a tuple of (x,y) coordinates
        if pos[0] > self.x and pos[0] < self.x + self.width:
            if pos[1] > self.y and pos[1] < self.y + self.height:
                return True

        return False



pygame.init()
# create screen
screen = pygame.display.set_mode( (800, 600) )

# Background
background = pygame.image.load( 'background.png' )

# Background sound




# Title and icon

pygame.display.set_caption( 'Space Invaders' )
icon = pygame.image.load( 'spaceship.png' )
pygame.display.set_icon( icon )

# Player
playerImg = pygame.image.load( 'Player.png' )
playerX = 370
playerY = 480
playerX_change = 0

mute_state = 'off'

# enemy
enemyImg=[]
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []
num_of_enemies = 6

for i in range(num_of_enemies):



    enemyImg.append (pygame.image.load( 'enemy.png' ))
    enemyX.append( random.randint(0, 736))
    enemyY.append( random.randint(50, 150))
    enemyX_change.append(3)
    enemyY_change.append(40)


# bullet
bulletImg = pygame.image.load('bullet.png')
bulletX = 0
bulletY = 480
bulletX_change = 0
bulletY_change = 6
bullet_state = 'ready'

score_value = 0
font = pygame.font.Font('freesansbold.ttf',32)

textX = 10
textY = 10
mixer.music.load( 'background.wav' )
mixer.music.play( -1 )

#Game over
over_font = pygame.font.Font('freesansbold.ttf',64)


def show_score(x,y):
    score = font.render('Score: '+str(score_value), True, (255,255,255))
    screen.blit(score,(x, y))

def game_over_text():
    over_text = over_font.render( 'GAME OVER', True, (255, 255, 255) )
    screen.blit(over_text,(200,250))



def player(x, y):
    screen.blit( playerImg, (x, y) )


def enemy(x, y, i):
    screen.blit( enemyImg[i], (x, y) )

def fire_bullet(x,y):
    global bullet_state
    bullet_state = 'fire'
    screen.blit(bulletImg,(x + 16,y + 10))

def isCollision(enemyX,enemyY,bulletX,bulletY):
    distence = math.sqrt((math.pow(enemyX-bulletX,2)) + (math.pow(enemyY-bulletY,2)))
    if distence < 27:
        return True
    else:
        return False

def music(mute_state):
    if mute_state is 'off':
        mixer.music.play( -1 )
    if mute_state is 'on':
        mixer.music.pause()
def levels(enemy_speed, num_of_enemies):
        enemy_speed+= 1
        num_of_enemies += 2


music(mute_state)

# Game loop
running = True
while running:
    # Background
    screen.fill( (0, 0, 0) )
    # Backgound image
    screen.blit( background, (0, 0) )
    mute_button = button((225,225,225),200,2,80,40,text='Mute Music')
    mute_button.draw(screen,(0,0,0))








    # Events
    for event in pygame.event.get():
        # Mute Button
        if event.type == pygame.QUIT:
            running = False


        pos = pygame.mouse.get_pos()
        if event.type == pygame.MOUSEBUTTONDOWN:
            if mute_button.isOver(pos):
                if mute_state is 'on':
                    mute_state = 'off'
                    music(mute_state)
                    print('play music')

                elif mute_state is 'off':
                    mute_state = 'on'
                    music(mute_state)
                    print( 'pause music' )









        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                playerX_change = -5
            if event.key == pygame.K_RIGHT:
                playerX_change = 5

            if event.key == pygame.K_SPACE:
                if bullet_state is 'ready':
                    bullet_sound= mixer.Sound('laser.wav')
                    bullet_sound.play()
                    bulletX = playerX
                    fire_bullet(bulletX,bulletY)

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_RIGHT or event.key == pygame.K_LEFT:
                playerX_change = 0

    #  Boundries
    playerX += playerX_change

    if playerX <= 0:
        playerX = 0
    elif playerX >= 736:
        playerX = 736


    for i in range (num_of_enemies):

        if enemyY[i] > 440:
            for j in range( num_of_enemies ):
                enemyY[j] = 2000
            game_over_text()
            break
        enemyX[i] += enemyX_change[i]
        if enemyX[i] <= 0:
            enemyX_change[i]= 3
            enemyY[i] += enemyY_change[i]
        elif enemyX[i]>= 736:
            enemyX_change[i] = -3
            enemyY[i] += enemyY_change[i]


        # Collision
        collision = isCollision( enemyX[i], enemyY[i], bulletX, bulletY )
        if collision:
            explosion_sound = mixer.Sound( 'explosion.wav' )
            explosion_sound.play()
            bulletY = 480
            bullet_state = 'ready'
            score_value += 1

            enemyX[i] = random.randint( 0, 735 )
            enemyY[i]= random.randint( 50, 150 )
        enemy( enemyX[i], enemyY[i], i )

    # bullet movement
    if bulletY <=0 :
        bulletY =480
        bullet_state= 'ready'
    if bullet_state is 'fire':
        fire_bullet(bulletX,bulletY)
        bulletY-= bulletY_change









    player( playerX, playerY )
    show_score(textX,textY)
    pygame.display.update()
