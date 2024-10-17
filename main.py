from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from database import engine, get_db
from models import *

Base.metadata.create_all(bind=engine)

app = FastAPI()

# Создание значка
@app.post("/icons/", summary="Создать новый значок")
def create_icon(name: str, price: float, db: Session = Depends(get_db)):
    # Проверяем, существует ли значок с таким именем
    icon = db.query(Icon).filter(Icon.name == name).first()
    if icon:
        raise HTTPException(status_code=400, detail="Значок с таким именем уже существует")
    
    # Создаем новый значок
    new_icon = Icon(name=name, price=price)
    db.add(new_icon)
    db.commit()
    db.refresh(new_icon)
    
    return {"message": "Значок создан успешно", "icon": {"name": new_icon.name, "price": new_icon.price}}

# Получение всех значков
@app.get("/icons/", summary="Получить список всех значков")
def get_icons(db: Session = Depends(get_db)):
    icons = db.query(Icon).all()
    return {"icons": [{"name": icon.name, "price": icon.price} for icon in icons]}

# Получение значка по ID
@app.get("/icons/{icon_id}", summary="Получить значок по ID")
def get_icon(icon_id: int, db: Session = Depends(get_db)):
    icon = db.query(Icon).filter(Icon.id == icon_id).first()
    if not icon:
        raise HTTPException(status_code=404, detail="Значок не найден")
    return {"name": icon.name, "price": icon.price}

# Обновление значка
@app.put("/icons/{icon_id}", summary="Обновить значок")
def update_icon(icon_id: int, name: str = None, price: float = None, db: Session = Depends(get_db)):
    icon = db.query(Icon).filter(Icon.id == icon_id).first()
    if not icon:
        raise HTTPException(status_code=404, detail="Значок не найден")
    
    if name:
        icon.name = name
    if price is not None:
        icon.price = price
    
    db.commit()
    db.refresh(icon)
    
    return {"message": "Значок обновлен", "icon": {"name": icon.name, "price": icon.price}}

# Удаление значка
@app.delete("/icons/{icon_id}", summary="Удалить значок")
def delete_icon(icon_id: int, db: Session = Depends(get_db)):
    icon = db.query(Icon).filter(Icon.id == icon_id).first()
    if not icon:
        raise HTTPException(status_code=404, detail="Значок не найден")
    
    db.delete(icon)
    db.commit()
    
    return {"message": "Значок удален"}