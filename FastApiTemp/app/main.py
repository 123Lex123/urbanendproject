from fastapi import FastAPI, Depends, HTTPException, Request, Form
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, RedirectResponse
from sqlalchemy.orm import Session
from database import SessionLocal, engine
from models import Base
from schemas import PollCreate, Poll
from crud import create_poll, get_poll, vote_option, get_polls  # Импортируем функцию get_polls

# Создаем все таблицы в базе данных
Base.metadata.create_all(bind=engine)

app = FastAPI()
templates = Jinja2Templates(directory="templates")

# Dependency для получения сессии базы данных
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Маршрут для отображения всех опросов на главной странице
@app.get("/", response_class=HTMLResponse)
def read_all_polls(request: Request, db: Session = Depends(get_db)):
    polls = get_polls(db=db)
    return templates.TemplateResponse("index.html", {"request": request, "polls": polls})

# Маршрут для создания нового опроса
@app.post("/polls/", response_model=Poll)
def create_new_poll(poll: PollCreate, db: Session = Depends(get_db)):
    return create_poll(db=db, poll=poll)

# Маршрут для отображения формы опроса
@app.get("/polls/{poll_id}/", response_class=HTMLResponse)
def show_poll_form(poll_id: int, request: Request, db: Session = Depends(get_db)):
    poll = get_poll(db=db, poll_id=poll_id)
    if not poll:
        raise HTTPException(status_code=404, detail="Poll not found")
    return templates.TemplateResponse("poll_form.html", {"request": request, "poll": poll})

# Маршрут для обработки голосования
@app.post("/polls/{poll_id}/", response_class=HTMLResponse)
def submit_vote(poll_id: int, option: int = Form(...), db: Session = Depends(get_db)):
    option_record = vote_option(db=db, option_id=option)
    if not option_record:
        raise HTTPException(status_code=404, detail="Option not found")
    return RedirectResponse(url=f"/polls/{poll_id}/", status_code=303)
