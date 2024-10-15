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
  - For more information about the direct upload process implementation and how it works, refer to this [HackSoft article](https://www.hacksoft.io/blog/direct-to-s3-file-upload-with-django).

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

## Database Models

- **User**: Stores user information and authentication details.
- **CarPost**: Stores information about car posts.
- **File**: Stores information about the uploaded files.
- **CalculatorEntry**: Stores data entries for the earnings calculator.

## API Endpoints

- **Auth**

  - `POST /api/register`: Register user.
  - `POST /api/login`: Login user.
  - `POST /api/logout`: Logout user.
  - `GET /api/user`: Get user data.
  - `PUT /api/user-update`: Update user data.
  - `DELETE /api/user-delete`: Delete user account.

- **Calculator**

  - `POST /api/add-calculator-entry`: Create a new calculator entry.
  - `GET /api/get-calculator-entries`: Based on a 'page' query parameter it lists 10 calculator entries.
  - `GET /api/get-recent-calculator-entries`: Based on a 'days' query parameter it retrieves last 7, 30 or 90 days calculator entries.
  - `PATCH /api/update-calculator-entry/calculator-entry-id`: I takes an in positional argument and updates its data.
  - `DELETE /api/delete-calculator-entry/calculator-entry-id`: I deletes the calculator entry based on its id.

- **CarPosts**

  - `POST /api/add-carpost`: Add a car post.
  - `GET /api/get-carposts/page-number`: Retrieves 10 car posts based on a page number positional argument.
  - `GET /api/het-carpost/carpost-id`: Retrieve a specific car post.
  - `GET /api/get-user-carposts/carpost-id`: Retrieve car-posts associated with the current logged in user.
  - `PUT /api/update-ridepost/carpost-id:` Update a specific car post.
  - `DELETE /api/delete-ridepost`: Delete a specific car post.

- **Files**
  - `POST /api/upload/direct/start`: Starts the presigned url generation and stores image data.
  - `POST /api/upload/direct/finish`: Marks the upload process as finished and sets the file upload date.
  - `GET /api/get-image-by-post-id/car-post-id`: Gets the image based on the car post id.

## Running the Project

To run the project locally, follow the setup and installation steps mentioned above. Once the setup is complete, start the development server:

```bash
python manage.py runserver
```

## Frontend Integration

This backend project is designed to work seamlessly with the Rideshare Copilot V2 frontend application. For more details and to access the frontend repository, visit [Rideshare Copilot V2 Frontend Repository](https://github.com/yourusername/rideshare-copilot-frontend).

### Dev Tips

- **Sort Imports with isort**:

  - To sort imports in a specific file:
    ```bash
    isort filename.py
    ```
  - To sort imports for the entire project:
    ```bash
    isort .
    ```
  - To ensure modifications don't introduce syntax errors:
    ```bash
    isort --atomic filename.py
    ```
  - For VS Code users, install the isort extension and add the following to your settings to automatically sort imports on save:
    ```json
    "[python]": {
    "editor.defaultFormatter": "ms-python.black-formatter",
    "editor.formatOnSave": true,
    "editor.codeActionsOnSave": {
      "source.organizeImports": true
    }
    },
    "isort.args": ["--profile", "black"]
    ```
    Use `Shift + Alt + O` to manually sort imports.

- **Format Code with Black**:
  - To format the entire project:
    ```bash
    black .
    ```
  - To format a specific file:
    ```bash
    black filename.py
    ```

3. **Check Code with flake8**:

- To check a specific file for code errors:
  ```bash
  flake8 filename.py
  ```
- To check the current directory:
  ```bash
  flake8 .
  ```
