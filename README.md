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

- [Auth](#auth)
- [Calculator](#calculator)
- [Car posts](#car-posts)
- [Files](#files)

## Auth

### Register User API

The Register User API allows new users to create an account by providing their name, email, and password. The registration process includes password validation to ensure security.

#### Endpoint

- **URL**: `/api/register`
- **Method**: `POST`

#### Request Body

```json
{
  "name": "string",
  "email": "string",
  "password": "string"
}
```

#### Response

- **Success**: Returns the created user data (excluding the password).

  - **Status Code**: `201 Created`
  - **Response Body**:
    ```json
    {
      "id": "integer",
      "name": "string",
      "email": "string"
    }
    ```

- **Error**: Returns an error message if the password validation fails or if the provided data is invalid.
  - **Status Code**: `400 Bad Request`
  - **Response Body**:
    ```json
    {
      "error": "string"
    }
    ```

#### Password Validation

The password must pass the following validators:

- **UserAttributeSimilarityValidator**: Ensures the password is not too similar to the user's other attributes.
- **MinimumLengthValidator**: Ensures the password has a minimum length.
- **CommonPasswordValidator**: Prevents the use of common passwords.
- **NumericPasswordValidator**: Ensures the password is not entirely numeric.

#### Example Request

```bash
curl -X POST "http://localhost:8000/api/register" \
-H "Content-Type: application/json" \
-d '{
  "name": "John Doe",
  "email": "john.doe@example.com",
  "password": "SecureP@ssw0rd"
}'
```

#### Example Response

```json
{
  "id": 1,
  "name": "John Doe",
  "email": "john.doe@example.com"
}
```

### Login User API

Login view handles user authentication and JWT token generation.
This view allows users to log in by providing their email and password. Upon successful authentication, a JWT token is generated and set as an HTTP-only cookie in the response.

#### Endpoint

- **URL**: `/api/login`
- **Method**: `POST`

#### Request Body

```json
{
  "email": "string",
  "password": "string"
}
```

#### Response

- **Success**: Returns the JWT token for the authenticated user.

  - **Status Code**: `200 OK`
  - **Response Body**:
    ```json
    {
      "jwt": "string"
    }
    ```

- **Error**: Returns an error message if the authentication fails or if the provided data is invalid.

  - **Status Code**: `403 Forbidden`
  - Raises **AuthenticationFailed**

#### Example Request

```bash
curl -X POST "http://localhost:8000/api/login" \
-H "Content-Type: application/json" \
-d '{
  "email": "john.doe@example.com",
  "password": "SecureP@ssw0rd"
}'
```

#### Example Response

```json
{
  "jwt": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..."
}
```

### Get User API

The Get User API allows authenticated users to retrieve their own user data. This endpoint ensures that only authenticated users can access their personal information.

#### Endpoint

- **URL**: `/api/user`
- **Method**: `GET`

#### Request

- **Headers**:
  - `Authorization`: `Bearer <JWT token>`

#### Response

- **Success**: Returns the authenticated user's data.

  - **Status Code**: `200 OK`
  - **Response Body**:
    ```json
    {
      "id": "integer",
      "name": "string",
      "email": "string"
    }
    ```

- **Error**: Returns an error message if the user is not authenticated.

  - **Status Code**: `403 Forbidden`
  - **Response Body**:
    ```json
    {
      "detail": "Unauthenticated"
    }
    ```

#### Example Request

```bash
curl -X GET "http://localhost:8000/api/user" \
-H "Authorization: Bearer <JWT token>"
```

#### Example Response

```json
{
  "id": 1,
  "name": "John Doe",
  "email": "john.doe@example.com"
}
```

### Update User API

The Update User API allows authenticated users to update their account information, including their password. This endpoint ensures that only authenticated users can update their personal information.

#### Endpoint

- **URL**: `/api/update-user`
- **Method**: `PUT`

#### Request

- **Headers**:

  - `Authorization`: `Bearer <JWT token>`

- **Body**:
  ```json
  {
    "name": "string",
    "password": "string"
  }
  ```

#### Response

- **Success**: Returns the updated user data.

  - **Status Code**: `200 OK`
  - **Response Body**:
    ```json
    {
      "id": "integer",
      "name": "string",
      "email": "string"
    }
    ```

- **Error**: Returns an error message if the update fails or if the provided data is invalid.

  - **Status Code**: `400 Bad Request`
  - **Response Body**:
    ```json
    {
      "error": "string"
    }
    ```

#### Example Request

```bash
curl -X PUT "http://localhost:8000/api/update-user" \
-H "Authorization: Bearer <JWT token>" \
-H "Content-Type: application/json" \
-d '{
  "name": "Jane Doe",
  "password": "NewSecureP@ssw0rd"
}'
```

#### Example Response

```json
{
  "id": 1,
  "name": "Jane Doe",
  "email": "jane.doe@example.com"
}
```

### Logout User API

The Logout User API allows authenticated users to log out by deleting the JWT token stored in the HTTP-only cookie. This endpoint ensures that the user's session is terminated securely.

#### Endpoint

- **URL**: `/api/logout`
- **Method**: `POST`

#### Request

- **Headers**:
  - `Authorization`: `Bearer <JWT token>`

#### Response

- **Success**: Confirms that the user has been logged out successfully.

  - **Status Code**: `200 OK`
  - **Response Body**:
    ```json
    {
      "message": "success"
    }
    ```

- **Error**: Returns an error message if the logout process fails.

  - **Status Code**: `400 Bad Request`
  - **Response Body**:
    ```json
    {
      "error": "string"
    }
    ```

#### Example Request

```bash
curl -X POST "http://localhost:8000/api/logout" \
-H "Authorization: Bearer <JWT token>"
```

#### Example Response

```json
{
  "message": "success"
}
```

### Delete User API

The Delete User API allows authenticated users to delete their own account. This endpoint ensures that only authenticated users can delete their personal information.

#### Endpoint

- **URL**: `/api/delete-user`
- **Method**: `DELETE`

#### Request

- **Headers**:
  - `Authorization`: `Bearer <JWT token>`

#### Response

- **Success**: Confirms that the user has been deleted successfully.

  - **Status Code**: `204 No Content`

- **Error**: Returns an error message if the deletion process fails.

  - **Status Code**: `400 Bad Request`
  - **Response Body**:
    ```json
    {
      "error": "string"
    }
    ```

#### Example Request

```bash
curl -X DELETE "http://localhost:8000/api/delete-user" \
-H "Authorization: Bearer <JWT token>"
```

#### Example Response

```json
{
  "message": "User deleted successfully"
}
```

## Calculator

### Add Calculator Entry API

The Add Calculator Entry API allows authenticated users to add a new calculator entry to their account.

#### Endpoint

- **URL**: `/api/add-calculator-entry`
- **Method**: `POST`

#### Request Body

```json
{
  "app_income": "number",
  "commission": "number",
  "expenses": "number",
  "earnings": "number"
}
```

#### Response

- **Success**: Returns the created calculator entry data.

  - **Status Code**: 200 OK
  - **Response Body**:
    ```json
    {
      "id": "integer",
      "app_income": "string",
      "comission": "string",
      "expenses": "string",
      "earnings": "string",
      "date": "date"
    }
    ```

- **Error**: Returns an error message if the provided data is invalid.

  - **Status Code**: `400 Bad Request`
  - **Response Body**:
    ```json
    {
      "error": "string"
    }
    ```

#### Example Request

```bash
curl -X POST "http://localhost:8000/api/add-calculator-entry" \
-H "Authorization: Bearer <JWT token>" \
-H "Content-Type: application/json" \
-d '{
  "app_income": "1000",
  "earnings": "1000",
}'
```

#### Example Response

```json
{
  "id": 1,
  "app_income": "1000",
  "comission": null,
  "expenses": null,
  "earnings": 1000,
  "date": "2024-10-16T15:56:47.167956+03:00"
}
```

### Get Calculator Entries API

The Get Calculator Entries API allows authenticated users to retrieve their calculator entries, with pagination support to manage large datasets. This ensures that the frontend can sort the data without having to handle large data sets directly.

#### Endpoint

- **URL**: `/api/get-calculator-entries`
- **Method**: `GET`

#### Request

- **Headers**:

  - `Authorization`: `Bearer <JWT token>`

- **Query Parameters**:
  - `page`: The page number to retrieve (default is 1).

#### Response

- **Success**: Returns a paginated list of calculator entries for the authenticated user.

  - **Status Code**: `200 OK`
  - **Response Body**:
    ```json
    {
      "data": [
        {
          "id": "integer",
          "app_income": "number",
          "commission": "number",
          "expenses": "number",
          "earnings": "number",
          "date": "date"
        }
      ],
      "count": "integer",
      "pagination": {
        "current_page": "integer",
        "total_pages": "integer",
        "has_previous": "boolean",
        "has_next": "boolean",
        "previous_page_number": "integer or null",
        "next_page_number": "integer or null"
      }
    }
    ```

- **Error**: Returns an error message if the page number is invalid or out of range.

  - **Status Code**: `400 Bad Request`
  - **Response Body**:
    ```json
    {
      "error": "string"
    }
    ```

#### Example Request

```bash
curl -X GET "http://localhost:8000/api/get-calculator-entries?page=1" \
-H "Authorization: Bearer <JWT token>"
```

#### Example Response

```json
{
  "data": [
    {
      "id": 1,
      "app_income": "1000",
      "commission": "100",
      "expenses": "50",
      "earnings": "850",
      "date": "2024-10-16T15:56:47.167956+03:00"
    }
  ],
  "count": 1,
  "pagination": {
    "current_page": 1,
    "total_pages": 1,
    "has_previous": false,
    "has_next": false,
    "previous_page_number": null,
    "next_page_number": null
  }
}
```

### Get Recent Calculator Entries API

The Get Recent Calculator Entries API allows authenticated users to retrieve their calculator entries from the past 7, 30, or 90 days.

- Recent calculator entries serve as the data source for generating charts on the frontend dashboard, providing users with visual insights into their earnings over the selected period.
- These entries are ordered by publication date, ensuring that the frontend does not need to handle sorting for chart generation.

#### Endpoint

- **URL**: `/api/get-recent-calculator-entries`
- **Method**: `GET`

#### Request

- **Headers**:

  - `Authorization`: `Bearer <JWT token>`

- **Query Parameters**:
  - `days`: The number of days to look back (must be 7, 30, or 90). Default is 7.

#### Response

- **Success**: Returns a list of recent calculator entries for the authenticated user.

  - **Status Code**: `200 OK`
  - **Response Body**:
    ```json
    {
      "data": [
        {
          "id": "integer",
          "app_income": "string",
          "commission": "string",
          "expenses": "string",
          "earnings": "string",
          "date": "date"
        }
      ]
    }
    ```

- **Error**: Returns an error message if the `days` parameter is invalid.

  - **Status Code**: `400 Bad Request`
  - **Response Body**:
    ```json
    {
      "detail": "Invalid number of days. Must be 7, 30, or 90."
    }
    ```

#### Example Request

```bash
curl -X GET "http://localhost:8000/api/get-recent-calculator-entries?days=30" \
-H "Authorization: Bearer <JWT token>"
```

#### Example Response

```json
{
  "data": [
    {
      "id": 1,
      "app_income": "1000",
      "commission": "100",
      "expenses": "50",
      "earnings": "850",
      "date": "2024-10-16T15:56:47.167956+03:00"
    }
  ]
}
```

### Update Calculator Entry API

The Update Calculator Entry API allows authenticated users to update an existing calculator entry. This endpoint ensures that only the owner of the entry can make updates.

#### Endpoint

- **URL**: `/api/update-calculator-entry/<calcentry_id>`
- **Method**: `PATCH`

#### Request

- **Headers**:

  - `Authorization`: `Bearer <JWT token>`

- **Body**:
  ```json
  {
    "app_income": "string",
    "commission": "string",
    "expenses": "string",
    "earnings": "string"
  }
  ```

#### Response

- **Success**: Returns the updated calculator entry data.

  - **Status Code**: `200 OK`
  - **Response Body**:
    ```json
    {
      "id": "integer",
      "app_income": "string",
      "commission": "string",
      "expenses": "string",
      "earnings": "string",
      "date": "date"
    }
    ```

- **Error**: Returns an error message if the update fails or if the user does not have permission to update the entry.

  - **Status Code**: `403 Forbidden`
  - **Response Body**:
    ```json
    {
      "detail": "You do not have permission to edit this entry."
    }
    ```

#### Example Request

```bash
curl -X PATCH "http://localhost:8000/api/update-calculator-entry/1" \
-H "Authorization: Bearer <JWT token>" \
-H "Content-Type: application/json" \
-d '{
  "app_income": "1200",
  "commission": "150",
  "expenses": "60",
  "earnings": "990"
}'
```

#### Example Response

```json
{
  "id": 1,
  "app_income": "1200",
  "commission": "150",
  "expenses": "60",
  "earnings": "990",
  "date": "2024-10-16T15:56:47.167956+03:00"
}
```

### Delete Calculator Entry API

The Delete Calculator Entry API allows authenticated users to delete an existing calculator entry. This endpoint ensures that only the owner of the entry can delete it.

#### Endpoint

- **URL**: `/api/delete-calculator-entry/<calcentry_id>`
- **Method**: `DELETE`

#### Request

- **Headers**:
  - `Authorization`: `Bearer <JWT token>`

#### Response

- **Success**: Confirms that the calculator entry has been deleted successfully.

  - **Status Code**: `204 No Content`

- **Error**: Returns an error message if the user does not have permission to delete the entry or if the entry does not exist.
  - **Status Code**: `403 Forbidden`
  - **Response Body**:
    ```json
    {
      "detail": "You do not have permission to delete this entry."
    }
    ```

#### Example Request

```bash
curl -X DELETE "http://localhost:8000/api/delete-calculator-entry/1" \
-H "Authorization: Bearer <JWT token>"
```

#### Example Response

```json
{
  "message": "Calculator entry deleted successfully"
}
```

## Car posts

### Add Car Post API

The Add Car Post API allows authenticated users to add a new car post to their account.
For more information on how the image upload and linkage to post is handled, refer to the [Files](#files) section.

#### Endpoint

- **URL**: `/api/add-carpost`
- **Method**: `POST`

#### Request Body

```json
{
  "car_name": "string",
  "model": "string",
  "version": "string",
  "year": "string",
    ...

}
```

#### Response

- **Success**: Returns the created car post data.

  - **Status Code**: `201`
  - **Response Body**:
    ```json
    {
      "id": "integer",
      "car_name": "string",
      "model": "string",
      "version": "string",
      "year": "string",
      ...
    }
    ```

- **Error**: Returns an error message if the provided data is invalid.

  - **Status Code**: `400 Bad Request`
  - **Response Body**:
    ```json
    {
      "error": "string"
    }
    ```

#### Example Request

```bash
curl -X POST "http://localhost:8000/api/add-carpost" \
-H "Authorization: Bearer <JWT token>" \
-H "Content-Type: application/json" \
-d '{
  "car_name": "Volvo",
  "model": "XC90",
  "version": null,
  "year": "2010"
}'
```

#### Example Response

```json
{
  "id": 1,
  "user": 2,
  "created_at": "2024-10-16T15:56:47.167956+03:00",
  "car_name": "Volvo",
  "model": "XC90",
  "version": null,
  "year": "2010",
  "engine": null,
  "fuel": null,
  "body": null,
  "transmission": null,
  "gear_number": null,
  "color": null,
  "seat_number": null,
  "door_number": null,
  "milleage": null,
  "power": null,
  "mpg": null,
  "description": null,
  "emission_standard": null,
  "location": null,
  "contact": null,
  "price": null
}
```

### Get All Car Posts API

The Get All Car Posts API allows authenticated users to retrieve a paginated list of all car posts. This endpoint ensures that users can browse through car posts efficiently.

#### Endpoint

- **URL**: `/api/get-carposts/<path:page>`
- **Method**: `GET`

#### Request

- **Headers**:
  - `Authorization`: `Bearer <JWT token>`

#### Response

- **Success**: Returns a paginated list of car posts.

  - **Status Code**: `200 OK`
  - **Response Body**:
    ```json
    {
      "data": [
        {
          "id": "integer",
          "car_name": "string",
          "model": "string",
          "version": "string",
          "year": "string",
          ...
        }
      ],
      "count": "integer",
      "pagination": {
        "current_page": "integer",
        "total_pages": "integer",
        "has_previous": "boolean",
        "has_next": "boolean",
        "previous_page_number": "integer or null",
        "next_page_number": "integer or null"
      }
    }
    ```

- **Error**: Returns an error message if the page number is invalid or out of range.

  - **Status Code**: `400 Bad Request`
  - **Response Body**:
    ```json
    {
      "error": "string"
    }
    ```

#### Example Request

```bash
curl -X GET "http://localhost:8000/api/get-carposts/1" \
-H "Authorization: Bearer <JWT token>"
```

#### Example Response

```json
{
  "data": [
    {
      "id": 1,
      "car_name": "Volvo",
      "model": "XC90",
      "version": null,
      "year": "2010",
      ...
    }
  ],
  "count": 1,
  "pagination": {
    "current_page": 1,
    "total_pages": 1,
    "has_previous": false,
    "has_next": false,
    "previous_page_number": null,
    "next_page_number": null
  }
}
```

### Get User Car Posts API

The Get User Car Posts API allows authenticated users to retrieve their own car posts. This endpoint functions similarly to the Get All Car Posts API but filters the results to only include car posts associated with the current user.

#### Endpoint

- **URL**: `/api/get-user-carposts`
- **Method**: `GET`

### Get Single Car Post API

The Get Single Car Post API allows authenticated users to retrieve a specific car post by its ID. This endpoint ensures that users can view detailed information about a particular car post.

#### Endpoint

- **URL**: `/api/get-carpost/<car_post_id>`
- **Method**: `GET`

#### Request

- **Headers**:
  - `Authorization`: `Bearer <JWT token>`

#### Response

- **Success**: Returns the car post data for the specified ID.

  - **Status Code**: `200 OK`
  - **Response Body**:
    ```json
    {
      "id": "integer",
      "car_name": "string",
      "model": "string",
      "version": "string",
      "year": "string",
      ...
    }
    ```

- **Error**: Returns an error message if the car post does not exist or if the user is not authenticated.

  - **Status Code**: `404 Not Found`
  - **Response Body**:
    ```json
    {
      "detail": "Not found."
    }
    ```

#### Example Request

```bash
curl -X GET "http://localhost:8000/api/get-carpost/1" \
-H "Authorization: Bearer <JWT token>"
```

#### Example Response

```json
{
  "id": 1,
  "car_name": "Volvo",
  "model": "XC90",
  "version": null,
  "year": "2010",
  ...
}
```

### Update Car Post API

The Update Car Post API allows authenticated users to update an existing car post. This endpoint ensures that only the owner of the car post can make updates.

#### Endpoint

- **URL**: `/api/update-carpost/<car_post_id>`
- **Method**: `PUT`

#### Image Upload Process for Car Post

Handles the image upload process for a car post.

This function performs the following steps:

- Checks if a file associated with the car post already exists.
- If a file exists and an image is provided in the request:
  - Validates the image size.
  - Generates a presigned URL for updating the image from the AWS S3 Bucket.
  - Puts the image to S3 using the presigned URL.
  - Returns an error response if the upload fails.
- If no file exists and an image is provided in the request:
  - Validates the image size.
  - Generates presigned data for uploading the image to S3.
  - Extracts the presigned URL and fields from the presigned data.
  - Uploads the image to S3 using the presigned URL and fields.
  - Returns an error response if the upload fails.
  - Marks the upload process as finished by updating the file record.

#### Parameters:

- **request**: The HTTP request object containing the image file.
- **car_post_id**: The car post object associated with the file.

#### Returns:

- **Response**: An HTTP response indicating the success or failure of the image upload process.

#### Request

- **Headers**:

  - `Authorization`: `Bearer <JWT token>`

- **Body**:
  ```json
  {
    "car_name": "string",
    "model": "string",
    "version": "string",
    "year": "string",
    ...
  }
  ```

#### Response

- **Success**: Returns the updated car post data.

  - **Status Code**: `200 OK`
  - **Response Body**:
    ```json
    {
      "id": "integer",
      "car_name": "string",
      "model": "string",
      "version": "string",
      "year": "string",
      ...
    }
    ```

- **Error**: Returns an error message if the update fails or if the user does not have permission to update the car post.

  - **Status Code**: `403 Forbidden`
  - **Response Body**:
    ```json
    {
      "detail": "You do not have permission to edit this car post."
    }
    ```

#### Example Request

```bash
curl -X PUT "http://localhost:8000/api/update-carpost/1" \
-H "Authorization: Bearer <JWT token>" \
-H "Content-Type: application/json" \
-d '{
  "car_name": "Volvo",
  "model": "XC90",
  "version": "T6",
  "year": "2015"
}'
```

#### Example Response

```json
{
  "id": 1,
  "car_name": "Volvo",
  "model": "XC90",
  "version": "T6",
  "year": "2015",
  ...
}
```

### Delete Car Post API

The Delete Car Post API allows authenticated users to delete an existing car post. This endpoint ensures that only the owner of the car post can delete it.

#### Endpoint

- **URL**: `/api/delete-carpost/<car_post_id>`
- **Method**: `DELETE`

#### Request

- **Headers**:
  - `Authorization`: `Bearer <JWT token>`

#### Response

- **Success**: Confirms that the car post has been deleted successfully.

  - **Status Code**: `204 No Content`

- **Error**: Returns an error message if the user does not have permission to delete the car post or if the car post does not exist.
  - **Status Code**: `403 Forbidden`
  - **Response Body**:
    ```json
    {
      "detail": "You do not have permission to delete this car post."
    }
    ```

#### Example Request

```bash
curl -X DELETE "http://localhost:8000/api/delete-carpost/1" \
-H "Authorization: Bearer <JWT token>"
```

#### Example Response

```json
{
  "message": "Car post deleted successfully"
}
```

## Files

### Start Direct Upload API

The Start Direct Upload API allows authenticated users to initiate the file upload process by generating a presigned URL for direct upload to AWS S3.

- Files are linked to a created post via a Foreign Key set to CASCADE on delete, ensuring that associated file entries and AWS S3 bucket files are removed when a car post is deleted.

#### Endpoint

- **URL**: `/api/upload/direct/start`
- **Method**: `POST`

#### Request Body

```json
{
  "file_name": "string",
  "file_type": "string",
  "car_post_id": "integer"
}
```

#### Response

- **Success**: Returns the presigned URL and additional data required for the direct upload.

  - **Status Code**: `200 OK`
  - **Response Body**:
    ```json
    {
      "id": "integer",
      "url": "string",
      "fields": {
        "acl": "string",
        "key": "string",
        "policy": "string",
        "x-amz-algorithm": "string",
        "x-amz-credential": "string",
        "x-amz-date": "string",
        "x-amz-signature": "string"
      }
    }
    ```

- **Error**: Returns an error message if the request data is invalid or if the user does not have permission to upload the file.

  - **Status Code**: `400 Bad Request`
  - **Response Body**:
    ```json
    {
      "error": "string"
    }
    ```

#### Example Request

```bash
curl -X POST "http://localhost:8000/api/upload/direct/start" \
-H "Authorization: Bearer <JWT token>" \
-H "Content-Type: application/json" \
-d '{
  "file_name": "example.jpg",
  "file_type": "image/jpeg",
  "car_post_id": 1
}'
```

#### Example Response

```json
{
  "url": "https://your-bucket.s3.amazonaws.com/",
  "fields": {

    {
      "id": 1,
      "url": "https://your-bucket.s3.amazonaws.com/",
      "fields": {
        "acl": "public-read",
        "key": "uploads/example.jpg",
        "policy": "eyJleHBpcmF0aW9uIjoiMjAyNC0xMC0xNlQxNTo1Njo0Ny4xNjc5NTZaIiwiY29uZGl0aW9ucyI6W3siYnVja2V0IjoieW91ci1idWNrZXQifSx7ImtleSI6InVwbG9hZHMvZXhhbXBsZS5qcGcifSx7ImFjbCI6InB1YmxpYy1yZWFkIn0seyJjb250ZW50LXR5cGUiOiJpbWFnZS9qcGVnIn1dfQ==",
        "x-amz-algorithm": "AWS4-HMAC-SHA256",
        "x-amz-credential": "AKIAIOSFODNN7EXAMPLE/20241016/us-east-1/s3/aws4_request",
        "x-amz-date": "20241016T155647Z",
        "x-amz-signature": "bWq2s1WEIj+Ydj0vQ697zp1hbx0="
      }
    }
  }
}
```

### Finish Direct Upload API

The Finish Direct Upload API allows authenticated users to mark the file upload process as complete and set the file upload date.

#### Endpoint

- **URL**: `/api/upload/direct/finish`
- **Method**: `POST`

#### Request Body

```json
{
  "car_post_id": "integer",
  "file_name": "string"
}
```

#### Response

- **Success**: Confirms that the file upload process has been completed successfully.

  - **Status Code**: `200 OK`
  - **Response Body**:
    ```json
    {
      "id": "integer"
    }
    ```

- **Error**: Returns an error message if the request data is invalid or if the user does not have permission to complete the upload.

  - **Status Code**: `400 Bad Request`
  - **Response Body**:
    ```json
    {
      "error": "string"
    }
    ```

#### Example Request

```bash
curl -X POST "http://localhost:8000/api/upload/direct/finish" \
-H "Authorization: Bearer <JWT token>" \
-H "Content-Type: application/json" \
-d '{
  "car_post_id": 1,
  "file_name": "example.jpg"
}'
```

#### Example Response

```json
{
  "id": 180
}
```

### Get Image by Car Post ID API

The Get Image by Car Post ID API allows authenticated users to retrieve the image associated with a specific car post.

#### Endpoint

- **URL**: `/api/get-image-by-post-id/<car_post_id>`
- **Method**: `GET`

#### Request

- **Headers**:
  - `Authorization`: `Bearer <JWT token>`

#### Response

- **Success**: Returns the image data for the specified car post ID.

  - **Status Code**: `200 OK`
  - **Response Body**:
    ```json
    {
      "url": "string"
    }
    ```

- **Error**: Returns an error message if the car post does not exist or if the user is not authenticated.

  - **Status Code**: `404 Not Found`
  - **Response Body**:
    ```json
    {
      "message": "The car post does not exist!."
    }
    ```

#### Example Request

```bash
curl -X GET "http://localhost:8000/api/get-image-by-post-id/1" \
-H "Authorization: Bearer <JWT token>"
```

#### Example Response

```json
{
  "url": "https://example-bucket.s3.amazonaws.com/example-bucket--euw2-az2--x-s3/user-1/photos/example-photo.jpg?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Credential=DUMMYCREDENTIAL%2F20241016%2Feu-west-2%2Fs3%2Faws4_request&X-Amz-Date=20241016T161307Z&X-Amz-Expires=3600&X-Amz-SignedHeaders=host&X-Amz-Signature=dummysignature1234567890abcdef"
}
```

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
