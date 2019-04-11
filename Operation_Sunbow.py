# Imports
import pygame
import random
import math
from fleets import fleets

# Initialize game engine
pygame.init()


# Window
WIDTH = 1400
HEIGHT = 1000
SIZE = (WIDTH, HEIGHT)
TITLE = "Operation Sunbow"
screen = pygame.display.set_mode(SIZE, pygame.FULLSCREEN)
pygame.display.set_caption(TITLE)


# Timer
clock = pygame.time.Clock()
refresh_rate = 60

     
# Colors
RED = (255, 0, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
YELLOW = (255, 255, 0)
GREEN = (100, 255, 100)


# Fonts
FONT_SM = pygame.font.Font(None, 24)
FONT_MD = pygame.font.Font("assets/fonts/spacerangerboldital.ttf", 40)
FONT_LG = pygame.font.Font("assets/fonts/spacerangerboldital.ttf", 64)
FONT_XL = pygame.font.Font("assets/fonts/spacerangerboldital.ttf", 96)


# Images
ship_img1 = pygame.image.load('assets/images/Powerglide1.png').convert_alpha()
'''ship_img2 = pygame.image.load('assets/images/Powerglide2.png').convert_alpha()'''

laserRed_img = pygame.image.load('assets/images/PGLaser.png').convert_alpha()
laserGreen_img = pygame.image.load('assets/images/ConLaser.png').convert_alpha()
biglaser_img = pygame.image.load('assets/images/ConBigLaser.png').convert_alpha()

enemyship_img = pygame.image.load('assets/images/seeker1.png').convert_alpha()
enemyship1_img = pygame.image.load('assets/images/seeker2.png').convert_alpha()

space_img = pygame.image.load('assets/images/GalagaBackground.jpeg').convert_alpha()

shieldpowerup_img = pygame.image.load('assets/images/ShieldPow.png').convert_alpha()
laserpowerup_img = pygame.image.load('assets/images/LaserPow.png').convert_alpha()

Thomas_img = pygame.image.load('assets/images/Thomas.png').convert_alpha()

# Sounds
EXPLOSION1 = pygame.mixer.Sound('assets/sounds/PlayerExplosion.wav')
EXPLOSION2 = pygame.mixer.Sound('assets/sounds/EnemyExplosion.wav')
LASER1 = pygame.mixer.Sound('assets/sounds/AutobotLaser.wav')
LASER2 = pygame.mixer.Sound('assets/sounds/DecepticonLaser.wav')
WHISTLE = pygame.mixer.Sound('assets/sounds/Thomas Whistle2.wav')
Damage = pygame.mixer.Sound('assets/sounds/Damage.wav')
Powerup = pygame.mixer.Sound('assets/sounds/Powerup.wav')

# Stages
START = 0
PLAYING = 1
BADEND = 2
GOODEND = 3
INTRO = 4

# Other
fleet_no = 0
Thomas = False

# Game classes
class Ship(pygame.sprite.Sprite):
    def __init__(self,image):
        super().__init__()

        self.image = image
        self.rect = self.image.get_rect()
        self.speed = 7
        self.shield = 1
        self.double_shot = False
        
    def move_left(self):
        self.rect.x -= self.speed
    
    def move_right(self):
        self.rect.x += self.speed
        
    def move_up(self):
        self.rect.y -= self.speed
    
    def move_down(self):
        self.rect.y += self.speed

    def shoot(self):
            if self.double_shot == False:
                if len(lasers) < 3:
                    LASER1.play()
                    print("LASER SOUND")
                    laser = Laser(laserRed_img)
                    laser.rect.centerx = self.rect.centerx
                    laser.rect.centery = self.rect.top
                    lasers.add(laser)
            else:
                if len(lasers) < 6:
                    LASER1.play()
                    print("DOUBLE LASER SOUND")
                    laser1 = Laser(laserRed_img)
                    laser1.rect.centerx = self.rect.right
                    laser1.rect.y = self.rect.top
                    laser2 = Laser(laserRed_img)
                    laser2.rect.centerx = self.rect.left
                    laser2.rect.y = self.rect.top
                    lasers.add(laser1, laser2)

    def update(self):
        if self.rect.left < 0:
            self.rect.left = 0
        elif self.rect.right > WIDTH:
            self.rect.right = WIDTH

        if self.rect.top < 0:
            self.rect.top = 0
        elif self.rect.bottom > HEIGHT:
            self.rect.bottom = HEIGHT


        hit_list = pygame.sprite.spritecollide(self, powerups, True)

        for hit in hit_list:
            hit.apply(self)
        
        hit_list = pygame.sprite.spritecollide(self, bombs, True)

        for hit in hit_list:
            self.shield -= 1
            if self.shield > 0:
                Damage.play()
                
            if self.shield == 0:
                pygame.mixer.music.stop()
                EXPLOSION1.play()
                print("OUCH!")
                self.kill()

        hit_list = pygame.sprite.spritecollide(self, mobs, True)

        if len(hit_list) > 0:
            pygame.mixer.music.stop()
            EXPLOSION1.play()
            print("OUCH!")
            self.kill()
        
class Laser(pygame.sprite.Sprite):    
    def __init__(self, image):
        super().__init__()

        self.image = image
        self.rect = self.image.get_rect()

        self.speed = 20

    def update(self):
        self.rect.y -= self.speed

        if self.rect.bottom < 0:
            self.kill()

class Mob1(pygame.sprite.Sprite):
    def __init__(self, x, y, image):
        super().__init__()

        self.image = image
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def bomb(self):
        LASER2.play()
        print("LASER SOUND")

        bomb = Bomb(laserGreen_img)
        bomb.rect.centerx = self.rect.centerx
        bomb.rect.centery = self.rect.bottom
        bombs.add(bomb)

    def update(self):
        hit_list = pygame.sprite.spritecollide(self, lasers, True)

        if len(hit_list) > 0:
            player.score += 100
            EXPLOSION2.play()
            self.kill()

class Mob2(pygame.sprite.Sprite):
    def __init__(self, x, y, image):
        super().__init__()

        self.image = image
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def bomb(self):
        LASER2.play()
        print("LASER SOUND")

        bomb = Bomb(biglaser_img)
        bomb.rect.centerx = self.rect.centerx
        bomb.rect.centery = self.rect.bottom
        bombs.add(bomb)

    def update(self):
        hit_list = pygame.sprite.spritecollide(self, lasers, True)

        if len(hit_list) > 0:
            player.score += 200
            EXPLOSION2.play()
            self.kill()

class Bomb(pygame.sprite.Sprite):
    def __init__(self, image):
        super().__init__()

        self.image = image
        self.rect = self.image.get_rect()

        self.speed = 10

    def update(self):
        self.rect.y += self.speed

        if self.rect.bottom > HEIGHT:
            self.kill()

class ShieldPowerUp(pygame.sprite.Sprite):
    def __init__(self, x, y, image):
        super().__init__()

        self.image = image
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.speed = 5

    def apply(self, ship):
        Powerup.play()
        ship.shield += 2
        self.kill()

    def update(self):
        self.rect.y += self.speed

        if self.rect.top > HEIGHT:
            self.kill()

class LaserPowerUp(pygame.sprite.Sprite):
    def __init__(self, x, y, image):
        super().__init__()

        self.image = image
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.speed = 5

    def apply(self, ship):
        Powerup.play()
        ship.double_shot = True
        self.kill()

    def update(self):
        self.rect.y += self.speed

        if self.rect.top > HEIGHT:
            self.kill()

class Fleet():
    def __init__(self, mobs):
        self.mobs = mobs
        self.speed = 3
        self.moving_right = True
        self.drop_speed = 8
        self.bomb_rate = 30 # lower is faster

    def move(self):
        hits_edge = False

        for m in mobs:
            if self.moving_right:
                m.rect.x += self.speed

                if m.rect.right >= WIDTH:
                    hits_edge = True
            else:
                m.rect.x -= self.speed

                if m.rect.left <= 0:
                    hits_edge = True

        if hits_edge:
            self.reverse()
            self.move_down()

    def reverse(self):
        self.moving_right = not self.moving_right

    def move_down(self):
        for m in mobs:
            m.rect.y += self.drop_speed

    def choose_bomber(self):
        rand = random.randrange(self.bomb_rate)
        mob_list = mobs.sprites()
        
        if len(mob_list) > 0 and rand == 0:
            bomber = random.choice(mob_list)
            bomber.bomb()
        
    def update(self):
        self.move()
        self.choose_bomber()

    def __len__(self):
        return len(mobs)
        
# Game helper functions
def show_title_screen():
    title_text1 = FONT_MD.render("The Transformers", 0, RED)
    title_text2 = FONT_XL.render("Operation Sunbow", 0, YELLOW)
    w1 = title_text1.get_width()
    w2 = title_text2.get_width()
    screen.blit(title_text1, [WIDTH/2 - w1/2, 350])
    screen.blit(title_text2, [WIDTH/2 - w2/2, 400])

def konami_code():
    global KEYS, code, Thomas
    
    _up = 273
    _down = 274
    _left = 276
    _right = 275
    _x = 120
    _z = 122
    _enter = 13

    _code = [273, 273, 274, 274, 276, 275, 276, 275, 120, 122, 13]
    
    if len(KEYS) > 11:
        del KEYS[0]

    if KEYS == _code:
        WHISTLE.play()
        ship.image = Thomas_img
        ship.rect = ship.image.get_rect()
        ship.shield = 3
        ship.rect.centerx = WIDTH / 2
        ship.rect.bottom = HEIGHT - 30
        Thomas = True

def game_over():
    text1 = FONT_LG.render("GAME OVER", 0, WHITE)
    text2 = FONT_LG.render("Press SPACE to restart.", 0, WHITE)
    w1 = text1.get_width()
    w2 = text2.get_width()
    screen.blit(text1, [WIDTH/2 - w1/2, 450])
    screen.blit(text2, [WIDTH/2 - w2/2, 500])

def get_ready():
    global ticks, stage
    ticks -= 1

    text = FONT_MD.render("READY", 0, WHITE)
    w = text.get_width()
    screen.blit(text, [WIDTH/2 - w/2, HEIGHT/2])
    if ticks == 0:
        stage = PLAYING
        
def show_stats():
    score_text = FONT_MD.render(str(player.score), 1, WHITE)
    score_rect = score_text.get_rect()
    score_rect.centerx = WIDTH / 2
    score_rect.top = 20
    screen.blit(score_text, score_rect)

def prep_fleet(fleet, mobs):
    for mob in fleet:
        if mob[0] == "a":
            mobs.add(Mob1(mob[1], mob[2], enemyship_img))
        if mob[0] == "b":
            mobs.add(Mob2(mob[1], mob[2], enemyship1_img))

def game_win():
    text1 = FONT_LG.render("You've done it hooray!", 0, WHITE)
    text2 = FONT_LG.render("Press SPACE to restart.", 0, WHITE)
    w1 = text1.get_width()
    w2 = text2.get_width()
    screen.blit(text1, [WIDTH/2 - w1/2, 450])
    screen.blit(text2, [WIDTH/2 - w2/2, 500])

def setup():
    global stage, done, ticks, powerups, KEYS, Thomas
    global player, ship, lasers, mobs, fleet, bombs, fleet_no

    fleet_no = 0
    
    ''' Make game objects '''
    ship = Ship(ship_img1)
    ship.rect.centerx = WIDTH / 2
    ship.rect.bottom = HEIGHT - 30

    ''' Make sprite groups '''
    player = pygame.sprite.GroupSingle()
    player.add(ship)
    player.score = 0

    lasers = pygame.sprite.Group()
    bombs = pygame.sprite.Group()
    
    mobs = pygame.sprite.Group()
    prep_fleet(fleets[fleet_no], mobs)

    fleet = Fleet(mobs)

    powerup1 = ShieldPowerUp(200, -2000, shieldpowerup_img)
    powerup2 = LaserPowerUp(800, -4000, laserpowerup_img)
    powerups = pygame.sprite.Group()
    powerups.add(powerup1, powerup2)
    
    ticks = 90    
    ''' music '''
    pygame.mixer.music.load("assets/sounds/Title2.wav")
    pygame.mixer.music.play(0)
    
    ''' set stage '''
    stage = START
    done = False
    KEYS = []
    
# Game loop
setup()

while not done:
    # Input handling (React to key presses, mouse clicks, etc.)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                done = True
            if stage == START:
                if event.key == pygame.K_SPACE:
                    if Thomas == False:
                        pygame.mixer.music.load("assets/sounds/Powerglide2.wav")
                        pygame.mixer.music.play(-1)
                    else:
                        pygame.mixer.music.load("assets/sounds/Thomas2.wav")
                        pygame.mixer.music.play(-1)
                    stage = INTRO
                else:
                    KEYS.append(event.key)
                    print(KEYS)
                    konami_code()
            elif stage == PLAYING:
                if event.key == pygame.K_z:
                    ship.shoot()                
            elif stage == BADEND:
                if event.key == pygame.K_SPACE:
                    setup()
                    stage = START
            
    pressed = pygame.key.get_pressed()

    if stage == PLAYING:
        if pressed[pygame.K_LEFT]:
            ship.move_left()
        elif pressed[pygame.K_RIGHT]:
            ship.move_right()
        if pressed[pygame.K_UP]:
            ship.move_up()
        elif pressed[pygame.K_DOWN]:
            ship.move_down()

        '''if pressed[pygame.K_x]:
            ship.shoot()'''
        
    # Game logic (Check for collisions, update points, etc.)
    if stage == PLAYING:
        player.update()
        lasers.update()
        bombs.update()
        fleet.update()
        mobs.update()
        powerups.update()

        if len(player) == 0:
            stage = BADEND

        if len(fleet) <= 0:
            fleet_no += 1
            if fleet.bomb_rate > 2:
                fleet.bomb_rate -= 2
            else:
                fleet.bomb_rate -= 0
            prep_fleet(fleets[fleet_no], mobs)

        if len(fleets) == 0:
            stage = GOODEND
    
    # Drawing code (Describe the picture. It isn't actually drawn yet.)
    if stage == INTRO:
        screen.blit(space_img, [0, 0])
        player.draw(screen)
        lasers.draw(screen)
        bombs.draw(screen)
        mobs.draw(screen)
        show_stats()
        get_ready()

    if stage == PLAYING:
        screen.blit(space_img, [0, 0])
        player.draw(screen)
        lasers.draw(screen)
        bombs.draw(screen)
        mobs.draw(screen)
        powerups.draw(screen)
        show_stats()
        
    if stage == START:
        screen.fill(BLACK)
        show_title_screen()

    if stage == BADEND:
        game_over()

    if stage == GOODEND:
        game_win()
        
    # Update screen (Actually draw the picture in the window.)
    pygame.display.flip()


    # Limit refresh rate of game loop 
    clock.tick(refresh_rate)


# Close window and quit
pygame.quit()
