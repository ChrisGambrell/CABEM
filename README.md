# CABEM

SECONDARY BRANCH

`TODO: Add description of project`

## Authors

Chris Gambrell, Another Name

## Frameworks Used

-   Cerberus - input validation
-   Flask
-   Marshmallow - database schema
-   PyJWT
-   python-dotenv
-   SQLAlchemy - database

## Getting the Code

### Cloning the Git Repository

Run the following command to clone the CABEM Git repository

```
git clone git@github.com:ChrisGambrell/CABEM.git ./CABEM
```

or

```
git clone https://github.com/ChrisGambrell/CABEM.git ./CABEM
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

### User

```
class Course(db.Model):
    idCourse = db.Column(db.Integer, nullable=False, primary_key=True)
    CourseTitle = db.Column(db.String(255), default=None)
    CourseStatus = db.Column(db.String(45), default=None)
    idProposal = db.Column(db.Integer, default=None)
    idProgram = db.Column(db.Integer, default=None)
    CourseNumber = db.Column(db.String(45), default=None)
    ProjectedStartDate = db.Column(db.DateTime, default=None)
    CourseStart = db.Column(db.DateTime, default=None)
    CourseEnd = db.Column(db.DateTime, default=None)
    isLaunched = db.Column(db.Integer, default='0')
    MarketingSignoff = db.Column(db.Integer, default='0')
    idUserMarketingSignoff = db.Column(db.Integer, default=None)
    DateMarketingSignoff = db.Column(db.DateTime, default=None)
    CMESignoff = db.Column(db.Integer, default='0')
    idUserCMESignoff = db.Column(db.Integer, default=None)
    DateCMESignoff = db.Column(db.DateTime, default=None)
    MedReviewSignoff = db.Column(db.Integer, default='0')
    idUserMedReviewSignoff = db.Column(db.Integer, default=None)
    DateMedReviewSignoff = db.Column(db.DateTime, default=None)
    AgendaComplete = db.Column(db.Integer, default='0')
    idUserAgendaComplete = db.Column(db.Integer, default=None)
    DateAgendaComplete = db.Column(db.DateTime, default=None)
    DateCreated = db.Column(db.DateTime, default=None)
    DateLastUpdated = db.Column(db.DateTime, default=None)
    idCourseType = db.Column(db.Integer, default=None)
    idUserCreated = db.Column(db.Integer, default=None)
    Renewal = db.Column(db.Integer, default='0')
    NASWApprovalNumber = db.Column(db.Integer, default=None)
    ProposalDueDate = db.Column(db.DateTime, default=None)
    idModule = db.Column(db.Integer, default=None)
    idWorkflowStep = db.Column(db.Integer, default=None)
    idPreviousWorkflowStep = db.Column(db.Integer, default=None)
    Valid = db.Column(db.Integer, default='1')
    idCVentEvent = db.Column(db.Integer, default=None)
    ClosureReason = db.Column(db.String(255), default=None)
    ClosureDescription = db.Column(db.String)
    CVentEventCode = db.Column(db.String(45), default=None)
    IsFree = db.Column(db.Integer, nullable=False, default='0')
    CatalogLinkout = db.Column(db.String(255), default=None)
    isLiveStream = db.Column(db.Integer, nullable=False, default='0')
```

```
class User(db.Model):
    idUser = db.Column(db.Integer, primary_key=True)
    Email = db.Column(db.String(255), unique=True, nullable=False, default='')
    Password = db.Column(db.String(255), nullable=False)
    FirstName = db.Column(db.String(255), nullable=False)
    LastName = db.Column(db.String(255), nullable=False)
    Enabled = db.Column(db.Integer, nullable=False, default='1')
    LoggedIn = db.Column(db.Integer, nullable=False, default='0')
    SecurityQuestion = db.Column(db.String)
    SecurityAnswer = db.Column(db.String)
    StartDate = db.Column(db.DateTime, default=None)
    LastSeen = db.Column(db.DateTime, default=None)
    Img = db.Column(db.String(255), default=None)
    SaltKey = db.Column(db.String(255), nullable=False)
    Phone = db.Column(db.String(20), default=None)
    idAddress = db.Column(db.Integer, default=None)
    PasswordSetDate = db.Column(db.DateTime, default=datetime.utcnow())
    idSecurityQuestion = db.Column(db.Integer, nullable=False, default='0')
    RegistrationSent = db.Column(db.Integer, nullable=False, default='0')
    UseTwoFactor = db.Column(db.Integer, nullable=False, default='0')
    idUserDigestPreference = db.Column(db.Integer, default=None)
    isAdmin = db.Column(db.Integer, default='0')
    isLearner = db.Column(db.Integer, default='0')
    CourseMgt = db.Column(db.Integer, default='0')
    Registered = db.Column(db.Integer, nullable=False, default='0')
    DateOfBirth = db.Column(db.String(255), default=None)
    UpdatedAt = db.Column(db.DateTime, nullable=False, default=datetime.utcnow())
    CreatedAt = db.Column(db.DateTime, nullable=False, default=datetime.utcnow())
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
    Email: <str>,
    Password: <str>
}
```

Return:

```
{
    token: <jwt token>
}
```

### `GET /course/`

Gets all courses

Headers:

```
Authorization: Bearer [token]
```

Return:

```
[
    {
        Course
    }
]
```

### `POST /course/`

Creates a course

Headers:

```
Authorization: Bearer [token]
```

Input:

```
{
    CourseTitle: <str | optional>,
    CourseStatus: <str | optional>,
    idProposal: <int | optional>,
    idProgram: <int | optional>,
    CourseNumber: <str | optional>,
    ProjectedStartDate: <datetime | optional>,
    CourseStart: <datetime | optional>,
    CourseEnd: <datetime | optional>,
    isLaunched: <int | optional>,
    MarketingSignoff: <int | optional>,
    idUserMarketingSignoff: <int | optional>,
    DateMarketingSignoff: <datetime | optional>,
    CMESignoff: <int | optional>,
    idUserCMESignoff: <int | optional>,
    DateCMESignoff: <datetime | optional>,
    MedReviewSignoff: <int | optional>,
    idUserMedReviewSignoff: <int | optional>,
    DateMedReviewSignoff: <datetime | optional>,
    AgendaComplete: <int | optional>,
    idUserAgendaComplete: <int | optional>,
    DateAgendaComplete: <datetime | optional>,
    DateCreated: <datetime | optional>,
    DateLastUpdated: <datetime | optional>,
    idCourseType: <int | optional>,
    idUserCreated: <int | optional>,
    Renewal: <int | optional>,
    NASWApprovalNumber: <int | optional>,
    ProposalDueDate: <datetime | optional>,
    idModule: <int | optional>,
    idWorkflowStep: <int | optional>,
    idPreviousWorkflowStep: <int | optional>,
    Valid: <int | optional>,
    idCVentEvent: <int | optional>,
    ClosureReason: <str | optional>,
    ClosureDescription: <str | optional>,
    CVentEventCode: <str | optional>,
    IsFree: <int | optional>,
    CatalogLinkout: <str | optional>,
    isLiveStream: <int | optional>,
}
```

Return:

```
{
    Course
}
```

### `GET /course/<course_id>`

Gets a course by its ID

Headers:

```
Authorization: Bearer [token]
```

Return:

```
{
    Course
}
```

### `PATCH /course/<course_id>`

Updates a course

Headers:

```
Authorization: Bearer [token]
```

Input:

```
{
    CourseTitle: <str | optional>,
    CourseStatus: <str | optional>,
    idProposal: <int | optional>,
    idProgram: <int | optional>,
    CourseNumber: <str | optional>,
    ProjectedStartDate: <datetime | optional>,
    CourseStart: <datetime | optional>,
    CourseEnd: <datetime | optional>,
    isLaunched: <int | optional>,
    MarketingSignoff: <int | optional>,
    idUserMarketingSignoff: <int | optional>,
    DateMarketingSignoff: <datetime | optional>,
    CMESignoff: <int | optional>,
    idUserCMESignoff: <int | optional>,
    DateCMESignoff: <datetime | optional>,
    MedReviewSignoff: <int | optional>,
    idUserMedReviewSignoff: <int | optional>,
    DateMedReviewSignoff: <datetime | optional>,
    AgendaComplete: <int | optional>,
    idUserAgendaComplete: <int | optional>,
    DateAgendaComplete: <datetime | optional>,
    DateCreated: <datetime | optional>,
    DateLastUpdated: <datetime | optional>,
    idCourseType: <int | optional>,
    idUserCreated: <int | optional>,
    Renewal: <int | optional>,
    NASWApprovalNumber: <int | optional>,
    ProposalDueDate: <datetime | optional>,
    idModule: <int | optional>,
    idWorkflowStep: <int | optional>,
    idPreviousWorkflowStep: <int | optional>,
    Valid: <int | optional>,
    idCVentEvent: <int | optional>,
    ClosureReason: <str | optional>,
    ClosureDescription: <str | optional>,
    CVentEventCode: <str | optional>,
    IsFree: <int | optional>,
    CatalogLinkout: <str | optional>,
    isLiveStream: <int | optional>,
}
```

Return:

```
{
    Course
}
```

### `DELETE /course/<course_id>`

Deletes a course

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

### `POST /user/`

Creates a user

Input:

```
{
    Email: <str>,
    Password: <str>,
    FirstName: <str>,
    LastName: <str>,
    SecurityQuestion: <str | optional>,
    SecurityAnswer: <str | optional>,
    StartDate: <datetime | optional>,
    Img: <str | optional>,
    SaltKey: <str>,
    Phone: <str | optional>,
    CourseMgt: <int | optional>,
    DateOfBirth: <str | optional>,
}
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
    Email: <str>,
    FirstName: <str>,
    LastName: <str>,
    SecurityQuestion: <str | optional>,
    SecurityAnswer: <str | optional>,
    StartDate: <datetime | optional>,
    Img: <str | optional>,
    Phone: <str | optional>,
    CourseMgt: <int | optional>,
    DateOfBirth: <str | optional>,
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
