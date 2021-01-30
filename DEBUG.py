# Модуль DEBUG

DEBUG = False

def debug(msg):
    global DEBUG

#    print(DEBUG)
    if DEBUG:
        print(msg)

def debugOn():
    global DEBUG

#    print(DEBUG)
    DEBUG = True
#    print(DEBUG)

def debugOff():
    global DEBUG

    DEBUG = False

def setDebug(dbg):
    global DEBUG

    cur = DEBUG
    DEBUG = dbg
    return cur
