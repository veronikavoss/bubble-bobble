#%%
import pygame
from setting import *
#%%
class Player(pygame.sprite.Sprite):
    def __init__(self,x,y):
        super().__init__()
        self.size=self.size_w,self.size_h=16,16
        self.add_images()
        self.player_action=0
        self.index_img=0
        self.animation_speed=0.15
        
        self.image=self.images[self.player_action][self.index_img]
        self.image=pygame.transform.scale(self.image,(self.size_w*2,self.size_h*2))
        self.rect=self.image.get_rect(x=x,y=y-self.size_h)
        self.image=pygame.transform.flip(self.image,True,False)
        self.image.set_colorkey((15,79,174))
        
        self.direction=pygame.math.Vector2(0,0)
        self.dx,self.dy=self.direction.x,self.direction.y
        self.move_speed=3
        
        self.update_time=pygame.time.get_ticks()
        self.animation_cooldown=500
    
    def get_images(self,column,row):
        sheet=pygame.image.load('image/Bubble Bobble - General Sprites_fixed.png').convert_alpha()
        self.image=pygame.Surface(self.size).convert_alpha()
        self.image.blit(sheet,(0,0),(6+(21*column),row,self.size_w,self.size_h))
        return self.image
    
    def add_images(self):
        self.temp=[]
        for i in range(16,37,20):
            for j in range(15):
                self.temp.append(self.get_images(j,i))
        self.images=[
            self.temp[:3:2], # standby
            self.temp[:7], # move
            self.temp[7:9] # jump
        ]
    
    def set_input(self):
        self.key_input=pygame.key.get_pressed()
        if self.key_input[pygame.K_LEFT]:
            self.dx=-self.move_speed
        elif self.key_input[pygame.K_RIGHT]:
            self.player_action=1
            self.animation_cooldown=100
            self.dx=self.move_speed
        else:
            self.dx=0
            self.player_action=0
            self.animation_cooldown=500
        self.rect.x+=self.dx
    
    def collision(self,tiles):
        for tile in tiles:
            if pygame.sprite.collide_rect(self,tile):
                if self.dx<0:
                    self.rect.left=tile.rect.right
                    self.dx=0
                elif self.dx>0:
                    self.rect.right=tile.rect.left
                    self.dx=0
    
    def animation(self):
        self.current_time=pygame.time.get_ticks()
        # if self.player_action==0:
        #     self.animation_cooldown=500
        if self.current_time-self.update_time>=self.animation_cooldown:
            self.index_img+=1
            self.update_time=self.current_time
            if self.index_img>=len(self.images[self.player_action]):
                self.index_img=0
        self.image=self.images[self.player_action][self.index_img]
        self.image=pygame.transform.scale(self.image,(self.size_w*2,self.size_h*2))
        self.image.set_colorkey((15,79,174))
    
    def update(self,tiles):
        self.set_input()
        self.collision(tiles)
        self.animation()
        print(self.rect,len(self.images[self.player_action]))
    
    # def draw(self,display):
    #     display.blit(self.images[self.player_action][self.index_img],self.rect)
    #     print(self.images)