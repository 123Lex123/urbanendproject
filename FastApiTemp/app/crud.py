from sqlalchemy.orm import Session
from models import Poll, Option
from schemas import PollCreate

def create_poll(db: Session, poll: PollCreate):
    db_poll = Poll(question=poll.question)
    db.add(db_poll)
    db.commit()
    db.refresh(db_poll)

    for option in poll.options:
        db_option = Option(text=option.text, poll_id=db_poll.id)
        db.add(db_option)
        db.commit()
        db.refresh(db_option)

    return db_poll

def get_poll(db: Session, poll_id: int):
    return db.query(Poll).filter(Poll.id == poll_id).first()

def get_polls(db: Session):
    return db.query(Poll).all()

def vote_option(db: Session, option_id: int):
    option = db.query(Option).filter(Option.id == option_id).first()
    if option:
        option.votes += 1
        db.commit()
        db.refresh(option)
    return option
