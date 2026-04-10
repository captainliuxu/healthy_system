from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.exception import BusinessException
from app.models.user import User
from app.schemas.user import UserUpdate


class UserService:
    def update_basic_info(
        self,
        db: Session,
        current_user: User,
        payload: UserUpdate,
    ) -> User:
        update_data = payload.model_dump(exclude_unset=True)

        if "username" in update_data and update_data["username"] != current_user.username:
            exists = db.scalar(select(User).where(User.username == update_data["username"]))
            if exists:
                raise BusinessException(
                    code=40004,
                    message="username already exists",
                    status_code=400,
                )

        if "email" in update_data and update_data["email"] != current_user.email:
            exists = db.scalar(select(User).where(User.email == update_data["email"]))
            if exists:
                raise BusinessException(
                    code=40005,
                    message="email already exists",
                    status_code=400,
                )

        if "phone" in update_data and update_data["phone"] != current_user.phone:
            exists = db.scalar(select(User).where(User.phone == update_data["phone"]))
            if exists:
                raise BusinessException(
                    code=40006,
                    message="phone already exists",
                    status_code=400,
                )

        for field, value in update_data.items():
            setattr(current_user, field, value)

        db.add(current_user)
        db.commit()
        db.refresh(current_user)
        return current_user


user_service = UserService()