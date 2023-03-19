# TODO list
Simple TODO list implementation on Django

## Installation
Use `.env.sample` as example and create file `.env` with your settings
```
git clone https://github.com/ansicat/todo_proj.git
cd todo-proj
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

## Features
- Deadline may be given for a task
- Tasks have user defined tags
