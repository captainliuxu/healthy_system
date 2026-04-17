"""convert existing timestamps to beijing

Revision ID: 6d9e0c8c88f7
Revises: d22717b4ee61
Create Date: 2026-04-17 10:45:00.000000

"""

from datetime import datetime, timedelta
from typing import Any, Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "6d9e0c8c88f7"
down_revision: Union[str, Sequence[str], None] = "d22717b4ee61"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

TIME_SHIFT = timedelta(hours=8)
TABLE_COLUMNS: dict[str, list[str]] = {
    "users": ["created_at", "updated_at"],
    "profiles": ["created_at", "updated_at"],
    "records": ["record_time", "created_at", "updated_at"],
    "conversations": ["created_at", "updated_at"],
    "messages": ["created_at"],
    "trigger_rules": ["created_at", "updated_at"],
    "active_logs": ["created_at"],
    "proactive_windows": ["created_at", "updated_at"],
    "proactive_messages": ["created_at", "displayed_at"],
}


def _parse_datetime_value(value: Any) -> datetime | None:
    if value is None:
        return None

    if isinstance(value, datetime):
        return value

    text_value = str(value).strip()
    if not text_value:
        return None

    normalized = text_value.replace("Z", "+00:00")
    try:
        return datetime.fromisoformat(normalized)
    except ValueError:
        pass

    for fmt in ("%Y-%m-%d %H:%M:%S.%f", "%Y-%m-%d %H:%M:%S"):
        try:
            return datetime.strptime(text_value, fmt)
        except ValueError:
            continue

    raise ValueError(f"unsupported datetime value: {value!r}")


def _shift_datetime_columns(delta: timedelta) -> None:
    bind = op.get_bind()

    for table_name, columns in TABLE_COLUMNS.items():
        selectable_columns = ", ".join(["id", *columns])
        rows = bind.execute(
            sa.text(f"SELECT {selectable_columns} FROM {table_name}")
        ).mappings().all()

        for row in rows:
            update_values: dict[str, Any] = {}
            for column_name in columns:
                parsed = _parse_datetime_value(row[column_name])
                if parsed is None:
                    continue
                update_values[column_name] = parsed + delta

            if not update_values:
                continue

            set_clause = ", ".join(
                f"{column_name} = :{column_name}"
                for column_name in update_values
            )
            bind.execute(
                sa.text(f"UPDATE {table_name} SET {set_clause} WHERE id = :id"),
                {"id": row["id"], **update_values},
            )


def upgrade() -> None:
    """Upgrade schema."""
    _shift_datetime_columns(TIME_SHIFT)


def downgrade() -> None:
    """Downgrade schema."""
    _shift_datetime_columns(-TIME_SHIFT)
