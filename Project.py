import pygame
import random

pygame.init()



class Button:

    def __init__(self, screen, colour, rect, border_radius=20, width=0):
        self.screen = screen
        self.colour = colour
        self.pos = rect
        self.rect = pygame.Rect(rect)
        self.border_radius = border_radius
        self.width = width

    def draw(self):
        pygame.draw.rect(self.screen, self.colour, self.pos, border_radius=self.border_radius, width=self.width)

    def interaction(self, mousepos):
        if self.rect.collidepoint(mousepos):
            return True, self.colour



# x = x coord
#y = y coord
#col = colour
#w,h = width, height
class Drawing:
    def __init__(self, x, y, col, w, h, surface):
        self.x = x
        self.y = y
        self.col = col
        self.w = w
        self.h = h
        self.surface = surface

    def draw(self):
        #pygame.draw.line(self.surface,self.col,(self.prevx,self.prevy),(self.x,self.y))
        pygame.draw.circle(self.surface,self.col,(self.x,self.y),self.w*1.2)

        #ink = pygame.Rect(self.x, self.y, self.w, self.h)
        #pygame.draw.rect(self.surface, self.col, ink)



class Rubber(Drawing):

    def __init__(self, x, y, col, w, h, surface, speedx, speedy):
        super().__init__(x, y, col, w, h, surface)
        self.speedx = speedx
        self.speedy = speedy
        self.currspeedx = speedx
        self.currspeedy = speedy


    def draw(self):
        rubber = pygame.Rect(self.x,self.y,self.w,self.h)
        pygame.draw.rect(self.surface,self.col,rubber)

    def draw_white(self):
        rubber = pygame.Rect(self.x, self.y, self.w, self.h)
        pygame.draw.rect(self.surface, (255, 255, 255), rubber)

    def changecoord(self):
        self.x += self.currspeedx
        self.y += self.currspeedy

    def collisions(self):
        if self.x + 200 > 1280 :
            self.currspeedx = -self.speedx
        elif self.x < 0:
            self.currspeedx = self.speedx

        if self.y + 100 > 720:
            self.currspeedy = -self.speedy
        elif self.y < 155:
            self.currspeedy = self.speedy






class Whiteboard:


    def __init__(self, resolution, framerate):
        self.screen = pygame.display.set_mode(resolution)
        self.clock = pygame.time.Clock()
        self.framerate = framerate

        # initialise stuff
        self.black = Button(self.screen, (0, 0, 0), (100, 50, 50, 50))
        self.red = Button(self.screen, (255, 0, 0), (200, 50, 50, 50))
        self.green = Button(self.screen, (0, 255, 0), (300, 50, 50, 50))
        self.blue = Button(self.screen, (0, 0, 255), (400, 50, 50, 50))
        self.yellow = Button(self.screen, (255, 255, 0), (500, 50, 50, 50))
        self.purple = Button(self.screen, (128, 0, 255), (600, 50, 50, 50))
        self.cyan = Button(self.screen, (0, 255, 255), (700, 50, 50, 50))
        self.orange = Button(self.screen, (255, 128, 0), (800, 50, 50, 50))

        self.widthbox = Button(self.screen, (0, 0, 0), (900, 50, 200, 50), width=3)

        self.mousepen = Drawing(pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1], (0,0,0), 5,  5, self.screen)

        self.rubber = Rubber(0, 155, (232,132,123), 200, 100, self.screen, 2, 2)


    def run(self):

        self.screen.fill((255, 255, 255))

        pygame.draw.line(self.screen, (0, 0, 0), (0, 150), (1280, 150), 3)

        self.black.draw()
        self.red.draw()
        self.green.draw()
        self.blue.draw()
        self.yellow.draw()
        self.purple.draw()
        self.cyan.draw()
        self.orange.draw()

        self.widthbox.draw()

        font = pygame.font.SysFont("david", 32)
        text_render = font.render("Random Width", True, (0, 0, 0))
        pos = text_render.get_rect(center=self.widthbox.rect.center)
        self.screen.blit(text_render, pos)

        run = True
        while run:



            keys = pygame.key.get_pressed()
            mousepos = pygame.mouse.get_pos()
            mousedown = pygame.mouse.get_pressed()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False


                if keys[pygame.K_ESCAPE]:
                    run = False


            if mousedown[0]:

                self.mousepen.x = mousepos[0]
                self.mousepen.y = mousepos[1]

                # wall
                if self.black.interaction(mousepos):
                    self.mousepen.col = self.black.interaction(mousepos)[1]
                elif self.red.interaction(mousepos):
                    self.mousepen.col = self.red.interaction(mousepos)[1]
                elif self.green.interaction(mousepos):
                    self.mousepen.col = self.green.interaction(mousepos)[1]
                elif self.blue.interaction(mousepos):
                    self.mousepen.col = self.blue.interaction(mousepos)[1]
                elif self.yellow.interaction(mousepos):
                    self.mousepen.col = self.yellow.interaction(mousepos)[1]
                elif self.purple.interaction(mousepos):
                    self.mousepen.col = self.purple.interaction(mousepos)[1]
                elif self.cyan.interaction(mousepos):
                    self.mousepen.col = self.cyan.interaction(mousepos)[1]
                elif self.orange.interaction(mousepos):
                    self.mousepen.col = self.orange.interaction(mousepos)[1]

                elif self.widthbox.interaction(mousepos):
                    self.mousepen.w = random.randint(1, 75)

                if self.mousepen.y > 150 + self.mousepen.w*1.2:
                    self.mousepen.draw()


            self.rubber.draw_white()
            self.rubber.collisions()
            self.rubber.changecoord()
            self.rubber.draw()

            self.clock.tick(self.framerate)
            pygame.display.flip()


whiteboard = Whiteboard((1280, 720), 60)
whiteboard.run()