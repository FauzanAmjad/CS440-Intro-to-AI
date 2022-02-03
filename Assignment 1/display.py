import pygame, sys

data = [
    [0, 0, 0, 0],
    [0, 1, 0, 0],
    [1, 0, 1, 0]
]


def main():
    pygame.init()
    window = pygame.display.set_mode((480, 360))
    window.fill((255, 255, 255))
    pygame.display.set_caption('A*/Theta* simulation')
    draw_grid(window, window.get_width(), window.get_height(), 4)
    while True:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.display.quit()
                pygame.quit()
                sys.exit()
        pygame.display.update()


def draw_grid(window, width, height, cols):
    size = int(width / cols)
    i = 0
    j = 0
    for x in range(0, width, size):
        for y in range(0, height, size):
            rect = pygame.Rect(x, y, size, size)
            if data[i][j] == 1:
                pygame.draw.rect(window, (174, 174, 174), rect)
            pygame.draw.rect(window, (0, 0, 0), rect, 1)
            i = i+1
        j = j + 1
        i = 0



main()
