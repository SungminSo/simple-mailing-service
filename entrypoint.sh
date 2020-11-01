# Apply database migrations
echo "Apply database migrations"
python manage.py db migrate
python manage.py db upgrade

# Start server
echo "Start server"
python manage.py run