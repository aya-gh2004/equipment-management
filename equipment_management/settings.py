"""
Django settings for equipment_management project — version corrigée.
"""

import os
from pathlib import Path
import dj_database_url

# ================================
# 🔧 Base paths
# ================================
BASE_DIR = Path(__file__).resolve().parent.parent

# ================================
# 🔐 Secret key & Debug
# ================================
SECRET_KEY = os.environ.get("DJANGO_SECRET_KEY", "changeme-in-production")

DEBUG = os.environ.get("DEBUG", "True") == "True"

ALLOWED_HOSTS = [
    os.environ.get("RENDER_EXTERNAL_HOSTNAME", "127.0.0.1"),
    "localhost",
]

# ================================
# 👤 Authentification
# ================================
AUTH_USER_MODEL = 'equipment.CustomUser'

AUTHENTICATION_BACKENDS = [
    'equipment.backends.EmailBackend',        # ✅ ton backend personnalisé pour login avec email
    'django.contrib.auth.backends.ModelBackend',  # ✅ fallback classique
]

LOGIN_URL = '/login/'
LOGIN_REDIRECT_URL = '/dashboard/'
LOGOUT_REDIRECT_URL = '/'

# ================================
# 📦 Installed apps
# ================================
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # Local apps
    'equipment',
    # External packages
    'widget_tweaks',
    'rest_framework',
    'corsheaders',
    'rest_framework.authtoken',
    'django_filters',
    'django_extensions',
    'dal',
    'dal_select2',
]

# ================================
# ⚙️ Middleware
# ================================
MIDDLEWARE = [
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "django.middleware.locale.LocaleMiddleware",
]

# ================================
# 🧩 Templates
# ================================
TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

# ================================
# 🛠 URLs & WSGI
# ================================
ROOT_URLCONF = "equipment_management.urls"
WSGI_APPLICATION = "equipment_management.wsgi.application"

# ================================
# 🗄 Base de données
# ================================
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'equipment_db',
        'USER': 'postgres',
        'PASSWORD': 'aya2004',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}

# ✅ Automatic config si DATABASE_URL existe (Render)
DATABASES['default'] = dj_database_url.config(
    default=os.environ.get(
        'DATABASE_URL',
        'postgresql://postgres:aya2004@localhost:5432/equipment_db'
    ),
    conn_max_age=600,
)

# ================================
# 🔐 Password validators
# ================================
AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

# ================================
# 🌍 Internationalisation
# ================================
LANGUAGE_CODE = "fr"
USE_I18N = True
USE_L10N = True
USE_TZ = True

# ================================
# 📁 Static & media
# ================================
STATIC_URL = "/static/"
STATIC_ROOT = BASE_DIR / "staticfiles"
STATICFILES_DIRS = [BASE_DIR / "static"]
STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"

MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "media"

# ================================
# 🔄 REST Framework
# ================================
REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": [
        "rest_framework.authentication.SessionAuthentication",
        "rest_framework.authentication.TokenAuthentication",
    ],
    "DEFAULT_PERMISSION_CLASSES": [
        "rest_framework.permissions.IsAuthenticated",
    ],
}

# ================================
# 🌐 CORS & CSRF
# ================================
CORS_ALLOW_ALL_ORIGINS = True
CORS_ALLOW_CREDENTIALS = True
CSRF_TRUSTED_ORIGINS = [
    "https://*.onrender.com",
    "http://localhost:8000",
    "http://127.0.0.1:8000",
]

# ================================
# 📧 Email
# ================================
EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_HOST = "smtp.gmail.com"
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = "ayaghimouze594@gmail.com"
EMAIL_HOST_PASSWORD = "hionsshrtmfpdvnz"
DEFAULT_FROM_EMAIL = EMAIL_HOST_USER

# ================================
# 🧠 Sessions
# ================================
SESSION_ENGINE = "django.contrib.sessions.backends.db"
SESSION_COOKIE_AGE = 3600
SESSION_EXPIRE_AT_BROWSER_CLOSE = True

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
