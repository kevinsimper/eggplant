"""
Django settings for eggplant project.

For more information on this file, see
https://docs.djangoproject.com/en/1.8/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.8/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
from os.path import dirname, abspath

from django.utils.translation import ugettext_lazy as _
from django.contrib.messages import constants as messages_constants

COOP_NAME = '{settings.COOP_NAME}'
COOP_DESCRIPTION = '{settings.COOP_DESCRIPTION}'
COOP_LOGO = 'img/missing-coop-logo.png'


MESSAGE_TAGS = {
    messages_constants.ERROR: 'danger',
}


BASE_DIR = dirname(dirname(dirname(abspath(__file__))))
PROJECT_DIR = os.path.join(BASE_DIR, 'eggplant_project')


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.8/howto/deployment/checklist/

ALLOWED_HOSTS = []

SITE_ID = 1
DOMAIN = 'localhost'
DEFAULT_HTTP_PROTOCOL = 'http'

AUTHENTICATION_BACKENDS = (
    # Needed to login by username in Django admin, regardless of `allauth`
    'django.contrib.auth.backends.ModelBackend',

    # `allauth` specific authentication methods, such as login by e-mail
    'allauth.account.auth_backends.AuthenticationBackend',

    # invited users only
    'eggplant.invitations.auth_backends.InvitationBackend',
)


# Application definition

INSTALLED_APPS = (
    'suit',  # django-admin-bootstrapped

    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',

    # 3rd-party apps.
    'django_filters',  # django-filter
    'bootstrap3',  # django-bootstrap3
    'allauth',  # django-allauth
    'allauth.account',
    'captcha',  # django-recaptcha
    'getpaid',  # django-getpaid
    'getpaid.backends.epaydk',

    # Project apps.
    'eggplant.accounts',
    'eggplant.core',
    'eggplant.dashboard',
    'eggplant.departments',
    'eggplant.invitations',
    'eggplant.market',
    'eggplant.permissions',
    'eggplant.profiles',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'eggplant.profiles.middleware.NewUserForceProfileMiddleware',
    'getpaid.middleware.SetRemoteAddrFromForwardedForMiddleware',
)

ROOT_URLCONF = 'eggplant_project.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            os.path.join(PROJECT_DIR, 'templates'),
        ],
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.template.context_processors.i18n',
                'django.template.context_processors.media',
                'django.template.context_processors.static',
                'django.template.context_processors.tz',
                'django.contrib.messages.context_processors.messages',
                'allauth.account.context_processors.account',
                'eggplant.core.context_processors.coop_vars',
            ],
            'loaders': [
                'django.template.loaders.filesystem.Loader',
                'django.template.loaders.app_directories.Loader',
            ],
        },
    },
]


WSGI_APPLICATION = 'eggplant_project.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.8/ref/settings/#databases

# Internationalization
# https://docs.djangoproject.com/en/1.8/topics/i18n/

LANGUAGE_CODE = 'en-us'

LANGUAGES = (
    ('en', _('English')),
    ('da', _('Danish')),
)

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.8/howto/static-files/

# please use `collectstatic` command
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATICFILES_DIRS = (os.path.join(PROJECT_DIR, 'static'), )

MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
MEDIA_URL = '/media/'

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'default': {
            'format': '%(asctime)s  [%(name)s:%(lineno)s]  %(levelname)s - %(message)s',
        },
        'simple': {
            'format': '%(levelname)s %(message)s',
        },
    },
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse',
        }
    },
    'handlers': {
        'null': {
            'level': 'DEBUG',
            'class': 'logging.NullHandler',
        },
        'console': {
            'level': 'INFO',
            'class': 'logging.StreamHandler',
            'formatter': 'default',
        },
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler',
        }
    },
    'loggers': {
        # Silence SuspiciousOperation.DisallowedHost exception ('Invalid
        # HTTP_HOST' header messages). Set the handler to 'null' so we don't
        # get those annoying emails.
        'django.security.DisallowedHost': {
            'handlers': ['null'],
            'propagate': False,
        },
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': True,
        },
        'django.db': {
            'handlers': ['console', ],
            'level': 'INFO',
        },
        'eggplant': {
            'handlers': ['console', ],
            'level': 'INFO',
        }
    }
}

ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_AUTHENTICATION_METHOD = 'email'
ACCOUNT_CONFIRM_EMAIL_ON_GET = False
USER_MODEL_USERNAME_FIELD = 'email'
# ACCOUNT_EMAIL_CONFIRMATION_ANONYMOUS_REDIRECT_URL = LOGIN_URL
# ACCOUNT_USER_MODEL_USERNAME_FIELD = None
ACCOUNT_USERNAME_REQUIRED = False
ACCOUNT_EMAIL_VERIFICATION = 'mandatory'
ACCOUNT_SIGNUP_PASSWORD_VERIFICATION = True
def ACCOUNT_USER_DISPLAY(u):
    return u.email
ACCOUNT_LOGIN_ON_EMAIL_CONFIRMATION = True
ACCOUNT_PASSWORD_MIN_LENGTH = 8
ACCOUNT_ADAPTER = 'eggplant_project.authnadapter.EggplantAccountAdapter'
# ACCOUNT_SIGNUP_FORM_CLASS
ACCOUNT_SESSION_REMEMBER = None

SITE_OPEN_FOR_SIGNUP = True
SIGNUP_URL_NAME = 'eggplant:profiles:signup'

LOGOUT_URL = 'account_logout'
LOGIN_URL = 'account_login'
LOGIN_REDIRECT_URL = 'eggplant:dashboard:home'

USE_RECAPTCHA = False
RECAPTCHA_PUBLIC_KEY = os.getenv('RECAPTCHA_PUBLIC_KEY', '6LfCEAcTAAAAAJsJhexp8LznEvngOghaw2ckFfq1')
RECAPTCHA_PRIVATE_KEY = os.getenv('RECAPTCHA_PRIVATE_KEY', '')
NOCAPTCHA = False
RECAPTCHA_USE_SSL = False

DATABASES = {}

from moneyed import DKK
DEFAULT_CURRENCY = DKK

GETPAID_ORDER_MODEL = 'market.Payment'

GETPAID_BACKENDS = (
    'getpaid.backends.epaydk',
)

GETPAID_BACKENDS_SETTINGS = {
    'getpaid.backends.epaydk': {
        'merchantnumber': os.getenv('EPAYDK_MERCHANTNUMBER', ''),
        'secret': os.getenv('EPAYDK_SECRET', ''),
        'callback_secret_path': os.getenv('EPAYDK_CALLBACK_SECRET_PATH', ''),
    },
}

GETPAID_SUCCESS_URL_NAME = 'eggplant:market:payment_accepted'
GETPAID_FAILURE_URL_NAME = 'eggplant:market:payment_rejected'

# If a new user has not completed his/her profile we force him to complete it.
NEW_USER_FORCE_PROFILE_ALLOWED_URL_NAMES = (
    'eggplant:profiles:profile',
    'account_login',
    'account_logout',
    'account_set_password',
)
