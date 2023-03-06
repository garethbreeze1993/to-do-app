# TO-DO App

This project is a TO-DO App. 
The UI is powered by React using create react app and uses FastAPI to implement the 
"backend logic". Both are included in this repository

## How to use the project

The user is able to sign up and login to the platform.

The fastapi backend uses JWT authentication for users.

Once the user is logged in the user can view, create, complete and delete their tasks.

## See the project in production

A working production version of the project is available at
[https://garethbreeze-todo-app.xyz/](https://garethbreeze-todo-app.xyz/)

## How to run the project locally

After cloning the repository

Make sure you have docker and docker compose installed on your computer

In the top level of the repository on the same level as backend, frontend etc.
Add an .env file with these environment variables

```
DATABASE_PORT=
DATABASE_PASSWORD=
DATABASE_NAME=
DATABASE_USERNAME=
ALGORITHM=
SECRET_KEY=
REFRESH_SECRET_KEY=
ACCESS_TOKEN_EXPIRE_MINUTES=
REFRESH_TOKEN_EXPIRE_MINUTES=
```

After this the easist way to get the project running is to run this command using docker compose

> docker compose -f docker-compose-dev.yml up -d

Then in a browser navigate to localhost:3000 to see the project locally


