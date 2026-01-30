from datetime import datetime
from extension import db
from sqlalchemy_serializer import SerializerMixin

class BaseModel(db.Model, SerializerMixin):
    __abstract__ = True

    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    deleted_at = db.Column(db.DateTime, nullable=True)

    # This ensures deleted_at is excluded from serialization
    serialize_rules = ('-deleted_at',)

    def soft_delete(self):
        """Mark a record as deleted."""
        self.deleted_at = datetime.utcnow()
        db.session.commit()

    @property
    def is_deleted(self):
        """Check if a record is soft-deleted."""
        return self.deleted_at is not None

    def as_dict(self):
        """Convert the model to a dictionary."""
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}

    @classmethod
    def get_all(cls):
        """Get all non-soft-deleted records."""
        return cls.query.filter_by(deleted_at=None).all()
    
    @classmethod
    def get_by_id(cls, id):
        """Get a single record by ID, ensure it's not soft-deleted."""
        return cls.query.filter_by(id=id, deleted_at=None).first()
