from collections.abc import Generator

from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, Session, sessionmaker

from app.core.config import settings

# 所有 ORM 模型的共同父类
# Alembic 会通过它拿到所有表的元数据
class Base(DeclarativeBase):
    pass


connect_args = {}
if settings.DATABASE_URL.startswith("sqlite"):
    connect_args = {"check_same_thread": False}

# 真正负责和数据库建立连接
# 这是 SQLAlchemy 的底层连接入口
engine = create_engine(
    settings.DATABASE_URL,
    pool_pre_ping=True,
    connect_args=connect_args,
)

# 每次业务操作都从这里拿一个数据库会话
# 不在路由里手写 Session(engine)，统一从这里出
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
    class_=Session,
)

# 给 FastAPI 的依赖注入系统使用
# 每个请求拿到一个独立会话
# 请求结束后自动关闭
def get_db() -> Generator[Session, None, None]:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()