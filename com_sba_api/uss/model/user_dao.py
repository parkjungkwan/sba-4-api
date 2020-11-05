from com_sba_api.uia.model.user_dto import UserDto
from typing import List
from flask import request
from flask_restful import Resource, reqparse
from sklearn.ensemble import RandomForestClassifier # rforest
from sklearn.tree import DecisionTreeClassifier # dtree
from sklearn.ensemble import RandomForestClassifier # rforest
from sklearn.naive_bayes import GaussianNB # nb
from sklearn.neighbors import KNeighborsClassifier # knn
from sklearn.svm import SVC # svm
from sklearn.model_selection import train_test_split
from sklearn.model_selection import KFold  # k value is understood as count
from sklearn.model_selection import cross_val_score
from sqlalchemy import func
from pathlib import Path
from sqlalchemy import and_, or_
from com_sba_api.util.file import FileReader
from flask import jsonify
from com_sba_api.ext.db import db, openSession
import pandas as pd
import json
import os
import pandas as pd
import numpy as np

Session = openSession()
session = Session()

class UserDao(UserDto):
    
    @classmethod
    def bulk(cls, user_dfo):
        dfo = user_dfo.create()
        print(dfo.head())
        session.bulk_insert_mappings(cls, dfo.to_dict(orient="records"))
        session.commit()
        session.close()

    @staticmethod
    def save(user):
        session.add(user)
        session.commit()

    @classmethod
    def update(cls, user):
        session.query(cls).filter(cls.user_id == user['userId'])\
            .update({cls.password:user['password'],\
                cls.pclass:user['pclass'],\
                cls.embarked:user['embarked']})                                                        
        session.commit()

    @classmethod
    def delete(cls,user_id):
        data = cls.query.get(user_id)
        db.session.delete(data)
        db.session.commit()

    @classmethod
    def count(cls):
        return session.query(func.count(cls.user_id)).one()

    @classmethod
    def find_all(cls):
        # sql = cls.query
        # df = pd.read_sql(sql.statement, sql.session.bind)
        # return json.loads(df.to_json(orient='records'))
        return session.query(cls).all()

    
    '''
    SELECT *
    FROM users
    WHERE user_name LIKE 'a'
    '''
    # like() method itself produces the LIKE criteria 
    # for WHERE clause in the SELECT expression.
    
    @classmethod
    def find_one(cls, user_id):
        return session.query(cls)\
            .filter(cls.user_id == user_id).one()
    '''
    SELECT *
    FROM users
    WHERE user_name LIKE 'name'
    '''
    # the meaning of the symbol %
    # A% ==> Apple
    # %A ==> NA
    # %A% ==> Apple, NA, BAG 
    @classmethod
    def find_by_name(cls, name):
        return session.query(cls).filter(cls.user_id.like(f'%{name}%')).all()

    '''
    SELECT *
    FROM users
    WHERE user_id IN (start, end)
    '''
    # List of users from start to end ?
    @classmethod
    def find_users_in_category(cls, start, end):
        return session.query(cls)\
                      .filter(cls.user_id.in_([start,end])).all()

    '''
    SELECT *
    FROM users
    WHERE gender LIKE 'gender' AND name LIKE 'name%'
    '''
    # Please enter this at the top. 
    # from sqlalchemy import and_
    @classmethod
    def find_users_by_gender_and_name(cls, gender, name):
        return session.query(cls)\
                      .filter(and_(cls.gender.like(gender),
                       cls.name.like(f'{name}%'))).all()

    '''
    SELECT *
    FROM users
    WHERE pclass LIKE '1' OR age_group LIKE '3'
    '''
    # Please enter this at the top. 
    # from sqlalchemy import or_
    @classmethod
    def find_users_by_gender_and_name(cls, gender, age_group):
        return session.query(cls)\
                      .filter(or_(cls.pclass.like(gender),
                       cls.age_group.like(f'{age_group}%'))).all()
    
    '''
    SELECT *
    FROM users
    WHERE user_id LIKE '1' AND password LIKE '1'
    '''
    @classmethod
    def login(cls, user):
        return session.query(cls)\
            .filter(cls.user_id == user.user_id, 
            cls.password == user.password).one()
            

