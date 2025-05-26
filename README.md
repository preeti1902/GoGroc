# 🛒 GoGroc - Online Grocery Store

GoGroc is a Python Django-based e-commerce website for groceries. 

## 🚀 Features
- User authentication (Login, Signup, Logout, Forgot Password)
- User profile management
- Add to cart and wishlist
- Product browsing and search
- Price comparison with other websites (data from an Excel sheet)
- Secure payments via Razorpay (QR code & UPI)
- Email verification
- Responsive UI for mobile adaptation


## 🛠️ Installation & Setup

1. Clone the repository:
   ```bash
   git clone https://github.com/preeti1902/GoGroc.git
   cd GoGroc
2. Create a virtual environment and activate it:
    ```bash
    python -m venv venv
    
    # for mac
    source venv/bin/activate  
    # On Windows use 
    venv\Scripts\activate
3. Install dependencies:
    ```bash
    pip install -r requirements.txt
4. Run migrations:
    ```bash
    python manage.py migrate
5. Start the development server:
    ```bash
    python manage.py runserver
6. Open your browser and visit: http://127.0.0.1:8000

## ⚙️ Technologies Used
    Backend: Django, Python
    Frontend: HTML, CSS, JavaScript (Bootstrap)
    Database: SQLite (can be upgraded to PostgreSQL)
    Payment Gateway: Razorpay (QR & UPI)
    Other: Pandas (for price comparison from Excel)

## 🤝 Contributing
    We welcome contributions! Feel free to open issues or submit pull requests.

## 📁 Project Structure

```text 
ApnaBazar/
│-- apnabazar/                   # Main Django project directory
│   │-- __init__.py
│   │-- settings.py               # Django settings
│   │-- urls.py                    # Project URL configurations
│   │-- wsgi.py
│   │-- asgi.py
│-- apps/
│   │-- home/                  # home (home page)
│   │   │-- migration
│   │   │   │-- __init__.py
│   │   │-- models.py
│   │   │-- views.py
│   │   │-- urls.py
│   │   │-- forms.py
│   │   │-- test.py
│   │   │-- apps.py
│   │-- accounts/                  # Handles user authentication (login, signup, logout, profile)
│   │   │-- migration
│   │   │   │-- __init__.py
│   │   │-- models.py
│   │   │-- views.py
│   │   │-- urls.py
│   │   │-- forms.py
│   │   │-- test.py
│   │   │-- apps.py
│   │-- store/                     # Handles product management, cart, and wishlist
│   │   │-- migration
│   │   │   │-- __init__.py
│   │   │-- models.py
│   │   │-- views.py
│   │   │-- urls.py
│   │   │-- forms.py
│   │   │-- test.py
│   │   │-- apps.py
│   │-- payment/                    # Handles Razorpay integration
│   │   │-- migration
│   │   │   │-- __init__.py
│   │   │-- models.py
│   │   │-- views.py
│   │   │-- urls.py
│   │   │-- forms.py
│   │   │-- test.py
│   │   │-- apps.py
│   │-- price_comparison/           # Fetches price data from an Excel sheet
│   │   │-- utils.py
│-- static/                        # Static files (CSS, JS, Images)
│   │-- css
│   │   │-- base.css
│   │   │-- home.css
│   │-- images                      # Uploaded images
│   │   │-- *.jpg/png
│   │-- js
│   │   │-- script.js
│   │-- favicon.svg
│-- templates/                     # Global templates                       
│   │-- accounts
│   │   │-- login.html
│   │-- base
│   │   │-- base.html
│   │-- home
│   │   │-- index.html
│-- db.sqlite3                      # SQLite Database (can be changed to PostgreSQL)
│-- requirements.txt                 # Dependencies
│-- manage.py                        # Django's CLI management tool
│-- README.md                        # Project documentation

```
