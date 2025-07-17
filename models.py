# models.py
from sqlalchemy import create_engine, Column, Integer, String, DateTime, Text, UniqueConstraint, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
import os

load_dotenv()

Base = declarative_base()

# In models.py - keep your existing constraints
class Player(Base):
    __tablename__ = 'players'
    id = Column(Integer, primary_key=True)
    name = Column(String(255), unique=True, nullable=False)  # Unique on name

class Decklist(Base):
    __tablename__ = 'decklists'
    id = Column(Integer, primary_key=True)
    player_id = Column(Integer, ForeignKey('players.id'), nullable=False)
    tournament = Column(String(255), nullable=False)
    hero = Column(String(100), nullable=False)
    decklist_url = Column(String(255), nullable=False)
    
    __table_args__ = (
        UniqueConstraint('player_id', 'tournament', name='uq_player_tournament'),
    )

# Database setup
# Replace your DB_URL with this container-aware version:
DB_URL = "postgresql://root:root@db:5432/fab_db"
engine = create_engine(DB_URL)
Session = sessionmaker(bind=engine)
session = Session()

async def create_tables(engine):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

# Create tables if they don't exist
# Base.metadata.create_all(engine)