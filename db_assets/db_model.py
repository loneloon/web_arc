from sqlalchemy import create_engine, Table, Column, Integer, \
    String, MetaData, ForeignKey, DateTime, Boolean
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from models import *


def compose_table(model_name, model_attrs, metadata):
    columns = []

    for key in model_attrs:

        if 'id' == key:
            columns.append(Column(key, Integer, primary_key=True))
        elif 'parent' in key:
            columns.append(Column(key, Integer, default=None))
        elif 'is_' in key:
            columns.append(Column(key, Boolean, default=True))
        elif 'date' in key:
            columns.append(Column(key, DateTime))
        elif 'fk' in key:
            columns.append(Column(key,
                                  ForeignKey(key.split("_")[0].capitalize()+".id")))
        else:
            columns.append(Column(key, String))
    return Table(model_name, metadata, *columns)


class WebsiteDB:

    def __init__(self, db_name, model_class):
        self.db_engine = create_engine(db_name, echo=False, pool_recycle=7200)

        self.metadata = MetaData()

        Base = declarative_base()

        for model in model_class.get_inner_classes():
            self.__setattr__(model.__name__.lower()+'_table',
                             compose_table(model.__name__, model.__slots__, self.metadata))

            self.__setattr__(
                model.__name__.lower()+"_class",
                type(model.__name__.lower(), (Base, ),
                     {"__table__":self.__getattribute__(model.__name__.lower()+'_table')}))

        self.metadata.create_all(self.db_engine)

        Session = sessionmaker(bind=self.db_engine)
        self.session = Session()

        self.session.commit()

    def create_object(self, model, **kwargs):
        try:
            obj = self.__getattribute__(model.__name__.lower()+'_class')(**kwargs)
            self.session.add(obj)
            self.session.commit()
            return True
        except Exception as e:
            print(e)
            return False

    def get_object(self, model, **kwargs):
        try:
            obj_model = self.__getattribute__(model.__name__.lower()+'_class')
            result = self.session.query(obj_model).filter_by(**kwargs)
            if result.count():
                return result.first()
            else:
                return None
        except Exception as e:
            print(e)
            return None

    def delete_object(self, model, **kwargs):
        try:
            result = self.get_object(model, **kwargs)
            self.session.delete(result)

            self.session.commit()
        except Exception as e:
            print(e)

