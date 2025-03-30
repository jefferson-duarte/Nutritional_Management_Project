# 🥦 Nutritional Management Project

A web application built with **Django** to manage nutritional information, track appointments, and facilitate communication between **nutritionists** and **patients**.

## 🚀 Features

- 📅 **Appointment scheduling** with nutritionists  
- 🛠️ **Dashboard** for managing patient data  
- 📋 **Nutritional plans** management  
- 🔐 **Secure authentication system (JWT-based API authentication included)**  

## 📌 Getting Started

These instructions will help you set up and run the project on your local machine for development and testing purposes.

### ✅ Prerequisites

- Python 3.10 or higher
- Django 5.1.5
- pip (Python package installer)

### 📥  Installation

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
## 👤 Creating a Superuser

To access the Django admin panel, you'll need to create a superuser. Follow these steps:

1. **Activate your virtual environment** if it's not already activated:
    ```sh
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

2. **Run the following command to create a superuser**:
    ```sh
    python manage.py createsuperuser
    ```
    You will be prompted to enter:
    - **Username**
    - **Email address**
    - **Password**

3. After creating the superuser, run the development server:
    ```sh
    python manage.py runserver
    ```

4. Access the Django Admin panel at:  
    ```
    http://127.0.0.1:8000/admin/
    ```
    Login using the superuser credentials you just created.

## 🧪 Running Tests with Coverage

1. **Install Coverage** if it's not already installed:
    ```sh
    pip install coverage
    ```

2. **Run the tests with Coverage**:
    ```sh
    coverage run manage.py test
    ```

3. **Generate a report in the terminal**:
    ```sh
    coverage report
    ```

4. **Generate an HTML report** to view coverage in a browser:
    ```sh
    coverage html
    ```
    This will create a `htmlcov/` folder with an interactive HTML report.

    Open the `index.html` file in a browser:
    ```sh
    xdg-open htmlcov/index.html  # On Linux
    start htmlcov\index.html     # On Windows
    open htmlcov/index.html      # On macOS
    ```

### 🏗️ Project Structure

- `core/`: Contains the main project settings and URLs.
- `authentication/`: Contains the authentication app.
- `dashboard/`: Contains the dashboard app.
- `nutritional_plans/`: Contains the nutritional plans app.
- `base_templates/`: Contains the base templates for the project.
- `base_static/`: Contains the static files for the project.
- `media/`: Contains the media files for the project.
- `requirements.txt`: Project dependencies
- `manage.py`: Django management script

### 🛠️ Built With

- [Django](https://www.djangoproject.com/) - The web framework used
- [Django REST framework](https://www.django-rest-framework.org/) - For building REST APIs
- [Simple JWT](https://django-rest-framework-simplejwt.readthedocs.io/en/latest/) - For JWT authentication
