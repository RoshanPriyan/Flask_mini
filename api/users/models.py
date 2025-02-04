from sqlalchemy import Column, String, Integer,DateTime, ForeignKey
from sqlalchemy.orm import validates, relationship
from datetime import datetime
from config import Base
import  bcrypt


class UserModel(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String, nullable=False)
    email= Column(String, nullable=False)
    city = Column(String, nullable=False)
    hash_password = Column(String, nullable=False)
    state_id = Column(Integer, ForeignKey("states.id"), nullable=False)
    created_date = Column(DateTime, nullable=False, default=datetime.now)
    role = Column(String, nullable=False)

    state = relationship("StatesModel", back_populates="users")
    user_auth = relationship("UserAuthInfoModel", back_populates="user")

    @validates('hash_password')
    def validate_password(self, key, password):
        """Automatically hash the password before saving to the database."""
        salt = bcrypt.gensalt()
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)
        return hashed_password.decode('utf-8')


class StatesModel(Base):
    __tablename__ = "states"

    id = Column(Integer, primary_key=True, autoincrement=True)
    state_code = Column(String, nullable=False, unique=True)
    state_name = Column(String, nullable=False, unique=True)

    users = relationship("UserModel", back_populates="state")


class UserAuthInfoModel(Base):
    __tablename__ = "user_auth_info"

    id = Column(Integer, primary_key=True, autoincrement=True)
    token = Column(String(255), nullable=False)
    update_date = Column(DateTime, nullable=False, default=datetime.now)
    user_id = Column(Integer, ForeignKey("users.id", ondelete='CASCADE'), nullable=False)

    user = relationship("UserModel", back_populates="user_auth")
