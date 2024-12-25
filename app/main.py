# app/main.py
from fastapi import FastAPI, HTTPException, Depends, Query
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session
from typing import List, Optional
from . import models, schemas
from .database import SessionLocal, engine

# Создаем таблицы в базе данных
models.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Глоссарий терминов ВКР",
    description="API для управления глоссарием терминов",
    version="1.0.0"
)

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/", tags=["root"])
async def root():
    """
    Перенаправление на документацию API
    """
    return RedirectResponse(url="/docs")

@app.get("/api/health", tags=["health"])
async def health_check():
    """
    Проверка работоспособности API
    """
    return {"status": "healthy", "message": "API работает нормально"}

@app.get("/terms/", response_model=List[schemas.Term], tags=["terms"])
def get_terms(
    skip: int = Query(0, description="Количество пропускаемых записей"),
    limit: int = Query(100, description="Максимальное количество возвращаемых записей"),
    search: Optional[str] = Query(None, description="Поиск по термину"),
    db: Session = Depends(get_db)
):
    """
    Получение списка всех терминов с возможностью пагинации и поиска.
    """
    query = db.query(models.Term)
    if search:
        query = query.filter(models.Term.term.ilike(f"%{search}%"))
    return query.offset(skip).limit(limit).all()

@app.get("/terms/{term_id}", response_model=schemas.Term, tags=["terms"])
def get_term(term_id: int, db: Session = Depends(get_db)):
    """
    Получение информации о конкретном термине по его ID.
    """
    term = db.query(models.Term).filter(models.Term.id == term_id).first()
    if term is None:
        raise HTTPException(status_code=404, detail="Термин не найден")
    return term

@app.post("/terms/", response_model=schemas.Term, tags=["terms"])
def create_term(term: schemas.TermCreate, db: Session = Depends(get_db)):
    """
    Создание нового термина в глоссарии.
    """
    db_term = db.query(models.Term).filter(models.Term.term == term.term).first()
    if db_term:
        raise HTTPException(status_code=400, detail="Термин уже существует")
    db_term = models.Term(**term.dict())
    db.add(db_term)
    db.commit()
    db.refresh(db_term)
    return db_term

@app.put("/terms/{term_id}", response_model=schemas.Term, tags=["terms"])
def update_term(term_id: int, term: schemas.TermUpdate, db: Session = Depends(get_db)):
    """
    Обновление существующего термина по его ID.
    """
    db_term = db.query(models.Term).filter(models.Term.id == term_id).first()
    if db_term is None:
        raise HTTPException(status_code=404, detail="Термин не найден")
    
    term_data = term.dict(exclude_unset=True)
    for key, value in term_data.items():
        setattr(db_term, key, value)
    
    db.commit()
    db.refresh(db_term)
    return db_term

@app.delete("/terms/{term_id}", tags=["terms"])
def delete_term(term_id: int, db: Session = Depends(get_db)):
    """
    Удаление термина по его ID.
    """
    db_term = db.query(models.Term).filter(models.Term.id == term_id).first()
    if db_term is None:
        raise HTTPException(status_code=404, detail="Термин не найден")
    
    db.delete(db_term)
    db.commit()
    return {"message": "Термин успешно удален"}