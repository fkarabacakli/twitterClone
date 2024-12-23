# Twitter Clone

This repository contains a **Twitter Clone** project developed using Django. The project aims to replicate core functionalities of the Twitter platform, providing a hands-on experience with web development, backend programming, and database integration.

## Features

- **User Authentication:** Sign-up, login, and logout functionalities.
- **Tweet Functionality:** Users can create, edit, and delete tweets.
- **Timeline Feed:** Displays tweets in reverse chronological order.
- **Follow System:** Users can follow and unfollow each other.
- **Like and Comment:** Users can like and comment on tweets.
- **Responsive Design:** Ensures usability across various devices.

## Technologies Used

- **Backend Framework:** Django
- **Frontend:** HTML, CSS, Bootstrap
- **Database:** SQLite (can be replaced with other relational databases)
- **Others:** Django Authentication, Django ORM
  
## Project Structure

```plaintext
twitterClone/
├── manage.py               # Django management script
├── twitterClone/           # Project configuration
│   ├── settings.py         # Project settings
│   ├── urls.py             # URL configurations
│   ├── wsgi.py             # WSGI configuration
│   └── asgi.py             # ASGI configuration
├── app/                    # Main application folder
│   ├── models.py           # Database models
│   ├── views.py            # Application views
│   ├── urls.py             # Application URL routes
│   ├── templates/          # HTML templates
│   └── static/             # CSS, JavaScript, and images
├── db.sqlite3              # SQLite database
├── requirements.txt        # Python dependencies
└── README.md               # Documentation
```

## Key Learning Outcomes

- Understanding Django's Model-View-Template (MVT) architecture.
- Gaining experience with user authentication and authorization.
- Building RESTful routes and handling HTTP requests.
- Designing database schemas and working with Django ORM.
