from sqlalchemy import *
from sqlalchemy.exc import PendingRollbackError, SQLAlchemyError
from sqlalchemy.orm import *
from psycopg2.errors import Error

Base = declarative_base()


class DatabaseManager:
    engine = None
    session = None

    def __init__(self):
        self.engine = create_engine("postgresql+psycopg2://zxcasdQWE123:zxcasdQWE123@localhost:5432/postgres")
        Base.metadata.create_all(self.engine)
        _session = sessionmaker(bind=self.engine)
        self.session = _session()

    def save(self, obj):
        try:
            self.session.add(obj)
            self.session.commit()
            return True
        except PendingRollbackError:
            self.session.rollback()
            self.save(obj)
        except SQLAlchemyError as e:
            print(e)
            self.session.rollback()
            return False
        self.session.rollback()
        return False

    def delete(self, obj):
        try:
            self.session.delete(obj)
            self.session.commit()
            return True
        except PendingRollbackError:
            self.session.rollback()
            self.save(obj)
        except SQLAlchemyError:
            self.session.rollback()
            return False
        except Exception as e:
            print(e)  # TODO: Logging
        self.session.rollback()
        return False

    def get(self, obj, predicate):
        return self.session.query(obj).filter(predicate).first()

    def get_with_related(self, obj, predicate):
        return self.session.query(obj).options(joinedload(obj.__dict__)).filter(predicate).first()

    def get_all(self, obj):
        return self.session.query(obj).all()

    def get_all_with_related(self, obj):
        return self.session.query(obj).options(joinedload(obj.__dict__)).all()
