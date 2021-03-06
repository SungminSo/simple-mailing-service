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


### API
- Postman Docs: https://documenter.getpostman.com/view/4736816/TVYM2uvX

       
### Env
|key                |value           |
|-------------------|----------------|
|POSTGRES_HOST      |localhost       |
|POSTGRES_PORT      |5432            |
|POSTGRES_USER      |developer       |
|POSTGRES_DB_NAME   |mailing         |
|POSTGRES_TEST_DB_NAME|mail_test     |
|POSTGRES_PROD_DB_NAME|mail_prod     |
|POSTGRES_PASSWORD  |password        |
|CORS_ORIGINS       |*               |
|CORS_METHODS       |GET,POST,PATCH,DELETE,OPTIONS|
|CORS_HEADERS       |Origin,Authorization,Content-Type|
|FLASK_ENV          |dev             |
|HERRENCORP_BASE_URL|http://python.recruit.herrencorp.com|
|HERRENCORP_MAIL_AUTH|herren-recruit-python|
|HERRENCORP_SEND_MAIL_URL|/api/v1/mail|
|HERRENCORP_SEND_MAIL_URL_V2|/api/v2/mail|
|HERRENCORP_GET_MAIL_URL|/api/v1/inbox/|

**for jetbrains user**
```PYTHONUNBUFFERED=1;POSTGRES_HOST=localhost;POSTGRES_PORT=5432;POSTGRES_USER=developer;POSTGRES_DB_NAME=mailing;POSTGRES_TEST_DB_NAME=mail_test;POSTGRES_PROD_DB_NAME=mail_prod;POSTGRES_PASSWORD=password;CORS_ORIGINS=*;CORS_METHODS=GET,POST,PATCH,DELETE,OPTIONS;CORS_HEADERS=Origin,Authorization,Content-Type;FLASK_ENV=dev;HERRENCORP_BASE_URL=http://python.recruit.herrencorp.com;HERRENCORP_MAIL_AUTH=herren-recruit-python;HERRENCORP_SEND_MAIL_URL=/api/v1/mail;HERRENCORP_GET_MAIL_URL=/api/v1/inbox/;HERRENCORP_SEND_MAIL_URL_V2=/api/v2/mail```


### Project Structure
```
- app
    - models
        - __init__.py
        - users.py
    - test
        - __init__.py
        - conftest.py
        - test_api.py
        - test_mail.py
        - test_user.py
    - utils
        - __init__.py
        - validate.py
    - views
        - __init__.py
        - mails.py
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
- .flake8
- .gitignore
- docker-compose.yml
- Dockerfile
- entrypoint.sh
- Makefile
- manage.py
- Pipfile
- Pipfile.lock
- README.md
```
