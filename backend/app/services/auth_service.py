from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.exception import BusinessException
from app.core.security import create_access_token, hash_password, verify_password
from app.models.user import User
from app.schemas.auth import Token, UserRegisterRequest


class AuthService:
    def get_by_username(self, db: Session, username: str) -> User | None:
        return db.scalar(select(User).where(User.username == username))

    def get_by_email(self, db: Session, email: str) -> User | None:
        return db.scalar(select(User).where(User.email == email))

    def get_by_phone(self, db: Session, phone: str) -> User | None:
        return db.scalar(select(User).where(User.phone == phone))

    # 唯一性校验
    # 哈希密码
    # 创建用户

    def register(self, db: Session, payload: UserRegisterRequest) -> User:
        if self.get_by_username(db, payload.username):
            raise BusinessException(
                code=40001,
                message="username already exists",
                status_code=400,
            )

        if payload.email and self.get_by_email(db, payload.email):
            raise BusinessException(
                code=40002,
                message="email already exists",
                status_code=400,
            )

        if payload.phone and self.get_by_phone(db, payload.phone):
            raise BusinessException(
                code=40003,
                message="phone already exists",
                status_code=400,
            )

        user = User(
            username=payload.username,
            email=payload.email,
            phone=payload.phone,
            password_hash=hash_password(payload.password),
            is_active=True,
        )

        db.add(user)
        db.commit()
        db.refresh(user)
        return user

    # 查用户名
    # 校验密码
    # 检查是否激活
    def authenticate(self, db: Session, username: str, password: str) -> User:
        user = self.get_by_username(db, username)
        if not user:
            raise BusinessException(
                code=40101,
                message="incorrect username or password",
                status_code=401,
            )

        if not verify_password(password, user.password_hash):
            raise BusinessException(
                code=40101,
                message="incorrect username or password",
                status_code=401,
            )

        if not user.is_active:
            raise BusinessException(
                code=40301,
                message="user is inactive",
                status_code=403,
            )

        return user
    # 调用认证
    # 签发 JWT
    # 返回 token 对象
    def login(self, db: Session, username: str, password: str) -> Token:
        user = self.authenticate(db, username, password)
        access_token = create_access_token(subject=user.id)
        return Token(access_token=access_token, token_type="bearer")


auth_service = AuthService()