from sqlalchemy.orm import Session

from database.database_worker import SQLAlchemyStorage, Storage, engine

storage: Storage = SQLAlchemyStorage(lambda: Session(engine))
