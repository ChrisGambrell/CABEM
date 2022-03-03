# flask_template

Sample boilerplate flask project

## Frameworks Used

- Cerberus - input validation
- Flask
- Marshmallow - database schema
- PyJWT
- python-dotenv
- SQLAlchemy - database

## Getting the Code

### Cloning the Git Repository

Run the following command to clone the flask_template Git repository

```
git clone git@github.com:ChrisGambrell/flask_template.git ./flask_template
```

or

```
git clone https://github.com/ChrisGambrell/flask_template.git ./flask_template
```

## Installation

Project is installable using `pip`

```
pip install -e .
```

Add the necessary directories to your `PATH`:

```
Tools/Scripts
```

Generate environment variables:

```
flaskr gen-env
```

## Running

```
flaskr run
```

## Testing

```
flaskr test
```

## Contribute

1. Create new branch & pull request
2. Run `flaskr check-style` to make sure style matches guidelines
3. Run `flaskr test` to make sure there is 100% coverage
4. Push to the pull request
5. Request review
6. Merge into main after review approval

### Change database schemas

This project uses `Flask-Migrate` to manipulate the schemas.

1. Run `export FLASK_APP=Tools/Scripts/migrate.py` to select the migration script
2. Change the schemas to your desired configuration in `flaskr/db.py`
3. Run `flask db migrate -m "Some commit message"` to create a commit. Make sure the message contains the necessary message for how the schema is changing
4. Diagnose and change the generated revision file found in `migrations/versions` for upgrading and downgrading
5. Run `flask db upgrade` to enable to changes to the schemas

## Schemas

### Task

```
class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user = db.relationship('User', back_populates='tasks')
    body = db.Column(db.String, nullable=False)
    completed = db.Column(db.Boolean, default=False)
    updated_at = db.Column(db.DateTime, default=datetime.now(), onupdate=datetime.now(), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.now(), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
```

### User

```
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    username = db.Column(db.String, unique=True, nullable=False)
    password = db.Column(db.String, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.now(), onupdate=datetime.now(), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.now(), nullable=False)
    tasks = db.relationship('Task', back_populates='user', cascade='all, delete')
```

## API Reference

### `GET /hello`

Gets a hello message

Return:

```
hello, world
```

### `GET /secret`

Tests authentication with a greeting

Headers:

```
Authorization: Bearer [token]
```

Return:

```
{
    hello: [name]
}
```

### `POST /auth/login`

Logs in a user

Input:

```
{
    username: <str>,
    password: <str>
}
```

Return:

```
{
    token: <jwt token>
}
```

### `POST /auth/register`

Registers a user

Input:

```
{
    name: <str>,
    username: <str>,
    password: <str>
}
```

Return:

```
{
    User
}
```

### `GET /tasks/`

Get all tasks for authenticated user

Headers:

```
Authorization: Bearer [token]
```

Return:

```
[
    {
        Task
    }
]
```

### `POST /tasks/`

Creates and adds a new task to the database

Headers:

```
Authorization: Bearer [token]
```

Input:

```
{
    body: <str>,
    completed: <bool, nullable>
}
```

Return:

```
{
    Task
}
```

### `GET /tasks/<task_id>`

Gets a task with a certain ID created by the authenticated user

Headers:

```
Authorization: Bearer [token]
```

Return:

```
{
    Task
}
```

### `PATCH /tasks/<task_id>`

Updates a task with a certain ID created by the authenticated user

Headers:

```
Authorization: Bearer [token]
```

Input:

```
{
    body: <str, nullable>,
    completed: <bool, nullable>
}
```

Return:

```
{
    Task
}
```

### `DELETE /tasks/<task_id>`

Deletes a task with a certain ID created by the authenticated user

Headers:

```
Authorization: Bearer [token]
```

Return:

```
{}
```

### `GET /user/`

Gets the authenticated user

Headers:

```
Authorization: Bearer [token]
```

Return:

```
{
    User
}
```

### `PATCH /user/`

Updates the authenticated user

Headers:

```
Authorization: Bearer [token]
```

Input:

```
{
    name: <str, nullable>,
    username: <str, nullable>
}
```

Return:

```
{
    User
}
```

### `DELETE /user/`

Deletes the authenticated user

Headers:

```
Authorization: Bearer [token]
```

Return:

```
{}
```

### `GET /user/<user_id>`

Gets a user by their ID

Headers:

```
Authorization: Bearer [token]
```

Return:

```
{
    User
}
```
