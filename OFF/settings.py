from pathlib import Path
import os
from dotenv import load_dotenv

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

load_dotenv(BASE_DIR / '.env')

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

# CORREÇÃO APLICADA: Adicionando 'dev' como valor padrão,
# para evitar que TARGET_ENV seja None se a variável não estiver definida.
TARGET_ENV = os.getenv('TARGET_ENV', 'dev') 
NOT_PROD = not TARGET_ENV.lower().startswith('prod')

if NOT_PROD:
    # SECURITY WARNING: don't run with debug turned on in production!
    DEBUG = True
    # SECURITY WARNING: keep the secret key used in production secret!
    SECRET_KEY = '60zm-t6f&&s4pdu=pn3u4ie2$qykg(22gpq+fe@=qz@gf(shjp'
    ALLOWED_HOSTS = []
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        }
    }
else:
    SECRET_KEY = os.getenv('SECRET_KEY')
    DEBUG = os.getenv('DEBUG', '0').lower() in ['true', 't', '1']
    ALLOWED_HOSTS = os.getenv('ALLOWED_HOSTS').split(' ')
    CSRF_TRUSTED_ORIGINS = os.getenv('CSRF_TRUSTED_ORIGINS').split(' ')

    SECURE_SSL_REDIRECT = \
        os.getenv('SECURE_SSL_REDIRECT', '0').lower() in ['true', 't', '1']

    if SECURE_SSL_REDIRECT:
        SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql',
            'NAME': os.environ.get('DBNAME'),
            'HOST': os.environ.get('DBHOST'),
            'USER': os.environ.get('DBUSER'),
            'PASSWORD': os.environ.get('DBPASS'),
            'OPTIONS': {'sslmode': 'require'},
        }
    }
    
# Application definition


# ======================
# APPS
# ======================

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "whitenoise.runserver_nostatic",
    "storages",       # ✅ adicionado para suporte Azure Blob
    "core",
]

# ======================
# MIDDLEWARE
# ======================

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

# ======================
# URLS / TEMPLATES / WSGI
# ======================

ROOT_URLCONF = 'OFF.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
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

WSGI_APPLICATION = 'OFF.wsgi.application'

# ======================
# PASSWORDS
# ======================

AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# ======================
# INTERNACIONALIZAÇÃO
# ======================

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

STATIC_URL = os.environ.get('DJANGO_STATIC_URL', "/static/")
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static'),
    os.path.join(BASE_DIR, 'images'),   # Onde estão suas fotos de fundo
]

STATICFILES_STORAGE = ('whitenoise.storage.CompressedManifestStaticFilesStorage')
# MEDIA FILES (LOCAL + AZURE)
# ======================

if NOT_PROD:
    # Ambiente local: salvar e servir da pasta /midia/
    MEDIA_URL = '/midia/'
    MEDIA_ROOT = BASE_DIR / 'midia'

else:
    # Ambiente de produção (Azure Blob Storage)
    AZURE_ACCOUNT_NAME = os.getenv('AZURE_ACCOUNT_NAME')
    AZURE_ACCOUNT_KEY = os.getenv('AZURE_ACCOUNT_KEY')
    AZURE_CONTAINER = os.getenv('AZURE_CONTAINER', 'media')

    DEFAULT_FILE_STORAGE = 'storages.backends.azure_storage.AzureStorage'
    AZURE_URL_EXPIRATION_SECS = None    # URLs fixas (sem expiração)

    # URL base dos arquivos armazenados no Azure Blob
    MEDIA_URL = f'https://{AZURE_ACCOUNT_NAME}.blob.core.windows.net/{AZURE_CONTAINER}/'
 
# ======================
# AUTENTICAÇÃO
# ======================

AUTH_USER_MODEL = 'core.Usuario'
LOGIN_URL = 'login'
LOGIN_REDIRECT_URL = 'core:home'
LOGOUT_REDIRECT_URL = 'core:home'

# ======================
# SESSÃO
# ======================

SESSION_COOKIE_AGE = 60 * 60 * 24 * 30  # 30 dias
SESSION_EXPIRE_AT_BROWSER_CLOSE = False
SESSION_COOKIE_SAMESITE = None
CSRF_COOKIE_SAMESITE = None
SESSION_COOKIE_SECURE = False
CSRF_COOKIE_SECURE = False

# ======================
# PADRÃO DJANGO
# ======================

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'