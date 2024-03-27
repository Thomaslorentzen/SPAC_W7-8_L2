from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

class DBforbindelse:
    _instance = None  # Store the single instance of the class
    _engine = None  # Store the SQLAlchemy engine
    _Session = None  # Store the SQLAlchemy session class

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            # Create SQLAlchemy engine
            cls._engine = create_engine('mysql+mysqlconnector://root:Kom12345@localhost/lagerstyring')
            # Create session class
            cls._Session = sessionmaker(bind=cls._engine)
            print("Connection to the database has been established.")
        return cls._instance

    def __init__(self):
        pass

    @classmethod
    def get_session(cls):
        return cls._Session()


