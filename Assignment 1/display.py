import pygame, sys, os, pygame_gui
from .Vertex import vertex
import heapq
import math

data = [
    [0, 0, 0, 0],
    [0, 1, 0, 0],
    [1, 0, 1, 0]
]

vertices = {}
filewidth = 0
filelength = 0
blockedcells = []
filelist = []
startx = 0
starty = 0
startindex =0
endindex=0
goalx = 0
goaly = 0
blockedxcoord = []
blockedycoord = []
temparr= None
directory=""


def main():

    #specify input type
    print("This program either takes input in File Form or in Auto-Generated Form")
    inputform=input("Enter \"File\" or \"Auto-Generated\" for Input Type:")

    if inputform=="File":
       file=input("Please enter path where test files is located: ")
       readfile(file)
    elif inputform=="Auto-Generated":
        print()
       #logic for this
    else:
        print("Invalid Input Type; Program is Exiting")
        exit()
    # making the display
    grid_width = 480
    grid_height = 360
    pygame.init()
    window = pygame.display.set_mode((grid_width * 3 / 2, grid_height * 3 / 2))
    window.fill((255, 255, 255))
    view_rect = pygame.Rect(0, 0, grid_width, grid_height)
    view_rect.center = window.get_rect().center
    pygame.display.set_caption('A*/Theta* simulation')
    manager = pygame_gui.UIManager((window.get_width(), window.get_height()), 'theme.json')
    draw_grid(window, view_rect.width, view_rect.height, 4, view_rect, manager)
    clock = pygame.time.Clock()
    while True:
        time_delta = clock.tick(60) / 1000.0
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.display.quit()
                pygame.quit()
                sys.exit()
            manager.process_events(event)

        manager.update(time_delta)
        pygame.display.update()
        manager.draw_ui(window)






def readfile(filename):
    f = open(filename, "r")
    count = 1
    for line in f:
        internalcount = 1
        localx = 0
        localy = 0
        for word in line.split():

            if count == 1:
                if internalcount == 1:
                    startx = int(word)
                elif internalcount == 2:
                    starty = int(word)
            elif count == 2:
                if internalcount == 1:
                    goalx = int(word)
                elif internalcount == 2:
                    goaly = int(word)
            elif count == 3:
                if internalcount == 1:
                    filewidth = int(word)
                elif internalcount == 2:
                    filelength = int(word)
            else:
                if count == 4:
                    temparr = [[0] * filewidth] * filelength
                if internalcount == 1:
                    localx = int(word)
                elif internalcount == 2:
                    localy = int(word)
                elif internalcount == 3:
                    indicator = int(word)
                    if indicator == 1:
                        blockedxcoord.append(localx)
                        blockedycoord.append(localy)
                        temparr[localy-1][localx-1]=1


            internalcount = internalcount + 1
        count = count + 1
    # setupnodes()


# def setupnodes():


def draw_grid(window, width, height, cols, view, manager):
    size = int(width / cols)
    i = 0
    j = 0
    for x in range(view.x, view.x + width, size):
        for y in range(view.y, view.y + height, size):
            rect = pygame.Rect(x, y, size, size)
            if data[i][j] == 1:
                pygame.draw.rect(window, (174, 174, 174), rect)
            else:
                # pygame.draw.rect(window, (0, 0, 0), rect, 1)
                add_verts((x, y), (j, i), size)
            i = i + 1
        j = j + 1
        i = 0

    for key in vertices:
        if vertices[key].coords[0]==startx and vertices[key].coords[1]==starty:
            startindex=key
        if vertices[key].coords[0]==goalx and vertices[key].coords[1]==goaly:
            endindex=key

        vertices[key].draw_vertex(window, manager)
        vertices[key].draw_lines(window)
        # print(f"{vertices[key].get_coords()}->{vertices[key].get_img_coords()}")


def create_vert(img_coords: tuple, coords: tuple):
    if coords in vertices:
        return vertices[coords]
    vertices[coords] = vertex(img_coords, coords)
    return vertices[coords]


def add_verts(img_coords: tuple, coords: tuple, size):
    verts = [create_vert(img_coords, coords),
             create_vert((img_coords[0] + size, img_coords[1]), (coords[0] + 1, coords[1])),
             create_vert((img_coords[0], img_coords[1] + size), (coords[0], coords[1] + 1)),
             create_vert((img_coords[0] + size, img_coords[1] + size), (coords[0] + 1, coords[1] + 1))]
    for i in range(0, len(verts)):
        for j in range(0, len(verts)):
            if j != i:
                verts[i].neighbors.append(verts[j])


def draw_tooltip(surface, width, height, x, y):
    rect = pygame.Rect(x, y, width, height)
    pygame.draw.rect(surface, (208, 208, 208), rect, border_radius=width // 8)

def hfunction(pointx, pointy):
    root2=math.sqrt(2)
    xminusgoal=abs(pointx-goalx)
    yminusgoal=abs(pointy-goaly)
    answer=(root2*min(xminusgoal,yminusgoal))+max(xminusgoal,yminusgoal)-min(xminusgoal,yminusgoal)
    return answer
def lineofsight(sourcex, sourcey,pointx, pointy):
    x0=sourcex
    y0=sourcey
    x1=pointx
    y1=pointy
    f=0
    dy=y1-y0
    dx=x1-x0
    sy=0
    sx=0
    if dy<0:
        dy= -1*dy
        sy=-1
    else:
        sy=1
    if dx<0:
        dx= -1*dx
        sx= -1
    else:
        sx=1
    if dx >= dy:
        while (x0 != x1):
            f=f+dy
            addx0 = -1
            addy0 = -1
            if sx == 1:
                addx0 = 0
            if sy == 1:
                addy0 = 0
            blocked= data[x0+addx0-1][y0+addy0-1]
            blocked2=data[x0+addx0-1][y0-1]
            blocked3=data[x0+addx0-1][y0-1-1]
            if f >= dx:
                if blocked == 1:
                    return False
                y0=y0+sy
                f=f-dx

            if f!=0 and blocked==1:
                return False
            if dy==0 and blocked2==1 and blocked3==1:
                return False
            x0=x0+sx


    else:
        while (y0 != y1):
            f=f+dx
            addx0 = -1
            addy0 = -1
            if sx == 1:
                addx0 = 0
            if sy == 1:
                addy0 = 0
            blocked= data[x0+addx0-1][y0+addy0-1]
            blocked2=data[x0-1][y0+addy0-1]
            blocked3=data[x0-1-1][y0+addy0-1]
            if f >= dy:
                if blocked == 1:
                    return False
                x0=x0+sx
                f=f-dy

            if f!=0 and blocked==1:
                return False
            if dx==0 and blocked2==1 and blocked3==1:
                return False
            y0=y0+sy
    return True


def Astar():
    #Compute h for all of them

    #Start

    #Update Vertex


def Thetastar():


main()
