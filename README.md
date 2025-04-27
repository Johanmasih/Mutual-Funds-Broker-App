# Mutual-Funds-Broker-App

# 🚀 Funds Management Backend

A Django REST API project for managing Fund Families, Mutual Funds, and Portfolios.  
The Funds Management Backend is a Django-based REST API designed for managing Fund Families, Mutual Funds, and Portfolios. This backend system allows users to securely manage their mutual funds and portfolios, with features like periodic data fetching, authentication, and robust exception handling. It integrates external APIs to fetch live mutual fund data and enables users to track and manage their financial portfolios effectively.

The project leverages technologies such as Django, Celery, Redis, Django-Celery-Beat, and JWT for secure user authentication, background task management, and scalable periodic data fetching.

Includes scheduled background tasks powered by **DjangoDRF**, **JWT Authentication**, **Celery**, **Redis**, and **Django Celery Beat**.

----

# Project Features
1) JWT Authentication: Secure login, registration, and logout functionality with token-based authentication.

2) Fetch Mutual Funds: Integrates with external APIs to fetch mutual fund data using Celery and Redis for background processing.

3) Buy & Track Investments: Allows users to buy and track mutual fund investments.

4) Fully Paginated and Versioned REST APIs: All APIs are paginated and versioned for better scalability and organization.

5) Centralized Exception Handling: Error handling and response management for clean and consistent error messages.

6) Background Jobs with Celery & Redis: Uses Celery with Redis for handling background jobs such as periodic data fetching and processing.

7) Periodic Tasks with Celery Beat: Schedule tasks like hourly data fetching using Django-Celery-Beat for periodic job management.

8) Token Blacklisting: Implements JWT blacklisting on logout to ensure invalidation of tokens and prevent unauthorized access after logout.

9) Centeralized Logging: Logs user actions, errors, and other relevant events in a centralized manner for debugging and monitoring.

10) Custom Middleware for Authentication: Implements a custom middleware to verify user authentication on specific routes.

11) Integration with Third-Party APIs: Uses the requests module to interact with third-party APIs, fetch mutual fund data, and integrate that into the app.

12) DRF Serializers: Custom serializers for better handling of input and output data, validation, and transformation for API endpoints.

13) Indexing: Indexes email/username for fast querying, improving performance in large-scale deployments.

14) Reusable Components: Components are designed to be reusable and extendable for future features and scalability.

15) Extendable User Model: The user model is extendable, allowing easy customization as the app scales, supporting custom fields for future needs.


---


Key API Endpoints

Method	Endpoint	Description
POST	/api/v1/accounts/login/	Login (JWT Token)
POST	/api/v1/accounts/register-user/	User Registration
POST	/api/v1/accounts/logout-user/	Logout (JWT Blacklisting)
GET	/api/v1/funds/list-fund-families/	List all Fund Families
GET	/api/v1/funds/fetch-external-funds/	Fetch Funds from API
POST	/api/v1/funds/purchase-fund/	Purchase a Mutual Fund
GET	/api/v1/funds/user-portfolio/	View your Portfolio


📂 Project Structure

MutualFundBroker/
├── accounts/         # User Authentication App
├── funds/            # Fund & Portfolio App
├── core/             # Project Core (settings, exception handler)
├── venv/             # Virtual Environment (excluded in repo)
├── manage.py
├── requirements.txt
└── README.md


## 📦 Tech Stack

- Python 3.10+
- Django 4.2+
- Django REST Framework
- Celery 5+
- Redis (as Celery broker)
- Django-Celery-Beat (for periodic tasks)
- PostgreSQL / MySQL (or any preferred DB)

---

##  Prerequisites

Make sure you have installed:

- Python 3.10+ 🐍
- PostgreSQL or MySQL 🎯
- Redis Server (Running locally or remotely) 🚀
- (Optional) Docker for easier Redis setup 🐳

---

## Installation Steps

1. **Clone the repository**

```bash
git clone https://github.com/yourusername/yourproject.git
cd yourproject
Create a virtual environment


python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
Install dependencies


pip install -r requirements.txt
Configure environment variables


Create a .env file or configure environment variables:


# .env
SECRET_KEY=django-insecure-l!=8n%e!#@lcl$e#&140hxj#sn^%7xd*6@jrb#a74lkf(&s@y^
DEBUG=True
DB_NAME=mydatabase
DB_USER=myuser
DB_PASSWORD=mypassword
DB_HOST=localhost
DB_PORT=5432
rapid_api_url = your_rapidapi_url
RAPIDAPI_KEY = your_rapidapi_host
RAPIDAPI_HOST = your_rapidapi_endpoint
CELERY_RESULT_BACKEND=redis://localhost:6379/0    # your endpoint
CELERY_BROKER_URL=redis://localhost:6379/0    # your endpoint
ENVIRONMENT=development


Apply migrations

python manage.py migrate
Create superuser (for Django Admin)


python manage.py createsuperuser
Run the development server


python manage.py runserver

Running Celery and Beat Workers
Make sure Redis is running first!

1. Run Celery Worker

celery -A MutualFundBroker worker --loglevel=info

2. Run Celery Beat Scheduler

celery -A MutualFundBroker beat --loglevel=info
(This handles scheduled background jobs.)


 Scheduled Tasks
The project uses django-celery-beat to create periodic tasks stored in the database.

A database migration is included to auto-create the necessary PeriodicTask during first deploy.

 Optional: Running Redis via Docker (easy setup)

docker run -d -p 6379:6379 redis

 Useful Commands CheatSheet
Command	Description
python manage.py migrate	  # Apply database migrations
python manage.py createsuperuser	# Create admin user
celery -A your_project worker --loglevel=info	   #Start Celery Worker
celery -A your_project beat --loglevel=info	   #Start Celery Beat
docker run -d -p 6379:6379 redis	    # Start Redis using Docker



**Note**
Troubleshooting
Missing Migrations: If you encounter database errors, ensure that all migrations have been applied with python manage.py migrate.

Celery Not Running: Ensure that both Redis and the Celery worker are running.


This README provides the essential steps to get the project up and running. If you encounter any issues or have further questions, feel free to reach to me.






