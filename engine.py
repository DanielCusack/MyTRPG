import pygame
import csv
import math
import numpy as np
from spritesheet import *
from functions import *

class Selector:
    def __init__(self,width,height,colour):
        self.surface=pygame.Surface((width, height)).convert_alpha()
        self.surface.fill(colour)
        self.mouse_pos = 0
        self.mouse_x = 0
        self.mouse_y = 0



class Button:
    'Class to create and display buttons'
    def __init__(self,width,height):
        self.width=width
        self.height=height
        self.surface=pygame.Surface((width,height))
    
    def text_objects(self,text, font):
        'Helper function for button text'
        textSurface = font.render(text, True, (0,0,0))
        return textSurface, textSurface.get_rect(center=(self.width/2, self.height/2))

    def make_button(self,color,text,font):
        'Fill button surface with colour and add text'
        self.surface.fill(color)
        textSurface,textrect=self.text_objects(text,font)
        self.surface.blit(textSurface,textrect)

    def place_button(self,pos,surface):
        'Place the button or whatever I dunno...'
        surface.blit(self.surface,pos)

    def button_rect(self,pos):
        self.pos=pos
        self.collisionrect=self.surface.get_rect().move(self.pos)





class Map:
    'Class for handling everything related to the map including generating it from the data and updating to reflect changes'
    def __init__(self,tileset,filename,objlist=[]):
        #Get the spritesheet object
        self.spritesheet=tileset
        self.objlist=objlist
        #Get mapdata from csv to a list of lists
        self.mapdata=csv_to_list(filename)
        #Create a list of lists of equal length to the mapdata to track occupied spaces
        self.mapobject=[[0 for j in self.mapdata[0]] for i in self.mapdata]

    def generate_map(self):
        '''Generate a surface of the map from the map data'''
        self.tile_width=self.spritesheet.cellwidth
        self.tile_height=self.spritesheet.cellheight
        self.map_width=self.tile_width*len(self.mapdata[0])
        self.map_height=self.tile_height*len(self.mapdata)
        self.mapsurface=pygame.Surface((self.map_width,self.map_height))

        for y,i in enumerate(self.mapdata):
            ypos=y*self.tile_height
            for x,j in enumerate(i):
                xpos=x*self.tile_width
                self.mapsurface.blit(self.spritesheet.sheet,(xpos,ypos),self.spritesheet.cells[j])

    #This needs testing
    def terrain_properties_foot(self,filename):
        #Get the movement cost data for each tile
        self.cost_map_foot=[]
        with open(filename) as csvfile:
            for i in csv.reader(csvfile, delimiter=','):
                self.cost_map_foot.extend(i)
        
        for n,i in enumerate(self.cost_map_foot):
            if i == 'inf':
                self.cost_map_foot[n]= float('inf')
            else:
                self.cost_map_foot[n]= int(i)
        #Make list of list of movement cost onto each tile
        self.terrain_map_foot=[]
        for rowlist in self.mapdata:
            appendlist=[]
            for i in rowlist:
                appendlist.append(self.cost_map_foot[i])
            self.terrain_map_foot.append(appendlist)
        #Convert list of list representation of the map terrain cost into a graph representation
        self.terrain_graph_foot=Graph(self.terrain_map_foot)


    def give_display_rect(self,obj):
        'Gives obj a parameter for the rectangle to display it on screen. obj must be an instance of Character or its subclasses'
        self.mapobject[obj.pos[1]][obj.pos[0]]=obj
        obj.disp_rect=pygame.Rect(obj.pos[0]*self.tile_width,obj.pos[1]*self.tile_height,self.tile_width,self.tile_height)

    def display_objects(self,surface,selector,index=0,screen_window=False,other_disp_rects=0):
        'Display a list of objects onto a surface and optionally update the display efficiently'

        #If the surface being blitted on is the screen window, then create dirty rectangles for display update
        if screen_window==True:
            disp_rect_list=[i.disp_rect for i in self.objlist]
            if type(other_disp_rects) == list:
                disp_rect_list.extend(other_disp_rects)
            selector_rect=selector.surface.get_rect().move(selector.mouse_x,selector.mouse_y)
            for i in disp_rect_list:
                surface.blit(self.mapsurface,i,area=i)
            surface.blit(self.mapsurface,selector_rect,area=selector_rect)
            surface.blit(selector.surface,(selector.mouse_x,selector.mouse_y))
        
        #blit objects to the surface
        for i in self.objlist:
            i.draw(surface,index,i.pos[0]*self.tile_width,i.pos[1]*self.tile_height)
        
        #Update screen
        if screen_window==True:
            pygame.display.update(disp_rect_list)
            pygame.display.update(selector_rect)
            
    def remove_object_from_display(self,obj,surface,screen_window=False,selector=True):
        'Remove an object currently displayed on a given surface'
        obj_rect=obj.surface.get_rect().move(obj.mouse_x,obj.mouse_y)
        surface.blit(self.mapsurface,obj_rect,area=obj_rect)
        if screen_window == True:
            pygame.display.update(obj_rect)

    def check_object(self,selector):
        'Function to help see if the selector is on an object'
        return self.mapobject[int(selector.mouse_y/self.tile_height)][int(selector.mouse_x/self.tile_width)]

    def check_adjacent(self,pos,distance=1):
        'Check what tiles are occupied around a position'
        pass


    def choose_movement(self,obj,clock,FPS,surface,selector):
        'Function to deal with moving a character'
        loop=True
        movement_dict=self.terrain_graph_foot.dijkstra(obj.pos,obj.character_class.move)
        print(movement_dict)
        while loop:
            dt=clock.tick(FPS)
            before_display_list=0
            for event in pygame.event.get():
                #before_display_list is needed to remove the previous position of the object and selector from the screen
                before_display_list=[obj.disp_rect,selector.surface.get_rect().move(selector.mouse_x,selector.mouse_y)]

                if event.type == pygame.MOUSEMOTION:
                    mouse_pos =          pygame.mouse.get_pos()
                    mouse_x =            math.floor(mouse_pos[0] / self.tile_width) * self.tile_width
                    mouse_y =            math.floor(mouse_pos[1] / self.tile_height) * self.tile_height
                    selector.mouse_pos = pygame.mouse.get_pos()
                    selector.mouse_x =   math.floor(selector.mouse_pos[0] / self.tile_width) * self.tile_width
                    selector.mouse_y =   math.floor(selector.mouse_pos[1] / self.tile_height) * self.tile_height
                if event.type == pygame.MOUSEBUTTONUP:
                    #####Set up conditional to avoid selecting a place where an object is already present
                    selected_coordinate= (int(selector.mouse_x/self.tile_width),int(selector.mouse_y/self.tile_height))
                    if self.mapobject[selected_coordinate[1]][selected_coordinate[0]] == 0 and selected_coordinate in movement_dict:
                        self.mapobject[obj.pos[1]][obj.pos[0]]= 0
                        obj.pos = selected_coordinate
                        self.give_display_rect(obj)
                        loop=False
                if event.type == pygame.KEYDOWN:
                    pressed=pygame.key.get_pressed()
                    if pressed[pygame.K_ESCAPE]:
                        loop=False
            
            self.display_objects(surface,selector,screen_window=True,other_disp_rects=before_display_list)