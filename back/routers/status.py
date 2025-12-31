from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import select
from datetime import datetime, timezone

from db import get_db
from back.models.status import UserStatus
from back.get_current_user import get_current_user
from back.models.users import User

router = APIRouter(prefix="/user", tags=["user_status"])

# ========== ВСЕГО 2 ЭНДПОИНТА ==========

@router.get("/{user_id}/status")
def get_user_status(
    user_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Получить статус пользователя (онлайн/оффлайн + время последней активности)"""
    # Проверяем существует ли пользователь
    user = db.execute(
        select(User).where(User.id == user_id)
    ).scalar_one_or_none()
    
    if not user:
        raise HTTPException(status_code=404, detail="Пользователь не найден")
    
    # Получаем статус
    status = db.execute(
        select(UserStatus).where(UserStatus.user_id == user_id)
    ).scalar_one_or_none()
    
    if not status:
        # Если статуса нет - создаем дефолтный
        status = UserStatus(
            user_id=user_id,
            is_online=False,
            last_seen=datetime.now(timezone.utc),
            last_activity=datetime.now(timezone.utc)
        )
        db.add(status)
        db.commit()
        db.refresh(status)
    
    # Форматируем время для ответа
    last_seen_formatted = format_exact_time(status.last_seen) if status.last_seen else "никогда"
    
    return {
        "user_id": user_id,
        "is_online": status.is_online,
        "last_seen": status.last_seen,
        "last_seen_formatted": last_seen_formatted,
        "first_name": user.first_name
    }

@router.post("/status/update")
def update_user_status(
    is_online: bool,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Обновить свой статус (онлайн/оффлайн)"""
    now = datetime.now(timezone.utc)
    
    # Ищем существующий статус
    status = db.execute(
        select(UserStatus).where(UserStatus.user_id == current_user.id)
    ).scalar_one_or_none()
    
    if status:
        # Обновляем
        status.is_online = is_online
        status.last_seen = now
        if is_online:
            status.last_activity = now
    else:
        # Создаем новый
        status = UserStatus(
            user_id=current_user.id,
            is_online=is_online,
            last_seen=now,
            last_activity=now if is_online else now
        )
        db.add(status)
    
    db.commit()
    
    last_seen_formatted = format_exact_time(status.last_seen)
    
    return {
        "user_id": current_user.id,
        "is_online": status.is_online,
        "last_seen": status.last_seen,
        "last_seen_formatted": last_seen_formatted,
        "message": f"Статус обновлен: {'онлайн' if is_online else 'оффлайн'}"
    }

# ========== ВСПОМОГАТЕЛЬНАЯ ФУНКЦИЯ ==========

def format_exact_time(timestamp: datetime) -> str:
    """Форматирует время в точный формат"""
    if not timestamp:
        return "никогда"
    
    # Всегда показываем точную дату и время
    return timestamp.strftime("%d.%m.%Y %H:%M")