import pygame

from input import Input
from button import Button

pygame.init()

width, height = 1280, 720
fps = 60

win = pygame.display.set_mode((width, height))
pygame.display.set_caption('widgets test')
clock = pygame.time.Clock()

font = pygame.font.Font(None, 32)

bt = Button(win, x = 100, y = 100, width = 200, fontSize = 60, borderRadius = 25, text = 'Click!')
input = Input(win, x = 100, y = 400, borderRadius = 15, maxChars = 256, noText = 'Enter your text...', cursorColor = (255, 0, 0))

while 1:
    clock.tick(fps)
    win.fill((60, 60, 60))

    for event in pygame.event.get():
        if event.type == pygame.QUIT: exit()
        elif event.type == pygame.KEYDOWN: input.Press(event.unicode)

    bt.update()
    input.update()

    fpsINFO = font.render(str(int(clock.get_fps())), 1, (255, 255, 255))
    win.blit(fpsINFO, (10, 10))
    
    pygame.display.update()