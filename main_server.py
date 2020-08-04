from flask import Flask, render_template, redirect, request, abort
from data import db_session
from data.users import User
from data.room import Rooms

import data.resources.db_resource as db_resource

from flask_login import LoginManager, login_user, current_user, login_required
from flask_login import logout_user
from flask_restful import abort, Api

import os
import datetime


NORM = 72.5


def get_ch_ch_date(date):   # запись даты в человеко читаемом формате
    year, month, day = date.split('-')
    return f"{day}.{month}.{year}"


def get_num_of_day(date):   # нужно для  сортировки по дате
    year, month, day = date.split('-')
    num = int(year) * 365
    num += int(month) * 30
    if int(day) == 30:   # для верных подсчётов в конце месяца
        num += 29.5
    elif int(day) == 31:
        num += 29.9
    else:
        num += int(day)
    return num


app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'
api = Api(app)

login_manager = LoginManager()
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    session = db_session.create_session()
    return session.query(User).get(user_id)


def main():
    global list_of_products, list_of_products_with_varfarin
    db_session.global_init("db/rooms.sqlite")

    """
    api.add_resource(timetable_resource.TimetablesResource,
                     '/api/timetable/<int:timetable_id>')
    api.add_resource(timetable_resource.TimetablesDuplicate,
                     '/api/timetable_duplicate/<int:timetable_id>')
    api.add_resource(timetable_resource.TimetablesListResource,
                     '/api/timetable')
    api.add_resource(users_resource.UsersResource, '/api/users/<int:user_id>')
    api.add_resource(users_resource.UsersListResource, '/api/users')
    """
    api.add_resource(db_resource.RoomCreateResource, '/api/create_room')
    api.add_resource(db_resource.RoomGetFreeResource, '/api/get_free_room')
    api.add_resource(db_resource.UsersListResource, '/api/create_new_user')
    api.add_resource(db_resource.UsersResource, '/api/delete_user/<int:user_id>')
    api.add_resource(db_resource.RoomUpdateResource, '/api/update_room/<int:room_id>')
    api.add_resource(db_resource.RoomMoveResource,
                     '/api/update_room/<int:room_id>/<int:x>/<int:y>/<int:is_1_player>')
    api.add_resource(db_resource.RoomStartHit, '/api/start_hit/<int:room_id>')
    api.add_resource(db_resource.RoomCreateHit, '/api/create_hit/<int:room_id>')



    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)


if __name__ == '__main__':
    main()   # старт
