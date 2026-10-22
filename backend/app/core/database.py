from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from .config import settings

# Create engine
# The engine owns the connection pool and is created once per process: SQLAlchemy
# pools are thread-safe, so the same engine can be shared by all the request
# handlers of the web server.
# pool_pre_ping makes the pool validate a connection before handing it out, which
# transparently replaces the connections killed by a database restart or by an
# idle timeout - the usual cause of "server closed the connection" errors.
# pool_size=10 keeps 10 connections open per process, max_overflow=20 allows 20
# extra ones during a burst of traffic.
# The pool options belong to QueuePool, which SQLAlchemy 2.0 uses for a
# file-based SQLite database; the URL always resolves to a file path here.
# On SQLite the pysqlite dialect passes check_same_thread=False for file based
# databases, which is what allows the pool to hand a connection over to a thread
# other than the one that opened it. The engine relies on that implicit default
# instead of setting the flag explicitly.
engine = create_engine(
    settings.DATABASE_URL,
    pool_pre_ping=True,
    pool_size=10,
    max_overflow=20,
)

# Session factory
# autocommit=False: nothing reaches the database until the caller commits.
# autoflush=False: a pending change is not flushed by an implicit query, so the
# endpoint layer keeps control of when the INSERT/UPDATE is actually issued.
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class for models
# Every ORM model inherits from this Base, so all the tables share one MetaData:
# create_all() sees the whole schema and Alembic autogenerate finds every table.
Base = declarative_base()


def get_db():
    """Dependency for getting database session"""
    # FastAPI resolves this generator as a dependency: one session per request,
    # handed to the endpoint as `db` and closed in the finally block even when
    # the endpoint raises, which returns the connection to the pool.
    # The dependency deliberately does not commit: writing is the caller's job.
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

