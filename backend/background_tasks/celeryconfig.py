from app.config import settings

# broker_url = 'amqp://garethrabbit:zPXtW2RK2wtjLbE@localhost:5672/myvhosttodo'
broker_url = f"{settings.broker_protocol}://{settings.broker_username}:{settings.broker_password}" \
             f"@{settings.broker_host}:{settings.broker_port}/{settings.broker_vhost}"


include = ['background_tasks.app_tasks']
result_backend = f'db+postgresql://{settings.database_username}:{settings.database_password}' \
                 f'@{settings.database_hostname}:{settings.database_port}/{settings.database_name}'
