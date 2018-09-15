import csv
import pygame

def create_window(ww,wh):
    'Create the display window'
    window_width, window_height=ww,wh
    window_title='The Adamant Wars'
    pygame.display.set_caption(window_title)
    return pygame.display.set_mode((window_width, window_height))

def csv_to_list(filename):
    'Helper function to convert a csv file to a list of lists'
    csvlist = []
    with open(filename) as csvfile:
        csvobject = csv.reader(csvfile, delimiter=',')
        for i in csvobject:
            csvlist.append([int(k)for k in i])
    return csvlist

def display_surf(dsurf,bsurf,pos=(0,0),rects=None,screen_window=True):
    'Helper function for blitting objects to a surface'
    if type(bsurf)==list and type(bsurf)==list and rects==None:
        for i,j in zip(bsurf,pos):
            dsurf.blit(i,j)
            if screen_window==True:
                pygame.display.update()
    elif type(bsurf)==list and type(bsurf)==list and rects!=None:
        for i,j in zip(bsurf,pos):
            dsurf.blit(i,j)
            if screen_window==True:
                pygame.display.update(rects)
    else:
        dsurf.blit(bsurf,pos)
        if screen_window==True:
            pygame.display.update()

def graph_maker(cost):
    '''Turn list of list into a dictionary with the coordinate as the key and value as a dictionary'''
    graph_dict={}
    width=len(cost[0])
    height=len(cost)
    for nh in range(height):
        for nw in range(width):
            graph_dict[(nw,nh)]={}
            if nw != 0:#Check if tile to the left exists
                graph_dict[(nw,nh)][(nw-1,nh)] = cost[nh][nw-1]
            if nw != width-1:#Check if tile to the right exists
                graph_dict[(nw,nh)][(nw+1,nh)] = cost[nh][nw+1]
            if nh != 0:#Check if tile above exists
                graph_dict[(nw,nh)][(nw,nh-1)] = cost[nh-1][nw]
            if nh != height-1:#Check if tile below exists
                graph_dict[(nw,nh)][(nw,nh+1)] = cost[nh+1][nw]
    return graph_dict

class Graph:
    def __init__(self,cost):
        'Cost are list of lists giving the movement cost to move onto a particular tile'
        self.cost=cost
        self.graph=graph_maker(self.cost)
    
    def dijkstra(self,start,goal):
        '''Dijkstra algorithm for pathfinding.
        graph: must be in the form of a dictionary where the key is NOT a int or float type and the value is also a dictionary
        start: the key of the starting vertex
        goal: either the maximum distance you can move (int or float) or the key of the destination vertex
        returns either a reduced dictionary of possible vertices to visit or the shortest path to the target vertex'''
        shortest_distance = {}
        predecessor = {}
        unseenNodes = dict(self.graph)
        infinity = float('inf')
        path = []
        for node in unseenNodes:
            shortest_distance[node] = infinity
        shortest_distance[start] = 0
 
        while unseenNodes:
            minNode = None
            for node in unseenNodes:
                if minNode is None:
                    minNode = node
                elif shortest_distance[node] < shortest_distance[minNode]:
                    minNode = node
 
            for childNode, weight in self.graph[minNode].items():
                if weight + shortest_distance[minNode] < shortest_distance[childNode]:
                    shortest_distance[childNode] = weight + shortest_distance[minNode]
                    predecessor[childNode] = minNode
            unseenNodes.pop(minNode)

        if type(goal) == int or type(goal) == float:
            #If distance type goal then return a reduced dictional where the distance to the vertex < goal
            reduced_graph={}
            for k,v in shortest_distance.items():
                if v <=goal:
                    reduced_graph[k]=v
            return reduced_graph

 
        currentNode = goal
        while currentNode != start:
            try:
                path.insert(0,currentNode)
                currentNode = predecessor[currentNode]
            except KeyError:
                return 'Path not reachable'
        path.insert(0,start)
        return path