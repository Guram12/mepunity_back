# MepUnity Backend

This is the backend application for MepUnity, a company specializing in electrical, mechanical, and plumbing projects. The backend is built using Django and Django REST Framework, and it provides APIs for managing projects, user authentication, and other related functionalities.



## Installation

1. Clone the repository:

```
git clone https://github.com/Guram12/mepunity_back.git
cd mepunity_back
```

2. Create and activate a virtual environment:

```
python3 -m venv venv
source venv/bin/activate
```

3. Install the dependencies:

```
pip install -r requirements.txt
```

## Configuration

1. Create a .env file in the root directory and add the following environment variables:

```
DB_NAME=your_db_name
DB_USER=your_db_user
DB_PASSWORD=your_db_password
DB_HOST=your_db_host
DB_PORT=your_db_port

AWS_ACCESS_KEY_ID=your_aws_access_key_id
AWS_SECRET_ACCESS_KEY=your_aws_secret_access_key
AWS_STORAGE_BUCKET_NAME=your_aws_storage_bucket_name
AWS_S3_REGION_NAME=your_aws_s3_region_name

EMAIL_HOST_USER=your_email_host_user
EMAIL_HOST_PASSWORD=your_email_host_password
DEFAULT_FROM_EMAIL=your_default_from_email

GOOGLE_CLIENT_ID=your_google_client_id
GOOGLE_CLIENT_SECRET=your_google_client_secret
```

2. Apply the database migrations:

```
python manage.py makemigrations
python manage.py migrate
```


3. Create a superuser:

```
python manage.py createsuperuser
```


### Running the Application

```
python manage.py runserver
```

## API Endpoints

### Authentication

* POST /auth/registration/ - Register a new user
* POST /auth/login/ - Login a user
* POST /auth/logout/ - Logout a user
* POST /auth/token/ - Obtain JWT token
* POST /auth/token/refresh/ - Refresh JWT token
* POST /auth/token/verify/ - Verify JWT token

### User Profile

* GET /auth/profile/ - Get user profile
* PUT /auth/profile/complite/ - Complete user profile
* PUT /auth/profile/update/ - Update user profile


### Projects

* GET /api/projects/ - List all projects
* POST /api/projects/ - Create a new project
* GET /api/projects/{id}/ - Retrieve a project
* PUT /api/projects/{id}/ - Update a project
* DELETE /api/projects/{id}/ - Delete a project


### Minimum Space

* GET /api/minimum-space/ - List all minimum space entries
* POST /api/minimum-space/ - Create a new minimum space entry
* GET /api/minimum-space/{id}/ - Retrieve a minimum space entry
* PUT /api/minimum-space/{id}/ - Update a minimum space entry


### Project Services

* GET /api/project-services/ - List all project services


### File Upload

* POST /api/send-file/ - Send file to email


## Authentication

his application uses JWT for authentication. You can obtain a JWT token by sending a POST request to /auth/token/ with your username and password. Use the obtained token to authenticate subsequent requests by including it in the Authorization header as Bearer <token>.

## Email Functionality

The application supports sending emails using the SMTP settings configured in the .env file. It uses AWS S3 for storing uploaded files and includes functionality to send these files via email.

## Static and Media Files

Static and media files are served using AWS S3. Ensure that your AWS credentials and bucket settings are correctly configured in the .env file.