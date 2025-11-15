#!/usr/bin/env bash
# exit on error
set -o errexit

# Install dependencies
pip install -r requirements.txt

# Collect static files
python manage.py collectstatic --no-input

# Run migrations
python manage.py migrate

# Comando para criar o superusuário se ele ainda não existir.
# As credenciais são lidas de variáveis de ambiente do Render.
python manage.py createsuperuser --no-input || true