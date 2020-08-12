import asyncio, time, math
from requests import get, post, put, delete
from data.objects import *
from data.functions import pw, ph
from data.maps import *

url = 'http://192.168.0.16:5000'
type_menu = 'main'
mous_x = 0
mous_y = 0
old_mous_x = 0
old_mous_y = 0


def close_window():
    global running
    running = False


def move(event, *args):
    global mous_x, mous_y
    mous_x = event.x
    mous_y = event.y


def click(event, *args):
    global is_click, old_mous_x, old_mous_y
    is_click = True
    old_mous_x = mous_x
    old_mous_y = mous_y
    for grope in all_gropes:
        grope.check(mous_x, mous_y, is_clik=True)

    if type_menu == 'game_1':
        pointer.show()


def clik_out(event, *args):
    global is_click, is_ended
    if type_menu == 'game_1':
        if is_click:
            is_ended = True

    is_click = False
    for grope in all_gropes:
        grope.check(mous_x, mous_y, is_clik=False)



def main_cycle(canvas_, all_gropes_):
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
    global type_menu, room_id, is_1_player, hole, grass, walls, all_map, player_1, player_2
    type_menu = 'game'
    main_grope, game_grope = all_gropes

    if get(f'{url}/api/get_free_room').json()['room_id'] != -1:
        room_id = get(f'{url}/api/get_free_room').json()['room_id']
        is_1_player = False
        print(put(f'{url}/api/create_room', json={'user_id': my_id, 'room_id': room_id}).json())
        my_room = get(f'{url}/api/update_room/{room_id}').json()
        hole, grass, walls, coords, all_map = get_map(my_room['map'], canvas)
        x_1, y_1, x_2, y_2 = coords
    else:
        map = 0
        hole, grass, walls, coords, all_map = get_map(map, canvas)
        walls.hide_all()
        grass.hide_all()
        hole.hide()
        x_1, y_1, x_2, y_2 = coords
        is_1_player = True
        room_id = post(f'{url}/api/create_room',
           json={'user_1': my_id,
                 'x_1': x_1,
                 'y_1': y_1,
                 'x_2': x_2,
                 'y_2': y_2,
                 'map': map,
                 'rotate': 0,
                 'power': 1,
                 'is_turn_ended': True,
                 'is_turn_player_1': True,
                 'is_first_turn_player_1': True,}).json()['room_id']
        main_grope.hide_all()
        text = Object(300, 200, 600, 200, 'text_1.png', canvas)
        loading = Object(550, 350, 100, 100, 'loading.gif', canvas)

        type_menu = 'waiting'
        while running:
            if get(f'{url}/api/update_room/{room_id}').json()['user_2'] != -1:
                break
            loading.rotation_on(-30)
            time.sleep(0.07)
            canvas.update()

        type_menu = 'game'

        text.hide()
        loading.hide()

    grass.show_all()
    walls.show_all()
    hole.show()

    game_grope.show_all()
    main_grope.hide_all()

    player_1 = Object(x_1, y_1, 25, 25, 'blue_ball.png', canvas, mode_coord=True)
    player_2 = Object(x_2, y_2, 25, 25, 'red_ball.png', canvas, mode_coord=True)

    if is_1_player:
        name_1 = Text(100, 30, 'Я', canvas)
        name_2 = Text(1100, 30, 'Соперник', canvas)
    else:
        name_1 = Text(100, 30, 'Соперник', canvas)
        name_2 = Text(1100, 30, 'Я', canvas)

    timer = time.time()
    while running:
        type_menu = 'game'
        my_room = get(f'{url}/api/update_room/{room_id}').json()
        if my_room['is_turn_player_1']:
            if is_1_player:
                choice_of_direction(canvas, (player_1, player_2), is_1_player, (name_1, name_2))
                my_room = get(f'{url}/api/update_room/{room_id}').json()
                to_hit(canvas, my_room['rotate'], my_room['power'], player_1)
            else:
                expectation(canvas, is_1_player, player_1, player_2, (name_1, name_2))
                my_room = get(f'{url}/api/update_room/{room_id}').json()
                to_hit(canvas, my_room['rotate'], my_room['power'], player_1)
        else:
            if not is_1_player:
                choice_of_direction(canvas, (player_1, player_2), is_1_player, (name_1, name_2))
                my_room = get(f'{url}/api/update_room/{room_id}').json()
                to_hit(canvas, my_room['rotate'], my_room['power'], player_2)
            else:
                expectation(canvas, is_1_player, player_1, player_2, (name_1, name_2))
                my_room = get(f'{url}/api/update_room/{room_id}').json()
                to_hit(canvas, my_room['rotate'], my_room['power'], player_2)

        canvas.update()
        dt = time.time() - timer
        dt = (1 / 120) - dt
        if dt > 0:
            time.sleep(dt)
        #print(1 / (time.time() - timer))
        timer = time.time()


def expectation(canvas, is_1_player, player_1, player_2, names):
    if is_1_player:
        bg_left = Object(0, 0, 200, 800, 'blue_pale.png', canvas)
        bg_right = Object(1000, 0, 200, 800, 'red.png', canvas)
    else:
        bg_left = Object(0, 0, 200, 800, 'blue.png', canvas)
        bg_right = Object(1000, 0, 200, 800, 'red_pale.png', canvas)

    name_1, name_2 = names
    player_1.reshow()
    player_2.reshow()
    name_1.reshow()
    name_2.reshow()
    time.sleep(0.2)
    while running:
        my_room = get(f'{url}/api/update_room/{room_id}').json()
        if my_room['is_turn_ended']:
            bg_left.hide()
            bg_right.hide()
            del bg_left
            del bg_right
            return

        canvas.update()


def choice_of_direction(canvas, players, is_1_player, names):
    global type_menu, is_ended, pointer
    player_1, player_2 = players
    type_menu = 'game_1'
    is_ended = False
    if is_1_player:
        pointer = Object(player_1.x, player_1.y, 150, 150, 'painter.png', canvas, False, mode_coord=True)
        bg_left = Object(0, 0, 200, 800, 'blue.png', canvas)
        bg_right = Object(1000, 0, 200, 800, 'red_pale.png', canvas)
    else:
        pointer = Object(player_2.x, player_2.y, 150, 150, 'painter.png', canvas, False, mode_coord=True)
        bg_left = Object(0, 0, 200, 800, 'blue_pale.png', canvas)
        bg_right = Object(1000, 0, 200, 800, 'red.png', canvas)

    name_1, name_2 = names
    player_1.reshow()
    player_2.reshow()
    name_1.reshow()
    name_2.reshow()

    rez = put(f'{url}/api/start_hit/{room_id}').json()
    tap_1 = Object(0, 0, 40, 40, 'grey_circle.png', canvas, False, mode_coord=True)
    tap_2 = Object(0, 0, 40, 40, 'grey_circle.png', canvas, False, mode_coord=True)
    pointer_mous = None
    pointer_mous_2 = None
    power = 0
    rotate = 0
    while running:
        if is_click:
            if not tap_1.visibility:
                tap_1.show()
                tap_2.show()
                pointer_mous = canvas.create_oval(old_mous_x - 175, old_mous_y - 175, old_mous_x + 175, old_mous_y + 175, outline="gray", width=3)
                tap_1.go_to(mous_x, mous_y)

            tap_2.go_to(mous_x, mous_y)
            power = int((abs(old_mous_x - mous_x) ** 2 + abs(old_mous_y - mous_y) ** 2) ** 0.5)

            print(rotate)

            if power >= 175:
                power = 174

            if power > 0:
                try:
                    if old_mous_y - mous_y >= 0 and old_mous_x - mous_x >= 0:
                        rotate = math.atan((old_mous_y - mous_y) / (old_mous_x - mous_x)) * 180 / math.pi
                        rotate = rotate * -1 - 90
                    elif old_mous_y - mous_y >= 0 and old_mous_x - mous_x < 0:
                        rotate = math.atan((old_mous_y - mous_y) / (old_mous_x - mous_x)) * 180 / math.pi
                        rotate = rotate * -1 + 90
                    elif old_mous_y - mous_y <= 0 and old_mous_x - mous_x < 0:
                        rotate = math.atan((old_mous_y - mous_y) / (old_mous_x - mous_x)) * 180 / math.pi
                        rotate = rotate * -1 + 90
                    else:
                        rotate = math.atan((old_mous_y - mous_y) / (old_mous_x - mous_x)) * 180 / math.pi
                        rotate = rotate * -1 - 90
                except Exception:
                    pass

                canvas.delete(pointer_mous_2)
                pointer_mous_2 = canvas.create_oval(old_mous_x - power, old_mous_y - power, old_mous_x + power, old_mous_y + power, outline="gray", width=3)


                pointer.change_img('painter.png', int(power * 1.6), int(power * 1.6))
                pointer.rotation(rotate)


        if is_ended:
            pointer.hide()
            tap_1.hide()
            tap_2.hide()
            canvas.delete(pointer_mous)
            del pointer_mous
            canvas.delete(pointer_mous_2)
            del pointer_mous_2
            break
        canvas.update()

    rez = put(f'{url}/api/create_hit/{room_id}', json={
        'rotate': rotate,
        'power': power / 100}).json()
    bg_left.hide()
    bg_right.hide()
    del bg_left
    del bg_right


def to_hit(canvas, rotate, power, moving_player):
    speed = power * 25

    # hole, grass, walls
    while speed > 1 and running:
        player_x = moving_player.x
        player_y = moving_player.y
        speed_ = speed / speed
        for _ in range(int(speed)):
            d_x = math.sin(rotate * (math.pi / 180)) * speed_
            d_y = math.cos(rotate * (math.pi / 180)) * speed_
            player_x += d_x
            player_y += d_y

            if hole.check_point(player_x, player_y):
                wright_winner(canvas, moving_player, hole, grass, walls)

            for object in walls.all_objects:
                if object.check_point(player_x, player_y):
                    rotate = object.get_rotation(rotate)
                    print('rotate:', rotate)
                    print('-----')

                    j = 0
                    while object.check_point(player_x, player_y, 5):
                        j += 1
                        d_x = math.sin(rotate * (math.pi / 180)) * speed_
                        d_y = math.cos(rotate * (math.pi / 180)) * speed_
                        player_x += d_x
                        player_y += d_y
                        if j % 2 == 0:
                            moving_player.go_to(int(player_x), int(player_y))
                            canvas.update()


        moving_player.go_to(int(player_x), int(player_y))
        call = all_map.get_call(int(player_x), int(player_y))
        if call:
            speed += call.d_speed
        time.sleep(0.0366)
        canvas.update()


def wright_winner(canvas, moving_player, hole, grass, walls):
    global type_menu

    if moving_player is player_1:
        text = Text(550, 300, 'Победил синий!', canvas)
    else:
        text = Text(550, 300, 'Победил красный!', canvas)

    hole.hide()
    grass.hide_all()
    walls.hide_all()

    type_menu = 'wright_winner'
    while running:
        canvas.update()
        if is_click:
            text.hide()


