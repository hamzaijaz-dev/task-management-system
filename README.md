# Task Management System
This Task Management System is a web-based solution constructed using Django, FastAPI, and Celery. Its functionality encompasses task creation, modification, deletion, and assignment, alongside features like user authentication, asynchronous task handling, RESTful API integration, and thorough unit testing. The system also incorporates workflows for conducting code sanity checks.

## Requirements
- Python 3.x
- Django
- FastAPI
- Celery
- uvicorn
- Redis (for Celery)

### Project Structure
**user_app:** Django application for the web interface, user authentication and backend logic.

**api_list:** FastAPI application for the RESTful API.

**celery_tasks:** Celery task for asynchronous email notifications.

**Sanity checks:** GitHub workflows triggered with each code push, ensuring the maintenance of high code quality.

### Setup
1. Clone the repository:
    ```bash
   git clone https://github.com/your-username/task-management-system.git
2. Create and activate a virtual environment:
    ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```
3. Install dependencies:
    ```bash
   pip install -r requirements.txt
   ```
4. Migrate the database:
   ```bash
   cd user_app
   python manage.py migrate
   ```
### Running the Application
1. Start the Django server:
   ```bash
    cd user_app
    python manage.py runserver
   ```
2. Start the Celery worker:
   ```bash
    cd user_app
    celery -A user_app worker --loglevel=info
   ```
3. Start the FastAPI server:
   ```bash
    cd api_list
    uvicorn main:app --reload --port=8001
   ```

### Usage
Access the web application at http://localhost:8000.
Use the API endpoints at http://localhost:8001.

### Test cases
Run unit tests:
   ```bash
    cd user_app
    python manage.py test
   ```

<img src="https://github.com/hamzaijaz-dev/task-management-system/blob/main/assets/fastapi.png" alt="FastAPI Docs">
<br>
<img src="https://github.com/hamzaijaz-dev/task-management-system/blob/main/assets/django.png" alt="Django">

