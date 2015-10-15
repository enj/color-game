#!/usr/bin/env python
# encoding: utf-8

from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base

# An engine has a Dialect / Pool object which establish a DBAPI connection
# This could easily be switched to PostgreSQL; SQLite is just simpler to use
# Set echo to True to see the SQL that is emitted by the ORM
engine = create_engine('sqlite:///test.db', echo=False, convert_unicode=True)

# Interface for persistence operations with the database
db_session = scoped_session(sessionmaker(autocommit=False,
                                         autoflush=False,
                                         bind=engine))

# The base that all models inherit from
Base = declarative_base()
Base.query = db_session.query_property()

def init_db():
    '''Creates the tables / constraints that are defined by the models.'''
    # import all modules that define models so that
    # they will be registered properly on the metadata.
    from ..models import ColorPattern, ColorGame, ColorGuess, ColorFeedback
    Base.metadata.create_all(bind=engine)
