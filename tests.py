import os
import sys
import django


def main():
    """
    Standalone django model test with a 'memory-only-django-installation'.
    You can play with a django model without a complete django app installation.
    http://www.djangosnippets.org/snippets/1044/
    """
    import logging
    logging.basicConfig()

    os.environ["DJANGO_SETTINGS_MODULE"] = "django.conf.global_settings"
    from django.conf import global_settings

    global_settings.SECRET_KEY = "SECRET"
    global_settings.INSTALLED_APPS = (
        'django.contrib.auth',
        'django.contrib.contenttypes',
        'beproud.django.mailer',
        'djcelery',
    )
    global_settings.DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': ':memory:',
        }
    }

    # For Celery Tests
    global_settings.CELERY_ALWAYS_EAGER = True
    global_settings.CELERY_EAGER_PROPAGATES_EXCEPTIONS = True

    if django.VERSION > (1, 7):
        django.setup()

    from django.test.utils import get_runner
    test_runner = get_runner(global_settings)

    if django.VERSION > (1, 2):
        test_runner = test_runner()
        if django.VERSION > (1, 6):
            tests = ['beproud.django.mailer']
        else:
            tests = ['mailer']
        failures = test_runner.run_tests(tests)
    else:
        failures = test_runner(['mailer'], verbosity=1)

    sys.exit(failures)

if __name__ == '__main__':
    main()
