#%%
import pygame
from setting import *
#%%
class Tile(pygame.sprite.Sprite):
    def __init__(self,x,y):
        super().__init__()
        self.image=pygame.Surface(tile_size).convert_alpha()
        self.rect=self.image.get_rect(x=x,y=y)
        self.get_tile_image()
        
    def get_tile_image(self):
        self.tile_sheet=pygame.image.load('image/Bubble Bobble - Level Tiles.png')
        self.image.blit(self.tile_sheet,(0,0),(39,26,tile_size_w,tile_size_h))
        self.image.set_colorkey((4,2,4))