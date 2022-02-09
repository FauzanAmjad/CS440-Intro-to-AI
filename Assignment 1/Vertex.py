import pygame
import pygame_gui
import math


class vertex:

    def __init__(self, img_coords: tuple, coords: tuple):
        self.img_coords = img_coords
        self.coords = coords
        self.neighbors = []
        self.parent = None
        self.is_closed = False
        self.gvalue = math.inf
        self.hvalue = 0
        self.clickable = None
        self.is_clicked = False

    def draw_vertex(self, surface, manager: pygame_gui.UIManager, cols, marked=False):
        size = 10 if cols < 50 else 5
        rect = pygame.Rect(0, 0, size, size)
        rect.center = self.img_coords
        if marked:
            self.clickable = pygame_gui.elements.UIButton(relative_rect=rect,
                                                          text=" ",
                                                          manager=manager, object_id="#important_button")
        else:
            self.clickable = pygame_gui.elements.UIButton(relative_rect=rect,
                                                          text=" ",
                                                          manager=manager)


    def draw_lines(self, surface):
        for vert in self.neighbors:
            pygame.draw.line(surface, (0, 0, 0), self.img_coords, vert.img_coords)

    def __str__(self):
        return f"img coords: {self.img_coords} coords: {self.coords}"

    def close(self):
        self.is_closed = True

    def close(self):
        self.is_closed = True

    def _eq_(self, other):
        if self.coords[0] == other.coords[0] and self.coords[1] == other.coords[1]:
            return True
        else:
            return False

    def __lt__(self, other):
        return self.fvalue < other.fvalue
