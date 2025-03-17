# Project Setup Instructions

## 1. Clone the Repository
```sh
git clone https://github.com/GreatTeapot/pl_hh.git 
cd pl_hh
```

## 2. Set Up Virtual Environment
```sh
python -m venv .venv
source .venv/bin/activate  # On macOS/Linux
.venv\Scripts\activate  # On Windows
```

## 3. Install Dependencies
```sh
pip install -r requirements.txt
```

## 4. Set Up Environment Variables
Create a `.env` file in the project root and add the necessary configurations. Example:
```
SECRET_KEY=dsifsanouibf638f2g7u3gf38o2afuijea
DEBUG=True
ALLOWED_HOSTS=*

PG_DATABASE=postgres
PG_USER=postgres
PG_PASSWORD=postgres
DB_HOST=localhost
DB_PORT=5432

ACCESS_TOKEN_LIFETIME=6000 #minutes
REFRESH_TOKEN_LIFETIME=7 #days
ALGORITHM = HS256

TIMEZONE=Europe/Moscow

STATIC_FILES=./static/
MEDIA_FILES=./media/


```

## 5. Run Migrations
```sh
python src/manage.py makemigrations
python src/manage.py migrate
```

## 6. Create a Superuser (Optional)
```sh
python src/manage.py createsuperuser
```

## 7. Run the Server
```sh
python src/manage.py runserver
```

## 8. API Documentation (Swagger UI)
Swagger documentation is available at:
```
http://localhost:8000/api/v1/
```

## User Roles
The system has the following roles:
- **ADMIN (ADM)** – Administrator
- **EMPLOYER (EMPLOYEE)** – Employee
- **APPLICANT (APPLICANT)** – Applicant
- **ANONYMOUS (ANON)** – Anonymous User

## Job Vacancies Types
The following types of job vacancies are available:
- **Full Time (FULL)**
- **Part Time (PART)**
- **Remote Time (REMOTE)**