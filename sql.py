from sqlalchemy import Column, Integer, String, create_engine
import sqlalchemy as sa
from sqlalchemy.orm import sessionmaker, declarative_base

Base = declarative_base()


class Players(Base):
    __tablename__ = 'Players'

    id = sa.Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String)
    team = Column(String)
    league = Column(String)
    national = Column(String)
    position = Column(String)
    goals = Column(Integer)
    assists = Column(Integer)

    def __init__(self, name, team, league, national, position, goals, assists):
        self.name = name
        self.team = team
        self.league = league
        self.national = national
        self.position = position
        self.goals = goals
        self.assists = assists

    def __repr__(self):
        return f"Players(name='{self.name}'id='{self.id}, team='{self.team}', league='{self.league}', national='{self.national}', position='{self.position}', goals={self.goals}, assists={self.assists})"


    def __str__(self):
        return f"Player ID: {self.id} Name: {self.name} Team: {self.team} League: {self.league} National: {self.national} Position: {self.position} Goals: {self.goals} Assists: {self.assists}\n"


if __name__ == '__main__':
    engine = create_engine('sqlite:///tcp.db', echo=False)
    Base.metadata.create_all(engine)
    session = sessionmaker(bind=engine)
    db_session = session()
