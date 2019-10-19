import sqlalchemy as sa
import sqlalchemy.orm as orm
from sqlalchemy.orm import Session

from data.modelbase import SqlAlchemyBase

__factory = None

def notasi_engine():
    conn_str = 'postgresql://notasi:notasi@localhost/notasi'

    engine = sa.create_engine(conn_str, echo=False, pool_size=20, max_overflow=40)
    return engine

def global_init():
    global __factory

    if __factory:
        return
    engine = notasi_engine()
    __factory = orm.sessionmaker(bind=notasi_engine())

    # noinspection PyUnresolvedReferences
    import data.source

    SqlAlchemyBase.metadata.create_all(engine)


def create_session() -> Session:
    global __factory
    return __factory()