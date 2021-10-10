#%%
import pygame,sys

from setting import *
from tile import *
from controller import *
#%%
class Game(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        pygame.init()
        pygame.display.set_caption(title)
        self.screen=pygame.display.set_mode(screen_size,pygame.RESIZABLE)
        self.clock=pygame.time.Clock()
        self.start_screen()
    
    def start_screen(self):
        self.start()
    
    def start(self):
        self.controller=Controller()
        self.loop()
    
    def loop(self):
        self.playing=True
        while self.playing:
            self.fps=self.clock.tick(FPS)/1000
            self.event()
            self.update()
            self.draw()
            pygame.display.update()
    
    def event(self):
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                self.playing=False
                # sys.exit()
                break
            if event.type==pygame.VIDEORESIZE:
                width,height=event.w,event.h
                self.screen=pygame.display.set_mode((width,height),pygame.RESIZABLE)
            # if event.type==pygame.KEYDOWN:
            #     if event.key==pygame.K_UP:
            #         self.controller.player_jump()
                    
            #     if event.key==pygame.K_SPACE:
            #         pass
                    
            # elif event.type==pygame.KEYUP:
            #     if event.key==pygame.K_LEFT or event.key==pygame.K_RIGHT:
            #         self.p1.direction.x=0
            #         self.p1.player_action=0
            #         self.p1.index_img=0
    
    def update(self):
        # self.p1.update(self.controller.tiles)
        self.controller.update()
    
    def draw(self):
        self.screen.fill('black')
        self.controller.draw(self.screen)
        

bubble_bobble=Game()
pygame.quit()
quit()
# sys.exit()
#%%
