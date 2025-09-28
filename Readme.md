# Project: TODOBOT

<p style="text-align: center;">
<kbd>
</kbd>
</p>
TODOBOT it is a simple Telegram bot for tracking your tasks 
___


## Contents:
- [Description](#description)
- [Installation and starting](#installation-and-starting)

---

## Technologies


**Programming languages and modules:**

[![Python](https://img.shields.io/badge/-python_3.10^-464646?logo=python)](https://www.python.org/)


**Frameworks:**

[![Django](https://img.shields.io/badge/-Django-464646?logo=Django)](https://www.djangoproject.com/)
[![Django REST Framework](https://img.shields.io/badge/-Django%20REST%20Framework-464646?logo=Django)](https://www.django-rest-framework.org/)
[![Aiogram](https://img.shields.io/badge/-Aiogram-464646?logo=telegram)](https://aiogram.dev/)

**Databases:**

[![PostgreSQL](https://img.shields.io/badge/-PostgreSQL-464646?logo=PostgreSQL)](https://www.postgresql.org/)


**Containerization:**

[![docker](https://img.shields.io/badge/-Docker-464646?logo=docker)](https://www.docker.com/)
[![docker_compose](https://img.shields.io/badge/-Docker%20Compose-464646?logo=docker)](https://docs.docker.com/compose/)

[⬆️Contents](#contents)

---

## Installation and starting

<details><summary>Pre-conditions</summary>

It is assumed that the user has installed [Docker](https://docs.docker.com/engine/install/) and [Docker Compose](https://docs.docker.com/compose/install/) on the local machine or on the server where the project will run. You can check if they are installed using the command:

```bash
docker --version && docker-compose --version
```
</details>


Local launch:

1. Clone the repository from GitHub:
```bash
git clone https://github.com/TannedRose/ToDoBot.git
```

1.1 Enter the data for the environment variables in the [.env] file:

```
POSTGRES_DB=
POSTGRES_USER=
POSTGRES_PASSWORD=
POSTGRES_HOST=
BOT_TOKEN=
API_URL=
```


<details><summary>Lounch via Docker: Docker Compose</summary>

2. From the root directory of the project, execute the command:
```bash
docker-compose -f docker-compose up -d --build
```

3. You can stop docker and delete containers with the command from the root directory of the project:
```bash
docker-compose -f docker-compose down
```
add flag -v to delete volumes ```docker-compose -f docker-compose down -v```
</details><h1></h1>

[⬆️Contents](#contents)
