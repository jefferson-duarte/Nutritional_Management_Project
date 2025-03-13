# Nutritional Management Project

This is a Django project for managing nutritional information.

## Getting Started

These instructions will help you set up and run the project on your local machine for development and testing purposes.

### Prerequisites

- Python 3.10 or higher
- Django 5.1.5
- pip (Python package installer)

### Installation

1. Clone the repository:
    ```sh
    git clone https://github.com/jefferson-duarte/Nutritional_Management_Project.git
    cd Nutritional_Management_Project
    ```

2. Create and activate a virtual environment:
    ```sh
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

3. Install the required packages:
    ```sh
    pip install -r requirements.txt
    ```

4. Create a `.env` file in the root directory and add your secret key:
    ```env
    SECRET_KEY=your_secret_key
    ```

5. Apply the migrations:
    ```sh
    python manage.py migrate
    ```

6. Run the development server:
    ```sh
    python manage.py runserver
    ```

### Project Structure

- `core/`: Contains the main project settings and URLs.
- `authentication/`: Contains the authentication app.
- `dashboard/`: Contains the dashboard app.
- `base_templates/`: Contains the base templates for the project.
- `base_static/`: Contains the static files for the project.
- `media/`: Contains the media files for the project.

### Built With

- [Django](https://www.djangoproject.com/) - The web framework used
- [Django REST framework](https://www.django-rest-framework.org/) - For building REST APIs
- [Simple JWT](https://django-rest-framework-simplejwt.readthedocs.io/en/latest/) - For JWT authentication
