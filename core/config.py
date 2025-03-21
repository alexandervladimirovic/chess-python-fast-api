from pathlib import Path

from pydantic_settings import BaseSettings

BASE_DIR = Path(__file__).resolve().parent.parent


class Settings(BaseSettings):
    """Class for downloading settings from file '.env' using pydantic.

    Class uses Pydantic to load variables environments
    from the '.env` file to class attributes. This makes it easy
    manage the application configuration, for example, to connect to a database.

    Attributes:
        postgres_db_url (str): URL of the connection to the PostgreSQL database.
        db_echo (bool): DEBUG mode for view sql-request.

    Configuration:
        env_file (str): The path to the '.env' file from which
        the environment variables are loaded.
        env_file_encoding (str): Encoding of the '.env' file.
        By default, 'utf-8' is used.

    """

    api_v1_prefix: str = "/api/v1"
    postgres_db_url: str
    db_echo: bool = True

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


settings = Settings()
