# Simple Django Blog

This is a simple blog application built with Django. It provides core blogging features such as user registration, authentication, and the ability for users to create, view, and manage their own posts.
This project was developed as part of the **"Python Backend Developer" course by Yandex Practicum**.
---

## Features

- User registration and login
- Create, edit, and delete blog posts
- View posts by all users
- Basic user profile pages
- Responsive design with Bootstrap 5

---

## Tech Stack

- Python 3.12
- Django 5.1
- SQLite (default database)
- HTML/CSS (Bootstrap 5 using `django-bootstrap5`)

---

## Installation

1. **Clone the repository**
2. **Create a virtual environment**:
   python -m venv venv
   source venv/bin/activate
3. **Install dependencies:**:
   pip install -r requirements.txt
4. **Apply migrations:**:
   python manage.py migrate
5. **Run the development server:**:
   python manage.py runserver
