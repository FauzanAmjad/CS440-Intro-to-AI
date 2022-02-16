import pygame, sys, os, pygame_gui
from Vertex import vertex
import heapq
import math
from Pathfinder import pathfinder

data = [
    [0, 0, 0, 0],
    [0, 0, 0, 1],
    [1, 0, 1, 0]
]
# ((vertex.coords, <vertex object>))
vertices = {}
filewidth = 0
filelength = 0
blockedcells = []
filelist = []
startx = 1
starty = 1
startindex = (1, 1)
endindex = (5, 4)
goalx = 5
goaly = 4
blockedxcoord = []
blockedycoord = []
temparr = []
directory = ""
RED = (255, 46, 31)
BLUE = (69, 118, 255)


def main():
    # specify input type
    if len(sys.argv) < 2:
        print("This program either takes input in File Form or in Auto-Generated Form")
        inputform = input("Enter \"File\" or \"Auto-Generated\" for Input Type:")

        if inputform == "File":
            file = input("Please enter path where test files is located: ")
            readfile(file)
        elif inputform == "Auto-Generated":
            print()
        # logic for this
        else:
            print("Invalid Input Type; Program is Exiting")
            exit()
    readfile(sys.argv[1])

    # making the display
    grid_cols = filewidth
    grid_rows = filelength
    cell_size = 120 if filewidth < 50 else 10
    grid_width = cell_size * grid_cols
    grid_height = cell_size * grid_rows
    pygame.init()
    window = pygame.display.set_mode((grid_width + 120, grid_height * 11 / 10))
    window.fill((255, 255, 255))
    view_rect = pygame.Rect(0, 0, grid_width, grid_height)
    view_rect.center = window.get_rect().center
    pygame.display.set_caption('A*/Theta* simulation')
    manager = pygame_gui.UIManager((window.get_width(), window.get_height()), 'theme.json')
    draw_grid(window, view_rect.width, view_rect.height, grid_cols, view_rect, manager)
    text_box = None
    clicked = next(iter(vertices))
    clock = pygame.time.Clock()
    option_rect_1 = pygame.Rect(0, 0, 60, grid_height)

    button_pos = pygame.Rect(0, 0, 30, 30)
    button_pos.center = option_rect_1.center
    toggle = pygame_gui.elements.UIButton(relative_rect=button_pos,
                                          text="Θ*",
                                          manager=manager, object_id="#toggle")
    toggle_Astar = True

    blank_cache = pygame.Surface.copy(window)
    pf = pathfinder(vertices, startx, starty, goalx, goaly, filewidth, filelength, data)
    pf.Astar()
    draw_path(vertices[endindex], window, RED)
    cache = pygame.Surface.copy(window)
    # event loop
    while True:
        time_delta = clock.tick(60) / 1000.0
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.display.quit()
                pygame.quit()
                sys.exit()

            if event.type == pygame_gui.UI_BUTTON_PRESSED:
                if text_box is not None:
                    text_box.hide()
                    text_box = None
                if event.ui_element == toggle:
                    if toggle_Astar:
                        toggle.select()
                        toggle.set_text("A*")
                        window.blit(source=blank_cache, dest=(0, 0))
                        pf.Thetastar()
                        draw_path(vertices[endindex], window, BLUE)
                        cache = pygame.Surface.copy(window)
                        toggle_Astar = False
                    else:
                        toggle.unselect()
                        toggle.set_text("Θ*")
                        window.blit(source=blank_cache, dest=(0, 0))
                        pf.Astar()
                        draw_path(vertices[endindex], window, RED)
                        cache = pygame.Surface.copy(window)
                        toggle_Astar = True
                window.blit(source=cache, dest=(0, 0))
                vertices[clicked].clickable.unselect()
                for key in vertices:
                    if event.ui_element == vertices[key].clickable:
                        if not vertices[key].is_clicked:
                            vertices[key].clickable.select()
                            clicked = key
                            rect = pygame.Rect(vertices[key].img_coords[0], vertices[key].img_coords[1], 120, 120)
                            if vertices[key].coords[1] > grid_rows / 2:
                                rect.bottomleft = (vertices[key].img_coords[0], vertices[key].img_coords[1])
                            if vertices[key].coords[0] > grid_cols / 2:
                                rect.right = vertices[key].img_coords[0]
                            text_box = pygame_gui.elements.UITextBox(html_text=f"   <u>{vertices[key].coords}</u><br>"
                                                                               f"g: {'{:.2f}'.format(vertices[key].gvalue)}<br>"
                                                                               f"h: {'{:.2f}'.format(vertices[key].hvalue)}<br>"
                                                                               f"f: {'{:.2f}'.format(vertices[key].gvalue + vertices[key].hvalue)}<br>",
                                                                     relative_rect=rect, manager=manager)
                            vertices[key].is_clicked = True
                        else:
                            vertices[key].is_clicked = False
            manager.process_events(event)
        manager.update(time_delta)
        pygame.display.update()
        manager.draw_ui(window)


def readfolder(foldername):
    filelist = os.list("testfiles/")


def readfile(filename):
    f = open(filename, "r")
    count = 1
    global startx
    global startindex
    global endindex
    global starty
    global data
    global goalx
    global goaly
    global filewidth
    global filelength
    global temparr
    global blockedxcoord
    global blockedycoord

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
                if count == 4 and internalcount == 1:
                    # temparr = [[0] * filewidth] * filelength
                    temparr = []
                    for i in range(0, filelength):
                        new = []
                        for j in range(0, filewidth):
                            new.append(0)
                        temparr.append(new)
                if internalcount == 1:
                    localx = int(word)
                elif internalcount == 2:
                    localy = int(word)
                elif internalcount == 3:
                    indicator = int(word)
                    if indicator == 1:
                        blockedxcoord.append(localx)
                        blockedycoord.append(localy)
                        in1 = localy - 1
                        in2 = localx - 1
                        temparr[in1][in2] = 1
            startindex = (startx, starty)
            endindex = (goalx, goaly)

            internalcount = internalcount + 1
        count = count + 1
    data = temparr


def draw_grid(window, width, height, cols, view, manager):
    global startindex
    global endindex
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
                add_verts((x, y), (j + 1, i + 1), size)
            i = i + 1
        j = j + 1
        i = 0

    for key in vertices:
        if key == startindex or key == endindex:
            vertices[key].draw_vertex(window, manager, filewidth, marked=True)
        else:
            vertices[key].draw_vertex(window, manager, filewidth)
        vertices[key].draw_lines(window)


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
                if verts[j] not in verts[i].neighbors:
                    verts[i].neighbors.append(verts[j])


def draw_path(endpoint: vertex, window, color):
    vert = endpoint.parent
    prev_point = endpoint.img_coords
    size = 4 if filewidth < 50 else 3
    while vert is not None and prev_point != vert.img_coords:
        pygame.draw.line(window, color, vert.img_coords, prev_point, size)
        prev_point = vert.img_coords
        vert = vert.parent





main()
