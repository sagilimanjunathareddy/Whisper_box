import os
from pathlib import Path

# Base directory
BASE_DIR = Path(__file__).resolve().parent.parent

# SECURITY WARNING: keep secret key safe in production!
SECRET_KEY = 'django-insecure-test-key-change-it-later'

# Development mode
DEBUG = True

ALLOWED_HOSTS = []

# Installed apps
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # Third-party
    'rest_framework',

    # Project apps
    'stories',
    'comments',
    'heatmap',
    'admin_dashboard',
]

# Middleware
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'whisperbox.urls'

# Templates
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',

        # Global templates folder
        'DIRS': [BASE_DIR / 'templates'],

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

WSGI_APPLICATION = 'whisperbox.wsgi.application'

# DATABASE (SQLite – easiest)
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',   # REQUIRED
        'NAME': BASE_DIR / 'db.sqlite3',         # REQUIRED
    }
}

# Password validators (disabled for dev)
AUTH_PASSWORD_VALIDATORS = []

# Localization
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'Asia/Kolkata'
USE_I18N = True
USE_TZ = True

# Static files
STATIC_URL = '/static/'
STATICFILES_DIRS = [
    BASE_DIR / 'static',   # PROJECT-LEVEL STATIC DIRECTORY
]

# Auto field
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# At bottom of settings.py
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# Add a maximum upload size (bytes) — e.g., 5 MB
MAX_UPLOAD_SIZE = 5 * 1024 * 1024  # 5 MiB
# Allowed content types
ALLOWED_UPLOAD_CONTENT_TYPES = ['image/jpeg', 'image/png', 'image/webp', 'application/pdf']

