import uuid
from datetime import datetime

from sqlalchemy import Column, String, DateTime, JSON, inspect

from database import Base
from sqlalchemy.dialects.postgresql import UUID


class user_details(Base):
    __tablename__ = "user_details"
    __table_args__ = {'user_details': True}
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    number = Column(String(300), nullable=True)
    creation_at = Column(DateTime, default=datetime.utcnow)
    user_meta = Column(JSON, nullable=True)

    def toDict(self):
        return {c.key: getattr(self, c.key) for c in inspect(self).mapper.column_attrs}
