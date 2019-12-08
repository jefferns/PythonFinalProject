# Nicholas Jefferis
# Python Final Project
# CS 2021
# Fred Anexstein

import pygame
import math
pygame.init()



ScreenHeight = 500
ScreenWidth = 800

win = pygame.display.set_mode((ScreenWidth,ScreenHeight))
pygame.display.set_caption("Stick Figure Game")

walkRight = [pygame.image.load('R1_.png'), pygame.image.load('R2_.png'), pygame.image.load('R3_.png'), pygame.image.load('R4_.png'), pygame.image.load('R5_.png'), pygame.image.load('R6_.png'), pygame.image.load('R7_.png'), pygame.image.load('R8_.png'), pygame.image.load('R9_.png'),pygame.image.load('ShootingR_.png')]
walkLeft = [pygame.image.load('L1_.png'), pygame.image.load('L2_.png'), pygame.image.load('L3_.png'), pygame.image.load('L4_.png'), pygame.image.load('L5_.png'), pygame.image.load('L6_.png'), pygame.image.load('L7_.png'), pygame.image.load('L8_.png'), pygame.image.load('L9_.png'),pygame.image.load('ShootingL_.png')]
bg = pygame.image.load('bg.png')
end = pygame.image.load('EndGame_.png')
char = pygame.image.load('standing_.png')

clock = pygame.time.Clock()
score = 0


class Player(object):
    def __init__(self,x,y,height,width):
        self.y = y
        self.x = x
        self.height = height
        self.width = width
        self.vel = 5
        self.stepcount = 0
        self.left = False
        self.right = False
        self.jumping = False
        self.shooting = False
        self.onPlatform = False
        self.jumpCount = 10
        self.hitbox = (self.x + 15,self.y-5,35,70)

    def damaged(self):
        self.x = 100
        self.y = 396
        self.stepcount = 0
        text = ScoreLossFont.render('-10',1,(255,0,0))
        win.blit(text,(700,50))
        pygame.display.update()
        i = 0
        while i < 100:
            pygame.time.delay(10)
            i += 1
        
    def draw(self,win):
        if self.stepcount + 1 >= 27:
            self.stepcount = 0
        if self.left:
            if self.shooting:
                win.blit(walkLeft[9], (self.x,self.y))
                self.shooting = False
            else:
                win.blit(walkLeft[self.stepcount // 3], (self.x,self.y))
                self.stepcount += 1
        elif self.right:
            if self.shooting:
                win.blit(walkRight[9], (self.x,self.y))
                self.shooting = False
            else:
                win.blit(walkRight[self.stepcount // 3], (self.x,self.y))
                self.stepcount += 1
        else:
            if self.shooting:
                if facing == -1:
                    win.blit(walkLeft[9], (self.x,self.y))
                if facing == 1:
                    win.blit(walkRight[9], (self.x,self.y))
            else:
                win.blit(char,(self.x,self.y))
        self.hitbox = (self.x + 15,self.y-5,35,70)
        
        #uncomment to view player hitbox
        #pygame.draw.rect(win, (255,0,0),self.hitbox,2)

        
class AI_Enemy:
    walkRight = [pygame.image.load('EnemyR1_.png'), pygame.image.load('EnemyR2_.png'), pygame.image.load('EnemyR3_.png'), pygame.image.load('EnemyR4_.png'), pygame.image.load('EnemyR5_.png'), pygame.image.load('EnemyR6_.png'), pygame.image.load('EnemyR7_.png'), pygame.image.load('EnemyR8_.png'), pygame.image.load('EnemyR9_.png'),pygame.image.load('ShootingR_.png')]
    walkLeft = [pygame.image.load('EnemyL1_.png'), pygame.image.load('EnemyL2_.png'), pygame.image.load('EnemyL3_.png'), pygame.image.load('EnemyL4_.png'), pygame.image.load('EnemyL5_.png'), pygame.image.load('EnemyL6_.png'), pygame.image.load('EnemyL7_.png'), pygame.image.load('EnemyL8_.png'), pygame.image.load('EnemyL9_.png'),pygame.image.load('ShootingL_.png')]

    def __init__(self,x,y,height,width,end):
        self.x = x
        self.y = y
        self.height = height
        self.width = width
        self.vel = 3
        self.end = end
        self.path = [self.x,self.end]
        self.hitbox = (self.x + 15,self.y-5,35,70)
        self.stepCount = 0
        self.health = 9
        self.visible = True
        
        
    def draw(self,win):
        self.move()
        if self.visible:
            if self.stepCount + 1 >= 27:
                self.stepCount = 0
            if self.vel > 0:
                win.blit(self.walkRight[self.stepCount // 3], (self.x,self.y))
                self.stepCount += 1
            else:
                win.blit(self.walkLeft[self.stepCount // 3], (self.x,self.y))
                self.stepCount += 1

            pygame.draw.rect(win,(255,0,0),(self.hitbox[0], self.hitbox[1]-20,50,10))
            pygame.draw.rect(win,(0,200,0),(self.hitbox[0], self.hitbox[1]-20,55 - (4.75 * (10 - self.health)),10))
            self.hitbox = (self.x + 15,self.y-5,35,70)
            #pygame.draw.rect(win, (255,0,0),self.hitbox,2)
        
    def damaged(self):
        if self.health >0:
            self.health -= 1
        else:
            self.visible = False
        
    
    def move(self):
        if self.vel > 0:
            if self.x + self.vel < self.path[1]:
                self.x += self.vel
            else:
                self.vel = self.vel * (-1)
                self.stepCount = 0
        else:
            if self.x - self.vel > self.path[0]:
                self.x += self.vel
            else:
                self.vel = self.vel * (-1)
                self.stepCount = 0

class Princess:
    def __init__(self,x,y,height,width):
        self.x = x
        self.y = y
        self.height = height
        self.width = width
    def draw(self,win):
        win.blit(pygame.image.load('Princess_.png'),(self.x,self.y))
        
      

class platform:
    def __init__(self,TLx,TLy,BRx,BRy,transparent=False):
        self.TLx = TLx
        self.TLy = TLy
        self.BRx = BRx
        self.BRy = BRy
        self.transparent = transparent
        self.color = (50,20,40)
        self.hitbox = (self.TLx,self.TLy, (self.BRx - self.TLx),(self.BRy-self.TLy))
    def draw(self,win):
        if not self.transparent:
            pygame.draw.rect(win,self.color,self.hitbox)
    


class bullet:
    def __init__(self,x,y,radius,color,direction):
        self.x = x
        self.y=y
        self.radius=radius
        self.color=color
        self.direction=direction
        self.vel = 10 * direction
    def draw(self,win):
        pygame.draw.circle(win,self.color,(self.x,self.y),self.radius)



def redraw():
    win.blit(bg,(0,0)) #displaying background
    text = font.render('Score: '+ str(score),1,(0,0,0)) #making a surface for the scoreboard
    win.blit(text,(680,10))
    player1.draw(win)
    princess.draw(win)
    for i in enemiesOnScreen:
        if not i.visible:
            enemiesOnScreen.pop(enemiesOnScreen.index(i))
        else:
            i.draw(win)
    for i in platforms:
        i.draw(win)
    for i in bulletsOnScreen:
        i.draw(win)    
    pygame.display.update()

# Character Creation
player1 = Player(100,396,64,64)
princess = Princess(110,80-64,64,64)

# Enemy Creation
enemiesOnScreen = []
enemy1 = AI_Enemy(400,251,64,64,580)
enemiesOnScreen += [enemy1]
enemy2 = AI_Enemy(150,190-64,64,64,310-64)
enemiesOnScreen += [enemy2]

# creating the platforms
platforms = []
plat1 = platform(120,370,320,385)
platforms += [plat1]
plat2 = platform(15,80,250,95)
platforms += [plat2]
plat3 = platform(400,315,620,330)
platforms += [plat3]
plat4 = platform(750,240,800,255)
platforms += [plat4]
plat5 = platform(150,190,310,205)
platforms += [plat5]
Ground = platform(0,470,800,500,True)
platforms += [Ground]

##################
#     TEXT 
font = pygame.font.SysFont('comicsans',30,True)
ScoreLossFont = pygame.font.SysFont('comicsans', 30,True)                                            
#
##################



#################################################
#            Running Game Loop                  #
#################################################


bulletsOnScreen=[]
shot = 0
run = True
while run:
    clock.tick(27) # change based on number of sprites
    
    # X button in top right corner of game window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    #adds a delay to the rate of bullets fired
    if shot >0:
        shot+=1
    if shot >5:
        shot = 0



    #player/princess collision
    if player1.hitbox[1] < princess.y + princess.height and player1.hitbox[1] + player1.hitbox[3] > princess.y:
        if player1.x + player1.width > princess.x and player1.x < princess.x + princess.width:
            run = False
            

    #player/enemy collision
    for j in enemiesOnScreen:
        if player1.hitbox[1] < j.hitbox[1] + j.hitbox[3] and player1.hitbox[1] + player1.hitbox[3] > j.hitbox[1]:  # player is within the vertical hitbox
            if player1.x + player1.width > j.hitbox[0] and player1.x < j.hitbox[0] +j.hitbox[2]: # player is within the horizontal hitbox
                score -= 10
                player1.damaged()
                
    #bullet mechanics
    for i in bulletsOnScreen:
        for j in enemiesOnScreen:
            if i.y - i.radius > j.hitbox[1] and i.y + i.radius < j.hitbox[1]+j.height:  # bullet is within the vertical hitbox
                if i.x + i.radius > j.hitbox[0] and i.x - i.radius < j.hitbox[0] +j.hitbox[2]: # bullet is within the horizontal hitbox
                    score += 5
                    j.damaged()
                    bulletsOnScreen.pop(bulletsOnScreen.index(i))
        
        if i.x < ScreenWidth and i.x > 0:
            i.x += i.vel
        else:
            bulletsOnScreen.pop(bulletsOnScreen.index(i))
        
    keys = pygame.key.get_pressed()


        ##### SHOOTING #####
    if keys[pygame.K_RIGHT] and shot ==0: 
        if len(bulletsOnScreen) < 5:
            if not player1.left:
                facing = 1
                player1.shooting = True
                bulletsOnScreen.append(bullet(math.floor(player1.x+player1.width),math.floor(player1.y+20),5,(0,0,0),facing))
                shot = 1
    if keys[pygame.K_LEFT] and shot ==0:
        if len(bulletsOnScreen) < 5:
            if not player1.right:
                facing = -1
                player1.shooting = True
                bulletsOnScreen.append(bullet(math.floor(player1.x+15),math.floor(player1.y+20),5,(0,0,0),facing))
                shot = 1

        ##### MOVEMENT #####
    if keys[pygame.K_a] and player1.x > player1.vel:
        player1.x -= player1.vel
        player1.left = True
        player1.right = False
        player1.standing = False
    elif keys[pygame.K_d] and player1.x < ScreenWidth - player1.width - player1.vel:
        player1.x += player1.vel
        player1.left = False
        player1.right = True
        player1.standing = False
    else:
        player1.left = False
        player1.right = False
        player1.standing = True
        player1.stepcount = 0

    if not(player1.jumping):
        if keys[pygame.K_SPACE]:
            player1.jumping = True
            player1.left = False
            player1.right = False
            player1.stepcount = 0
        else:
            player1.onPlatform = False
            for plat in platforms:
                if plat.TLy-10<player1.y+player1.height<plat.TLy+10 and (player1.x + player1.width > plat.TLx and player1.x < plat.BRx):
                    player1.y = plat.TLy - player1.height 
                    player1.onPlatform = True
                    player1.jumping = False
            if not player1.onPlatform:
                player1.y += 10
                if player1.y > 470 - player1.height:
                    player1.y = 470 - player1.height
                
                        

    else:
        if player1.jumpCount >= -10:
            i = 1
            if player1.jumpCount < 0:
                i = -1
            player1.vel = 8
            player1.y -= (player1.jumpCount ** 2) *0.25 * i
            player1.jumpCount -= 1

            for plat in platforms:
                newY = player1.y -(player1.jumpCount ** 2) *0.25 * i + player1.height
                if newY > plat.TLy and newY < 20 + plat.BRy and player1.x + player1.width > plat.TLx and player1.x <plat.BRx and i < 0:
                    player1.y = plat.TLy - player1.height                  
                    player1.vel = 5
                    player1.jumping = False
                    player1.onPlatform = True
                    player1.jumpCount = 10
                
        else:
            player1.vel = 5
            player1.jumping = False
            player1.jumpCount = 10
    
    redraw()

win.blit(pygame.image.load('EndGame_.png'),(0,0))
pygame.display.update()
pygame.time.delay(3000)
pygame.quit()
