
# 🚀 Funds Management Backend

A Django REST API project for managing Fund Families, Mutual Funds, and Portfolios.  
The Funds Management Backend is a Django-based REST API designed for managing Fund Families, Mutual Funds, and Portfolios. This backend system allows users to securely manage their mutual funds and portfolios, with features like periodic data fetching, authentication, and robust exception handling. It integrates external APIs to fetch live mutual fund data and enables users to track and manage their financial portfolios effectively.

The project leverages technologies such as Django, Celery, Redis, Django-Celery-Beat, and JWT for secure user authentication, background task management, and scalable periodic data fetching.

Includes scheduled background tasks powered by **DjangoDRF**, **JWT Authentication**, **Celery**, **Redis**, and **Django Celery Beat**.

----

# Project Features
JWT Authentication: Secure login, registration, and logout functionality with token-based authentication.

Fetch Mutual Funds: Integrates with external APIs to fetch mutual fund data using Celery and Redis for background processing.

Buy & Track Investments: Allows users to buy and track mutual fund investments.

Fully Paginated and Versioned REST APIs: All APIs are paginated and versioned for better scalability and organization.

Centralized Exception Handling: Error handling and response management for clean and consistent error messages.

Background Jobs with Celery & Redis: Uses Celery with Redis for handling background jobs such as periodic data fetching and processing.

Periodic Tasks with Celery Beat: Schedule tasks like hourly data fetching using Django-Celery-Beat for periodic job management.

Token Blacklisting: Implements JWT blacklisting on logout to ensure invalidation of tokens and prevent unauthorized access after logout.

Centeralized Logging: Logs user actions, errors, and other relevant events in a centralized manner for debugging and monitoring.

Custom Middleware for Authentication: Implements a custom middleware to verify user authentication on specific routes.

Integration with Third-Party APIs: Uses the requests module to interact with third-party APIs, fetch mutual fund data, and integrate that into the app.

DRF Serializers: Custom serializers for better handling of input and output data, validation, and transformation for API endpoints.

Indexing: Indexes email/username for fast querying, improving performance in large-scale deployments.

Reusable Components: Components are designed to be reusable and extendable for future features and scalability.

Extendable User Model: The user model is extendable, allowing easy customization as the app scales, supporting custom fields for future needs.


---

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

# env
DEBUG=True
SECRET_KEY=your_secret_key
DATABASE_URL=your_database_url
REDIS_URL=redis://localhost:6379
RAPIDAPI_KEY=your_rapidapi_key
RAPIDAPI_HOST=your_rapidapi_host
RAPID_API_URL=your_rapidapi_endpoint


Apply migrations

python manage.py migrate
Create superuser (for Django Admin)


python manage.py createsuperuser
Run the development server


python manage.py runserver
  Running Celery and Beat Workers
Make sure Redis is running first!

1. Run Celery Worker

celery -A your_project_name worker --loglevel=info
2. Run Celery Beat Scheduler

celery -A your_project_name beat --loglevel=info
(This handles scheduled background jobs.)

Tip: You can combine both Worker and Beat together in production using process managers like supervisor, systemd, or docker-compose.

 Scheduled Tasks
The project uses django-celery-beat to create periodic tasks stored in the database.

You can manage periodic jobs (like Fetching Mutual Funds hourly) from the Django Admin panel.

A database migration is included to auto-create the necessary PeriodicTask during first deploy.

 Optional: Running Redis via Docker (easy setup)

docker run -d -p 6379:6379 redis
  Useful Commands CheatSheet

Command	Description
python manage.py migrate	Apply database migrations
python manage.py createsuperuser	Create admin user
celery -A your_project worker --loglevel=info	Start Celery Worker
celery -A your_project beat --loglevel=info	Start Celery Beat
docker run -d -p 6379:6379 redis	Start Redis using Docker

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

Additional Notes
Celery Tasks: Background tasks, such as fetching mutual fund data from third-party APIs, are handled by Celery. Ensure that both Redis and Celery workers are running to process these tasks.

Rate Limiting: Be mindful of rate limits when interacting with third-party APIs. Make sure to set proper API keys and limits to avoid disruptions.

Troubleshooting
Missing Migrations: If you encounter database errors, ensure that all migrations have been applied with python manage.py migrate.

Celery Not Running: Ensure that both Redis and the Celery worker are running.


This README provides the essential steps to get the project up and running. If you encounter any issues or have further questions, feel free to open an issue in the repository or reach out to the project maintainers.






