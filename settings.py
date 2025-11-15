import os
import dj_database_url
from dotenv import load_dotenv

load_dotenv()

from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent

# Ensure template directories exist
TEMPLATE_DIRS = [
    BASE_DIR / 'templates',
    BASE_DIR / 'templates/base',
    BASE_DIR / 'authentication/templates',
]
for template_dir in TEMPLATE_DIRS:
    template_dir.mkdir(parents=True, exist_ok=True)

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get('SECRET_KEY', '9qn38d*9#t*)oe0ic=cisa4oe%sbu2g@-2#!&wjqik%7b5!yjw')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = os.getenv('DEBUG', 'False') == 'True'

# Hosts permitidos
ALLOWED_HOSTS = ['*'] if DEBUG else ['pi2univesp.onrender.com', '.onrender.com']

# Silenciar check de URLs para o django-two-factor-auth que usa re_path
SILENCED_SYSTEM_CHECKS = ['urls.E004']

# CSRF settings
CSRF_TRUSTED_ORIGINS = ['https://pi2univesp.onrender.com', 'http://localhost:8000', 'http://127.0.0.1:8000']

# Application definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django_otp',
    'django_otp.plugins.otp_static',
    'django_otp.plugins.otp_totp',
    'two_factor',
    'caaordserv.apps.CaaordservConfig',
    'authentication.apps.AuthenticationConfig',
    'relatorios.apps.RelatoriosConfig',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django_otp.middleware.OTPMiddleware',
    'two_factor.middleware.threadlocals.ThreadLocals',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        # V-- CORREÇÃO: Adicionado 'templates/base' para encontrar base_auth.html
        'DIRS': [BASE_DIR / 'templates', BASE_DIR / 'templates/base'],
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

WSGI_APPLICATION = 'wsgi.application'

# Database
if DEBUG:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        }
    }
else:
    DATABASES = {
        'default': dj_database_url.config(
            default='postgresql://user:password@localhost/dbname',
            conn_max_age=600,
            conn_health_checks=True,
            ssl_require=True
        )
    }

# Password validation
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# Internationalization
LANGUAGE_CODE = 'pt-br'
TIME_ZONE = 'America/Sao_Paulo'
USE_I18N = True
USE_TZ = True

# Static files (CSS, JavaScript, Images)
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
# V-- CORREÇÃO: Removido para evitar conflitos com 'app/static/'
# STATICFILES_DIRS = [BASE_DIR / 'static']
STATICFILES_DIRS = []

# Configuração do WhiteNoise baseada no ambiente
STATICFILES_STORAGE = 'whitenoise.storage.CompressedStaticFilesStorage' if not DEBUG else 'django.contrib.staticfiles.storage.StaticFilesStorage'

# ============================================
# CONFIGURAÇÕES DE SESSÃO - CRÍTICO PARA 2FA
# ============================================
SESSION_ENGINE = 'django.contrib.sessions.backends.db'  # Usar banco de dados
SESSION_COOKIE_SECURE = not DEBUG  # True em produção (HTTPS)
SESSION_COOKIE_HTTPONLY = True
SESSION_COOKIE_SAMESITE = 'Lax'
SESSION_COOKIE_AGE = 86400  # 24 horas
SESSION_SAVE_EVERY_REQUEST = True  # Atualiza sessão a cada request
SESSION_EXPIRE_AT_BROWSER_CLOSE = False

# ============================================
# CONFIGURAÇÕES DE SEGURANÇA - PRODUÇÃO
# ============================================
if not DEBUG:
    SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
    SECURE_SSL_REDIRECT = True
    CSRF_COOKIE_SECURE = True
    # Cookies de sessão já configurados acima
else:
    SECURE_SSL_REDIRECT = False
    CSRF_COOKIE_SECURE = False

# Default primary key field type
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Configurações de mídia
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# ============================================
# CONFIGURAÇÕES DE AUTENTICAÇÃO E 2FA
# ============================================
LOGIN_URL = 'two_factor:login'
LOGIN_REDIRECT_URL = 'caaordserv'  # A sua página principal
LOGOUT_REDIRECT_URL = 'two_factor:login'

# Django-two-factor-auth settings
TWO_FACTOR_PATCH_ADMIN = True  # Protege o admin com 2FA
TWO_FACTOR_CALL_GATEWAY = None  # Desabilita chamadas telefônicas
TWO_FACTOR_SMS_GATEWAY = None   # Desabilita SMS

# QR Code settings
TWO_FACTOR_QR_FACTORY = 'qrcode.image.svg.SvgPathImage'

# ============================================
# LOGGING PARA DEBUG EM PRODUÇÃO
# ============================================
if not DEBUG:
    LOGGING = {
        'version': 1,
        'disable_existing_loggers': False,
        'formatters': {
            'verbose': {
                'format': '{levelname} {asctime} {module} {message}',
                'style': '{',
            },
        },
        'handlers': {
            'console': {
                'class': 'logging.StreamHandler',
                'formatter': 'verbose',
            },
        },
        'loggers': {
            'django': {
                'handlers': ['console'],
                'level': 'INFO',
            },
            'django.request': {
                'handlers': ['console'],
                'level': 'ERROR',
                'propagate': False,
            },
            'two_factor': {
                'handlers': ['console'],
                'level': 'DEBUG',
            },
        },
    }