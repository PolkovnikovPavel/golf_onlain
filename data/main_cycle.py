import asyncio, time
from requests import get, post, put, delete
from data.functions import pw, ph

url = 'http://192.168.0.22:5000'
type_menu = 'main'
mous_x = 0
mous_y = 0


def close_window():
    global running
    running = False


def move(event, *args):
    global mous_x, mous_y
    mous_x = event.x
    mous_y = event.y
    if type_menu == 'game':
        print(put(f'{url}/api/update_room/{room_id}/{mous_x}/{mous_y}/{int(is_1_player)}').json())
        if is_1_player:
            all_gropes[1].all_objects[0].go_to(mous_x, mous_y)
        else:
            all_gropes[1].all_objects[1].go_to(mous_x, mous_y)


def click(event, *args):
    for grope in all_gropes:
        grope.check(mous_x, mous_y, is_clik=True)


def clik_out(event, *args):
    for grope in all_gropes:
        grope.check(mous_x, mous_y, is_clik=False)



async def main_cycle(canvas_, screen_w, screen_h, all_gropes_):
    global canvas, running, all_gropes, my_id, type_menu
    canvas = canvas_
    all_gropes = all_gropes_
    main_grope, game_grope = all_gropes

    my_id = post(f'{url}/api/create_new_user').json()['user_id']

    timer = time.time()
    running = True

    while running:

        canvas.update()
        dt = time.time() - timer
        dt = (1 / 120) - dt
        if dt > 0:
            time.sleep(dt)
        #print(1 / (time.time() - timer))
        timer = time.time()

    print(delete(f'{url}/api/delete_user/{my_id}').json())


def game_cycle(*args):
    global type_menu, room_id, is_1_player
    type_menu = 'game'
    main_grope, game_grope = all_gropes

    if get(f'{url}/api/get_free_room').json()['room_id'] != -1:
        room_id = get(f'{url}/api/get_free_room').json()['room_id']
        is_1_player = False
        print(put(f'{url}/api/create_room', json={'user_id': my_id, 'room_id': room_id}).json())

    else:
        is_1_player = True
        room_id = post(f'{url}/api/create_room',
           json={'user_1': my_id,
                 'x_1': 0,
                 'y_1': 0,
                 'x_2': 0,
                 'y_2': 0,
                 'map': 1,
                 'rotate': 0,
                 'power': 1,
                 'is_turn_ended': True,
                 'is_turn_player_1': True,
                 'is_first_turn_player_1': True,}).json()['room_id']
        main_grope.hide_all()

        type_menu = 'waiting'
        while True:
            if get(f'{url}/api/update_room/{room_id}').json()['user_2'] != -1:
                break
            canvas.update()

        type_menu = 'game'



    game_grope.show_all()
    main_grope.hide_all()

    timer = time.time()
    while running:
        my_room = get(f'{url}/api/update_room/{room_id}').json()
        if is_1_player:
            all_gropes[1].all_objects[1].go_to(my_room['x_2'], my_room['y_2'])
        else:
            all_gropes[1].all_objects[0].go_to(my_room['x_1'], my_room['y_1'])

        canvas.update()
        dt = time.time() - timer
        dt = (1 / 120) - dt
        if dt > 0:
            time.sleep(dt)
        #print(1 / (time.time() - timer))
        timer = time.time()

