from sqlalchemy import create_engine, Table, Column, Integer, \
    String, MetaData, ForeignKey, DateTime
from sqlalchemy.orm import mapper, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from models import *
import datetime
import hashlib
import sys


def compose_table(model_name, model_attrs, metadata):
    columns = []

    for key in model_attrs:

        if 'id' in key:
            columns.append(Column(key, Integer, primary_key=True))
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
            self.__setattr__(model.__name__.lower()+'_table', compose_table(model.__name__, model.__slots__, self.metadata))
            self.__setattr__(model.__name__.lower()+"_class", type(model.__name__.lower(), (Base, ), {"__table__":self.__getattribute__(model.__name__.lower()+'_table')}))

        self.metadata.create_all(self.db_engine)

        Session = sessionmaker(bind=self.db_engine)
        self.session = Session()

        self.session.commit()

    def create_cat(self, name, parent, desc):
        cat = self.__getattribute__('category_class')(name=name, parent=parent, description=desc)
        self.session.add(cat)
        self.session.commit()


test = WebsiteDB('sqlite:///webserver_db.db3', TrainingSite)
test.create_cat('Basic', 0, 'test_description')
