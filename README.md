# Flask RESTful API for a Simple Blog

This is a simple Flask RESTful API application that allows users to create, read, update, and delete (CRUD) users and their associated blog posts. The application uses Flask-SQLAlchemy for database operations and Flask-RESTful for API endpoints.

## Features

- User management: Create, read, update, and delete users.
- Post management: Create, read, update, and delete posts associated with a user.

## Getting Started

### Prerequisites

- Python 3.6 or higher
- Flask
- Flask-SQLAlchemy
- Flask-RESTful

### Installation

1. Clone the repository:

```bash
git clone https://github.com/your-username/flask-restful-blog.git
cd flask-restful-blog
```

2. Create a virtual environment (optional but recommended):

```bash
python -m venv venv
source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
```

3. Install dependencies:

```bash
pip install flask flask-sqlalchemy flask-restful
```

4. Set up the database:

```bash
python
from app import db
db.create_all()
exit()
```

5. Run the application:

```bash
python app.py
```

The application will start running on `http://localhost:5000/`.

## API Endpoints

### Users

- GET `/api/users/` - Retrieve a list of all users.
- POST `/api/users/` - Create a new user.
- GET `/api/users/<int:id>` - Retrieve a user by ID.
- PATCH `/api/users/<int:id>` - Update a user by ID.
- DELETE `/api/users/<int:id>` - Delete a user by ID.

### Posts

- GET `/api/posts/` - Retrieve a list of all posts.
- POST `/api/posts/` - Create a new post.
- GET `/api/posts/<int:id>` - Retrieve a post by ID.
- PATCH `/api/posts/<int:id>` - Update a post by ID.
- DELETE `/api/posts/<int:id>` - Delete a post by ID.

## Contributing

Contributions are welcome! To get started, fork the repository and create a new branch for your changes. Make sure to follow the existing code style and add appropriate comments. Once you're done, submit a pull request and I'll review it.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for more information.
