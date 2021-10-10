#%%
import pygame
from setting import *
#%%
class Player(pygame.sprite.Sprite):
    def __init__(self,x,y):
        super().__init__()
        self.size=self.size_w,self.size_h=16,16
        self.add_images()
        self.action='standby'
        self.index_img=0
        self.animation_speed=0.15
        
        self.image=self.images[self.action][self.index_img]
        self.image=pygame.transform.scale(self.image,(self.size_w*2,self.size_h*2))
        self.image=pygame.transform.flip(self.image,True,False)
        self.image.set_colorkey((15,79,174))
        
        self.rect=self.image.get_rect(x=x,y=y-self.size_h)
        self.direction=pygame.math.Vector2(0,0)
        self.dx,self.dy=self.direction.x,self.direction.y
        self.move_speed=3
        self.current_x=0
        self.jump_speed=-5.5
        self.gravity=0.2
        
        self.jumped=False
        self.directicollide_right=True
        self.collide_left=False
        self.collide_right=False
        self.collide_ceiling=False
    
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
        self.images={
            'standby':self.temp[:3:2],
            'run':self.temp[:5],
            'water':self.temp[6:7],
            'jump':self.temp[26:27],
            'fall':self.temp[24:25]}
    
    def set_input(self):
        self.key_input=pygame.key.get_pressed()
        if self.key_input[pygame.K_LEFT]:
            self.dx=-self.move_speed
            self.directicollide_right=False
        elif self.key_input[pygame.K_RIGHT]:
            self.dx=self.move_speed
            self.directicollide_right=True
        else:
            self.dx=0
        
        if self.key_input[pygame.K_UP] and self.jumped==False:
            self.dy=self.jump_speed
        
        if self.key_input[pygame.K_SPACE]:
            pass
        
        self.rect.x+=self.dx
    
    def collision(self,tiles):
        for tile in tiles:
            if pygame.sprite.collide_rect(self,tile):
                print(tile)
                if self.dx<0:
                    self.rect.left=tile.rect.right
                    self.collide_left=True
                    self.current_x=self.rect.left
                elif self.dx>0 and self.jumped==False:
                # elif self.dx>0 and self.rect.left<tile.rect.left:
                    self.rect.right=tile.rect.left
                    self.collide_right=True
                    self.current_x=self.rect.right
                    
                elif self.dx>0 and self.rect.right>tile.rect.left:
                    self.rect.right=tile.rect.left
                    self.current_x=self.rect.right
        
        if self.collide_left and (self.rect.left<self.current_x or self.dx>=0):
            self.collide_left=False
        if self.collide_right and (self.rect.right>self.current_x or self.dx<=0):
            self.collide_right=False
        
        # gravity
        self.dy+=self.gravity
        self.rect.y+=self.dy
        if self.dy>3:
            self.dy=3
        
        for tile in tiles:
            if pygame.sprite.collide_rect(self,tile):
                if self.dy>=0:
                    self.rect.bottom=tile.rect.top
                    self.dy=0
                    self.jumped=False
                if self.rect.top<tile.rect.bottom and self.dy!=0:
                    # self.rect.top=tile.rect.bottom
                    # self.dy=0
                    
                    self.collide_ceiling=True
                    self.current_x=self.rect.x
                    self.dx=0
        
        if self.jumped==False and self.dy<0 or self.dy>1:
            self.jumped=True
        if self.collide_ceiling and self.dy>0:
            self.collide_ceiling=False
        if self.collide_ceiling and self.collide_right:
            self.rect.x=self.current_x
    
    def get_action(self):
        if self.dy<0:
            self.action='jump'
        elif self.dy>1:
            self.action='fall'
        else:
            if self.dx!=0:
                self.action='run'
                self.animation_speed=self.move_speed*0.05
            else:
                self.action='standby'
                self.animation_speed=0.04
    
    def animation(self):
        animation=self.images[self.action]
        self.index_img+=self.animation_speed
        if self.index_img>=len(animation):
            self.index_img=0
        self.image=animation[int(self.index_img)]
        if self.directicollide_right==True:
            self.image=pygame.transform.scale(self.image,(self.size_w*2,self.size_h*2))
            self.image=pygame.transform.flip(self.image,True,False)
            self.image.set_colorkey((15,79,174))
        else:
            self.image=pygame.transform.scale(self.image,(self.size_w*2,self.size_h*2))
            self.image.set_colorkey((15,79,174))
            
        if self.jumped==False and self.collide_left:
            self.rect=self.image.get_rect(bottomleft=self.rect.bottomleft)
        if self.jumped==False and self.collide_right:
            self.rect=self.image.get_rect(bottomright=self.rect.bottomright)
        if self.jumped==False:
            self.rect=self.image.get_rect(midbottom=self.rect.midbottom)
        elif self.collide_ceiling and self.collide_left:
            self.rect=self.image.get_rect(topleft=self.rect.topleft)
        elif self.collide_ceiling and self.collide_right:
            self.rect=self.image.get_rect(topright=self.rect.topright)
        elif self.collide_ceiling:
            self.rect=self.image.get_rect(midtop=self.rect.midtop)
    
    def update(self,tiles):
        self.set_input()
        self.collision(tiles)
        self.get_action()
        self.animation()
        
        # print(self.jumped,self.action,self.current_x,self.rect.left)
        # print(
        #     'l:',self.collide_left,
        #     'r:',self.collide_right,
        #     'c:',self.collide_ceiling)
    
    # def draw(self,display):
    #     display.blit(self.images[self.player_action][self.index_img],self.rect)
    #     print(self.images)