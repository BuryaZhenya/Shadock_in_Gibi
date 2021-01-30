# Модуль GameObject

import pygame as pg

from pgColors import *
from DEBUG import *

# настройка папки ассетов
#game_folder = os.path.dirname(__file__)
#img_folder = os.path.join(game_folder, 'img')
#player_img = pygame.image.load(os.path.join(img_folder, 'p1_jump.png')).convert()

COORD_X = 0
COORD_Y = 1

X_MIN = 0
X_MAX = 2
Y_MIN = 1
Y_MAX = 3

SUCCESS = 0
FAILURE = 1

class GameObject(pg.sprite.Sprite):

    ## fname - полный путь к образу спрайта
    ## pos   - список координат позиции спрайта (X, Y)
    ## name  - имя объекта
    def __init__(self, fname, pos, name=""):
#        debug(("GameObject", fname, pos, name))
        super().__init__()
        self.fname = fname
        self.image = pg.image.load(fname)
        self.pos = pos
        self.view_pos = (0, 0) # координаты отображения объекта

        if name != "":
            self.name = name
        else:
            self.name = fname

    def get_name(self):
        return self.name

    def get_pos(self):
        return self.pos

    def get_x(self):
        return self.pos[COORD_X]

    def get_y(self):
        return self.pos[COORD_Y]

    def get_fname(self):
        return self.fname

    def get_view_pos(self):
        return view_pos

    def set_pos(self, pos):
        self.pos = pos

    def set_x(self, x):
        self.set_pos((x, self.pos[COORD_Y]))

    def set_y(self, y):
        self.set_pos((self.pos[COORD_X], y))

    def set_view_pos(self, view_pos):
        self.view_pos = view_pos

    def set_image(self, fname):
        self.fname = fname
        self.image = pg.image.load(fname)

    def show(self, window):
        window.blit(self.image, self.view_pos)
        

class GameStaticObject(GameObject):

    ## fname - полный путь к образу спрайта
    ## pos   - список координат позиции объекта (X, Y)
    ## name  - имя объекта
    def __init__(self, fname, pos, name=""):
#        debug(("GameStaticObject", fname, pos, name))
        super().__init__(fname, pos, name)


class GameStaticScoredObject(GameStaticObject):

    ## fname - полный путь к образу спрайта
    ## pos   - список координат позиции объекта (X, Y)
    ## name  - имя объекта
    ## score - число очков за объект
    def __init__(self, fname, pos, score, name=""):
#        debug(("GameStaticScoredObject", fname, pos, name))
        super().__init__(fname, pos, name)
        self.score = score

    def get_score(self):
        return self.score

    def set_score(self, score):
        self.score = score


class GameMovingObject(GameObject):

    ## fname   - полный путь к образу спрайта
    ## pos     - список координат позиции объекта (X, Y)
    ## borders - список границ прямоугольной области для объекта (Xmin, Ymin, Xmax, Ymax)
    ## speed   - вектор скорости перемещения объекта (dx, dy)
    ## name    - имя объекта
    def __init__(self, fname, pos, borders, speed, name=""):
        super().__init__(fname, pos, name)
        self.speed = speed
        self.borders = borders
#        debug(("GameMovingObject", fname, self.pos, self.borders, self.speed, self.name))

    def move(self, dx, dy):
#        debug(("GameMovingObject::move", self, self.name, dx, dy, self.pos, self.speed, self.borders))

        x, y = self.pos[COORD_X] + dx, self.pos[COORD_Y] + dy
#        debug((x, self.borders[X_MIN], self.borders[X_MAX]))
#        debug((y, self.borders[Y_MIN], self.borders[Y_MAX]))

        if (x < self.borders[X_MIN]) or (x > self.borders[X_MAX]):
#            debug("X failure")
            return FAILURE

        if (y < self.borders[Y_MIN]) or (y > self.borders[Y_MAX]):
#            debug("Y failure")
            return FAILURE

        self.pos = (x, y)
#        debug(("SUCCESS", self.pos))

        return SUCCESS

    def get_borders(self):
        return self.borders

    def get_speed(self):
        return self.speed

    def set_borders(self, borders):
        self.borders = borders

    def set_speed(self, speed):
        self.speed = speed

    def action(self):
        flag = FAILURE

        while flag == FAILURE:
            dx, dy = self.speed[COORD_X], self.speed[COORD_Y]

            flag = self.move(dx, dy)
            if flag == FAILURE:
                speedX = -self.speed[COORD_X] if (self.pos[COORD_X] + dx < self.borders[X_MIN]) or (self.pos[COORD_X] + dx > self.borders[X_MAX]) else self.speed[COORD_X]
                speedY = -self.speed[COORD_Y] if (self.pos[COORD_Y] + dy < self.borders[Y_MIN]) or (self.pos[COORD_Y] + dy > self.borders[Y_MAX]) else self.speed[COORD_Y]

                self.speed = (speedX, speedY)
       

# Класс Player
class GamePlayerObject(GameMovingObject):

    def __init__(self, fname, pos, borders, speed, name=""):
#        debug(("GamePlayerObject", fname, pos, speed, borders, name))
        super().__init__(fname, pos, borders, speed, name)

    def action(self, key):
#        debug("GamePlayerObject::action")
        dx = 0
        dy = 0
        if key == pg.K_LEFT:
            dx = -self.speed[0]
        if key == pg.K_RIGHT:
            dx = self.speed[0]
        if key == pg.K_UP:
            dy = -self.speed[1]
        if key == pg.K_DOWN:
            dy = self.speed[1]

#        debug("move on " + str((dx, dy)))
        self.move(dx, dy)


