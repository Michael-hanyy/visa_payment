from pathlib import Path
import os
from dotenv import load_dotenv

# Load .env file
load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent

# --- Helper functions ---
def get_list(key):
    """Return a list from comma-separated .env values"""
    value = os.getenv(key, "")
    return [item.strip() for item in value.split(",") if item.strip()]

def get_password_validators():
    """Return password validators in Django format"""
    return [{'NAME': validator} for validator in get_list("AUTH_PASSWORD_VALIDATORS")]

def get_templates(base_dir):
    """Return templates configuration"""
    dirs = get_list("TEMPLATES_DIRS")
    return [
        {
            'BACKEND': 'django.template.backends.django.DjangoTemplates',
            'DIRS': [base_dir / d for d in dirs],
            'APP_DIRS': True,
            'OPTIONS': {
                'context_processors': [
                    'django.template.context_processors.debug',
                    'django.template.context_processors.request',
                    'django.contrib.auth.context_processors.auth',
                    'django.contrib.messages.context_processors.messages',
                ],
            },
        }
    ]

def get_database_config():
    """Return database dict"""
    return {
        'default': {
            'ENGINE': os.getenv("DB_ENGINE"),
            'NAME': os.getenv("DB_NAME"),
            'USER': os.getenv("DB_USER"),
            'PASSWORD': os.getenv("DB_PASSWORD"),
            'HOST': os.getenv("DB_HOST"),
            'PORT': os.getenv("DB_PORT"),
        }
    }

def get_rest_framework():
    """Return REST framework authentication config"""
    return {
        'DEFAULT_AUTHENTICATION_CLASSES': tuple(get_list("REST_AUTH_CLASSES"))
    }

def get_celery_config():
    """Return Celery config"""
    return {
        'broker_url': os.getenv("CELERY_BROKER_URL"),
        'accept_content': [os.getenv("CELERY_ACCEPT_CONTENT")],
        'task_serializer': os.getenv("CELERY_TASK_SERIALIZER"),
        'timezone': os.getenv("CELERY_TIMEZONE"),
    }

# --- Security ---
SECRET_KEY = os.getenv("SECRET_KEY")
DEBUG = os.getenv("DEBUG", "False").lower() == "true"
ALLOWED_HOSTS = get_list("ALLOWED_HOSTS")

# --- Apps & Middleware ---
INSTALLED_APPS = get_list("INSTALLED_APPS")
MIDDLEWARE = get_list("MIDDLEWARE")

# --- Root & Templates ---
ROOT_URLCONF = os.getenv("ROOT_URLCONF")
TEMPLATES = get_templates(BASE_DIR)
WSGI_APPLICATION = os.getenv("WSGI_APPLICATION")

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": os.getenv("DB_NAME"),
        "USER": os.getenv("DB_USER"),
        "PASSWORD": os.getenv("DB_PASSWORD"),
        "HOST": os.getenv("DB_HOST"),
        "PORT": os.getenv("DB_PORT"),
    }
}

# --- Password Validators ---
AUTH_PASSWORD_VALIDATORS = get_password_validators()

# --- Internationalization ---
LANGUAGE_CODE = os.getenv("LANGUAGE_CODE", "en-us")
TIME_ZONE = os.getenv("TIME_ZONE", "UTC")
USE_I18N = os.getenv("USE_I18N", "True").lower() == "true"
USE_TZ = os.getenv("USE_TZ", "True").lower() == "true"

# --- Static ---
STATIC_URL = os.getenv("STATIC_URL", "/static/")
DEFAULT_AUTO_FIELD = os.getenv("DEFAULT_AUTO_FIELD", "django.db.models.BigAutoField")

# --- DRF ---
REST_FRAMEWORK = get_rest_framework()

# --- Email ---
EMAIL_BACKEND = os.getenv("EMAIL_BACKEND")

# --- Celery ---
celery_conf = get_celery_config()
CELERY_BROKER_URL = celery_conf['broker_url']
CELERY_ACCEPT_CONTENT = celery_conf['accept_content']
CELERY_TASK_SERIALIZER = celery_conf['task_serializer']
CELERY_TIMEZONE = celery_conf['timezone']

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "users",
    "payments",
    "visa_payment",
  
]
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',   # Required
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',  # Required
    'django.contrib.messages.middleware.MessageMiddleware',    # Required
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

