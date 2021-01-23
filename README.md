curl -X POST 0.0.0.0:7016/predict -F 'file=@/home/data/_2737476_orig[1].jpg' -i

# NGINX - uWsgi - Flask with Docker

Nginx + uWsgi + Flask + TFX serving with docker-compose


## Project Structure

```bash
flask-nginx-uwsgi-Docker
├── docker-compose.yml
├── flask
│   ├── Dockerfile
│   ├── app.py
│   ├── requirements.txt
│   ├── route
│   ├── templates
│   └── uwsgi.ini
├── nginx
│   ├── Dockerfile
│   └── nginx.conf
└── venv
```

## Set Up with..?

- Docker를 사용해서 Flask와 uWsgi를 만들어주기
- Nginx서버를 Docker로 만들어주기
- docker-compose를 사용해서 생성된 Docker파일들을 하나로 묶어주기

## set virtualenv

```bash
$ pip3 install virtualenv
$ virtualenv venv
$ source venv/bin/activate
(venv) $ pip install flask uwsgi
(venv) $ pip install freeze > requirements.txt
```

## Docker로 Flask와 uWsgi 세팅하기

### Project Structure

```bash
flask
├── Dockerfile
├── app.py
├── requirements.txt
├── route
│   ├── __init__.py
│   └── app_route.py
├── templates
│   └── index.html
└── uwsgi.ini
```

### app.py

```python
from flask import Flask
from route.app_route import app_route

app = Flask(__name__)

app.register_blueprint(app_route)

if __name__ == '__main__':
    app.run(host='0.0.0.0')
```

### uwsgi.ini

```
[uwsgi]
wsgi-file = app.py
callable = app
socket = :8080
processes = 4
threads = 2
master = true
vacum = true
chmod-socket = 660
die-on-term = true
```

### route/app_route.py

```python
from flask import Blueprint, render_template

app_route = Blueprint('first_route',__name__)

@app_route.route('/')
def index():
    return render_template('index.html')
```

### requirements.txt

```
click==7.1.2
Flask==1.1.2
itsdangerous==1.1.0
Jinja2==2.11.2
MarkupSafe==1.1.1
uWSGI==2.0.19.1
Werkzeug==1.0.1
```

### templates/index.html

```html
<html>
    <head>
        <title>flask Docker</title>
    </head>
</html>
<body>
    <h5>
        this is index pages!
    </h5>
</body>
```

### Docker

```docker
FROM python:3

WORKDIR /app

ADD . /app
RUN pip install -r requirements.txt

CMD ["uwsgi","uwsgi.ini"]
```

## Docker-Nginx


### Project Structure

```bash
nginx
├── Dockerfile
└── nginx.conf
```

### nginx.conf

```
server {

	listen 5000;
	
	location / {
		include uwsgi_params;
		uwsgi_pass flask:8080;
	}
}
```

### Dockerfile

```docker
FROM nginx

RUN rm /etc/nginx/conf.d/default.conf

COPY nginx.conf /etc/nginx/conf.d/
```


### docker-compose.yml

```docker
version: "3.7"

services: 
    flask:
        build: ./flask
        container_name: flask
        restart: always
        environment: 
            - APP_NAME=FlaskTest
        expose:
            - 8080

    nginx:
        build: ./nginx
        container_name: nginx
        restart: always
        ports:
            - "5000:5000
```

## Run docker-compose file

```bash
$ docker-compose up -d --build
```

완전 잘된다. 이제 덧붙일 개발을 시작해봐야겠습니다.