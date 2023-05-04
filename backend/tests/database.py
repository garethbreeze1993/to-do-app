from typing import Optional

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.config import settings

# SQLALCHEMY_DATABASE_URL = "postgresql://user:password@postgresserver/db"
# Structure just to keep until successful connect

SQLALCHEMY_DATABASE_URL = f"postgresql://{settings.database_username}:{settings.database_password}@" \
                          f"{settings.database_hostname}:{settings.database_port}/{settings.database_name}_test"

engine = create_engine(SQLALCHEMY_DATABASE_URL)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


class MockDBSession:
    """
    Class that mocks a SQLAlchemy database session query
    """

    def __init__(self, return_val: Optional[list] = None, completed_check: bool = False, owner_filter: bool = False,
                 owner_id: Optional[int] = None):
        """
        init dunder method to initialise the class.
        ::param return_value is what you want the mocked query to return so use this attribute in the tests
        """
        self.return_val = return_val
        self.return_index = 0
        self.completed_check = completed_check
        self.owner_filter = owner_filter
        self.owner_id = owner_id

    def query(self):
        """ Used in the patched query to override the SQLAlchemy query method """
        return self

    def filter(self, *args, **kwargs):
        """ Used in the patched query to override the SQLAlchemy filter method """
        if self.completed_check:
            self.return_val = [val for val in self.return_val if val.completed == True]
        if self.owner_filter:
            self.return_val = [val for val in self.return_val if val.owner_id == self.owner_id]
        return self

    def count(self):
        """ Used in the patched query to override the SQLAlchemy count method """
        return len(self.return_val)

    def __iter__(self):
        """ Used in the patched query to make the initalised object an iterable """
        return self

    def __next__(self):
        """ Used to loop through the objects attribute return_val """
        if self.return_index >= len(self.return_val):
            raise StopIteration
        else:
            self.return_index += 1
            return self.return_val[self.return_index - 1]
