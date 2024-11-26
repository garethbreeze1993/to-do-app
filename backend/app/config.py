import os
from pydantic import BaseSettings

database_username = os.getenv('DATABASE_USERNAME', 'POSTGRES')
database_password = os.getenv('DATABASE_PASSWORD', '<PASSWORD>')
database_hostname = os.getenv('DATABASE_HOSTNAME', 'localhost')
database_port = os.getenv('DATABASE_PORT', '5432')
database_name = os.getenv('DATABASE_NAME', 'postgres')

class Settings(BaseSettings):
    database_password: str = database_password
    database_username: str = database_username
    database_hostname: str = database_hostname
    database_port: str = database_port
    database_name: str = database_name
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
