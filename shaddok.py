import pygame as pg
import random as rnd
#import math

from pgColors import *
from DEBUG import *

import GameObject as gobj

from shaddok_init import *
from title import *


pi = 3.1415926


gmObjects = {}

def radian(degree):
    return (pi * degree) / 180


def time2str(time):
    r = time % 100
    if r < 10:
        s = "0" + str(r)
    else:
        s = str(r)

    return str(time // 100) + "." + s


class GameArea:

    def __init__(self, game_params, gobj_params):
        global gmObjects
        
        self.area_sizeX = game_params['game_area']['area_h']
        self.area_sizeY = game_params['game_area']['area_v']
        self.area_scaleX = game_params['square']['squareX']
        self.area_scaleY = game_params['square']['squareY']

        self.area_view_X = game_params['game_area_view']['warea_h']
        self.area_view_Y = game_params['game_area_view']['warea_v']

        self.area_view = (0, 0)

        self.area_view_offset_X = game_params['game_area_window']['OFFSET_X']
        self.area_view_offset_Y = game_params['game_area_window']['OFFSET_Y']

        self.game_window_size = self.game_windowX, self.game_windowY = game_params['window']['SIZE_X'], game_params['window']['SIZE_Y']
        self.game_window_info = (0, 0, self.game_windowX, 100)

        # Игровое пространство
        self.area = [[{'code': (cdFREE)} for i in range(self.area_sizeX)] for j in range(self.area_sizeY)]

        # Граница
        b = gobj_params['Border']
        obj = gobj.GameStaticObject(os.path.join(game_params['dirs']['spriteDir'], b['image']), (-1, -1), b['name'])

        for i in range(self.area_sizeX):
            self.area[0][i] = {'code': (cdBORDER), 'obj': obj}
            self.area[self.area_sizeY - 1][i] = {'code': (cdBORDER), 'obj': obj}

        for j in range(self.area_sizeY - 2):
            self.area[j + 1][0] = {'code': (cdBORDER), 'obj': obj}
            self.area[j + 1][self.area_sizeX - 1] = {'code': (cdBORDER), 'obj': obj}

        # Игрок
        p = gobj_params['Player']
        x, y = 0, 0
        while self.area[y][x]['code'] != (cdFREE):
            x = rnd.randint(1, self.area_sizeX - 1)
            y = rnd.randint(1, self.area_sizeY - 1)

        b = p['area'][1]
        if p['area'][0] == 'local':
            b[0] += x
            b[1] += y
            b[2] += x
            b[3] += y

        obj = gobj.GamePlayerObject(os.path.join(game_params['dirs']['spriteDir'], p['image']), (x, y), b, (1, 1), p['name'])
        self.area[y][x] = {'code': (p['code']), 'obj': obj}
        gmObjects['Player'] = obj
        self.area_align(obj)

        # Предметы статические
        sobj = gobj_params['Static']
        for k in sobj.keys():
            base_cd = sobj[k]['code']
            types = sobj[k]['types']
            prob = []
            for t in range(len(types)):
                for p in range(types[t]['prob']):
                    prob.append((base_cd, t))

            gmObjects[k] = []
            x, y = 0, 0
            for i in range(sobj[k]['count']):
                while self.area[y][x]['code'] != (cdFREE):
                    x = rnd.randint(1, self.area_sizeX - 1)
                    y = rnd.randint(1, self.area_sizeY - 1)

                p = rnd.randint(0, 99)

                sobj_par = types[prob[p][1]]
                obj = gobj.GameStaticObject(os.path.join(game_params['dirs']['spriteDir'], sobj_par['image']), (x, y), sobj_par['name'])

                self.area[y][x] = {'code': prob[p], 'obj': obj}

                gmObjects[k].append(obj)

        # Предметы статические с начислением очков
        sobj = gobj_params['StaticScored']
        for k in sobj.keys():
            base_cd = sobj[k]['code']
            types = sobj[k]['types']
            prob = []
            for t in range(len(types)):
                for p in range(types[t]['prob']):
                    prob.append((base_cd, t))

            gmObjects[k] = []
            x, y = 0, 0
            for i in range(sobj[k]['count']):
                while self.area[y][x]['code'] != (cdFREE):
                    x = rnd.randint(1, self.area_sizeX - 1)
                    y = rnd.randint(1, self.area_sizeY - 1)

                p = rnd.randint(0, 99)

                sobj_par = types[prob[p][1]]
                obj = gobj.GameStaticScoredObject(os.path.join(game_params['dirs']['spriteDir'], sobj_par['image']), (x, y), sobj_par['score'], sobj_par['name'])

                self.area[y][x] = {'code': prob[p], 'obj': obj}

                gmObjects[k].append(obj)

        # Персонажи
        mobj = gobj_params['Moved']
        for k in mobj.keys():
            base_cd = mobj[k]['code']
            types = mobj[k]['types']
            prob = []
            for t in range(len(types)):
                for p in range(types[t]['prob']):
                    prob.append((base_cd, t))
                
            gmObjects[k] = []
            x, y = 0, 0
            for i in range(mobj[k]['count']):
                while self.area[y][x]['code'] != (cdFREE):
                    x = rnd.randint(1, self.area_sizeX - 1)
                    y = rnd.randint(1, self.area_sizeY - 1)

                p = rnd.randint(0, 99)
        
                mobj_par = types[prob[p][1]]
                b = mobj_par['area']
                if b[0] == 'local':
                    border = (x + b[1][0], y + b[1][1], x + b[1][2], y + b[1][3])
                else:
                    border = b[1]

                obj = gobj.GameMovingObject(os.path.join(game_params['dirs']['spriteDir'], mobj_par['image']), (x, y), border, (1, 1), mobj_par['name'])

                self.area[y][x] = {'code': prob[p], 'obj': obj}

                gmObjects[k].append(obj)
        
    # Выравнивание отображаемой области по игроку
    def area_align(self, player):
        x = player.get_x() - self.area_view_X // 2
        y = player.get_y() - self.area_view_Y // 2

        if x < 0:
            x = 0
        if y < 0:
            y = 0
        if x + self.area_view_X > self.area_sizeX:
            x = self.area_sizeX - self.area_view_X
        if y + self.area_view_Y > self.area_sizeY:
            y = self.area_sizeY - self.area_view_Y
        
        self.area_view = (x, y)

    def area_init(self):
        self.window = pg.display.set_mode(self.game_window_size)
        self.window.fill(GREEN)
        self.window.fill(GREY, self.game_window_info)
        pg.display.update()

    def area_text(self, text, color):
        self.window.fill(GREY, self.game_window_info)
        self.font = pg.font.SysFont('arial', 48)
        text_image = self.font.render(text, True, color)
        self.window.blit(text_image, (50, 10))

    def area_show(self, texts):
        global gmObjects

        self.window.fill(GREEN)
        i0, j0 = self.area_view[0], self.area_view[1]
        for j in range(self.area_view_Y):
            for i in range(self.area_view_X):
                sq = self.area[j0 + j][i0 + i]
                if sq['code'] != (cdFREE):
                    obj = sq['obj']
                    obj.set_view_pos((self.area_view_offset_X + i * self.area_scaleX, self.area_view_offset_Y + j * self.area_scaleY))
                    obj.show(self.window)

        text = ""
        for t in texts:
            text += t['text']
            for i in range(len(t['text']) + 1, t.get('size', len(t['text']))):
                text += " "
            print("[" + text + "]")

        self.area_text(text, BLUE)

        pg.display.update()

# Класс Game
class Game():

    def __init__(self, game_params, gobj_params):
        self.area = GameArea(game_params, gobj_params)

        self.score = 0
        self.game_time = MAX_GAME_TIME

        self.area.area_init()
        self.area.area_show([{'text':"  Время: " + time2str(self.game_time), 'size':20}, {'text':"Лечебных цветов: " + str(self.score)}])

    def action(self):
        global gmObjects

        running = True
        actionTick = NEXT_ACTION_TIME
        while running:
            actionTick -= 1
#            debug(actionTick)
            if actionTick == 0:
                actionTick = NEXT_ACTION_TIME
                for g in gmObjects['gibies']:
                    x, y = g.get_x(), g.get_y()
                    d_min = 1000000
                    flw = (0, 0)
                    for f in gmObjects['flowers']:
                        d = (f.get_x() - x) ** 2 + (f.get_y() - y) ** 2
                        if d < d_min:
                            d_min = d
                            flw = (f.get_x(), f.get_y())

                    if x < flw[0]:
                        dx = 1
                    elif x > flw[0]:
                        dx = -1
                    else:
                        dx = 0

                    if y < flw[1]:
                        dy = 1
                    elif y > flw[1]:
                        dy = -1
                    else:
                        dy = 0

                    # Переместить персонажа с учетом его зоны действия
                    g.set_speed((dx, dy))
                    g.action()

                    # Проверить возможность перемещения на новую позицию
                    pos_new = g.get_pos()
                    sq = self.area.area[pos_new[1]][pos_new[0]]
#                    debug(sq)
                    if sq['code'] == (cdFREE):
                        self.area.area[pos_new[1]][pos_new[0]] = self.area.area[y][x]
                        self.area.area[y][x] = {'code': (cdFREE)}
                    elif sq['code'] == (cdBORDER):
                        g.set_pos((x, y))
                    elif sq['code'] == (cdSHADOK):
                        g.set_pos((x, y))
                    elif sq['code'][0] == cdFLOWER:
                        flw = self.area.area[pos_new[1]][pos_new[0]]['obj']
                        flw.set_pos((-1, -1)) # сорвать цветок
                        self.area.area[pos_new[1]][pos_new[0]] = self.area.area[y][x]
                        self.area.area[y][x] = {'code': (cdFREE)}
                    else:
                        # что-то мешает - возвращаем позицию
                        g.set_pos((x, y))

            for event in pg.event.get():
                if event.type == pg.QUIT:
                    running = False

                # Установка клавиш
                if event.type == pg.KEYDOWN:
#                    debug(str(event.key))
                    if event.key == pg.K_ESCAPE:
                        running = False
                    else:
                        pl = gmObjects['Player']
#                        debug(pl)
                        pos = pl.get_pos()
#                        debug(pos)
                        pl.action(event.key)
                        pos_new = pl.get_pos()
#                        print((pos, pos_new))
                        
                        # Проверить возможность перемещения на новую позицию
                        sq = self.area.area[pos_new[1]][pos_new[0]]
#                        print(sq)
                        if sq['code'] == (cdFREE):
                            self.area.area[pos_new[1]][pos_new[0]] = self.area.area[pos[1]][pos[0]]
                            self.area.area[pos[1]][pos[0]] = {'code': (cdFREE)}
                        elif sq['code'] == (cdBORDER):
                            pl.set_pos(pos)
                        elif sq['code'][0] == cdFLOWER:
                            flw = self.area.area[pos_new[1]][pos_new[0]]['obj']
                            flw.set_pos((-1, -1)) # сорвать цветок
                            self.score += flw.get_score()
                            self.area.area[pos_new[1]][pos_new[0]] = self.area.area[pos[1]][pos[0]]
                            self.area.area[pos[1]][pos[0]] = {'code': (cdFREE)}
                        elif sq['code'][0] == cdSHRUB:
                            sh = self.area.area[pos_new[1]][pos_new[0]]['obj']
                            # обобрать куст - получить очки (однократно!) и остаться на старом месте
                            self.score += sh.get_score()
                            sh.set_score(0)
                            pl.set_pos(pos)
                        else:
                            # что-то мешает - возвращаем позицию
                            pl.set_pos(pos)

            self.area.area_align(gmObjects['Player'])
             
            self.area.area_show([{'text':"  Время: " + time2str(self.game_time), 'size':20}, {'text':"Лечебных цветов: " + str(self.score)}])

            self.game_time -= 1
            if self.game_time == 0:
                running = False


    def done(self):
        pg.quit()


# Main

debugOff()
debug("Start")

debug(game_params['dirs']['gameDir'])
debug(game_params['dirs']['imageDir'])
debug(game_params['dirs']['soundDir'])
debug(game_params['dirs']['spriteDir'])

#debug((gobj_params, game_params))

pg.init()

GameIntro()

g = Game(game_params, gobj_params)
g.action()
g.done()


