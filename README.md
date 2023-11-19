# VirusApp - Web Server

This is the work done for my final project, this repository is for the web server side of the project. The web server was written in Python using the Django library. It also integrates the Django-REST Framework to implement the API.

This server is for the Virus Admin in the company to manage staff members, view & submit test results and most importantly, generate an isolation report.

## Installation

#### Software requires Python Version 3

Use the pip manager to install:
```
django
djangorestframework
mysql-client
```

## Usage

Firstly, migrate the database with the following commands:
```
python3 manage.py makemigrations
python3 manage.py migrate
```

You can start the server with the command:
```
python3 manage.py runserver 0.0.0.0:8000
```

## License
The software is a free open source license under the terms of GPL version 3.

## References/Acknowledgments
- [Django](https://www.djangoproject.com/)
- [Django REST Framework](https://www.django-rest-framework.org/)
- [MySQL](https://www.mysql.com/)