from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.exception import BusinessException
from app.models.profile import Profile
from app.schemas.profile import ProfileCreate, ProfileUpdate


class ProfileService:
    def get_by_user_id(self, db: Session, user_id: int) -> Profile | None:
        return db.scalar(select(Profile).where(Profile.user_id == user_id))

    def create_for_user(
        self,
        db: Session,
        user_id: int,
        payload: ProfileCreate,
    ) -> Profile:
        if self.get_by_user_id(db, user_id):
            raise BusinessException(
                code=40011,
                message="profile already exists",
                status_code=400,
            )

        profile = Profile(
            user_id=user_id,
            **payload.model_dump(),
        )
        db.add(profile)
        db.commit()
        db.refresh(profile)
        return profile

    def get_or_raise(self, db: Session, user_id: int) -> Profile:
        profile = self.get_by_user_id(db, user_id)
        if not profile:
            raise BusinessException(
                code=40411,
                message="profile not found",
                status_code=404,
            )
        return profile

    def update_for_user(
        self,
        db: Session,
        user_id: int,
        payload: ProfileUpdate,
    ) -> Profile:
        profile = self.get_or_raise(db, user_id)
        update_data = payload.model_dump(exclude_unset=True)

        for field, value in update_data.items():
            setattr(profile, field, value)

        db.add(profile)
        db.commit()
        db.refresh(profile)
        return profile


profile_service = ProfileService()