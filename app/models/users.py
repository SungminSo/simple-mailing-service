from datetime import datetime
#
from sqlalchemy.exc import OperationalError
#
from . import db

import uuid

USERS_PER_PAGE = 10


class User(db.Model):
    __table_name__ = "user"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    uuid = db.Column(db.String(128), unique=True, nullable=True)
    name = db.Column(db.String(32), nullable=False)
    email = db.Column(db.String(128), unique=True, nullable=False)
    created_at = db.Column(db.DateTime, nullable=False)
    updated_at = db.Column(db.DateTime, nullable=False)

    def __init__(self, name: str, email: str):
        self.uuid = str(uuid.uuid4())
        self.name = name
        self.email = email
        self.created_at = datetime.utcnow()
        self.updated_at = datetime.utcnow()

    def __repr__(self) -> str:
        return f"<user name: {self.name}, email: {self.email}"

    def create(self) -> str:
        db.session.add(self)
        return self.uuid

    def update(self, new_name: str, new_email: str):
        if self.name != new_name:
            setattr(self, 'name', new_name)
        if self.email != new_email:
            setattr(self, 'email', new_email)
        self.updated_at = datetime.utcnow()
        return self.uuid

    def delete(self):
        db.session.delete(self)

    @staticmethod
    def get_all_users(page: int) -> list:
        try:
            users_list = User.query.order_by(User.id.desc()).paginate(page, per_page=USERS_PER_PAGE)
        except OperationalError:
            users_list = None

        return users_list

    @staticmethod
    def get_user_by_email(email: str):
        return User.query.filter_by(email=email).first()
