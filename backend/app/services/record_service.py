from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.core.exception import BusinessException
from app.core.timezone import now_beijing
from app.models.record import Record
from app.schemas.record import RecordCreate, RecordQueryParams, RecordUpdate


class RecordService:
    def create_for_user(
        self,
        db: Session,
        user_id: int,
        payload: RecordCreate,
    ) -> Record:
        record = Record(
            user_id=user_id,
            record_type=payload.record_type.value,
            value=payload.value,
            unit=payload.unit,
            record_time=payload.record_time or now_beijing(),
            note=payload.note,
        )
        db.add(record)
        db.commit()
        db.refresh(record)
        return record

    def get_or_raise(
        self,
        db: Session,
        user_id: int,
        record_id: int,
    ) -> Record:
        stmt = select(Record).where(
            Record.id == record_id,
            Record.user_id == user_id,
        )
        record = db.scalar(stmt)
        if not record:
            raise BusinessException(
                code=40421,
                message="record not found",
                status_code=404,
            )
        return record

    def list_for_user(
        self,
        db: Session,
        user_id: int,
        query: RecordQueryParams,
    ) -> tuple[list[Record], int]:
        filters = [Record.user_id == user_id]

        if query.record_type:
            filters.append(Record.record_type == query.record_type.value)

        if query.start_time:
            filters.append(Record.record_time >= query.start_time)

        if query.end_time:
            filters.append(Record.record_time <= query.end_time)

        total = db.scalar(
            select(func.count()).select_from(Record).where(*filters)
        ) or 0

        stmt = (
            select(Record)
            .where(*filters)
            .order_by(Record.record_time.desc(), Record.id.desc())
            .offset((query.page - 1) * query.page_size)
            .limit(query.page_size)
        )
        items = list(db.scalars(stmt).all())
        return items, total

    def update_for_user(
        self,
        db: Session,
        user_id: int,
        record_id: int,
        payload: RecordUpdate,
    ) -> Record:
        record = self.get_or_raise(db, user_id, record_id)
        update_data = payload.model_dump(exclude_unset=True)

        if "record_type" in update_data:
            if update_data["record_type"] is None:
                raise BusinessException(
                    code=40021,
                    message="record_type cannot be null",
                    status_code=400,
                )
            update_data["record_type"] = update_data["record_type"].value

        if "value" in update_data and update_data["value"] is None:
            raise BusinessException(
                code=40022,
                message="value cannot be null",
                status_code=400,
            )

        if "record_time" in update_data and update_data["record_time"] is None:
            raise BusinessException(
                code=40023,
                message="record_time cannot be null",
                status_code=400,
            )

        for field, value in update_data.items():
            setattr(record, field, value)

        db.add(record)
        db.commit()
        db.refresh(record)
        return record

    def delete_for_user(
        self,
        db: Session,
        user_id: int,
        record_id: int,
    ) -> None:
        record = self.get_or_raise(db, user_id, record_id)
        db.delete(record)
        db.commit()


record_service = RecordService()
