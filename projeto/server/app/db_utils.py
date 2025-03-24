import os
from typing import Generator

import sqlalchemy as sql
from sqlalchemy.orm import Session
from sqlalchemy_utils import create_database, database_exists

from .base_model import Base
from .db_models import Contact

# 'mysql+pymysql://root:next@localhost:3307/projeto_next'
DATABASE_URL = os.environ.get('DB_URL')


def _get_db_engine(url: str) -> sql.Engine:
    engine = sql.create_engine(url)

    if not database_exists(engine.url):
        create_database(engine.url)

    return engine


def _init_db(url: str) -> Generator[Session, None, None]:
    engine = _get_db_engine(url)

    Base.metadata.create_all(engine)

    while True:
        with Session(engine) as db_session:
            yield db_session


_db_session_generator = _init_db(DATABASE_URL)


def get_db_session() -> Session:
    return next(_db_session_generator)


def get_all_contacts(db_session: Session) -> list[Contact]:
    contacts = db_session.scalars(sql.select(Contact)).all()
    return list(contacts)


def add_new_contact(db_session: Session, name: str, email: str, phone: str) -> Contact:
    new_contact = Contact(
        name=name,
        phone=phone,
        email=email,
    )

    db_session.add(new_contact)
    db_session.commit()

    return new_contact


def delete_contact(db_session: Session, contact_id: int) -> None:
    delete_contact_sql = sql.delete(Contact).where(Contact.id == contact_id)
    result = db_session.execute(delete_contact_sql)
    db_session.commit()

    if result.rowcount == 0:
        raise KeyError(f'Contato com id {contact_id} não encontrado!')


# if __name__ == '__main__':
#     db_session = get_db_session()
#     # users = list_users(db_session)
#     # print(users)
#     add_new_user(db_session, username='jloc2', password='abc123', email='jloc@next')
#     db_session = get_db_session()
#     new_user = User(username='jloc3', password='kkk789', email='jloc3@next.cesarschool')
#     update_user(db_session, user_id=4, new_user=new_user)
#     # delete_user(db_session, 2)
