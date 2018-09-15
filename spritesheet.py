import pygame
from functions import *

class Spritesheet:
    def __init__(self,filename,colu,rows,colkey=(255,255,255,255),use_alpha=False):
        self.sheet=pygame.image.load(filename)
        if use_alpha==True:
                self.sheet = self.sheet.convert_alpha()
        else:
            self.sheet = self.sheet.convert()
            self.sheet.set_colorkey(colkey)

        self.colu=colu
        self.rows=rows
        self.totalcellcount=colu*rows
        self.rect=self.sheet.get_rect()
        w=self.cellwidth=self.rect.width/colu
        h=self.cellheight=self.rect.height/rows
        hw,hh=self.cellcenter=(w/2,h/2)

        self.cells=list([(index%colu*w,index//colu*h,w,h) for index in range(self.totalcellcount)])
        self.handle=list([(0,0),(-hw,0),(-w,0),(0,-hh),(-hw,hh),(-w,-hh),(0,-h),(-hw,-h),(-w,-h)])

    def draw(self,surface,cellindex,x,y,handle=0):
        surface.blit(self.sheet,(x+self.handle[handle][0],y+self.handle[handle][1]),self.cells[cellindex])

class Character(Spritesheet):
    def __init__(self, filename, colu, rows, hp, strength, mag, dex, agl, fate, defs, res, pos=(0,0), colkey=(255,255,255,255), set_health=False, utype='foot'):
        Spritesheet.__init__(self,filename,colu,rows,colkey=colkey)
        self.pos=pos
        self.hp=hp

        #Conditional to handle starting health
        if set_health == False:
            self.current_hp=hp
        else:
            self.current_hp= set_health

        self.str=   strength
        self.mag=   mag
        self.dex=   dex
        self.agl=   agl
        self.fate=  fate
        self.defs=  defs
        self.res=   res
        self.utype= utype
    
    def define_class(self,class_object):
        'Give the character a class'
        self.character_class=class_object
    

class Player(Character):
    def __init__(self, filename, colu, rows, hp, strength, mag, dex, agl, fate, defs, res, pos=(0,0), colkey=(255,255,255,255), set_health=False, utype='Foot'):
        super().__init__(filename, colu, rows, hp, strength, mag, dex, agl, fate, defs, res, pos=pos, colkey=colkey, set_health=False, utype='Foot')
        self.exp=0
        self.hp_growth=   0
        self.str_growth=  0
        self.mag_growth=  0
        self.dex_growth=  0
        self.agl_growth=  0
        self.fate_growth= 0
        self.defs_growth= 0
        self.res_growth=  0

    def set_growth_rates(self, growthlist):
        'Set the growth rates of the player character'
        self.hp_growth=   growthlist[0]
        self.str_growth=  growthlist[1]
        self.mag_growth=  growthlist[2]
        self.dex_growth=  growthlist[3]
        self.agl_growth=  growthlist[4]
        self.fate_growth= growthlist[5]
        self.defs_growth= growthlist[6]
        self.res_growth=  growthlist[7]

    
class Enemy(Character):
    def __init__(self, filename, colu, rows, hp, strength, mag, dex, agl, fate, defs, res, pos=(0,0), colkey=(255,255,255,255), set_health=False, utype='Foot'):
        super().__init__(filename, colu, rows, hp, strength, mag, dex, agl, fate, defs, res, pos=pos, colkey=colkey, set_health=False, utype='Foot')

    def ai_agressive(self,map):
        pass


class Character_class:
    def __init__(self, class_name, level, hp_cap, str_cap, mag_cap, dex_cap, agl_cap, fate_cap, defs_cap, res_cap, move):
        self.class_name= class_name
        self.level=      level
        self.hp_cap=     hp_cap
        self.str_cap=    str_cap
        self.mag_cap=    mag_cap
        self.dex_cap=    dex_cap
        self.agl_cap=    agl_cap
        self.fate_cap=   fate_cap
        self.defs_cap=   defs_cap
        self.res_cap=    res_cap
        self.move=       move

class Swordsman(Character_class):
    def __init__(self,level):
        super().__init__('Swordsman', level, 40, 15, 5, 10, 15, 30, 15, 10, 5)

class Mage(Character_class):
    def __init__(self,level):
        super().__init__('Mage', level, 35, 5, 15, 10, 15, 30, 10, 15, 5)

class Archer(Character_class):
    def __init__(self,level):
        super().__init__('Mage', level, 35, 15, 5, 15, 15, 30, 10, 10, 5)

