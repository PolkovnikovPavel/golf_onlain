import time
#from __future__ import print_function

from data.main_cycle import *
from data.objects import *


def move_oval(event):
    global c
    c.destroy()
    c = tkinter.Canvas(master, width=20, height=20, bg="red", cursor="pencil")
    c.pack()


screen_w = 1200
screen_h = 800
master = tkinter.Tk()
master.geometry(f'{screen_w}x{screen_h}+200+100')
master.protocol("WM_DELETE_WINDOW", close_window)
teak_w_and_h(screen_w, screen_h)
canvas = tkinter.Canvas(master, bg='#6A5F80', height=screen_h, width=screen_w)
canvas.pack(fill=tkinter.BOTH, expand=1)
print(screen_w, screen_h)


all_gropes = []

main_grope = Group()
all_gropes.append(main_grope)
btn = Button(525, 360, 150, 80, 'btn_play.png', canvas, function=game_cycle)
main_grope.add_objects(btn)

game_grope = Group()
all_gropes.append(game_grope)
game_grope.hide_all()



master.bind('<Motion>', move)
master.bind('<Button-1>', click)
master.bind('<ButtonRelease-1>', clik_out)

main_cycle(canvas, all_gropes)






