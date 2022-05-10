import sqlalchemy as db
from sqlalchemy.orm import relationship, backref
from datetime import datetime
now = datetime.now()
from .connect_db import Base

#табель учета рабочего времени
class Time_Sheet(Base):
    __tablename__ = 'time_sheets'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    date = db.Column(db.TIMESTAMP, default=datetime.timestamp(now) ) 
    work_day_count = db.Column(db.Integer)
    emploe_id  = db.Column(db.Integer, db.ForeignKey('employees.id', ondelete='CASCADE'))
   
    def __repr__(self):
        return f'{self.date}'

#Сотрудник
class Employee(Base):
    __tablename__ = 'employees'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    branch_id = db.Column(db.Integer, db.ForeignKey('branches.id', ondelete='CASCADE'))
    position_id = db.Column(db.Integer, db.ForeignKey('positions.id', ondelete='CASCADE'))
    work_shift = db.Column(db.Integer, db.ForeignKey('working_shifts.id', ondelete='CASCADE')) 
    telegram_id = db.Column(db.String(50))
    status = db.Column(db.Boolean, nullable=True )
    name = db.Column(db.String(50))
    phone = db.Column(db.String(50))
   
    def __repr__(self):
        return f'{self.name}'

#Должность
class Position(Base):
    __tablename__ = 'positions'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    position_name = db.Column(db.String(50))
    day_salary = db.Column(db.String(50))
    
    def __repr__(self):
        return f'{self.position_name}'
#Отделения
class Branch(Base):
    __tablename__ = 'branches'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    date = db.Column(db.TIMESTAMP, default=datetime.timestamp(now) )
    branch_name = db.Column(db.String(50))
    req_shifts_num = db.Column(db.String(50))
    
    def __repr__(self):
        return f'{self.branch_name}'
#рабочая смена
class Working_Shift(Base):
    __tablename__ = 'working_shifts'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    shift_name = db.Column(db.String(50))
    num_of_day = db.Column(db.String(50))
    
    def __repr__(self):
        return f'{self.name}'

