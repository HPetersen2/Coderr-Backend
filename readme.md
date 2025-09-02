# Django REST Project

This is a Django REST Framework project created as part of a programming exam. It demonstrates best practices in Django REST development, including models, serializers, views, and project structure.

## Technologies

- Python 3.13.3
- Django
- Django REST Framework

## Features

- User registration and authentication (if implemented)
- CRUD operations for models
- Clean project structure suitable for REST applications
- Admin interface for data management

## Installation

### 1. Clone the repository

```bash
git clone <repository-url>
cd <repository-folder>
```

### 2. Create a virtual environment

```bash
python -m venv venv
```

Activate the virtual environment:  

**macOS/Linux:**
```bash
source venv/bin/activate
```

**Windows:**
```bash
venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Apply database migrations

```bash
python manage.py migrate
```

### 5. Create a superuser (optional)

```bash
python manage.py createsuperuser
```

### 6. Run the development server

```bash
python manage.py runserver
```

The project will be accessible at:

```
http://127.0.0.1:8000/
```

The Django admin interface (if superuser created) is available at:

```
http://127.0.0.1:8000/admin/
```

### 7. (Optional) Populate test data

If you have a script to populate test data:

```bash
python manage.py shell < create_testdata.py
```

## Database

This project uses SQLite (`db.sqlite3`), which is automatically created when running the server for the first time.

## API Documentation

Detailed API endpoint documentation is available here:  
https://cdn.developerakademie.com/courses/Backend/EndpointDoku/index.html?name=kanmind

## License

MIT License

Copyright (c) 2025 Henrik Petersen

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, subject to the following conditions:

1. The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.
2. The backend portion of this project was developed by Henrik Petersen.
3. The frontend portion is provided by Developer Akademie and used here with permission. All rights for the frontend remain with its original creators.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
