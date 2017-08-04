
import logging
import pygame

DISPLAY_WIDTH = 1280
DISPLAY_HEIGHT = 800

BORDER_COLOR = (188, 196, 209)
BACKGROUND_COLOR = (66, 134, 244)
myfont = None


class Box(object):
    def __init__(self, x, y, w, h):
        self._border = pygame.Rect(x, y, w, h)
        self._border_color = (150, 0, 0)
        self._background_color = (20, 20, 20)

    def render(self, surface):
        pygame.draw.rect(surface, self._border_color, self._border, 1)


class TitleBar(Box):

    HEIGHT = 20

    def __init__(self, x, y, w, title=None):
        super(TitleBar, self).__init__(x, y, w, TitleBar.HEIGHT)
        self._title_surface = None
        if title:
            self.set(title)

    def render(self, surface):
        super(TitleBar, self).render(surface)
        if self._title_surface:
            surface.blit(
                self._title_surface,
                self._border.x,
                self._border.y,
            )

    def set(self, title):
        global myfont
        self._title_surface = myfont.render(
            title,
            True,
            self._border_color,
            self._background_color
        )


class Window(Box):
    def __init__(self, x, y, w, h, title=None):
        super(Window, self).__init__(x, y+TitleBar.HEIGHT-1, w, h+TitleBar.HEIGHT-1)
        self._title = TitleBar(x, y, w, title)

    def render(self, surface):
        self._title.render(surface)
        super(Window, self).render(surface)

    def setTitle(self, title):
        self._title.set(title)


def _main():

    global myfont

    pygame.init()

    myfont = pygame.font.SysFont("monospace", 15)

    clock = pygame.time.Clock()
    pygame.display.set_caption('bufer v0')
    screen = pygame.display.set_mode((DISPLAY_WIDTH, DISPLAY_HEIGHT), 0)

    window = Window(50, 50, 300, 300, 'Disassembly')

    running = True
    while running:

        # Event handling.
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                pass

        window.render(screen)

        pygame.display.flip()
        clock.tick(30)


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    _main()
