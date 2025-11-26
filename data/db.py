# db.py
import sqlite3
import os
from contextlib import asynccontextmanager
from fastapi import FastAPI

from config.settings import Settings, get_settings
from data import DB_PATH, create_table
from seed_data import generate_mock_data


def get_db():
    '''
    Opens the DB
    Yields the DB connection
    Closes it after the request is finished
    -> prevents DB leaks
    '''
    # Creates/opens spendings.db in current folder
    conn = sqlite3.connect(DB_PATH) 
    # Makes rows behave like dicts: row["user_id"]
    conn.row_factory = sqlite3.Row
    try:
        yield conn
    finally:
        conn.close()


@asynccontextmanager
async def lifespan(app: FastAPI):
    settings = get_settings()
    # Startup: create DB + table if needed
    create_table(DB_PATH)
    if settings.environment == "deployment" and not os.path.exists(DB_PATH):
        generate_mock_data()
        
    yield  # App runs here

    # Shutdown: nothing special for now
    # (You could clean up global resources here if you had any.)
