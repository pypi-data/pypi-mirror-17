# ** Initial Settings **

#ApiBase settings
---------------------------------------------------------------------------------------------

```
#!python

API_TESTING = True

ACCESS_TOKEN_EXPIRE_DAYS = 15

INSTALLED_APPS = [
    ...
    'Common'  # Add Common module in installed apps like this
]

```

---------------------------------------------------------------------------------------------

```
#!python

# Should be included in the __init__.py file of the project directory
# so that it will run before the settings file is executed.
with open('.env', 'r+') as env_file:
    import re
    for line in env_file.readlines():
        data = re.match("([A-Z]\w+) = '(.*)'", line)
        os.environ.setdefault(data.group(1), data.group(2))

```

---------------------------------------------------------------------------------------------

```
#!python

# Copy the secret key from the django settings and add it in the sample env and .env file
# Replace secret key in django setting with below code
os.environ['SECRET_KEY']

```

----------------------------------------------------------------------------------------------

```
#!python

# Activate this middleware to handle all unhandled exception in code (Optional)
MIDDLEWARE_CLASSES = [
    ...
    'Common.CommonExceptionHandler.CommonExceptionHandler'  # CommonExceptionHandler Middleware should be added here
]

```

---------------------------------------------------------------------------------------------
# MySQL settings
```
#!python

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': os.environ['DATABASE_NAME'],
        'USER': os.environ['DATABASE_USER'],
        'PASSWORD': os.environ['DATABASE_PASSWORD'],
        'HOST': '',   # Or an IP Address that your DB is hosted on
        'PORT': '',
    }
}

```

---------------------------------------------------------------------------------------------
# ** Other Settings **
---------------------------------------------------------------------------------------------
# Email Configuration

```
#!python

#Email configuration
EMAIL_USE_TLS = True
EMAIL_HOST = os.environ['EMAIL_HOST']
EMAIL_PORT = 587  # Set port 2525, google compute engine doesn't support 587
EMAIL_HOST_USER = os.environ['EMAIL_HOST_USER']
EMAIL_HOST_PASSWORD = os.environ['EMAIL_HOST_PASSWORD']

```

---------------------------------------------------------------------------------------------
# Static/Media files settings

```
#!python

STATIC_URL = '/static/'

STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

STATICFILES_DIRS = (
    os.path.join(BASE_DIR, 'static'),
)


# Media files configuration
MEDIA_URL = '/media/'

MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

```

--------------------------------------------------------------------------------------------
# Logging Settings

```
#!python

# Logging settings
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': "[%(asctime)s] %(levelname)s [%(name)s:%(lineno)s] %(message)s",
            'datefmt': "%d/%b/%Y %H:%M:%S"
        },
        'simple': {
            'format': '%(levelname)s %(message)s'
        },
    },
    'handlers': {
        'file': {
            'level': 'INFO',
            'class': 'logging.FileHandler',
            'filename': 'mysite.log',
            'formatter': 'verbose'
        },
    },
    'loggers': {
        'django': {
            'handlers': ['file'],
            'propagate': True,
            'level': 'DEBUG',
        },
        'Common': {
            'handlers': ['file'],
            'level': 'INFO',
        },
    }
}

```

--------------------------------------------------------------------------------------
# Push Notification Settings (Only Applicable if using django-push-notifications package)

```
#!python

# Push notification settings
PUSH_NOTIFICATIONS_SETTINGS = {
        "GCM_API_KEY": os.environ['GCM_API_KEY'],
        "APNS_CERTIFICATE": os.path.join(BASE_DIR,'<location-to-apns-certificate>'),
}

```

-------------------------------------------------------------------------------------
# Media settings (Use in Base url.py file - Used if django don't recognize media url)

```
#!python

# Media settings
if settings.DEBUG:
    # static files (images, css, javascript, etc.)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

```

-------------------------------------------------------------------------------------