from pathlib import Path
import os

from dotenv import load_dotenv
import dj_database_url


BASE_DIR = Path(__file__).resolve().parent.parent


load_dotenv(
    BASE_DIR / '.env'
)


SECRET_KEY = 'django-insecure-change-this-later'


DEBUG = True


ALLOWED_HOSTS = []


# =========================================================
# APLICATIVOS
# =========================================================

INSTALLED_APPS = [

    'cadastro',

    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]


# =========================================================
# MIDDLEWARE
# =========================================================

MIDDLEWARE = [

    'django.middleware.security.SecurityMiddleware',

    'django.contrib.sessions.middleware.SessionMiddleware',

    'django.middleware.locale.LocaleMiddleware',

    'django.middleware.common.CommonMiddleware',

    'django.middleware.csrf.CsrfViewMiddleware',

    'django.contrib.auth.middleware.AuthenticationMiddleware',

    'django.contrib.messages.middleware.MessageMiddleware',

    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]


# =========================================================
# URLS
# =========================================================

ROOT_URLCONF = 'config.urls'


# =========================================================
# TEMPLATES
# =========================================================

TEMPLATES = [

    {
        'BACKEND':
            'django.template.backends.django.DjangoTemplates',

        'DIRS': [],

        'APP_DIRS': True,

        'OPTIONS': {

            'context_processors': [

                'django.template.context_processors.request',

                'django.contrib.messages.context_processors.messages',

                'django.contrib.auth.context_processors.auth',

                'django.template.context_processors.i18n',
            ],
        },
    },
]


WSGI_APPLICATION = 'config.wsgi.application'


# =========================================================
# BANCO DE DADOS
# =========================================================

DATABASES = {

    'default': dj_database_url.config(
        default=os.getenv('DATABASE_URL')
    )
}


# =========================================================
# IDIOMAS
# =========================================================

LANGUAGES = [

    (
        'pt-br',
        'Português (Brasil)'
    ),

    (
        'pt-pt',
        'Português (Portugal)'
    ),

    (
        'en',
        'English'
    ),

    (
        'ja',
        '日本語'
    ),

    (
        'de',
        'Deutsch'
    ),
]


LANGUAGE_CODE = 'pt-br'


LOCALE_PATHS = [

    BASE_DIR / 'locale',

]


# =========================================================
# SENHAS
# =========================================================

AUTH_PASSWORD_VALIDATORS = [

    {
        'NAME':
            'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'
    },

    {
        'NAME':
            'django.contrib.auth.password_validation.MinimumLengthValidator'
    },

    {
        'NAME':
            'django.contrib.auth.password_validation.CommonPasswordValidator'
    },

    {
        'NAME':
            'django.contrib.auth.password_validation.NumericPasswordValidator'
    },
]


# =========================================================
# IDIOMA / DATA
# =========================================================

TIME_ZONE = 'America/Sao_Paulo'

USE_I18N = True

USE_TZ = True


# =========================================================
# ARQUIVOS ESTÁTICOS
# =========================================================

STATIC_URL = 'static/'


# =========================================================
# BANCO
# =========================================================

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


# =========================================================
# SESSÃO
# =========================================================

SESSION_EXPIRE_AT_BROWSER_CLOSE = True