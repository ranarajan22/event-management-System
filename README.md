# Event Management System

A comprehensive web-based event management solution built with modern technologies.

## Technologies Used
- Python/Django - Backend framework
- HTML5 - Structure
- CSS3 - Styling
- JavaScript - Frontend interactivity
- SQLite3 - Database

## Features
- User Authentication
  - Login/Register functionality
  - Secure password handling
  - User roles (Admin/Regular User)

- Event Management
  - Create new events
  - Edit existing events
  - Delete events
  - View event details
  - Register for events

- Admin Dashboard
  - User management
  - Event oversight
  - Category management
  - Analytics and reporting

## Installation

1. Clone the repository
```bash
git clone https://github.com/yourusername/Event-management-System.git
```

2. Setup virtual environment
```bash
python -m venv venv
venv\Scripts\activate
```

3. Install requirements
```bash
pip install django
```

4. Run migrations
```bash
python manage.py makemigrations
python manage.py migrate
```

5. Start server
```bash
python manage.py runserver
```

## Usage
1. Access the application at `http://localhost:8000`
2. Register a new account or login with existing credentials
3. Browse available events or create new ones
4. Manage your events through the dashboard

## Contributing
Contributions are welcome! Please feel free to submit a Pull Request.

## License
This project is licensed under the MIT License.