import datetime
import os

import click
from dotenv import load_dotenv
from flask import Flask, current_app
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import DateTime, ForeignKey, Integer, String, func
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from typing_extensions import Annotated
from flask_jwt_extended import JWTManager
from typing import List


class Base(DeclarativeBase):
    pass


db = SQLAlchemy(model_class=Base)
migrate = Migrate()
jwt = JWTManager()


class Role(db.Model):

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String, nullable=False)
    user: Mapped[List["User"]] = relationship(back_populates="role")

    def __repr__(self) -> str:
        return f"Role(id={self.id!r}, name={self.name!r}"


class User(db.Model):
    __tablename__ = "user"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    username: Mapped[str] = mapped_column(String, unique=True, nullable=False)
    password: Mapped[str] = mapped_column(String, nullable=False)
    role_id: Mapped[int] = mapped_column(ForeignKey("role.id"))
    role: Mapped["Role"] = relationship(back_populates="user")

    def __repr__(self) -> str:
        return f"User(id={self.id!r}, username={self.username!r}"


class Post(db.Model):
    __tablename__ = "post"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    title: Mapped[str] = mapped_column(String, nullable=False)
    body: Mapped[str] = mapped_column(String, nullable=False)
    created: Mapped[datetime] = mapped_column(DateTime, default=datetime.datetime.now())
    author_id: Mapped[int] = mapped_column(ForeignKey("user.id"))

    def __repr__(self) -> str:
        return (
            f"User(id={self.id!r}, title={self.username!r}, author_id{self.author_id!r}"
        )


@click.command("init-db")
def init_db_command():
    """Clear the existing data and create new tables."""
    global db
    with current_app.app_context():
        db.create_all()
    click.echo("Initialized the database.")


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY=os.getenv("SECRET_KEY"),
        SQLALCHEMY_DATABASE_URI="sqlite:///posts.sqlite",
        JWT_SECRET_KEY=os.getenv("JWT_SECRET_KEY"),
    )

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile("config.py", silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # register cli command
    app.cli.add_command(init_db_command)

    # initialize extensins
    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)

    # register blueprint
    from src.controllers import post, user, auth, role

    app.register_blueprint(user.pages)
    app.register_blueprint(post.pages)
    app.register_blueprint(auth.pages)
    app.register_blueprint(role.pages)

    return app
