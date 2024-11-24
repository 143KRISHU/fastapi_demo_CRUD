from ..db import SessionLocal

# Dependency to get DB session
def get_db_dependency():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()