#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys
import environ

def main():
    """Run administrative tasks."""

    # Choix automatique de l'env local ou docker
    env = environ.Env()
    if os.path.exists(".env.local"):
        environ.Env.read_env(".env.local")
    elif os.path.exists(".env.docker"):
        environ.Env.read_env(".env.docker")

    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mollidays.settings')

    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)

if __name__ == '__main__':
    main()
