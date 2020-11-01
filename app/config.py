import os


def get_env_variable(name: str) -> str:
    try:
        return os.environ[name]
    except KeyError:
        message = f"expected environment variable {name} not set."
        raise Exception(message)


class Config:
    POSTGRES_HOST = get_env_variable("POSTGRES_HOST")
    POSTGRES_PORT = get_env_variable("POSTGRES_PORT")
    POSTGRES_USER = get_env_variable("POSTGRES_USER")
    POSTGRES_DB_NAME = get_env_variable("POSTGRES_DB_NAME")
    POSTGRES_PASSWORD = get_env_variable("POSTGRES_PASSWORD")
    SQLALCHEMY_DATABASE_URI = f"postgres://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB_NAME}"
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    CORS_ORIGINS = get_env_variable("CORS_ORIGINS")
    CORS_METHODS = get_env_variable("CORS_METHODS")
    CORS_HEADERS = get_env_variable("CORS_HEADERS")

    HERRENCORP_BASE_URL = get_env_variable('HERRENCORP_BASE_URL')
    HERRENCORP_SEND_MAIL_URL = get_env_variable("HERRENCORP_SEND_MAIL_URL")
    HERRENCORP_GET_MAIL_URL = get_env_variable("HERRENCORP_GET_MAIL_URL")
    HERRENCORP_MAIL_AUTH = get_env_variable("HERRENCORP_MAIL_AUTH")


class DevelopmentConfig(Config):
    DEBUG = True


class TestConfig(Config):
    DEBUG = True
    TESTING = True
    POSTGRES_DB_NAME = get_env_variable("POSTGRES_TEST_DB_NAME")


class ProductionConfig(Config):
    DEBUG = False


config_by_name = dict(
    dev=DevelopmentConfig,
    test=TestConfig,
    prod=ProductionConfig
)
