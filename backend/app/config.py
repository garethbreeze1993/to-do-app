import os
from pydantic import BaseSettings

database_username = os.getenv('DATABASE_USERNAME', 'POSTGRES')
database_password = os.getenv('DATABASE_PASSWORD', '<PASSWORD>')
database_hostname = os.getenv('DATABASE_HOSTNAME', 'localhost')
database_port = os.getenv('DATABASE_PORT', '5432')
database_name = os.getenv('DATABASE_NAME', 'postgres')
secret_key = os.getenv('SECRET_KEY', 'secret')
algorithm = os.getenv('ALGORITHM', 'HS256')
access_token_expire_minutes = os.getenv('ACCESS_TOKEN_EXPIRE_MINUTES', 60)
refresh_secret_key = os.getenv('REFRESH_SECRET_KEY', 'secret')
refresh_token_expire_minutes = os.getenv('REFRESH_TOKEN_EXPIRE_MINUTES', 60)
broker_protocol = os.getenv('BROKER_PROTOCOL', 'ampq')
broker_username = os.getenv('BROKER_USERNAME')
broker_password = os.getenv('BROKER_PASSWORD', '<PASSWORD>')
broker_host = os.getenv('BROKER_HOST', 'localhost')
broker_port = os.getenv('BROKER_PORT', '1234')
broker_vhost = os.getenv('BROKER_VHOST', 'localhost')
path_backend_dir = os.getenv('PATH_BACKEND_DIR', '')
email_sender = os.getenv('EMAIL_SENDER', '<EMAIL>')
email_app_password = os.getenv('EMAIL_APP_PASSWORD', '<PASSWORD>')




class Settings(BaseSettings):
    database_password: str = database_password
    database_username: str = database_username
    database_hostname: str = database_hostname
    database_port: str = database_port
    database_name: str = database_name
    secret_key: str = secret_key
    algorithm: str = algorithm
    access_token_expire_minutes: int = access_token_expire_minutes
    refresh_secret_key: str = refresh_secret_key
    refresh_token_expire_minutes: int = refresh_token_expire_minutes
    broker_protocol: str = broker_protocol
    broker_username: str = broker_username
    broker_password: str = broker_password
    broker_host: str = broker_host
    broker_port: int = broker_port
    broker_vhost: str = broker_vhost
    path_backend_dir: str = path_backend_dir
    email_sender: str = email_sender
    email_app_password: str = email_app_password

    class Config:
        env_file = './.env'


settings = Settings()
