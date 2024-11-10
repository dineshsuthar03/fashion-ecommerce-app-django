Django E-Commerce Project
This is a Django-based eCommerce platform, allowing users to browse products, make purchases, and manage accounts with Google login and Razorpay payment integration.


URL - http://shop.dineshsuthar.com/
Features:
User registration and authentication (via Google).
Product catalog and filtering.
Shopping cart functionality.
Checkout and payment via Razorpay.
Order management.
Email notifications and password reset.
Prerequisites:
Before you start, ensure you have the following installed:

Python 3.x
pip (Python package installer)
Virtualenv (optional, but recommended)
Installation Steps:
Step 1: Clone the Repository
bash
Copy code
git clone <your-repository-url>
cd <your-project-directory>
Step 2: Create a Virtual Environment (Optional but Recommended)
Create a virtual environment to keep your project dependencies isolated.

bash
Copy code
python3 -m venv venv
source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
Step 3: Install Dependencies
Install the required dependencies using pip. In your terminal, run:

bash
Copy code
pip install -r requirements.txt
This will install the following dependencies:

Django
django-allauth (for Google login)
Razorpay SDK
Other necessary packages for your project
Step 4: Create Environment Variables
In the project directory, create a .env file to store your environment variables securely. You can copy and paste the following template:

bash
Copy code
# Base URL for your application
APP_BASE_URL= <your-app-base-url>

# Google OAuth Credentials (Get them from Google Developer Console)
GOOGLE_CLIENT_ID= <your-google-client-id>
GOOGLE_CLIENT_SECRET= <your-google-client-secret>

# Email Configuration
EMAIL_USER= <your-email-address>
EMAIL_PASS= <your-email-password>

# Django Secret Key (Generate a unique key for production)
SECRET_KEY= <your-secret-key>

# Debug Mode (Set to True for development, False for production)
DEBUG=True

# Gmail SMTP Configuration for sending emails
EMAIL_HOST_USER= <your-email-address>
EMAIL_HOST_PASSWORD= <your-email-password>

# RazorPay API Keys (Get them from RazorPay account)
RAZORPAY_KEY_ID= <your-razorpay-key-id>
RAZORPAY_SECRET_KEY= <your-razorpay-secret-key>
Important:

You must replace the placeholders (e.g., <your-google-client-id>, <your-email-address>, etc.) with actual values from your Google Developer Console, email account, and RazorPay account.
Step 5: Run Migrations
Once you've set up your .env file, run the following command to set up the database:

bash
Copy code
python manage.py migrate
Step 6: Create a Superuser
To access the Django admin panel, you'll need to create a superuser:

bash
Copy code
python manage.py createsuperuser
Follow the prompts to set up your admin username, email, and password.

Step 7: Run the Development Server
Start the development server by running the following command:

bash
Copy code
python manage.py runserver
Now, open your browser and go to http://127.0.0.1:8000 to access the application locally.

Step 8: Admin Panel Access
To access the admin panel, go to:

bash
Copy code
http://127.0.0.1:8000/admin
Log in using the superuser credentials you created earlier.

App Overview:
1. Accounts:
Handles user registration, login, and account management, including Google authentication via django-allauth.

2. Products:
Manages the product catalog, including viewing products, filtering, and searching.

3. Cart:
Handles the shopping cart functionality. Users can add items to their cart, update quantities, and proceed to checkout.

4. Orders:
Manages order creation, order status, and integrates Razorpay for payment processing.

5. Payments:
Handles the integration with Razorpay, where users can securely complete their transactions.

6. Checkout:
Allows users to enter shipping details, confirm orders, and proceed to payment.

Common Environment Variables:
Ensure the following environment variables are set correctly in your .env file:

APP_BASE_URL: The base URL of your application (e.g., http://127.0.0.1:8000 or your production URL).
GOOGLE_CLIENT_ID & GOOGLE_CLIENT_SECRET: OAuth credentials for integrating Google login (from the Google Developer Console).
EMAIL_USER & EMAIL_PASS: Your email credentials used to send transactional emails (e.g., Gmail).
SECRET_KEY: A unique Django secret key. Make sure this is kept private.
DEBUG: Set to True for development and False for production.
EMAIL_HOST_USER & EMAIL_HOST_PASSWORD: Gmail SMTP configuration for sending emails.
RAZORPAY_KEY_ID & RAZORPAY_SECRET_KEY: Razorpay API credentials (from Razorpay Dashboard).
Running Tests
To run the tests for the application, execute the following command:

bash
Copy code
pytest
Ensure you have pytest and pytest-django installed by adding them to requirements.txt.

Deployment
For deployment in production, you can set the DEBUG variable to False and configure the production database and other environment variables accordingly. 
