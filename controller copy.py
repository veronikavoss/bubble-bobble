#%%
import pygame
from tile import *
from player import *
#%%
class Controller:
    def __init__(self):
        super().__init__()
        self.level=1
        self.get_map()
        self.map_list=[i.strip().replace(',','') for i in self.temp_list]
        self.set_map()
    
    def get_map(self):
        with open('map.csv','r') as r:
            self.temp_list=r.readlines()
    
    def set_map(self):
        self.tiles=pygame.sprite.Group()
        self.player=pygame.sprite.GroupSingle()
        for row_idx,row in enumerate(self.map_list):
            for column_idx,check_tile in enumerate(row):
                y=row_idx*tile_size_h+36
                x=column_idx*tile_size_w
                if check_tile==str(self.level):
                    tile=Tile(x,y)
                    self.tiles.add(tile)
                # if check_tile=='p':
                #     player=Player(x,y)
                #     self.player.add(player)
    
    def update(self):
        pass
    
    def draw(self,display):
        self.tiles.draw(display)
        self.player.draw(display)
#%%