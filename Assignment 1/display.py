import pygame, sys, os, pygame_gui
from Vertex import vertex

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
startx = 0
starty = 0
goalx = 0
goaly = 0
blockedxcoord = []
blockedycoord = []


def main():
    # making the display
    grid_cols = 4
    grid_rows = 3
    grid_width = 480
    grid_height = 360
    pygame.init()
    window = pygame.display.set_mode((grid_width * 3 / 2, grid_height * 3 / 2))
    window.fill((255, 255, 255))
    view_rect = pygame.Rect(0, 0, grid_width, grid_height)
    view_rect.center = window.get_rect().center
    pygame.display.set_caption('A*/Theta* simulation')
    manager = pygame_gui.UIManager((window.get_width(), window.get_height()), 'theme.json')
    draw_grid(window, view_rect.width, view_rect.height, grid_cols, view_rect, manager)
    cache = pygame.Surface.copy(window)
    text_box = None
    clicked = (0,0)
    clock = pygame.time.Clock()
    while True:
        time_delta = clock.tick(60) / 1000.0
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.display.quit()
                pygame.quit()
                sys.exit()

            if event.type == pygame_gui.UI_BUTTON_PRESSED:
                window.blit(source=cache, dest=(0, 0))
                vertices[clicked].clickable.unselect()
                for key in vertices:
                    if event.ui_element == vertices[key].clickable:
                        if text_box is not None:
                            text_box.hide()
                            text_box = None
                        if not vertices[key].is_clicked:
                            vertices[key].clickable.select()
                            clicked = key
                            rect = pygame.Rect(vertices[key].img_coords[0], vertices[key].img_coords[1], grid_width / 4,
                                               grid_width / 3)
                            if vertices[key].coords[1] > grid_rows/2:
                                rect.bottomleft = (vertices[key].img_coords[0], vertices[key].img_coords[1])
                            if vertices[key].coords[0] > grid_cols/2:
                                rect.right = vertices[key].img_coords[0]
                            text_box = pygame_gui.elements.UITextBox(html_text=f"   <u>{vertices[key].coords}</u><br>"
                                                                               f"g: {vertices[key].gvalue}<br>"
                                                                               f"h: {vertices[key].hvalue}<br>"
                                                                               f"f: {vertices[key].gvalue+vertices[key].hvalue}<br>",
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
        vertices[key].draw_vertex(window, manager)
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
                verts[i].neighbors.append(verts[j])


def draw_path(endpoint: vertex, window):
    vert = endpoint.parent
    prev_point = endpoint.img_coords
    while vert is not None:
        pygame.draw.line(window, (255, 46, 31), vert.img_coords, prev_point, 2)
        prev_point = vert.img_coords
        vert = vert.parent


main()
