#!/bin/sh

# Apply database migrations
echo "Apply database migrations"
python manage.py migrate

# Create superuser
echo "from django.contrib.auth.models import User; User.objects.create_superuser('admin', 'swat.ar123@gmail.com', '1')" | python manage.py shell

# Start server
echo "Starting server"
python manage.py runserver 0.0.0.0:8000

echo "End Connection"