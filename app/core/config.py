import os

from dotenv import load_dotenv

load_dotenv()


class JWTConfig:
    algorithm: str = os.getenv("JWT_ALGORITHM")
    secret_key: str = os.getenv("JWT_SECRET_KEY")
    token_time: int = int(os.getenv("JWT_LIFETIME"))


class YandexOAuthConfig:
    client_id: str = os.getenv("YANDEX_CLIENT_ID")
    client_secret: str = os.getenv("YANDEX_CLIENT_SECRET")
    redirect_uri: str = os.getenv("YANDEX_REDIRECT_URI")


class OAuth:
    yandex: YandexOAuthConfig = YandexOAuthConfig()


class DatabaseConfig:
    driver: str = "postgresql+asyncpg"
    user: str = os.getenv("POSTGRES_USER", "postgres")
    password: str = os.getenv("POSTGRES_PASSWORD", "postgres")
    host: str = os.getenv("POSTGRES_HOST", "localhost")
    port: int = int(os.getenv("POSTGRES_PORT", 5432))
    db_name: str = os.getenv("POSTGRES_DB", "default_db")

    echo: bool = os.getenv("DB_ECHO", "False").lower() == "true"
    echo_pool: bool = os.getenv("DB_ECHO_POOL", "False").lower() == "true"
    pool_size: int = int(os.getenv("DB_POOL_SIZE", 10))
    max_overflow: int = int(os.getenv("DB_MAX_OVERFLOW", 50))

    naming_convention: dict[str, str] = {
        "ix": "ix_%(column_0_label)s",
        "uq": "uq_%(table_name)s_%(column_0_N_name)s",
        "ck": "ck_%(table_name)s_%(constraint_name)s",
        "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
        "pk": "pk_%(table_name)s",
    }

    @property
    def url(self) -> str:
        return f"{self.driver}://{self.user}:{self.password}@{self.host}:{self.port}/{self.db_name}"


class Settings:
    db: DatabaseConfig = DatabaseConfig()
    jwt: JWTConfig = JWTConfig()
    oauth: OAuth = OAuth()


settings = Settings()
