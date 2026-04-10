# 第一阶段先不放业务表。
# 第二阶段开始，把所有 ORM 模型统一导入到这里，供 Alembic 自动发现。
from app.models.profile import Profile
from app.models.user import User

__all__ = ["User", "Profile"]