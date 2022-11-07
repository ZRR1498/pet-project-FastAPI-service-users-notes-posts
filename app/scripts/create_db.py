import app.db.database as database
from app.endpoints.users import models
from app.endpoints.notes import models
from app.endpoints.posts import models


def add_tables():
    return database.Base.metadata.create_all(bind=database.engine)


if __name__ == "__main__":
    add_tables()
