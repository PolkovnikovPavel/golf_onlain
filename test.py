from requests import get, post, put, delete
import json

def get_norm_rotate(rotate):
    rotate = rotate % 360
    if rotate > 180:
        rotate = -180 - (rotate - 180)
    elif rotate < -180:
        rotate = 180 + (rotate + 180)
    return rotate

"""
x = put('http://127.0.0.1:5000/api/create_room',
           json={'user_1': 1,
                 'x_1': 0,
                 'y_1': 0,
                 'x_2': 0,
                 'y_2': 0,
                 'map': 1,
                 'rotate': 0,
                 'power': 1,
                 'is_turn_ended': True,
                 'is_turn_player_1': True,
                 'is_first_turn_player_1': True,}).json()

print(json.dumps(x, sort_keys=True, indent=4, ensure_ascii=False))
"""
print(get_norm_rotate(-320))