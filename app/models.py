import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import Column, Integer, String, DateTime, func

POSTGRES_PASSWORD = os.getenv('POSTGRES_PASSWORD', '1234')
POSTGRES_USER = os.getenv('POSTGRES_USER', 'app')
POSTGRES_DB = os.getenv('POSTGRES_DB', 'netology')
POSTGRES_PORT = os.getenv('POSTGRES_PORT', '5431')
POSTGRES_HOST = os.getenv('POSTGRES_HOST', '127.0.0.1')


PG_DSN = f'postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}'

engine = create_engine(PG_DSN)
Session = sessionmaker(bind=engine)


class Base(DeclarativeBase):
    pass


class Notice(Base):
    __tablename__ = 'notices'

    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False, unique=True)
    text = Column(String, nullable=False)
    created_at = Column(DateTime, server_default=func.now())
    owner_name = Column(String(100), nullable=False)

    @property
    def dict(self):
        return {
            'id': self.id,
            'name': self.owner_name,
            'created_at': self.created_at.isoformat()
        }


Base.metadata.create_all(engine)
