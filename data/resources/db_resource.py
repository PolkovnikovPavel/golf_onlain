from flask_restful import abort, Resource, reqparse
from flask import jsonify
from data import db_session
from data.users import User
from data.room import Rooms


list_of_parameters_users = ['name', 'surname', 'age', 'id', 'is_varfarin',
                            'email', 'modified_date']


parser_do_hit = reqparse.RequestParser()
parser_do_hit.add_argument('rotate', required=True, type=float)
parser_do_hit.add_argument('power', required=True, type=float)

parser_join_to_room = reqparse.RequestParser()
parser_join_to_room.add_argument('user_id', required=True, type=int)
parser_join_to_room.add_argument('room_id', required=True, type=int)

parser_change = reqparse.RequestParser()
parser_change.add_argument('surname', required=False)
parser_change.add_argument('name', required=False)
parser_change.add_argument('age', required=False, type=int)
parser_change.add_argument('password', required=True)
parser_change.add_argument('is_varfarin', required=False)

parser_room = reqparse.RequestParser()
parser_room.add_argument('user_1', required=True)
parser_room.add_argument('x_1', required=True, type=int)
parser_room.add_argument('y_1', required=True, type=int)
parser_room.add_argument('x_2', required=True, type=int)
parser_room.add_argument('y_2', required=True, type=int)
parser_room.add_argument('map', required=True, type=int)
parser_room.add_argument('rotate', required=True, type=int)
parser_room.add_argument('power', required=True, type=int)
parser_room.add_argument('is_turn_ended', required=True, type=bool)
parser_room.add_argument('is_turn_player_1', required=True, type=bool)
parser_room.add_argument('is_first_turn_player_1', required=True, type=bool)


class RoomMoveResource(Resource):
    def put(self, room_id, x, y, is_1_player):
        session = db_session.create_session()
        room = session.query(Rooms).filter(Rooms.id == room_id).first()
        if room:
            if is_1_player:
                room.x_1 = x
                room.y_1 = y
            else:
                room.x_2 = x
                room.y_2 = y
            session.commit()
            return jsonify({'success': 'OK'})
        else:
            abort(404, message=f"incorrect id_room")



class RoomUpdateResource(Resource):
    def get(self, room_id):
        session = db_session.create_session()
        room = session.query(Rooms).filter(Rooms.id == room_id).first()
        if room:
            return jsonify({'x_1': room.x_1,
                            'y_1': room.y_1,
                            'x_2': room.x_2,
                            'y_2': room.y_2,
                            'rotate': room.rotate,
                            'power': room.power,
                            'is_turn_ended': room.is_turn_ended,
                            'is_turn_player_1': room.is_turn_player_1,
                            'is_first_turn_player_1': room.is_first_turn_player_1,
                            'user_1': room.user_1,
                            'user_2': room.user_2,
                            'map': room.map})
        else:
            abort(404, message=f"incorrect id_room")


class RoomGetOneResource(Resource):
    def get(self, room_id):
        session = db_session.create_session()
        room = session.query(Rooms).filter(Rooms.id == room_id).first()
        if room:
            return jsonify({'users': (room.user_1, room.user_2)})
        else:
            abort(404, message=f"incorrect id_room")


class RoomGetFreeResource(Resource):
    def get(self):
        session = db_session.create_session()
        room = session.query(Rooms).filter(Rooms.user_2 == -1).first()
        if room:
            return jsonify({'room_id': room.id})
        else:
            return jsonify({'room_id': -1})


class RoomCreateResource(Resource):
    def post(self):
        session = db_session.create_session()
        args = parser_room.parse_args()

        room = Rooms(
            user_1 = args['user_1'],
            x_1 = args['x_1'],
            y_1 = args['y_1'],
            x_2 = args['x_2'],
            y_2 = args['y_2'],
            map = args['map'],
            rotate = args['rotate'],
            power = args['power'],
            is_turn_ended = args['is_turn_ended'],
            is_turn_player_1 = args['is_turn_player_1'],
            is_first_turn_player_1 = args['is_first_turn_player_1']
        )
        session.add(room)
        session.commit()
        return jsonify({'success': 'OK', 'room_id': room.id})

    def put(self):
        session = db_session.create_session()
        args = parser_join_to_room.parse_args()

        room = session.query(Rooms).filter(Rooms.id == args['room_id']).first()
        if room:
            room.user_2 = args['user_id']
            session.commit()
            return jsonify({'success': 'OK', 'room_id': room.id})
        else:
            abort(404, message=f"incorrect id_room or id_user")


class UsersResource(Resource):
    def get(self, user_id):   # получить один
        abort_if_user_not_found(user_id)
        session = db_session.create_session()
        user = session.query(User).get(user_id)
        return jsonify({'user': user.to_dict(only=(list_of_parameters_users))})

    def put(self, user_id):   # изменить, нужен пароль
        args = parser_change.parse_args()
        if not check_password(user_id, args['password']):
            abort(404, message=f"incorrect password")

        session = db_session.create_session()
        user = session.query(User).get(user_id)

        if args['surname']:
            user.surname = args['surname']
        if args['name']:
            user.surname = args['name']
        if args['age']:
            user.surname = args['age']
        if args['is_varfarin']:
            user.surname = args['is_varfarin']

        session.commit()
        return jsonify({'success': 'OK'})

    def delete(self, user_id):   # удалить
        session = db_session.create_session()
        user = session.query(User).get(user_id)
        session.delete(user)

        session.commit()
        return jsonify({'success': 'OK'})


class UsersListResource(Resource):
    def get(self):   # получить всех пользователей
        session = db_session.create_session()
        users = session.query(User).all()
        return jsonify({'users': [user.to_dict(
            only=(list_of_parameters_users)) for user in users]})

    def post(self):   # создать нового
        session = db_session.create_session()

        user = User()
        user.hashed_password = ''
        session.add(user)
        session.commit()
        return jsonify({'success': 'OK', 'user_id': user.id})


def abort_if_user_not_found(user_id):   # проверка на наличие user
    session = db_session.create_session()
    users = session.query(User).get(user_id)
    if not users:
        abort(404, message=f"User {user_id} not found")


def check_password(user_id, password):   # проверяет пароль
    session = db_session.create_session()
    user = session.query(User).get(user_id)
    if user:
        return user.check_password(password)
    abort(404, message=f"User {user_id} not found")


class RoomCreateHit(Resource):
    def put(self, room_id):
        args = parser_do_hit.parse_args()
        session = db_session.create_session()
        room = session.query(Rooms).filter(Rooms.id == room_id).first()
        if room:
            room.power = args['power']
            room.rotate = args['rotate']
            room.is_turn_ended = True
            room.is_turn_player_1 = not room.is_turn_player_1
            session.commit()
            return jsonify({'success': 'OK'})
        else:
            abort(404, message=f"incorrect id_room")


class RoomStartHit(Resource):
    def put(self, room_id):
        session = db_session.create_session()
        room = session.query(Rooms).filter(Rooms.id == room_id).first()
        if room:
            room.power = 1
            room.rotate = 0
            room.is_turn_ended = False
            session.commit()
            return jsonify({'success': 'OK'})
        else:
            abort(404, message=f"incorrect id_room")
