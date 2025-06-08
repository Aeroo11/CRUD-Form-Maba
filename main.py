from fastapi import FastAPI, Request, Form
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from sqlalchemy.orm import Session

from database import SessionLocal, engine
from models import Base, Mahasiswa

app = FastAPI()

templates = Jinja2Templates(directory="templates")  # Ini WAJIB
Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/", response_class=HTMLResponse)
def index(request: Request):
    db = next(get_db())
    mahasiswa = db.query(Mahasiswa).all()
    return templates.TemplateResponse("index.html", {"request": request, "mahasiswa": mahasiswa, "form_mode": "create"})

@app.post("/create")
def create(nama: str = Form(...), email: str = Form(...), jurusan: str = Form(...)):
    db = next(get_db())
    mhs = Mahasiswa(nama=nama, email=email, jurusan=jurusan)
    db.add(mhs)
    db.commit()
    return RedirectResponse("/", status_code=303)

@app.get("/edit/{id}")
def form_edit(request: Request, id: int):
    db = next(get_db())
    mhs = db.query(Mahasiswa).filter(Mahasiswa.id == id).first()
    mahasiswa = db.query(Mahasiswa).all()
    return templates.TemplateResponse("index.html", {"request": request, "mahasiswa": mahasiswa, "mhs": mhs, "form_mode": "edit"})

@app.post("/edit/{id}")
def update(id: int, nama: str = Form(...), email: str = Form(...), jurusan: str = Form(...)):
    db = next(get_db())
    mhs = db.query(Mahasiswa).filter(Mahasiswa.id == id).first()
    mhs.nama = nama
    mhs.email = email
    mhs.jurusan = jurusan
    db.commit()
    return RedirectResponse("/", status_code=303)

@app.get("/delete/{id}")
def delete(id: int):
    db = next(get_db())
    mhs = db.query(Mahasiswa).filter(Mahasiswa.id == id).first()
    db.delete(mhs)
    db.commit()
    return RedirectResponse("/", status_code=303)
