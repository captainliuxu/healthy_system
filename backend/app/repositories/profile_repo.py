from sqlalchemy.orm import Session
from app.models.profile import Profile


class ProfileRepository:
    def create(self, db: Session, obj_in: dict) -> Profile:
        db_obj = Profile(**obj_in)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def get_by_id(self, db: Session, profile_id: int) -> Profile | None:
        return db.query(Profile).filter(Profile.id == profile_id).first()

    def list(self, db: Session, skip: int = 0, limit: int = 20) -> list[Profile]:
        return db.query(Profile).offset(skip).limit(limit).all()

    def update(self, db: Session, db_obj: Profile, obj_in: dict) -> Profile:
        for field, value in obj_in.items():
            setattr(db_obj, field, value)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def delete(self, db: Session, db_obj: Profile):
        db.delete(db_obj)
        db.commit()