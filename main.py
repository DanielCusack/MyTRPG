import pygame, sys, time, random
import math
import numpy as np
from spritesheet import *
from engine import *
from functions import *

pygame.init()
#------------------------------------------
#Variables of the program
running=True
runningmenu=True
tilew=40
tileh=40
ww=1600
wh=900
FPS=12
#------------------------------------------


window=create_window(ww,wh)
window.fill((255,255,255))


#Tileset
grassland=Spritesheet('graphics\\not-squeesh.png',9,4)

#Create map
firstfilename='map_data\\firstmap2.csv'
firstmap=Map(grassland,firstfilename)
firstmap.generate_map()
firstmap.terrain_properties_foot('graphics\\not-squeesh.csv')
print(firstmap.cost_map_foot)
print(firstmap.terrain_map_foot)

#Generate character
jamfile='graphics\\generic.png'
badjamfile='graphics\\generic_bad.png'
jam=Player(jamfile, 2, 2, 20, 5, 1, 5, 7, 5, 5, 1, pos=(2,1))
jam.define_class(Swordsman(1))
jam2=Enemy(badjamfile, 2, 2, 20, 5, 1, 5, 7, 5, 5, 1, pos=(2,3))
jam2.define_class(Swordsman(1))
firstmap.give_display_rect(jam)
firstmap.give_display_rect(jam2)
objlist=[jam,jam2]
firstmap.objlist=objlist

#Buttons
menusurf=pygame.Surface((ww,wh))
menusurf.fill((255,255,255,255))
textfont = pygame.font.Font('freesansbold.ttf',20)
startbutton=Button(100,50)
startbutton.make_button((0,200,0),'Start',textfont)
startbutton.button_rect((600,500))
#startbutton.button_rect((0,0))
endbutton=Button(100,50)
endbutton.make_button((200,0,0),'End',textfont)
endbutton.button_rect((900,500))
menubutton=[startbutton.surface,endbutton.surface]
menupos=[startbutton.pos,endbutton.pos]
display_surf(menusurf,menubutton,pos=menupos,screen_window=False)
display_surf(window,menusurf)


#Create the clock
clock=pygame.time.Clock()


#Menu Loop
runningmenu=True
while runningmenu:
    dt=clock.tick(FPS)
    for event in pygame.event.get():
        mouse=pygame.mouse.get_pos()
        if startbutton.collisionrect.collidepoint(mouse) and event.type == pygame.MOUSEBUTTONDOWN:
            runningmenu=False
        if endbutton.collisionrect.collidepoint(mouse) and event.type == pygame.MOUSEBUTTONDOWN:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            pressed=pygame.key.get_pressed()
            if pressed[pygame.K_ESCAPE]:
                runningmenu=False


#The create the map selector
selector =Selector(firstmap.tile_width,firstmap.tile_height,(100,149,237,100))


#Change the window so it displays the game
window.fill((255,255,255,255))
window.blit(firstmap.mapsurface,(0,0))
pygame.display.update()


count=0

while running:
    dt=clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.MOUSEMOTION:
            mouse_pos = pygame.mouse.get_pos()
            mouse_x = math.floor(mouse_pos[0] / firstmap.tile_width) * firstmap.tile_width
            mouse_y = math.floor(mouse_pos[1] / firstmap.tile_height) * firstmap.tile_height

            if mouse_x != selector.mouse_x or mouse_y != selector.mouse_y:
                firstmap.remove_object_from_display(selector,window,screen_window=True)

            if mouse_x < firstmap.map_width and mouse_y < firstmap.map_height:
                selector.mouse_pos = pygame.mouse.get_pos()
                selector.mouse_x =   math.floor(selector.mouse_pos[0] / firstmap.tile_width) * firstmap.tile_width
                selector.mouse_y =   math.floor(selector.mouse_pos[1] / firstmap.tile_height) * firstmap.tile_height

        if event.type == pygame.MOUSEBUTTONUP:
            selected_object = firstmap.check_object(selector)
            print(selector.mouse_x,selector.mouse_y)

            if isinstance(selected_object,Player):
                firstmap.choose_movement(selected_object,clock,FPS,window,selector)

        if event.type == pygame.KEYDOWN:
            pressed=pygame.key.get_pressed()
            
            if pressed[pygame.K_ESCAPE]:
                running=False
            
    firstmap.display_objects(window,selector,index=count,screen_window=True)
    count+=1
    if count>3:
        count=0



pygame.quit()
sys.exit()