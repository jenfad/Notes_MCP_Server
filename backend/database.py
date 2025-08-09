from sqlalchemy import create_engine, Column, Integer, String, Text, ForeignKey
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy.ext.declarative import declarative_base
from typing import List

#using sqlalchemy to create a database for the notes app and use ORM to easily map python code to SQL code

#create a database engine locally
engine = create_engine('sqlite:///notes.db')
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

class Note(Base):
    __tablename__ = 'notes'
    id = Column(Integer, primary_key=True, index=True) #setup index for id and user id to be able to search for notes by id or user id
    user_id = Column(String, index=True, nullable=False)
    title = Column(String, nullable=False)
    content = Column(Text, nullable=False)

#can add a user table if needed, but not necessary for this app
#class User(Base):
#    __tablename__ = 'users'
#    id = Column(Integer, primary_key=True)
#    email = Column(String, unique=True, nullable=False)

#look for classes that inherit from Base and create the tables in the database
Base.metadata.create_all(bind=engine)

#create a session to interact with the database
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

#create a repository to add and retrieve notes from the database
class NoteRepository:

    def get_notes_by_user(user_id: str) -> List[Note]:
        db = SessionLocal()
        try:
            return db.query(Note).filter(Note.user_id == user_id).all()
        finally:
            db.close()

    def create_note(user_id: str, title: str, content: str):
        db = SessionLocal()
        try:
            note = Note(user_id=user_id, title=title, content=content)
            db.add(note)
            db.commit()
            db.refresh(note)
            return note
        finally:
            db.close()

    def delete_note(note_id: int):
        db = SessionLocal()
        try:
            note = db.query(Note).filter(Note.id == note_id).first()
            if note:
                db.delete(note)
                db.commit()
            return note
        finally:
            db.close()