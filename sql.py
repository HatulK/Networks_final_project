from sqlalchemy import Column, Integer, String, create_engine
import sqlalchemy as sa
from sqlalchemy.orm import sessionmaker, declarative_base

# Creates a declarative base class for the ORM (Object-Relational Mapping)
Base = declarative_base()

# Creates a Players table with columns id, name, team, league, national, position, goals, and assists.
class Players(Base):
    __tablename__ = 'Players'

    # Column definitions
    id = sa.Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String)
    team = Column(String)
    league = Column(String)
    national = Column(String)
    position = Column(String)
    goals = Column(Integer)
    assists = Column(Integer)

    # Initializes a Players object with the given attributes.
    def __init__(self, name, team, league, national, position, goals, assists):
        self.name = name
        self.team = team
        self.league = league
        self.national = national
        self.position = position
        self.goals = goals
        self.assists = assists

    # Returns a string representation of a Players object.
    def __repr__(self):
        return f"Players(name='{self.name}'id='{self.id}, team='{self.team}', league='{self.league}', national='{self.national}', position='{self.position}', goals={self.goals}, assists={self.assists})"

    # Returns a string representation of a Players object.
    def __str__(self):
        return f"Player ID: {self.id} Name: {self.name} Team: {self.team} League: {self.league} National: {self.national} Position: {self.position} Goals: {self.goals} Assists: {self.assists}\n"

# Main function for creating a database engine and a session.
if __name__ == '__main__':
    # Creates a SQLite engine for the database with name tcp.db.
    engine = create_engine('sqlite:///tcp.db', echo=False)
    # Creates the Players table in the database.
    Base.metadata.create_all(engine)
    # Creates a session factory bound to the engine.
    session = sessionmaker(bind=engine)
    # Creates a database session.
    db_session = session()
