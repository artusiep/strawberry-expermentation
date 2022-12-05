# User management system

## Prerequisites

- poetry
- python 3.10 (used via poetry)
- docker-compose to initialize and run database

## Installation

Setup application dependencies:
```
poetry install
```

## Usage

1. Start the database:
```
docker-compose up -d
```

2. Create copy of `template.env` -> `.env` filling in `SECRET_KEY` with random value for example: `openssl rand -hex 32`

3. Start the application:
```
poetry shell
python -m home_assignment
```

After executing the last command, application should start up and expose api at: <http://localhost:8081/graphql>

## Description

The application is a user management system.

It distinguishes two kinds of users:
- admin
- regular users

Application require logging in from both types of users before they are able to call other graphql endpoints.
Admin user should be able to `login`, `list all users` and `set users passwords`.
Regular users on the other hand should be able to only `login` and `change their own passwords`.

Each user should have the following properties:
- username
- password
- last password modification date

## Decisions

Authorization used is JWT based, but it would be more user-friendly to use 
<http://localhost:8081/graphql> with cookie based authorization but newest versions 
of graphql supports custom headers and does not require installing browser extensions