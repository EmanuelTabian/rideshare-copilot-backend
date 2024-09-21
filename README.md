# Rideshare Copilot V2 Backend

## Description

This app ensure data flow through the Rideshare Copilot V2 app.

## Overview

Rideshare Copilot Backend is a Django-based application that manages user authentication and interacts with a PostgreSQL database. This project supports various functionalities such as user management, car posts, earnings calculator, document management, and user settings.

## Table of Contents

- [Features](#features)
- [Tech Stack](#tech-stack)
- [Setup and Installation](#setup-and-installation)
- [Database Models](#database-models)
- [API Endpoints](#api-endpoints)
- [Running the Project](#running-the-project)

## Features

- User Authentication (Registration, Login, JWT-based authentication)
- Car Post Management (CRUD operations)
- Earnings Calculator (Stores data for generating earnings graphs)
- Document Management (Alerts users for expiration dates)
- User Settings (Manage User credentials and dark theme toggle)

## Tech Stack

- **Backend**: Django, Django REST Framework, Simple JWT, Django Allauth
- **Database**: PostgreSQL
- **Authentication**: JWT (JSON Web Token)

## Setup and Installation

### Prerequisites

- Python 3.x
- PostgreSQL
- Virtualenv

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

4. **Set up PostgreSQL database**

   Create a PostgreSQL database and user for the project.

   ```sql
   CREATE DATABASE rideshare_copilot_db;
   CREATE USER rideshare_user WITH PASSWORD 'yourpassword';
   ALTER ROLE rideshare_user SET client_encoding TO 'utf8';
   ALTER ROLE rideshare_user SET default_transaction_isolation TO 'read committed';
   ALTER ROLE rideshare_user SET timezone TO 'UTC';
   GRANT ALL PRIVILEGES ON DATABASE rideshare_copilot_db TO rideshare_user;
   ```

5. **Configure environment variables**

   Create a `.env` file in the project root and add the following:

   ```
   SECRET_KEY=your_secret_key
   DEBUG=True
   DB_NAME=rideshare_copilot_db
   DB_USER=rideshare_user
   DB_PASSWORD=yourpassword
   DB_HOST=localhost
   DB_PORT=5432
   ```

6. **Apply migrations**

   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

7. **Create a superuser**

   ```bash
   python manage.py createsuperuser
   ```

8. **Start the development server**

   ```bash
   python manage.py runserver
   ```

## Database Models

- **User**: Stores user information and authentication details.
- **CarPost**: Stores information about car posts.
- **CalculatorEntry**: Stores data entries for the earnings calculator.
- **Document**: Stores document details and expiration dates.
- **Setting**: Stores user settings and preferences.

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
