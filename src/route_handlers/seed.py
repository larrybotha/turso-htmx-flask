import uuid
from datetime import datetime

from flask import redirect, url_for
from sqlalchemy import select
from sqlalchemy.orm import Session

from ..models import Base, Link, User

current_time = datetime.now()
current_time_in_seconds = int(
    float((current_time - datetime(1970, 1, 1)).total_seconds())
)


def seed_factory(db_engine, /):
    def seed():
        # Create all tables in metadata
        Base.metadata.create_all(db_engine)

        # Seed an account
        user_id = str(uuid.uuid4())
        delete_id = str(uuid.uuid4())

        with Session(db_engine) as session:
            links = [
                Link(
                    id=str(uuid.uuid4()),
                    user_id=user_id,
                    website="github",
                    link="https://github.com/tursodatabase",
                    created_at=current_time_in_seconds,
                ),
                Link(
                    id=str(uuid.uuid4()),
                    user_id=user_id,
                    website="linkedin",
                    link="https://linkedin.com/in/tursodatabase",
                    created_at=current_time_in_seconds,
                ),
                Link(
                    id=str(uuid.uuid4()),
                    user_id=user_id,
                    website="twitter",
                    link="https://twitter.com/tursodatabase",
                    created_at=current_time_in_seconds,
                ),
            ]
            user = User(
                id=user_id,
                email="tips@turso.tech",
                full_name="Iku Turso",
                user_name="turso",
                delete_id=delete_id,
                created_at=current_time_in_seconds,
                links=links,
            )
            session.add_all([user])
            session.commit()

        session = Session(db_engine)

        # get & print seeded user
        stmt = select(User).where(User.id.in_([user_id]))

        for user in session.scalars(stmt):
            print(user)

        return redirect(url_for("home"))

    return seed
