from os.path import join, abspath, dirname

here = lambda *x: join(abspath(dirname(__file__)), *x)
PROJECT_ROOT = here("..", "..")
root = lambda *x: join(abspath(PROJECT_ROOT), *x)

ALLOWED_HOSTS = []

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'webapp',
    'bootstrap3',
    'datetimewidget',
    'ckeditor',
    "ajaxuploader",
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'catalogarte.urls'

WSGI_APPLICATION = 'catalogarte.wsgi.application'

LANGUAGE_CODE = 'es'

TIME_ZONE = 'America/Mexico_City'

USE_I18N = True

USE_L10N = True

USE_TZ = True

STATIC_ROOT = root("static")
STATIC_URL = '/static/'

MEDIA_ROOT = root("media")
MEDIA_URL = '/media/'

CKEDITOR_UPLOAD_PATH = "uploads/"
CKEDITOR_IMAGE_BACKEND = 'pillow'
CKEDITOR_CONFIGS = {
    'default': {
        'toolbar': [
            [ 'Bold','Italic','Underline','Strike','Subscript','Superscript','-','RemoveFormat','-','Link','Unlink','-','Table','HorizontalRule' ],
            [ 'NumberedList','BulletedList','-','Outdent','Indent','-','Blockquote','-','JustifyLeft','JustifyCenter','JustifyRight','JustifyBlock' ],
            [ 'Styles','Format','Font','FontSize','TextColor','BGColor' ],
        ],
        'height': 300,
        'width': 550,
        'skin': 'bootstrapck',
    }
}

BOOTSTRAP3 = {
    'theme_url': '/static/webapp/css/material.min.css',
}

LOGIN_URL = "/login/"
