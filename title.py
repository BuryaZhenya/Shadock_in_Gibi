import pygame as pg

from pgColors import *


Title = "Душа Шаддока из Гибби"
Prolog = [
    "Королевство Гибби погрязло в болезни.",
    "Все расы пытаются выжить в эти сложные времена.",
    "Цены на лекарство выросли в несколько раз,",
    "потому что целебных трав не хватает.",
    "Как только кто-то узнавал про поляны с целебными",
    "травами, все люди и другие виды сразу пытались",
    "забрать себе как можно больше трав",
    "и продать их алхимикам.",
    "Таких людей назвали шаддоками.",
    " ",
    "Но эта работа весьма опасная..."
         ]
Prolog_Last = "... НЕ КАЖДАЯ ПОЛЯНА БЫВАЕТ ПУСТАЯ ..."

title_font_p = {'font':"gabriola", 'size':72, 'color':(255, 255, 100)}
prolog_font_p = {'font':"gabriola", 'size':48, 'color':(100, 255, 100)}
prolog_last_font_p = {'font':"gabriola", 'size':72, 'color':(200, 0, 0)}

title_effect_p = {'name':"print by chars", 'size_from':12, 'speed':950}
title_effect2_p = {'name':"scroll up by lines", 'line_from':"center", 'line_scroll':2, 'speed':300}
prolog_effect_p = {'name':"scroll up by lines", 'line_scroll':3}
prolog_last_effect_p = {'name':"scroll up by lines", 'line_to':"center", 'scroll':10, 'speed':100, 'delay':10000, 'visible':"always"}

music_p = {
    'file':"Two_Steps_From_Hell_-_Strength_of_a_Thousand_Men_66486333.mp3",
    'volume_from':0.2,
    'volume_to':1.0,
    'chpoints':[21400]
          }

class text_image():

    def __init__(self, show_text, font_name, font_size, color):
        self.font = pg.font.SysFont(font_name, font_size)
        self.text_block = self.font.render(show_text, True, color)
        
    def get_width(self):
        return self.text_block.get_width()

    def get_height(self):
        return self.text_block.get_height()

    def show(self, screen, pos):
        screen.blit(self.text_block, pos)


class text_effect():

    def __init__ (self, font_p, effect_p, text):
        self.is_active = False

        self.font_name = font_p['font']
        self.font_size_to = font_p['size']
        self.font_color = font_p['color']
        self.effect_name = "default"

        self.font_size_from = effect_p.get('size_from', self.font_size_to)

        self.text = text
        self.show_text = text
        self.font_size = self.font_size_from
        self.font_size_step = 0
        self.step_count = 1
        self.index = 0

    def enable(self):
        self.is_active = True

    def disable(self):
        self.is_active = True

    def get_active(self):
        return self.is_active

    def get_font_size_all(self):
        return {'size_from':self.font_size_from, 'size_to':self.font_size_to, 'size':self.font_size, 'size_step':self.font_size_step}

    def get_font_size(self):
        return self.font_size

    def get_text(self):
        return self.text

    def show_step(self, screen):
        if not self.is_active:
            return
        else:
            print("text_effect.show_step: " + self.effect_name)


class text_effect_enlarge_string_from_center(text_effect):

    def __init__(self, font_p, effect_p, text):
        super().__init__(font_p, effect_p, text)
        self.effect_name = "enlarge_string_from_center"
        self.show_text = ""
        self.index = 0

        self.step_count = len(text) // 2
        self.font_size_step = (self.font_size_to - self.font_size_from) // self.step_count

    def get_step_count(self):
        return self.step_count


class text_effect_print_by_chars(text_effect):

    def __init__(self, font_p, effect_p, text):
        super().__init__(font_p, effect_p, text)
        self.effect_name = "print_by_chars"

        self.step_count = len(text) - 1
        self.font_size_step = (self.font_size_to - self.font_size_from) // self.step_count
        self.show_text = ""
        self.index = 0

    def get_step_count(self):
        return self.step_count

    def show_step(self, screen):
        if not self.is_active:
            return

        if self.index <= self.step_count:
            self.show_text += self.text[self.index]
            self.index += 1

        out_text = text_image(self.show_text, self.font_name, self.font_size, self.font_color)
        out_text.show(
            screen,
            (
                screen.get_width() // 2 - out_text.get_width() // 2,
                screen.get_height() // 2 - out_text.get_height() // 2
            )
                     )

        self.font_size += self.font_size_step
        if self.font_size > self.font_size_to:
            self.font_size = self.font_size_to


class text_effect_scroll_by_line(text_effect):
    
    def __init__(self, font_p, effect_p, text):
        super().__init__(font_p, effect_p, text)
        self.effect_name = "scroll_by_line"

        self.step_count = 0
        self.font_size_step = 0

        self.line_from = effect_p.get('line_from', "bottom")
        self.line_to = effect_p.get('line_to', "top")
        self.line_scroll = effect_p.get('line_scroll', 1)
        self.line = -1000

        self.visible = effect_p.get('visible', "on scroll")

        self.out_text = text_image(self.show_text, self.font_name, self.font_size, self.font_color)

    def get_step_count(self):
        return self.step_count

    def get_top(self):
        return self.line

    def get_bottom(self):
        return self.line + self.out_text.get_height()

    def get_line(self):
        return self.line

    def get_line_all(self):
        return {'line_from':self.line_from, 'line_to':self.line_to, 'line':self.line, 'line_scroll':self.line_scroll}

    def is_border(self, screen, border):
        if border == "top":
            y = 0
        elif border == "bottom":
            y = screen.get_height()
        else:
            return False
        
        if self.line_scroll < 0:
            return (self.get_bottom() < y) and (self.get_bottom() - self.line_scroll >= y)
        else:
            return (self.line > y) and (self.line - self.line_scroll <= y)

    def set_bounds(self, screen):
        if self.line_from == "top":
            self.line_from = -self.out_text.get_height() - 1
        elif self.line_from == "center":
            self.line_from = screen.get_height() // 2 - self.out_text.get_height() // 2
        elif self.line_from == "bottom":
            self.line_from = screen.get_height() + 1
        
        if self.line_to == "top":
            self.line_to = -self.out_text.get_height() - 1
        elif self.line_to == "center":
            self.line_to = screen.get_height() // 2 - self.out_text.get_height() // 2
        elif self.line_to == "bottom":
            self.line_to = screen.get_height() + 1

        self.x_pos = screen.get_width() // 2 - self.out_text.get_width() // 2
        self.line = self.line_from

        if (self.line_to - self.line_from) * self.line_scroll < 0:
            self.line_scroll = -self.line_scroll
        
    def show_step(self, screen):
        if not self.is_active:
            return

        self.out_text.show(screen, (self.x_pos, self.line))

        if self.line == self.line_to + self.line_scroll:
            if self.visible == "on scroll":
                self.is_active = False

        else:
            self.line += self.line_scroll


class music_effect():

    def __init__(self, music_p={'file':""}, step_count=0):
        self.is_music = False

        if music_p['file'] != "":
            pg.mixer.music.load(music_p['file'])
            self.is_music = True

            self.chpoints = music_p.get('chpoints', [])
            self.chkpoint_index = 0

            self.loops = music_p.get('loops', 0)
            self.start = music_p.get('start', 0.0)
            self.fade_ms = music_p.get('fade_ms', 0)

            self.vol_from = music_p.get('volume_from', pg.mixer.music.get_volume())
            self.vol_to = music_p.get('volume_to', self.vol_from)
            self.vol = self.vol_from

            self.vol_step = 0
            if self.vol_to != self.vol_from:
                if step_count == 0:
                    self.vol_step = 0.01
                else:
                    self.vol_step = (self.vol_to - self.vol_from) / step_count

    def play(self):
        if self.is_music:
            pg.mixer.music.set_volume(self.vol)
            pg.mixer.music.play(loops=self.loops, start=self.start, fade_ms=self.fade_ms)

    def stop(self):
        if self.is_music:
            pg.mixer.music.stop()

    def get_play_status(self):
        if self.is_music:
            if pg.mixer.music.get_busy():
                return 1
            else:
                return 0
        else:
            return -1

    def chg_volume(self):
        if self.is_music:
            self.vol += self.vol_step

            if self.vol > 1.0:
                self.vol = 1.0
            elif self.vol < 0.0:
                self.vol = 0.0

            pg.mixer.music.set_volume(self.vol)

    def set_check_point(self, event_type):
        if self.is_music:
            if self.chkpoint_index < len(self.chpoints):
                pg.time.set_timer(event_type, self.chpoints[self.chkpoint_index])
                self.chkpoint_index += 1

    def set_endevent(self, event_type):
        if self.is_music:
            pg.mixer.music.set_endevent(event_type)


def GameIntro():
    size = (1200, 900)
    bkcolor = BLACK
    screen = pg.display.set_mode(size)
    pg.display.set_icon(pg.image.load('shaddok1.png'))
    pg.display.set_caption(Title)

    titles = []

    if title_effect_p['name'] == "enlarge string from center":
        t = text_effect_enlarge(title_font_p, title_effect_p, Title)
    elif title_effect_p['name'] == "print by chars":
        t = text_effect_print_by_chars(title_font_p, title_effect_p, Title)
    else:
        t = text_effect(title_font_p, title_effect_p, Title)

    t.enable()
    titles.append(t)

    m = music_effect(music_p, t.get_step_count())

    t = text_effect_scroll_by_line(title_font_p, title_effect2_p, Title)
    t.set_bounds(screen)
    titles.append(t)

    prolog_lines = []

    for p in Prolog:
        t = text_effect_scroll_by_line(prolog_font_p, prolog_effect_p, p)
        t.set_bounds(screen)
        prolog_lines.append(t)

    t = text_effect_scroll_by_line(prolog_last_font_p, prolog_last_effect_p, Prolog_Last)
    t.set_bounds(screen)
    prolog_last = [t]

    MYEVENTTYPE__MUSIC_END_EVENT = pg.USEREVENT + 1
    MYEVENTTYPE__MUSIC_CHK_POINT = MYEVENTTYPE__MUSIC_END_EVENT + 1
    MYEVENTTYPE__STEP_TIME = MYEVENTTYPE__MUSIC_CHK_POINT + 1
    MYEVENTTYPE__SCROLL_TIME = MYEVENTTYPE__STEP_TIME + 1
    MYEVENTTYPE__LAST_TIME = MYEVENTTYPE__SCROLL_TIME + 1

    screen.fill(bkcolor)
    pg.display.flip()

    running = True
    clock = pg.time.Clock()

    pg.time.set_timer(MYEVENTTYPE__STEP_TIME, title_effect_p['speed'])
    pg.display.flip()

    m.play()
    if m.get_play_status == -1:
        pg.time.set_timer(MYEVENTTYPE__MUSIC_END_EVENT, 120000)
        pg.time.set_timer(MYEVENTTYPE__MUSIC_CHK_POINT, music_p.get('chpoints', [0])[0])
    else:
        m.set_endevent(MYEVENTTYPE__MUSIC_END_EVENT)
        m.set_check_point(MYEVENTTYPE__MUSIC_CHK_POINT)

    while running:
        for event in pg.event.get():
            if event.type == MYEVENTTYPE__MUSIC_END_EVENT:
                running = False

            if event.type == MYEVENTTYPE__MUSIC_CHK_POINT:

                pg.time.set_timer(MYEVENTTYPE__MUSIC_CHK_POINT, 0)
                pg.time.set_timer(MYEVENTTYPE__STEP_TIME, 0)
                pg.time.set_timer(MYEVENTTYPE__SCROLL_TIME, title_effect2_p['speed'])

                prolog_index = 0
                titles[0].disable()
                titles[1].enable()
                prolog_lines[0].enable()

            if event.type == MYEVENTTYPE__STEP_TIME:
                screen.fill(bkcolor)

                titles[0].show_step(screen)                                

                m.chg_volume()

                pg.display.update()

            if event.type == MYEVENTTYPE__SCROLL_TIME:
                screen.fill(bkcolor)

                for p in prolog_lines:
                    p.show_step(screen)

                    if p.is_border(screen, "bottom"):
                        prolog_index += 1
                        if prolog_index < len(prolog_lines):
                            prolog_lines[prolog_index].enable()

                titles[1].show_step(screen)

                pg.display.update()

                if prolog_lines[len(prolog_lines)-1].is_border(screen, "top"):
                    pg.time.set_timer(MYEVENTTYPE__SCROLL_TIME, 0)
                    pg.time.set_timer(MYEVENTTYPE__LAST_TIME, prolog_last_effect_p['delay'])
                    prolog_last[0].enable()
                    is_starting = True

            if event.type == MYEVENTTYPE__LAST_TIME:
                if is_starting:
                    pg.time.set_timer(MYEVENTTYPE__LAST_TIME, prolog_last_effect_p['speed'])
                    is_starting = False
                    
                screen.fill(bkcolor)
                prolog_last[0].show_step(screen)
                pg.display.update()

            if event.type == pg.QUIT:
                running = False

            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    running = False


    m.stop()

# Main

if __name__ == '__main__':
    pg.init()
    GameIntro()
    pg.quit()
    
