from pydantic import BaseSettings


class Settings(BaseSettings):
    database_password: str
    database_username: str
    database_hostname: str
    database_port: str
    database_name: str
    secret_key: str
    algorithm: str
    access_token_expire_minutes: int
    refresh_secret_key: str
    refresh_token_expire_minutes: int
    broker_protocol: str
    broker_username: str
    broker_password: str
    broker_host: str
    broker_port: int
    broker_vhost: str
    path_backend_dir: str
    email_sender: str
    email_app_password: str

    class Config:
        env_file = './.env'


settings = Settings()
