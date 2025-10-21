
# Recipe Book and Meal Planner

Recipe Book and Meal Planner website created with Django.

Step 1: Ensure Prerequisites are Installed
Python: Ensure Python is installed (version 3.7 or above is recommended).
python --version
Pip: Ensure pip (Python's package manager) is installed:
pip --version
Django: Confirm Django is installed:
pip install django
Install Dependencies:
Navigate to the root of your project directory (where requirements.txt is located).
Install the required dependencies using:
pip install -r requirements.txt

Step 2: Database Setup
Apply migrations to set up the database schema:
(Optional) If the project uses seed data, load it:
python manage.py loaddata <fixture_name>
Replace <fixture_name> with the provided JSON files, if any.

Step 3: Static Files
Collect static files to serve them properly:
python manage.py collectstatic
Press yes or y if prompted.
Step 4: Run the Development Server
Start the server:
python manage.py runserver
Open a browser and go to the address displayed (usually http://127.0.0.1:8000).
Step 5: Access the Admin Interface
If the project uses Django’s admin interface:
Create a superuser account1:
python manage.py createsuperuser
Follow the prompts to set up a username, email, and password.
Log in at http://127.0.0.1:8000/admin/ using the superuser credentials.
Troubleshooting
If there’s an issue, check the project settings and .env files (if applicable).
Make sure required modules (like decouple) are installed:
pip install python-decouple
Review the README.md or other documentation included in the project for custom instructions.
