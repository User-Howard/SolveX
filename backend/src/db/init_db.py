from .session import Base, engine

def init_db():
    """Initialize database: Create all tables."""
    import src.db.models

    Base.metadata.create_all(bind=engine)


if __name__ == "__main__":
    init_db()