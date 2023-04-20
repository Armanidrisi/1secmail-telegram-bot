from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()

class User(Base):
    __tablename__ = 'users' # set the database table name as users
    id = Column(Integer, primary_key=True)
    first_name = Column(String)
    last_name = Column(String)
    chat_id = Column(Integer)
    email = Column(String)

class UserDatabase:
  #create database connection on constructor
    def __init__(self, database_url):
        self.engine = create_engine(database_url)
        self.Session = sessionmaker(bind=self.engine)

     # function for insert data
    def create_user(self, first_name, last_name, chat_id, email):
        session = self.Session()
        user = User(first_name=first_name, last_name=last_name, chat_id=chat_id, email=email)
        session.add(user)
        session.commit()
        session.refresh(user)
        return user
    
    #function for get data
    def get_user(self, user_id):
        session = self.Session()
        user = session.query(User).filter_by(chat_id=user_id).first()
        return user

     # function for update data
    def update_user(self, user_id, new_data):
        session = self.Session()
        user = session.query(User).filter_by(chat_id=user_id).first()
        if not user:
            return False
        for key, value in new_data.items():
            setattr(user, key, value)
        session.commit()
        return True
    
    #function for get num rows by id
    def get_num_rows_by_id(self, chat_id):
        session = self.Session()
        num_rows = session.query(User).filter_by(chat_id=chat_id).count()
        return num_rows
  
  # function for get all num rows
    def get_num_rows(self):
      session=self.Session()
      num_rows=session.query(User).count()
      return num_rows
