import os
import environ
from pathlib import Path
from decouple import config

# Initialize environment variables
env = environ.Env()
environ.Env.read_env()  # Read .env file

BASE_DIR = Path(__file__).resolve().parent.parent

# Email configuration
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = env('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = env('EMAIL_HOST_PASSWORD')
DEFAULT_FROM_EMAIL = EMAIL_HOST_USER

# Additional email for feedback (if used)
FEEDBACK_EMAIL_HOST_USER = env('FEEDBACK_EMAIL_HOST_USER', default=EMAIL_HOST_USER)
FEEDBACK_EMAIL_HOST_PASSWORD = env('FEEDBACK_EMAIL_HOST_PASSWORD', default=EMAIL_HOST_PASSWORD)

# Database settings
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# Static and media settings
STATIC_URL = 'static/'
STATICFILES_DIRS = [BASE_DIR / "static"]
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# Redirects after login/logout
LOGIN_REDIRECT_URL = "base:index"
LOGOUT_REDIRECT_URL = "base:login"

# Application definitions
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'corsheaders',
    'base',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'loginSignup.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

X_FRAME_OPTIONS = 'SAMEORIGIN'
# Zoom API Credentials
ZOOM_SECRET_TOKEN = config("ZOOM_SECRET_TOKEN")
ZOOM_VERIFICATION_TOKEN = config("ZOOM_VERIFICATION_TOKEN")
ZOOM_CLIENT_ID = config("ZOOM_CLIENT_ID")
ZOOM_CLIENT_SECRET = config("ZOOM_CLIENT_SECRET")
ZOOM_REDIRECT_URI = config("ZOOM_REDIRECT_URI")


 

