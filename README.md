## Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/Abhimanue-rajesh/ihrd-test-py-django.git

2. Create a virtual environment and activate it:

    ```bash
    python -m venv venv
      venv\Scripts\activate # On Mac, use: source venv/bin/activate

3. Install project dependencies:

    ```bash
    pip install -r requirements.txt

4. Apply database migrations:

    ```bash
    python manage.py migrate

5. Create a superuser for the admin panel:

    ```bash
    python manage.py createsuperuser

6. Start the development server:

    ```bash
    python manage.py runserver

7. Access the application in your web browser at http://http://127.0.0.1:8000/
