import os

from pgColors import *

# Установки

# Размер окна игры
window = {
    'SIZE_X': 1600,
    'SIZE_Y': 900
}

# Размер окна игрового пространства
game_area_window = {
    'WSIZE_X': 1600,
    'WSIZE_Y': 800,
    'OFFSET_X': 0,
    'OFFSET_Y': 100
}

# Размер ячейки на экране
square = {
    'squareX': 64,
    'squareY': 64
}

# Размер игрового пространства
game_area = {
    'area_h': 50,
    'area_v': 30
}

# Размер отображаемого игрового пространства
game_area_view = {
    'warea_h': game_area_window['WSIZE_X'] // square['squareX'],
    'warea_v': game_area_window['WSIZE_Y'] // square['squareY']
}

gameDir = os.path.dirname(__file__)
imageDir = os.path.join(gameDir, 'Image')

# Расположение
game_dirs = {
    'gameDir': gameDir,
    'imageDir': imageDir,
    'soundDir': os.path.join(gameDir, 'Sound'),
    'spriteDir': imageDir
}

game_params = {
    'dirs': game_dirs,
    'window': window,
    'game_area_window': game_area_window,
    'square': square,
    'game_area': game_area,
    'game_area_view': game_area_view
}

# Длительность событий
NEXT_ACTION_TIME = 300
MAX_GAME_TIME = 50000
backColors = (YELLOW, BLUE, CYAN, MAGENTA, RED)

# Коды предметов и персонажей
cdFREE = 0
cdSHADOK = 1
cdGIBI = 2
cdFLOWER = 10
cdSHRUB = 20
cdTREE = 30
cdSTONE = 100
cdBORDER = 255

# Область действия
global_area = ('global', (0, 0, game_area['area_h'], game_area['area_v']))
local_area = ('local', (-10, -5, 9, 4))

# Параметры предметов и персонажей
gobj_params = {
    'Player': {
        'code': cdSHADOK,
        'image': "shadok_sz64.png",
        'name': "Шадок",
        'area': global_area
              },
    'Border': {
        'code': cdBORDER,
        'image': "tree_sz64.png",
        'name': "Граница",
              },
    'Static': {
        'stones': {
            'code': cdSTONE,
            'count': 100,
            'types': [
                {
                    'image': "stone_sz64_01.png",
                    'name': "Камень",
                    'prob': 75
                },
                {
                    'image': "stone_sz64_02.png",
                    'name': "Камень разрушенный",
                    'prob': 25
                }
                     ]
                  }
              },
    'StaticScored': {
        'flowers': {
            'code': cdFLOWER,
            'count': 200,
            'types': [
                {
                    'image': "flowerL_sz32-4.png",
                    'name': "Цветок обыкновенный увядающий",
                    'score': 1,
                    'prob': 70
                },
                {
                    'image': "flowerL_sz32-8.png",
                    'name': "Цветок обыкновенный распустившийся",
                    'score': 2,
                    'prob': 15
                },
                {
                    'image': "flowerR_sz32-8.png",
                    'name': "Цветок душистый",
                    'score': 2,
                    'prob': 10
                },
                {
                    'image': "flowerR2_sz32-8.png",
                    'name': "Цветок ароматный",
                    'score': 3,
                    'prob': 5
                }
                     ]
                   },
        'shrub': {
            'code': cdSHRUB,
            'count': 50,
            'types': [
                {
                    'image': "shrub_sz48_06.png",
                    'name': "Куст 1",
                    'score': 5,
                    'prob': 50
                },
                {
                    'image': "shrub_sz48_07.png",
                    'name': "Куст 2",
                    'score': 5,
                    'prob': 50
                }
                     ]
                }
                    },
    'Moved': {
        'gibies': {
            'code': cdGIBI,
            'count': 50,
            'types': [
                {
                    'image': "gibi_sz48_01.png",
                    'name': "Гиби-1",
                    'area': global_area,
                    'prob': 30
                },
                {
                    'image': "gibi_sz48_02.png",
                    'name': "Гиби-2",
                    'area': global_area,
                    'prob': 25
                },
                {
                    'image': "gibi_sz48_03.png",
                    'name': "Гиби-3",
                    'area': local_area,
                    'prob': 20
                },
                {
                    'image': "gibi_sz48_04.png",
                    'name': "Гиби-4",
                    'area': local_area,
                    'prob': 15
                },
                {
                    'image': "gibi_sz48_05.png",
                    'name': "Гиби-5",
                    'area': local_area,
                    'prob': 10
                }
                      ]
                  }
             }
}
