import sqlalchemy

from .db_session import SqlAlchemyBase
from sqlalchemy_serializer import SerializerMixin


class Rooms(SqlAlchemyBase, SerializerMixin):
    __tablename__ = 'rooms'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    user_1 = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("users.id"))
    user_2 = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("users.id"), default=-1)
    x_1 = sqlalchemy.Column(sqlalchemy.Integer)
    y_1 = sqlalchemy.Column(sqlalchemy.Integer)
    x_2 = sqlalchemy.Column(sqlalchemy.Integer)
    y_2 = sqlalchemy.Column(sqlalchemy.Integer)
    map = sqlalchemy.Column(sqlalchemy.Integer)

    rotate = sqlalchemy.Column(sqlalchemy.Float)
    power = sqlalchemy.Column(sqlalchemy.Float)

    is_turn_ended = sqlalchemy.Column(sqlalchemy.Boolean)
    is_turn_player_1 = sqlalchemy.Column(sqlalchemy.Boolean)
    is_first_turn_player_1 = sqlalchemy.Column(sqlalchemy.Boolean)
    is_room_closed = sqlalchemy.Column(sqlalchemy.Boolean, default=False)
