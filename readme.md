## Run Commands
celery -A celery_app.worker worker                                  # celery worker
python3 app.py                                                      # flask app
python3 manage.py runserver                                         # django 
mysql -u root -p                                                    # mysql 
uvicorn app:app --host <host_name> --port <port>                    # fastapi

# Errors

## Database Errors
- error    : error connect to caching_sha2_password the specified module could not be found 
- solution :  db $mysql > ALTER USER 'root'@'localhost' IDENTIFIED WITH mysql_native_password BY 'db_password';
