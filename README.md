# Blog Posts API

A RESTful API built with Django and Django REST Framework (DRF) that allows clients to create, read, update, and delete blog posts and comments. It includes filtering, pagination, a like/dislike voting system, and rate throttling to protect the endpoints.

---

## Table of Contents

1. [Features](#features)
2. [Tech Stack](#tech-stack)
3. [Prerequisites](#prerequisites)
4. [Installation & Setup](#installation--setup)
5. [Configuration](#configuration)
6. [Running the Application](#running-the-application)
7. [API Endpoints](#api-endpoints)

   * [Posts](#posts)
   * [Comments (Nested)](#comments-nested)
8. [Filtering & Pagination](#filtering--pagination)
9. [Like/Dislike Voting](#likedislike-voting)
10. [Rate Throttling](#rate-throttling)
11. [Testing](#testing)
12. [Project Structure](#project-structure)
13. [Contributing](#contributing)
14. [License](#license)

---

## Features

* **CRUD** operations for blog posts and comments
* **Filtering** by author, title, and category
* **Pagination** to limit response sizes
* **Like/Dislike** voting endpoints
* **Rate Throttling** to prevent abuse
* **Browsable API** via DRF’s web interface
* **Unit Tests** covering core functionality

---

## Tech Stack

* **Python 3.8+**
* **Django 5.x**
* **Django REST Framework**
* **PostgreSQL**
* **django-filter** (for filtering backends)

---

## Prerequisites

* Python 3.8 or higher installed
* PostgreSQL database server
* `virtualenv` or similar to create isolated Python environments

---

## Installation & Setup

1. **Clone the repository**

   ```bash
   git clone <https://github.com/MisterGheb/Finsure.git>
   cd <repo-folder>
   ```

2. **Create and activate a virtual environment**

   ```bash
   python -m venv venv
   source venv/bin/activate   # On Windows: venv\\Scripts\\activate
   ```

3. **Install dependencies**

   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment variables**

   * Copy `.env.example` to `.env`
   * Set the following:

     ```dotenv
     SECRET_KEY=your_django_secret_key
     DEBUG=True
     DB_NAME=your_db_name
     DB_USER=your_db_user
     DB_PASS=your_db_password
     DB_HOST=localhost
     DB_PORT=5432
     ```

5. **Apply migrations**

   ```bash
   python manage.py migrate
   ```



---

## Running the Application

```bash
# Start the development server
git checkout main
python manage.py runserver
```

Visit **`http://127.0.0.1:8000/api/posts/`** 

---

## API Endpoints

### Posts

| Method | URL                       | Description                                       |
| ------ | ------------------------- | ------------------------------------------------- |
| GET    | `/api/posts/`             | List all posts (with filters & pages)             |
| POST   | `/api/posts/create/`      | Create a new post                                 |
| GET    | `/api/posts/{id}/`        | Retrieve a single post                            |
| PUT    | `/api/posts/{id}/update/` | Update a post                                     |
| DELETE | `/api/posts/{id}/delete/` | Delete a post                                     |
| POST   | `/api/posts/{id}/vote/`   | Like/dislike a post (`{ "like": true }` or false) |

### Comments (Nested under Posts)

| Method | URL                                                  | Description                 |
| ------ | ---------------------------------------------------- | --------------------------- |
| GET    | `/api/posts/{post_id}/comments/`                     | List comments for a post    |
| POST   | `/api/posts/{post_id}/comments/create/`              | Create a new comment        |
| GET    | `/api/posts/{post_id}/comments/{comment_id}/`        | Retrieve a specific comment |
| PUT    | `/api/posts/{post_id}/comments/{comment_id}/update/` | Update a comment            |
| DELETE | `/api/posts/{post_id}/comments/{comment_id}/delete/` | Delete a comment            |

---

## Filtering & Pagination

* **Filtering** by query params: `?author=`, `?title=`, `?category=`
* **Search** across title and content: `?search=keyword`
* **Pagination** via DRF’s `PageNumberPagination`:

  * `?page=2`
  * `?page_size=5` (max 100)

Response format for a paginated list:

```json
{
  "count": 57,
  "next": "http://.../api/posts/?page=2",
  "previous": null,
  "results": [ /* up to page_size items */ ]
}
```

---

## Like/Dislike Voting

`POST /api/posts/{id}/vote/` with body `{ "like": true }`

* Increments `likes` if `true` or `dislikes` if `false`
* Returns `{ "likes": 10, "dislikes": 2 }`

---

## Rate Throttling

* Configured via DRF’s `ScopedRateThrottle`
* **Posts** scope: `10/minute`
* **Votes** scope: `30/minute`
* Excess requests return **429 Too Many Requests** with a retry-after header

---

## Testing

Run the full test suite for posts, comments, pagination, permissions, and voting:

```bash
python manage.py test blog_posts
```

All critical scenarios are covered, including:

* Create Post
* List Posts (including pagination)
* Create Comment
* Update/Delete unrestricted by author
* Voting throttles

---

## Project Structure

```
config/                # Django project settings
  ├── urls.py
  └── settings.py
blog_posts/            # Main app
  ├── migrations/
  ├── models.py
  ├── serializers.py
  ├── views.py
  ├── urls.py
  └── tests.py
manage.py
README.md
requirements.txt
```

---


## License

This project is licensed under the MIT License. See [LICENSE](LICENSE) for details.
