from pathlib import Path

import yaml
from pydantic import BaseModel
from pydantic_settings import BaseSettings, SettingsConfigDict

BASE_DIR = Path(__file__).resolve().parent.parent
CONFIG_PATH = BASE_DIR / "config.yaml"


class AppSettings(BaseModel):
    """Settings for application.

    Attributes:
        root_path (str): Path to root directory of app.

    """

    root_path: str


class DatabaseSettings(BaseModel):
    """Settings for the database.

    Attributes:
        url (str): URL of database connection.
        echo (bool): Flag to enable logging of SQL queries in console.

    """

    url: str
    echo: bool


class AuthenticationJWT(BaseModel):
    """Class for work with JWT authentication using public and private keys.

    Attributes:
        private_key_path (Path): Path to private key file for JWT signature.
        public_key_path (Path): Path to public key file for verifying the JWT
        signature.

    """

    privave_key_path: Path
    public_key_path: Path
    algorithm: str


class Settings(BaseSettings):
    """Main class for application settings.

    Class combines all app settings, including settings for
    app, database, and other configurations.

    Attributes:
        app (AppSettings): Application settings.
        database (DatabaseSettings): Database settings.
        jwt (AuthenticationJWT): JWT settings.

    Methods:
        from_yaml(path:Path): Loads config from YAML file.

    """

    app: AppSettings
    database: DatabaseSettings
    jwt: AuthenticationJWT

    model_config = SettingsConfigDict(validate_default=True)

    @classmethod
    def from_yaml(cls, path: Path):
        """Load settings from YAML file and returns `Settings` object.

        Method read YAML file using path and downloads data
        and passes them to class to create object with configuration files
        settings. All fields specified in model will be updated
        validate using Pydantic.

        Parameters
        ----------
            path: Path to YAML config file.

        Returns
        -------
            Settings: Obj of `Settings' class containing downloaded
            settings.

        """
        if not path.exists():
            raise FileNotFoundError(f"Config file not found: {path}")
        with path.open("r", encoding="utf-8") as file:
            data = yaml.safe_load(file)
        return cls(**data)


settings = Settings.from_yaml(CONFIG_PATH)
