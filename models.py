from sqlalchemy import Column, Integer, String
from database import Base

class Mahasiswa(Base):
    __tablename__ = "mahasiswa"

    id = Column(Integer, primary_key=True, index=True)
    nama = Column(String, nullable=False)
    email = Column(String, nullable=False, unique=True)
    jurusan = Column(String, nullable=False)
