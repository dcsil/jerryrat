#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys
import django.db.utils
from django.db import connection

def main():
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myproject.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        )

    try:
        execute_from_command_line(sys.argv)
    except django.db.utils.OperationalError as dbError:
        if "1050" in str(dbError):
            pass
        else:
            raise dbError


if __name__ == '__main__':
    main()
