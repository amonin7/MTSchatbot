from abc import ABC, abstractmethod
from sqlalchemy import Column, Integer, String, ForeignKey, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from random import randint
import datetime


class IDataService(ABC):

    @abstractmethod
    def save_message(self, client_message, bot_answer, client_id):
        pass

    @abstractmethod
    def get_history(self, client_id):
        pass


class TextDataService(IDataService):

    def __init__(self, text_file_path=None):
        self.text_file_path = text_file_path or "tmp.txt"

    def save_message(self, client_message, bot_answer, client_id):
        saved_message = "{0}\t{1}\t{2}\t{3}\t\n".format(client_id, datetime.datetime.now(), client_message, bot_answer)
        with open(self.text_file_path, "at") as f:
            f.write(saved_message)

    def get_history(self, client_id):
        with open(self.text_file_path, "rt") as f:
            all_messages = [l.split("\t")[:-1] for l in f.readlines()]

        client_messages = list(filter(lambda x: str(client_id) in x[0], all_messages))
        sorted_client_messages = sorted(client_messages, key=lambda x: x[1])
        return [(client_message, bot_answer) for _, _, client_message, bot_answer in sorted_client_messages]

class DBDataService(IDataService):

    Base = declarative_base()
    engine = create_engine('sqlite:///messageHistory.db', echo=True)
    Base.metadata.create_all(bind=engine)
    Session = sessionmaker(bind=engine)
    session = Session()

    class User(Base):
        __tablename__ = "MessageHistory"

        id = Column('id', Integer, primary_key=True)
        username = Column('username', String, unique=True)
        messageHistory = Column('messageHistory', String)

    def get_history(self, client_id):
        user = self.session.query(self.User).filter(self.User.id == client_id)
        if (user.count() > 0):
            return user[0].messageHistory
        else:
            newUserId = randint(1000000, 1000000000)
            while (self.session.query(self.User).filter(self.User.id == newUserId).count() > 0):
                newUserId = randint(1000000, 1000000000)
            self.add_user(newUserId, "username" + str(newUserId))
            return ""

    def add_user(self, id, username):
        user = self.User()
        user.id = id
        user.username = username
        user.messageHistory = "noMessagesYet"
        self.session.add(user)
        self.session.commit()
        self.session.close()

    def add_user_withoutID(self, username):
        newUserId = randint(1000000, 1000000000)
        while (self.session.query(self.User).filter(self.User.id == newUserId).count() > 0):
            newUserId = randint(1000000, 1000000000)
        user = self.User()
        user.id = newUserId
        user.username = username
        user.messageHistory = "noMessagesYet"
        self.session.add(user)
        self.session.commit()
        self.session.close()
        return newUserId

    def save_message(self, client_message, bot_answer, client_id):
        user = self.session.query(self.User).filter(self.User.id == client_id)

        user[0].messageHistory = user[0].messageHistory + ' ' + client_message + ' ' + bot_answer

        self.session.commit()
        self.session.close()

    def del_history(self, client_id):
        user = self.session.query(self.User).filter(self.User.id == client_id)
        user[0].messageHistory = ""
        self.session.commit()
        self.session.close()

    def find_usr(self, username):
        user = self.session.query(self.User).filter(self.User.username == username)
        if (user.count() > 0):
            return user[0].id
        else:
            id = self.add_user_withoutID(username)
            return id
