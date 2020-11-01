# simple-mailing-service


### How to run
- local
    1. git clone https://github.com/SungminSo/simple-mailing-service.git
    1. set all of environments
    1. ``` python3 manage.py run ``` or ``` make run ```
    1. expected 
        ``` 
        * Serving Flask app "app" (lazy loading)
        * Environment: dev
        * Debug mode: off
        * Running on http://0.0.0.0:5000/ (Press CTRL+C to quit)
        
       ```
- docker
    1. git clone https://github.com/SungminSo/simple-mailing-service.git
    1. ``` make docker ```
    1. expected 
        ``` 
        * Serving Flask app "app" (lazy loading)
        * Environment: prod
        * Debug mode: off
        * Running on http://0.0.0.0:5000/ (Press CTRL+C to quit)
        
       ```
       
       
### How to install packages
```
make install
```
or
``` 
make install-dev
```

       
### Env
|key                |value           |
|-------------------|----------------|
|POSTGRES_HOST      |localhost       |
|POSTGRES_PORT      |5432            |
|POSTGRES_USER      |postgres        |
|POSTGRES_DB_NAME   |mail            |
|POSTGRES_PASSWORD  |password        |
|CORS_ORIGINS       |*               |
|CORS_METHODS       |GET,POST,PATCH,DELETE,OPTIONS|
|CORS_HEADERS       |Origin,Authorization,Content-Type|
|FLASK_ENV          |prod            |
|HERRENCORP_MAIL_URL|http://python.recruit.herrencorp.com/api/v1/mail|
|HERRENCORP_MAIL_AUTH|herren-recruit-python|

**for jetbrains user**
```PYTHONUNBUFFERED=1;POSTGRES_HOST=localhost;POSTGRES_PORT=5432;POSTGRES_USER=paul;POSTGRES_DB_NAME=mail;POSTGRES_PASSWORD=password;CORS_ORIGINS=*;CORS_METHODS=GET,POST,PATCH,DELETE,OPTIONS;CORS_HEADERS=Origin,Authorization,Content-Type;FLASK_ENV=prod;HERRENCORP_MAIL_URL=http://python.recruit.herrencorp.com/api/v1/mail;HERRENCORP_MAIL_AUTH=herren-recruit-python```


### Project Structure
```
- app
    - models
        - __init__.py
        - users.py
    - test
        - __init__.py
    - utils
        - __init__.py
        - validate.py
    - views
        - __init__.py
        - users.py
    - __init__.py
    - config.py
- migrations
    - versions
        - ...
    - alembic.ini
    - env.py
    - README
    - script.py.mako
- .gitignore
- docker-compose.yml
- Dockerfile
- Makefile
- manage.py
- Pipfile
- Pipfile.lock
- README.md
```
