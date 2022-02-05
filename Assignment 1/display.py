import pygame, sys, os, pygame_gui
from Vertex import vertex

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
goalx = 0
goaly = 0
blockedxcoord = []
blockedycoord = []


def main():
    pygame.init()
    window = pygame.display.set_mode((960, 600))
    window.fill((255, 255, 255))
    clicked = False
    view_rect = pygame.Rect(0, 0, 480, 360)
    view_rect.center = window.get_rect().center
    pygame.display.set_caption('A*/Theta* simulation')
    draw_grid(window, view_rect.width, view_rect.height, 4, view_rect)
    for n in vertices[(0, 0)].neighbors:
        print(n.coords)
    while True:

        if pygame.event.get(pygame.QUIT):
            pygame.display.quit()
            pygame.quit()
            sys.exit()
        if pygame.event.get(pygame.MOUSEBUTTONDOWN):
            for key in vertices:
                if vertices[key].rect.collidepoint(pygame.mouse.get_pos()):
                    clicked = not clicked
                    print(f"clicked vertex:{key}")
                    if clicked:
                        draw_tooltip(window, 60, 120, vertices[key].img_coords[0], vertices[key].img_coords[1])

        pygame.display.update()


def readfolder(foldername):
    filelist = os.list("testfiles/")


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

                if internalcount == 1:
                    localx = int(word)
                elif internalcount == 2:
                    localy = int(word)
                elif internalcount == 3:
                    indicator = int(word)
                    if indicator == 1:
                        blockedxcoord.append(localx)
                        blockedycoord.append(localy)
            internalcount = internalcount + 1
        count = count + 1
    # setupnodes()


# def setupnodes():


def draw_grid(window, width, height, cols, view):
    size = int(width / cols)
    i = 0
    j = 0
    for x in range(view.x, view.x + width, size):
        for y in range(view.y, view.y + height, size):
            rect = pygame.Rect(x, y, size, size)
            if data[i][j] == 1:
                pygame.draw.rect(window, (174, 174, 174), rect)
            else:
                #pygame.draw.rect(window, (0, 0, 0), rect, 1)
                add_verts((x, y), (j, i), size)
            i = i + 1
        j = j + 1
        i = 0

    for key in vertices:
        vertices[key].draw_vertex(window)
        vertices[key].draw_lines(window)
        #print(f"{vertices[key].get_coords()}->{vertices[key].get_img_coords()}")


def create_vert(img_coords: tuple, coords: tuple):
    if coords in vertices:
        return vertices[coords]
    vertices[coords] = vertex(img_coords, coords)
    return vertex(img_coords, coords)


def add_verts(img_coords: tuple, coords: tuple, size):
    verts = [create_vert(img_coords, coords),
             create_vert((img_coords[0] + size, img_coords[1]), (coords[0] + 1, coords[1])),
             create_vert((img_coords[0], img_coords[1] + size), (coords[0], coords[1] + 1)),
             create_vert((img_coords[0] + size, img_coords[1] + size), (coords[0] + 1, coords[1] + 1))]
    for i in range(0, len(verts)):
        for j in range(0, len(verts)):
            if j != i:
                verts[i].neighbors.append(verts[j])
                print(f"{verts[i].coords}->{verts[j].coords}")

def draw_tooltip(surface, width, height, x,y):
    rect = pygame.Rect(x, y, width, height)
    pygame.draw.rect(surface, (208, 208, 208), rect, border_radius= width//8)

main()
