from datetime import datetime

import sqlalchemy as sql
from sqlalchemy.orm import Mapped, Session, mapped_column, registry
from sqlalchemy_utils import create_database, database_exists


def get_engine(url: str) -> sql.Engine:
    engine = sql.create_engine(url)

    if not database_exists(engine.url):
        create_database(engine.url)

    return engine


table_registry = registry()


@table_registry.mapped_as_dataclass
class User:
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(init=False, primary_key=True)
    username: Mapped[str] = mapped_column(unique=True)
    password: Mapped[str]
    email: Mapped[str] = mapped_column(unique=True)
    created_at: Mapped[datetime] = mapped_column(init=False, server_default=sql.func.now())


def user_exists(session: Session, username: str, email: str) -> bool:
    existing_user = session.scalar(
        sql.select(User).where((User.username == username) | (User.email == email))
    )

    return existing_user is not None


def add_new_user(session: Session, username: str, password: str, email: str) -> None:
    if user_exists(session, username, email):
        print('Nome de usuário ou e-mail já cadastrado!')
        return

    new_user = User(
        username=username,
        password=password,
        email=email,
    )

    session.add(new_user)
    session.commit()


if __name__ == '__main__':
    url = 'postgresql+psycopg2://postgres:next@localhost:5432/next2025'
    engine = get_engine(url)

    table_registry.metadata.create_all(engine)

    with Session(engine) as session:
        add_new_user(session, username='jloc2', password='abc123', email='jloc2@next.cesarschool')

        users = session.scalars(sql.select(User)).all()

        print('\nLista de Usuários:')
        for user in users:
            print(user)
