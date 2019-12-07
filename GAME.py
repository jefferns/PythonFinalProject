import pygame
pygame.init()

ScreenHeight = 700
ScreenWidth = 1000

win = pygame.display.set_mode((ScreenWidth,ScreenHeight))
pygame.display.set_caption("First Game")



clock = pygame.time.Clock()

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
#character information
x = 5
y = 5
width = 40
height = 60
vel = 5



run = True

while run:
    pygame.time.delay(100)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    keys = pygame.key.get_pressed()
    
    if keys[pygame.K_LEFT] and x > vel:
        x -= vel

    if keys[pygame.K_RIGHT] and x < ScreenWidth - width - vel:
        x += vel

    if keys[pygame.K_UP] and y > vel:
        y -= vel

    if keys[pygame.K_DOWN] and y < 500 - height - vel:
        y += vel
    
    win.fill((0,0,0))  # Fills the screen with black
    pygame.draw.rect(win, (255,0,0), (x, y, width, height))   
    pygame.display.update() 
    
pygame.quit()
