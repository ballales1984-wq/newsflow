from typing import List
from pydantic_settings import BaseSettings
from pydantic import field_validator


class Settings(BaseSettings):
    """Application settings"""

    # pydantic-settings resolves every field in this order: the process
    # environment first, the .env file second, the declared default last.
    # An exported environment variable therefore always overrides the same key
    # written in .env.
    # case_sensitive = True (see the Config class below) means the environment
    # variable must be spelled exactly like the attribute: DATABASE_URL works,
    # database_url is ignored.
    #
    # Every group below maps to one concern of the application, so the whole
    # runtime configuration of a deployment fits in a single .env file.
    # App
    # Identity of the service, reported in the API docs and in the logs.
    # DEBUG changes the server behaviour and must stay False in production.
    APP_NAME: str = "NewsFlow"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = False

    # Database
    # Single knob for the storage backend: a postgres:// URL switches the whole
    # app to PostgreSQL (psycopg2 is in requirements.txt), everything else stays
    # on the local SQLite file.
    DATABASE_URL: str = "sqlite:///./newsflow.db"

    # The validator normalizes the URL instead of validating it: an empty value
    # or any value containing "sqlite:" is rewritten to the canonical file path.
    # That keeps a typo in .env from pointing the app at a different database.
    # Side effect worth knowing: "sqlite:///:memory:" also contains "sqlite:"
    # and is rewritten as well, so an in-memory database cannot be used here.
    # Non-sqlite URLs (postgres://...) are passed through untouched.
    @field_validator("DATABASE_URL")
    @classmethod
    def validate_database_url(cls, v: str) -> str:
        if not v or "sqlite:" in v:
            return "sqlite:///./newsflow.db"
        return v

    # Redis (optional)
    # Used as Celery broker and result backend (see core/celery_app.py).
    # The API answers requests without Redis; only the background workers need it.
    REDIS_URL: str = "redis://localhost:6379"

    # Security
    # SECRET_KEY is the only field without a default: the application refuses
    # to start when it is missing, which forces every deployment to inject its
    # own key. It signs the JWTs, so rotating it invalidates every issued token.
    # ALGORITHM is the JWT signing algorithm used by core/security.py.
    # ACCESS_TOKEN_EXPIRE_MINUTES is the lifetime of an access token; refresh
    # tokens have their own hard-coded 30 day window in core/security.py.
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    # CORS
    # Allowed browser origins, kept as one comma-separated string so the whole
    # allow-list fits into a single environment variable.
    CORS_ORIGINS: str = "http://localhost:4200"

    # The comma-separated string is split into the list of allowed origins and
    # the whitespace around each entry is stripped. An empty value yields
    # [""] (a list with one empty string) and not an empty list, so the
    # variable should always contain at least one real origin.
    @field_validator("CORS_ORIGINS")
    @classmethod
    def parse_cors_origins(cls, v: str) -> List[str]:
        return [origin.strip() for origin in v.split(",")]

    # News APIs
    # Credentials of the upstream providers. They are optional: the API
    # collector logs a warning and returns no article when a key is missing,
    # so the other sources keep working.
    NEWSAPI_KEY: str = ""
    GUARDIAN_API_KEY: str = ""

    # NLP Settings
    # Thresholds of the analysis pipeline. MAX_ARTICLE_AGE_DAYS is the cutoff
    # used by the cleanup task; SIMILARITY_THRESHOLD and MIN_ARTICLE_LENGTH
    # are declared here but are not referenced by the current services.
    SIMILARITY_THRESHOLD: float = 0.7
    MIN_ARTICLE_LENGTH: int = 200
    MAX_ARTICLE_AGE_DAYS: int = 30

    # Collection Settings
    # MAX_ARTICLES_PER_SOURCE caps how many items a single fetch keeps.
    # COLLECTION_INTERVAL_HOURS is declared here but is not referenced by the
    # current services: the cadence is driven by the Celery beat schedule.
    COLLECTION_INTERVAL_HOURS: int = 1
    MAX_ARTICLES_PER_SOURCE: int = 50

    # Email (optional)
    # SMTP credentials for the digest mailer. Declared for the notification
    # channel, but not read by the current code.
    SMTP_HOST: str = ""
    SMTP_PORT: int = 587
    SMTP_USER: str = ""
    SMTP_PASSWORD: str = ""

    # Telegram (optional)
    # Bot token of the Telegram delivery channel. Declared for the notification
    # channel, but not read by the current code.
    TELEGRAM_BOT_TOKEN: str = ""

    # External API (optional)
    # Base URL of an external NewsFlow-compatible API. Declared for the
    # additional source, but not read by the current code.
    NEWSFLOW_API_URL: str = ""

    class Config:
        # .env is resolved relative to the working directory the process was
        # started in, so the API and the Celery worker have to be launched from
        # the same directory to see the same file.
        # Note: class-based Config still works in pydantic-settings v2 but logs
        # a deprecation warning; model_config = SettingsConfigDict(...) is the
        # v3-ready form. Left as is on purpose.
        # extra = "ignore" keeps unrelated keys in .env from breaking startup.
        env_file = ".env"
        case_sensitive = True
        extra = "ignore"


# Single instance shared by the whole process: the settings are read once at
# import time, so changing an environment variable afterwards has no effect.
settings = Settings()
