from app.db.session import SessionLocal, engine
from app.models import Base
from app.db.seed import seed_demo_data


def main() -> None:
    Base.metadata.create_all(bind=engine)
    with SessionLocal() as db:
        seed_demo_data(db)
    print("database initialized")


if __name__ == "__main__":
    main()
