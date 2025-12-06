@echo off
REM Deployment script for LUVORA (Windows)

echo Starting LUVORA deployment...

REM Check if .env file exists
if not exist .env (
    echo Error: .env file not found!
    echo Please create .env file from .env.example
    exit /b 1
)

echo Building Docker images...
docker-compose build

echo Starting services...
docker-compose up -d

echo Waiting for database to be ready...
timeout /t 10 /nobreak

echo Running migrations...
docker-compose exec web python manage.py migrate

echo Collecting static files...
docker-compose exec web python manage.py collectstatic --noinput

echo.
echo Deployment completed successfully!
echo Application is running at: http://localhost
echo.
echo To create a superuser, run:
echo   docker-compose exec web python manage.py createsuperuser
echo.
echo To view logs, run:
echo   docker-compose logs -f

pause
