from pathlib import Path

import yaml
from argon2 import PasswordHasher
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


class HashPassword(BaseModel):
    """Config for password hashing using Argon2.

    Class defines param for configuring Argon2 password hashing algorithm.
    Settings are used determine time cost, memory cost, parallelism, of the hash
    generation process.

    Attributes:
        time_cost (int): Number iterations for hashing algorithm.
        memory_cost (int): Amount of memory (in KiB) used by the algorithm.
        parallelism (int): Number parallels computations algorithm should
        perform.
        hash_len (int): Length result hash in bytes.
        salt_len (int): Length salt used in hashing process in bytes.
        encoding (str): Encoding for result hash.

    """

    time_cost: int
    memory_cost: int
    parallelism: int
    hash_len: int
    salt_len: int
    encoding: str

    def create_hasher(self) -> PasswordHasher:
        """Create and return config instance PasswordHasher."""
        return PasswordHasher(
            time_cost=self.time_cost,
            memory_cost=self.memory_cost,
            parallelism=self.parallelism,
            hash_len=self.hash_len,
            salt_len=self.salt_len,
            encoding=self.encoding,
        )


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
    hash_password: HashPassword

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
ph = Settings.hash_password.create_hasher()
