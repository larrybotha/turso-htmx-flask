import uuid

from flask import render_template, request, url_for
from sqlalchemy import Engine
from sqlalchemy.orm import Session

from ..models import Link, User
from ..utils.time import get_current_time_in_seconds


def home_factory(db_engine: Engine, /):
    def home():
        current_time_in_seconds = get_current_time_in_seconds()

        if request.method == "POST":
            user_name = request.form["user_name"]
            email = request.form["email"]
            full_name = request.form["full_name"]
            github = request.form["github"]
            twitter = request.form["twitter"]
            youtube = request.form["youtube"]
            linkedin = request.form["linkedin"]
            facebook = request.form["facebook"]

            if not user_name:
                return '<div class="error">Username is required</div>'
            elif not email:
                return '<div class="error">Email is required</div>'
            elif not full_name:
                return '<div class="error">Your full name is required</div>'
            elif (
                not github
                and not twitter
                and not youtube
                and not linkedin
                and not facebook
                and not youtube
            ):
                return '<div class="error">At least one social link is required</div>'
            else:
                with Session(db_engine) as session:
                    user_id = str(uuid.uuid4())
                    delete_id = str(uuid.uuid4())
                    links = []
                    if github:
                        links.append(
                            Link(
                                id=str(uuid.uuid4()),
                                user_id=user_id,
                                website="github",
                                link=github,
                                created_at=current_time_in_seconds,
                            )
                        )
                    if twitter:
                        links.append(
                            Link(
                                id=str(uuid.uuid4()),
                                user_id=user_id,
                                website="twitter",
                                link=twitter,
                                created_at=current_time_in_seconds,
                            )
                        )
                    if youtube:
                        links.append(
                            Link(
                                id=str(uuid.uuid4()),
                                user_id=user_id,
                                website="youtube",
                                link=youtube,
                                created_at=current_time_in_seconds,
                            )
                        )
                    if linkedin:
                        links.append(
                            Link(
                                id=str(uuid.uuid4()),
                                user_id=user_id,
                                website="linkedin",
                                link=linkedin,
                                created_at=current_time_in_seconds,
                            )
                        )
                    if facebook:
                        links.append(
                            Link(
                                id=str(uuid.uuid4()),
                                user_id=user_id,
                                website="facebook",
                                link=facebook,
                                created_at=current_time_in_seconds,
                            )
                        )
                    user = User(
                        id=user_id,
                        delete_id=delete_id,
                        email=email,
                        full_name=full_name,
                        user_name=user_name,
                        created_at=current_time_in_seconds,
                        links=links,
                    )
                    session.add_all([user])
                    session.commit()

                    return f"""
                        <div class='success'>
                            Account added. Delete ID: ({delete_id})
                        </div>
                        <p class='p-2 text-center'>
                            You social links are now available at
                            <a href='{request.base_url}u/{user.user_name}' target='_blank'>
                            {request.base_url}u/{user.user_name}
                            </a>
                        </p>
                    """

        return render_template("index.html", page_url=url_for("home"))

    return home
