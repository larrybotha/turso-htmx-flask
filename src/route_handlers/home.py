import uuid

from flask import render_template, request, url_for
from sqlalchemy import Engine
from sqlalchemy.orm import Session

from ..models import Link, User
from ..utils.time import get_current_time_in_seconds


def _handle_post(db_engine: Engine, /):
    current_time_in_seconds = get_current_time_in_seconds()
    user_name = request.form["user_name"]
    email = request.form["email"]
    full_name = request.form["full_name"]
    github = request.form["github"]
    twitter = request.form["twitter"]
    youtube = request.form["youtube"]
    linkedin = request.form["linkedin"]
    facebook = request.form["facebook"]
    validations = [
        (user_name, "Username is required"),
        (email, "Email is required"),
        (full_name, "Your full name is required"),
        (
            any((github, twitter, youtube, linkedin, facebook)),
            "Please select at least one social link",
        ),
    ]

    for value, message in validations:
        if not value:
            return f'<div class="error">{message}</div>'

    configs = [
        (github, "github"),
        (twitter, "twitter"),
        (youtube, "youtube"),
        (linkedin, "linkedin"),
        (facebook, "facebook"),
    ]

    with Session(db_engine) as session:
        user_id = str(uuid.uuid4())
        delete_id = str(uuid.uuid4())
        links = [
            Link(
                created_at=current_time_in_seconds,
                id=str(uuid.uuid4()),
                link=link,
                user_id=user_id,
                website=name,
            )
            for link, name in configs
        ]
        user = User(
            created_at=current_time_in_seconds,
            delete_id=delete_id,
            email=email,
            full_name=full_name,
            id=user_id,
            links=links,
            user_name=user_name,
        )

        session.add_all([user])
        session.commit()

        return f"""
            <div class='success'>
                Account added. Delete ID: ({delete_id})
            </div>
            <p class='p-2 text-center'>
                You social links are now available at
                <a
                    href='{request.base_url}u/{user.user_name}'
                    target='_blank'
                >
                    {request.base_url}u/{user.user_name}
                </a>
            </p>
        """


def home_factory(db_engine: Engine, /):
    def home():
        if request.method == "POST":
            return _handle_post(db_engine)

        return render_template(
            "index.html",
            page_url=url_for("home"),
        )

    return home
