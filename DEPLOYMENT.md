# Deployment Guide

## Production Deployment Checklist

### 1. Environment Setup
- [ ] Set `DEBUG = False` in settings.py
- [ ] Generate a new `SECRET_KEY`
- [ ] Configure `ALLOWED_HOSTS` with your domain
- [ ] Create `.env` file with production values
- [ ] Set up PostgreSQL database (recommended for production)
- [ ] Configure email backend for notifications

### 2. Security Configuration
```python
# settings.py
DEBUG = False
SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
ALLOWED_HOSTS = ['your-domain.com', 'www.your-domain.com']
```

### 3. Database Setup
```bash
# Create PostgreSQL database
createdb pde_db
createuser pde_user
psql -U postgres -d pde_db -c "ALTER USER pde_user WITH PASSWORD 'strong_password';"

# Update settings.py or .env
DATABASE_URL=postgresql://pde_user:strong_password@localhost:5432/pde_db
```

### 4. Collect Static Files
```bash
python manage.py collectstatic --noinput
```

### 5. Run Migrations
```bash
python manage.py migrate
```

### 6. Create Superuser
```bash
python manage.py createsuperuser
```

### 7. Deployment Options

#### Option A: Heroku
```bash
# Install Heroku CLI
pip install heroku

# Create Procfile
echo "web: gunicorn pde_project.wsgi" > Procfile

# Create runtime.txt
echo "python-3.10.0" > runtime.txt

# Deploy
git push heroku main
```

#### Option B: Docker
```dockerfile
# Dockerfile
FROM python:3.10
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["gunicorn", "pde_project.wsgi:application", "--bind", "0.0.0.0:8000"]
```

```bash
docker build -t pde-solver .
docker run -p 8000:8000 pde-solver
```

#### Option C: Traditional VPS (Ubuntu/Debian)
```bash
# Update system
sudo apt-get update && sudo apt-get upgrade

# Install dependencies
sudo apt-get install python3-pip python3-venv postgresql postgresql-contrib nginx

# Clone project
git clone <repo> /var/www/pde-solver
cd /var/www/pde-solver

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install Python dependencies
pip install -r requirements.txt

# Create systemd service
sudo nano /etc/systemd/system/pde-solver.service
```

**systemd service file:**
```ini
[Unit]
Description=PDE Solver Django App
After=network.target

[Service]
User=www-data
WorkingDirectory=/var/www/pde-solver
ExecStart=/var/www/pde-solver/venv/bin/gunicorn \
          --workers 3 \
          --bind unix:/tmp/gunicorn.sock \
          pde_project.wsgi:application
Restart=always

[Install]
WantedBy=multi-user.target
```

```bash
# Enable and start service
sudo systemctl enable pde-solver
sudo systemctl start pde-solver
```

**Nginx configuration:**
```nginx
server {
    listen 80;
    server_name your-domain.com;

    location /static/ {
        alias /var/www/pde-solver/staticfiles/;
    }

    location /media/ {
        alias /var/www/pde-solver/media/;
    }

    location / {
        proxy_pass http://unix:/tmp/gunicorn.sock;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

### 8. SSL Certificate (Let's Encrypt)
```bash
sudo apt-get install certbot python3-certbot-nginx
sudo certbot certonly --nginx -d your-domain.com
```

### 9. Monitoring and Logging
```bash
# View logs
sudo journalctl -u pde-solver -f

# Monitor uptime
sudo apt-get install monit
```

### 10. Backup Strategy
```bash
# Backup database
pg_dump pde_db > backup_$(date +%Y%m%d).sql

# Backup static files
tar -czf static_backup_$(date +%Y%m%d).tar.gz staticfiles/

# Restore
psql pde_db < backup_YYYYMMDD.sql
```

## Performance Optimization

### 1. Database Optimization
```python
# settings.py
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'CONN_MAX_AGE': 600,  # Connection pooling
    }
}
```

### 2. Caching
```python
# Add Redis caching
CACHES = {
    'default': {
        'BACKEND': 'django_redis.cache.RedisCache',
        'LOCATION': 'redis://127.0.0.1:6379/1',
    }
}
```

### 3. Gunicorn Configuration
```bash
gunicorn --workers 4 \
         --worker-class sync \
         --worker-connections 1000 \
         --max-requests 1000 \
         --timeout 30 \
         pde_project.wsgi:application
```

## Troubleshooting

### 502 Bad Gateway
- Check if Gunicorn is running
- Verify Nginx configuration
- Check error logs: `sudo journalctl -u pde-solver -f`

### Static files not loading
```bash
python manage.py collectstatic --clear --noinput
```

### Database connection errors
```bash
# Test database connection
python manage.py shell
>>> from django.db import connection
>>> connection.ensure_connection()
```

### High memory usage
- Reduce Gunicorn workers
- Enable Redis caching
- Implement query optimization

## Monitoring Checklist

- [ ] Set up error tracking (Sentry)
- [ ] Configure logging
- [ ] Set up uptime monitoring
- [ ] Create database backup schedule
- [ ] Monitor CPU and memory usage
- [ ] Set up log rotation
- [ ] Configure rate limiting
- [ ] Implement CORS if needed

## Post-Deployment

1. Test all features in production
2. Set up automated backups
3. Configure monitoring alerts
4. Document deployment procedure
5. Create disaster recovery plan
6. Schedule regular security updates
