from datetime import datetime
from typing import Generator

import sqlalchemy as sql
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import DeclarativeBase, Mapped, MappedAsDataclass, Session, mapped_column
from sqlalchemy_utils import create_database, database_exists

DATABASE_URL = 'mysql+pymysql://root:next@localhost:3307/next2025'


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


class Base(DeclarativeBase, MappedAsDataclass):
    """Declarative Base class."""


class User(Base):
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(init=False, primary_key=True)
    username: Mapped[str] = mapped_column(sql.String(255), unique=True)
    password: Mapped[str] = mapped_column(sql.String(255))
    email: Mapped[str] = mapped_column(sql.String(255), unique=True)
    created_at: Mapped[datetime] = mapped_column(init=False, server_default=sql.func.now())


def user_exists(db_session: Session, username: str, email: str) -> bool:
    existing_user = db_session.scalar(
        sql.select(User).where((User.username == username) | (User.email == email))
    )

    return existing_user is not None


def add_new_user(db_session: Session, username: str, password: str, email: str) -> User:
    if user_exists(db_session, username, email):
        raise ValueError(f"Usuário '{username}' ou e-mail '{email}' já cadastrado!")

    new_user = User(
        username=username,
        password=password,
        email=email,
    )

    db_session.add(new_user)
    db_session.commit()

    return new_user


def list_users(db_session: Session) -> list[User]:
    users = db_session.scalars(sql.select(User)).all()
    return list(users)


def get_user(db_session: Session, user_id: int) -> User | None:
    return db_session.scalar(sql.select(User).where(User.id == user_id))


# Método 1: carrega o usuário na memória para poder alterá-lo ou deletá-lo

# def update_user(db_session: Session, user_id: int, new_user: User) -> None:
#     user = db_session.get(User, user_id)

#     if user is None:
#         raise KeyError(f'Usuário com id {user_id} não encontrado!')

#     user.username = new_user.username
#     user.email = new_user.email
#     user.password = new_user.password

#     db_session.commit()


# def delete_user(db_session: Session, user_id: int) -> None:
#     user = get_user(db_session, user_id)

#     if user is None:
#         raise KeyError(f'Usuário com id {user_id} não encontrado!')

#     db_session.delete(user)
#     db_session.commit()


# Método 2: mais eficiente pois executa o comando SQL direto no DB


def update_user(db_session: Session, user_id: int, new_user: User) -> None:
    try:
        update_user_sql = (
            sql.update(User)
            .where(User.id == user_id)
            .values(
                username=new_user.username,
                email=new_user.email,
                password=new_user.password,
            )
        )

        result = db_session.execute(update_user_sql)
        db_session.commit()
    except IntegrityError:
        raise ValueError(
            f"Outro usuário já possui o username '{new_user.username}' ou email '{new_user.email}'"
        )

    if result.rowcount == 0:
        raise KeyError(f'Usuário com id {user_id} não encontrado!')


def delete_user(db_session: Session, user_id: int) -> None:
    delete_user_sql = sql.delete(User).where(User.id == user_id)
    result = db_session.execute(delete_user_sql)
    db_session.commit()

    if result.rowcount == 0:
        raise KeyError(f'Usuário com id {user_id} não encontrado!')


if __name__ == '__main__':
    db_session = get_db_session()
    # users = list_users(db_session)
    # print(users)
    add_new_user(db_session, username='jloc2', password='abc123', email='jloc@next')
    db_session = get_db_session()
    new_user = User(username='jloc3', password='kkk789', email='jloc3@next.cesarschool')
    update_user(db_session, user_id=4, new_user=new_user)
    # delete_user(db_session, 2)
