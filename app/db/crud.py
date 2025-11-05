from sqlalchemy.orm import Session
from .model import UserStep

def get_user_step(db: Session, uuid: str) -> int:
    record = db.query(UserStep).filter(UserStep.uuid == uuid).first()
    return record.step if record else 1

def set_user_step(db: Session, uuid: str, step: int) -> None:
    record = db.query(UserStep).filter(UserStep.uuid == uuid).first()
    if record:
        record.step = step
    else:
        record = UserStep(uuid=uuid, step=step)
        db.add(record)
    db.commit()
