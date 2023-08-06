import os

import pathlib

from sqlalchemy import create_engine, select
from sqlalchemy.engine.mock import MockConnection
from sqlalchemy.exc import OperationalError
from sqlalchemy.orm import Session
from typing import List

from famegui.database.tables import Base, RecentlyUsedProject


def get_db_engine() -> MockConnection:
    try:
        path = os.path.join("sqlite:///", "fame_working_dir", "database.sqlite3")
        engine = create_engine(path, echo=True, future=True)
        engine.connect()
    except OperationalError:

        path = os.path.join("sqlite:///", "data", "database.sqlite3")
        engine = create_engine(path, echo=True, future=True)

    Base.metadata.create_all(engine)
    engine: MockConnection

    return engine


def check_if_project_was_already_opened(path: str) -> RecentlyUsedProject:
    stmt = select(RecentlyUsedProject).where(RecentlyUsedProject.path == path)

    with Session(get_db_engine()) as session:
        return session.scalar(stmt)


def insert_recent_project_into_db(path: str):
    with Session(get_db_engine()) as session:
        last_project = RecentlyUsedProject(
            path=path,
        )

        session.add_all([last_project])
        session.commit()


def get_recently_opened_projects() -> List[RecentlyUsedProject]:
    with Session(get_db_engine()) as session:
        stmt = select(RecentlyUsedProject)

        return [x for x in session.scalars(stmt)]


def manage_path_for_db(path: str):
    if not check_if_project_was_already_opened(str(path)):
        insert_recent_project_into_db(str(path))


if __name__ == '__main__':
    # DEBUG Purpose
    current_directory_path = pathlib.Path().resolve()
    if not check_if_project_was_already_opened(str(current_directory_path)):
        insert_recent_project_into_db(str(current_directory_path))
