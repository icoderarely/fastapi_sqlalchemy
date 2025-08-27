# --- What this file does (in plain English) ---------------------------------
# It sets up the "plumbing" so our app can talk to a database using SQLAlchemy.
# Think of it as:
# 1) Choosing which database to use and where it lives (a URL).
# 2) Creating an "engine" (the car engine that actually drives queries).
# 3) Creating a factory that gives us short-lived "sessions" (safe, single-use
#    helpers we use to read/write rows).
# 4) Creating a "Base" class that our table-model classes will inherit from.
# ---------------------------------------------------------------------------

# SQLAlchemy imports:
from sqlalchemy import create_engine  # builds the database engine
from sqlalchemy.orm import sessionmaker  # builds Session factory

# NOTE: This import works, but is the legacy path.
# Modern path is: from sqlalchemy.orm import declarative_base
from sqlalchemy.ext.declarative import (
    declarative_base,
)  # builds Base class for ORM models

# 1) DATABASE URL ------------------------------------------------------------
# This tells SQLAlchemy *which* database to use and *where* it is.
# Format (for SQLite file): "sqlite:///relative/path/to/file.db"
# Here, "./todosapp.db" means "a file named todosapp.db next to this script".
DATABASE_URL = "sqlite:///./todosapp.db"

# 2) ENGINE ------------------------------------------------------------------
# The Engine is the core connection object that knows how to talk to the DB.
# - connect_args={"check_same_thread": False}:
#     SQLite (the tiny file-based DB we’re using) is strict about which thread
#     uses a connection. Web frameworks often use multiple threads, so we relax
#     this rule. This is common/safe for local dev with SQLite.
# - echo=True:
#     Prints the actual SQL statements to the console. Super useful for learning
#     and debugging. Turn it off (echo=False) in production to reduce noise.
engine = create_engine(
    DATABASE_URL, connect_args={"check_same_thread": False}, echo=True
)

# 3) SESSION FACTORY ----------------------------------------------------------
# A Session is a short-lived "workbench" for talking to the DB:
# - You open a Session, do some work (queries/inserts/updates), then close it.
# - Think: "open Google Doc, type, save, close" — that’s a Session.
#
# sessionmaker(...) *creates a factory* that can make new Session objects for us.
# - autocommit=False:
#     Changes are NOT auto-saved; you must call session.commit() explicitly.
#     This protects you from accidental writes.
# - autoflush=False:
#     SQLAlchemy won’t push pending changes to the DB until needed or commit().
#     Keeping this False is simpler for beginners; you control when things happen.
# - bind=engine:
#     Connect these Sessions to the Engine we created above.
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# 4) DECLARATIVE BASE ---------------------------------------------------------
# The "Base" class is the parent for all your ORM models (your table classes).
# You’ll create classes like `class User(Base): ...` and define columns.
# SQLAlchemy uses this to know how to create tables and map rows <-> Python objects.
Base = declarative_base()
