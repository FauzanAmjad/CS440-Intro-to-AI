import pygame


class vertex:
    neighbors = []
    parent = None

    def __init__(self, img_coords: tuple, coords: tuple):
        self.img_coords = img_coords
        self.coords = coords

    def get_img_coords(self):
        return self.img_coords

    def get_coords(self):
        return self.coords

    def draw_vertex(self, surface):
        pygame.draw.circle(surface, (0, 0, 0), self.img_coords, 5)

    def draw_lines(self, surface):
        for vert in self.neighbors:
            pygame.draw.line(surface, (0, 0, 0), self.img_coords, vert.get_img_coords())

    def __str__(self):
        return f"img coords: {self.img_coords} coords: {self.coords}"
