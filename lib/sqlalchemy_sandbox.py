#!/usr/bin/env python3

from datetime import datetime

from sqlalchemy import (create_engine, desc, func,
    CheckConstraint, PrimaryKeyConstraint, UniqueConstraint,
    Index, Column, DateTime, Integer, String)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()

class Student(Base):
    __tablename__ = 'students'
    __table_args__ = (
        PrimaryKeyConstraint(
            'id',
            name = 'id_pk'
        ),
        UniqueConstraint(
            'email',
            name= 'unique_email'
        ),
        CheckConstraint(
            'grade BETWEEN 1 AND 12',
            name = 'grade_between_1_and_12'
        )
    )
    Index('index_name', 'name' )
    id = Column(Integer(), primary_key=True)
    name = Column(String())
    email = Column(String(55))
    grade = Column(Integer())
    birthday = Column(DateTime())
    enrolled_date = Column(DateTime(), default = datetime.now())

if __name__ == '__main__':
    engine = create_engine('sqlite:///:memory:')
    Base.metadata.create_all(engine)

    # we use the engine to configure a sessions class
    Session = sessionmaker(bind=engine)
    # and we use the session class to configure a session engine.
    session = Session()

    albert_einstein = Student (
        name = 'Albert Einstein',
        email = 'albert.einstain@zurich.edu',
        grade = 6,
        birthday = datetime(
            year = 1953,
            month= 3,
            day = 14
        ),
    )

    caroline_wanjiru = Student(
        name = 'caroline wanjiru',
        email = 'caroline.wanjiru@moringaschool',
        grade = 9,
        birthday = datetime(
            year = 2002,
            month = 7,
            day = 10
        ),
    )
    session.bulk_save_objects([albert_einstein, caroline_wanjiru])
    session.commit()

    students = session.query(Student) # this query method is used to retrieve data against your databse using more pythonic interface.
    grade = [grade for grade in session.query(caroline_wanjiru.grade)]

    student_by_grade_desc = [student for student in session.query(Student.name, Student.grade).order_by(desc(Student.grade))]
    print(f'New student ID is {albert_einstein.id}.')
    print(f'The new stundets name is {caroline_wanjiru.name}')
    print(grade)
    print(student_by_grade_desc)
