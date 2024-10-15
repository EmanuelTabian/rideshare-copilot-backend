# Rideshare Copilot V2 Backend

## Description

This app facilitates seamless data flow within the Rideshare Copilot V2 application. It manages user data, file storage, car rental listings, and calculator entries, while providing services to handle database interactions (GET, POST, PUT, DELETE). Additionally, it supports the generation of presigned URLs for secure image uploads to an AWS S3 bucket

## Overview

Django-based platform designed to manage user authentication and database interactions via PostgreSQL. The project contains a wide range of functionalities including user, car rental posts, and earnings calculations interaction, along with customizable user settings. The backend architecture ensures smooth, efficient operations for the Rideshare Copilot V2 app, supporting both data storage and real-time interactions with external services like AWS S3 for media management.It also provides admin access, with management capabilities through Django admin site.

## Table of Contents

- [Features](#features)
- [Tech Stack](#tech-stack)
- [Setup and Installation](#setup-and-installation)
- [Database Models](#database-models)
- [API Endpoints](#api-endpoints)
- [Running the Project](#running-the-project)

## Features

- User Authentication:

  - Registration, login, user update and user deletion services.
  - JWT-based authentication, with tokens valid for 24 hours (token refresh mechanism planned for a future update).
  - Django built-in password strength check.

- Car Post Management:

  - Full CRUD operations (Create, Read, Update, Delete) for car rental posts, allowing users to add, edit, or remove posts through the frontend app's form.
  - User Foreign Key set to CASCADE. Car Posts associated with a removed user automatically get deleted.
  - Car post updates support image uploads, with presigned URLs generated for secure image upload to AWS S3. The app tests two different methods for handling image uploads during car post creation and updates.

- File management:

  - Optional file input for each car post, allowing users to attach pictures.
  - Files are linked to car posts via a Foreign Key set to CASCADE on car-post deletion, ensuring associated file entry and AWS S3 bucket file removal.
  - File database entries store uploaded picture metadata.
  - The API services handle presigned URL generation for safe frontend app/AWS S3 interaction.

- Earnings Calculator:

  - Stores financial data, including app income, comission, expenses, and calculated earnings
  - Provides user access to rideshare earnings history.
  - Financial data is used for frontend app dashboard earnings chart generation.

- User Settings:
  - Allows users to update credentials (username and/or password).
  - Supports account deletion.

## Tech Stack

- **Backend**:

  - **Django**: A high-level Python web framework that encourages rapid development and clean, pragmatic design.
  - **Django REST Framework**: A powerful and flexible toolkit for building Web APIs in Django.
  - **Simple JWT**: A JSON Web Token authentication plugin for the Django REST Framework.

- **Database**:

  - **PostgreSQL**: A powerful, open-source object-relational database system with a strong reputation for reliability, feature robustness, and performance.

- **Storage**:

  - **AWS S3**: Amazon Simple Storage Service, an object storage service offering industry-leading scalability, data availability, security, and performance.

- **Environment Management**:

  - **Virtualenv**: A tool to create isolated Python environments, allowing dependencies to be installed on a per-project basis without interfering with the system-wide Python installation.

- **Code Formatting**:

  - **Black**: An uncompromising Python code formatter that ensures code readability and consistency.
  - **isort**: A Python utility for sorting imports, ensuring PEP8 compliance and improving code readability.

- **Linting**:

  - **flake8**: A tool for enforcing coding style (PEP8), checking for programming errors, and ensuring code quality in Python projects.

- **Deployment**:
  - **Amazon ECS**: A fully managed container orchestration service for deployment, management, and containerized applications scaling.
  - **RDS**: Amazon Relational Database Service, a managed relational database service that provides scalable and resizable database instances.
  - **CloudWatch**: A monitoring and observability service that provides data and actionable insights for AWS, hybrid, and on-premises applications and infrastructure resources.
  - **IAM**: AWS Identity and Access Management, a web service that helps securely control access to AWS services and resources for users.
  - **Route 53**: A scalable and highly available Domain Name System (DNS) web service designed to route end users to Internet applications by translating domain names into IP addresses.

## Setup and Installation

### Prerequisites

- Python 3.x
- PostgreSQL
- Virtualenv
- AWS account (for S3 bucket and IAM roles)

### Installation Steps

1. **Clone the repository**

   ```bash
   git clone https://github.com/yourusername/rideshare-copilot-backend.git
   cd rideshare-copilot-backend
   ```

2. **Create a virtual environment**

   ```bash
   python -m venv env
   source env/bin/activate  # On Windows use `env\Scripts\activate`
   ```

3. **Install dependencies**

   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment variables**

   - Create a `.env` file in the project root.
   - Access `.env.example` for environment variables description.

5. **Set up a PostgreSQL database**:

   - Access PostgreSQL console

     ```bash
         psql -U postgres
     ```

   - Create a database

     ```sql
     CREATE DATABASE your_db;
     CREATE USER rideshare_user WITH PASSWORD 'yourpassword';
     ALTER ROLE rideshare_user SET client_encoding TO 'utf8';
     ALTER ROLE rideshare_user SET default_transaction_isolation TO 'read committed';
     ALTER ROLE rideshare_user SET timezone TO 'UTC';
     GRANT ALL PRIVILEGES ON DATABASE rideshare_copilot_db TO rideshare_user;
     ```

6. **Set up an AWS S3 Storage Bucket with Cloudfront Distribution**.
   For a step-by-step guide on setting up an AWS S3 Storage Bucket with CloudFront Distribution, refer to this [YouTube tutorial](https://www.youtube.com/watch?v=RsiXzwesNLQ&t=1192s).

- **Create an S3 Bucket**

  - Log in to the AWS Management Console.
  - Navigate to the S3 service.
  - Click on "Create bucket".
  - Enter a unique bucket name and select a region.
  - Configure options as needed and click "Create bucket".

- **Set Bucket Permissions**

  - Select the newly created bucket.
  - Go to the "Permissions" tab.
  - Set the appropriate bucket policy to allow access to your application.

- **Create a CloudFront Distribution**

  - Navigate to the CloudFront service in the AWS Management Console.
  - Click on "Create Distribution".
  - Select "Web" as the delivery method.
  - Under "Origin Settings", set the "Origin Domain Name" to your S3 bucket.
  - Configure other settings as needed and click "Create Distribution".

- **Configure CloudFront Distribution**

  - Once the distribution is created, select it from the list.
  - Go to the "Behaviors" tab and click "Create Behavior".
  - Set the "Path Pattern" to `/*` to match all requests.
  - Configure other settings as needed and click "Create".

- **Update CORS Configuration**

  - Go back to your S3 bucket.
  - Navigate to the "Permissions" tab and click on "CORS configuration".
  - Add the necessary CORS rules to allow your application to interact with the bucket.

- **Update Environment Variables**

  - Add the CloudFront distribution URL and S3 bucket name to your `.env` file.
  - Ensure your application uses these variables for media storage and retrieval.

7. **Apply migrations**

   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

8. **Create a superuser**

   ```bash
   python manage.py createsuperuser
   ```

9. **Start the development server**

   ```bash
   python manage.py runserver
   ```

## Database Models

- **User**: Stores user information and authentication details.
- **CarPost**: Stores information about car posts.
- **File**: Stores information about the uploaded files.
- **CalculatorEntry**: Stores data entries for the earnings calculator.

## API Endpoints

- **Auth**
  - `POST /api/auth/login/`: Login user
  - `POST /api/auth/register/`: Register user
  - `POST /api/auth/token/`: Obtain JWT token
  - `POST /api/auth/token/refresh/`: Refresh JWT token
- **User**
  - `GET /api/user/`: Retrieve user information
  - `PUT /api/user/`: Update user information
- **CarPosts**
  - `GET /api/carposts/`: List all car posts
  - `POST /api/carposts/`: Create a new car post
  - `GET /api/carposts/:id/`: Retrieve a specific car post
  - `PUT /api/carposts/:id/`: Update a specific car post
  - `DELETE /api/carposts/:id/`: Delete a specific car post
- **Calculator**
  - `GET /api/calculator/`: List all calculator entries
  - `POST /api/calculator/`: Create a new calculator entry
  - `DELETE /api/calculator/`: Delete a calculator entry
- **Documents**
  - `GET /api/documents/`: List all documents
  - `POST /api/documents/`: Add a new document
- **Settings**
  - `GET /api/settings/`: Retrieve user settings
  - `PUT /api/settings/`: Update user settings

## Running the Project

To run the project locally, follow the setup and installation steps mentioned above. Once the setup is complete, start the development server:

```bash
python manage.py runserver
```

## Dev Tips

1. Run isort [filename.py] to sort the imports, or isort . to apply it for the entire project. Run isort --atomic [filename.py] or . to make sure the modifications don't introduce syntax errors.
   Note: if you install isort VS Code Extention, use Shift + Alt + 0 to format imports or add:

"[python]": {
"editor.defaultFormatter": "ms-python.black-formatter",
"editor.formatOnSave": true,
"editor.codeActionsOnSave": {
"source.organizeImports": true
},
},
"isort.args":["--profile", "black"],

This will automatically sort imports on save.

2. Run black . (inside of the root project folder) or mention a specific file to format code (simmilar to prettier for JS)

3. Use flake8 [filename] or flake8 . (applied for current directory) to check for code errors
