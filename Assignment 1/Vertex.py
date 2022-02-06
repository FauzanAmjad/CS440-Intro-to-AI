import pygame
import pygame_gui


class vertex:

    def __init__(self, img_coords: tuple, coords: tuple):
        self.img_coords = img_coords
        self.coords = coords
        self.neighbors = []
        self.parent = None
        self.is_closed = False
        self.gvalue = 0
        self.hvalue = 0
        self.clickable = None
        self.is_clicked = False

    def draw_vertex(self, surface, manager: pygame_gui.UIManager):
        #pygame.draw.circle(surface, (0, 0, 0), self.img_coords, 5)
        rect = pygame.Rect(0, 0, 10, 10)
        rect.center = self.img_coords
        self.clickable = pygame_gui.elements.UIButton(relative_rect= rect,
                                                    text=" ",
                                                    manager=manager)

    def draw_lines(self, surface):
        for vert in self.neighbors:
            pygame.draw.line(surface, (0, 0, 0), self.img_coords, vert.img_coords)

    def __str__(self):
        return f"img coords: {self.img_coords} coords: {self.coords}"

    def close(self):
        self.is_closed = True
