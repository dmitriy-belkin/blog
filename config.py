# from pydantic_settings import BaseSettings
#
#
# class Settings(BaseSettings):
#     secret_key: str
#     algorithm: str
#     access_token_expire_minutes: int
#     database_url: str
#
#     class Config:
#         env_file = ".env"
#         env_file_encoding = 'utf-8'
#
#
# settings = Settings()

# class Settings:
#     secret_key: str = "oITbuGu7lvDHvG681C300CH5dOgP2JRN5XBiwcYmp-Y"
#     algorithm: str = "HS256"
#     access_token_expire_minutes: int = 30
#     sentry_dsn: str = "https://f1f2c823d1a967ea8053febf9287b14f@o4507696840638464.ingest.de.sentry.io/4507696842997840"
#     database_url: str = "postgresql+psycopg2://blogger:1234567@localhost/blog"
#
#
# settings = Settings()

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    database_url: str
    secret_key: str
    algorithm: str
    access_token_expire_minutes: int
    sentry_dsn: str

    class Config:
        env_file = ".env"
        env_file_encoding = 'utf-8'


settings = Settings()
