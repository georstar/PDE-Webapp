# Troubleshooting Guide

## 🔧 Common Issues and Solutions

### Installation & Setup Issues

#### Issue: `ModuleNotFoundError: No module named 'django'`
**Solution:**
```bash
# Make sure virtual environment is activated
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows

# Install requirements
pip install -r requirements.txt

# Verify installation
python -c "import django; print(django.get_version())"
```

#### Issue: `Port 8000 already in use`
**Solution:**
```bash
# Use a different port
python manage.py runserver 8001

# Or kill the process using port 8000
# Linux/Mac:
lsof -ti:8000 | xargs kill -9

# Windows:
netstat -ano | findstr :8000
taskkill /PID <PID> /F
```

#### Issue: `No such table: pde_solver_pdesolution`
**Solution:**
```bash
# Run migrations to create tables
python manage.py migrate

# If that fails, reset database
rm db.sqlite3
python manage.py migrate
```

---

### Database Issues

#### Issue: `django.db.utils.ProgrammingError: relation does not exist`
**Solution:**
```bash
# Reset database completely
rm db.sqlite3
python manage.py migrate
python manage.py createsuperuser

# Or restore from backup
python manage.py loaddata backup.json
```

#### Issue: Database locked error
**Solution:**
```bash
# SQLite issue - close all connections
# Restart the server
python manage.py runserver

# For production, use PostgreSQL instead
```

#### Issue: Connection refused to PostgreSQL
**Solution:**
```bash
# Check if PostgreSQL is running
# Linux:
sudo systemctl status postgresql

# Start PostgreSQL
sudo systemctl start postgresql

# Check connection string in .env
DATABASE_URL=postgresql://user:password@localhost:5432/pde_db

# Test connection
psql -U postgres -d pde_db
```

---

### Application Issues

#### Issue: Static files not loading (404 errors)
**Solution:**
```bash
# Development - usually automatic, but can force:
python manage.py collectstatic --clear --noinput

# Check settings.py for correct paths
STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'

# Clear browser cache (Ctrl+Shift+Delete)
```

#### Issue: CSS/Bootstrap not styling properly
**Solution:**
```bash
# 1. Check Bootstrap CDN link in base.html
# Should be: https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css

# 2. Hard refresh browser (Ctrl+Shift+R on Windows/Linux, Cmd+Shift+R on Mac)

# 3. Check browser console for errors (F12 → Console)

# 4. Verify internet connection (CDN requires internet)
```

#### Issue: Forms not submitting
**Solution:**
```bash
# Check CSRF token in template
{% csrf_token %}  <!-- Should be in form -->

# Verify CSRF middleware is enabled in settings.py
'django.middleware.csrf.CsrfViewMiddleware'

# Check browser console for CSRF errors
```

---

### Solver Engine Issues

#### Issue: "Error solving PDE" message
**Solutions:**
1. Check equation notation:
   - Use `u_t` not `du/dt`
   - Use `u_xx` not `d²u/dx²`
   - Use `Eq(lhs, rhs)` format

2. Example of correct format:
   ```
   Eq(Derivative(u(x, t), t), Derivative(u(x, t), x, 2))
   ```

3. Or simpler form:
   ```
   Eq(u(x, t).diff(t), u(x, t).diff(x, 2))
   ```

#### Issue: PDE takes too long to solve
**Solution:**
```python
# Increase timeout in settings.py
PDE_SOLVER_TIMEOUT = 60  # Default is 30 seconds

# Or simplify the PDE:
# - Remove complex boundary conditions
# - Use standard forms (Heat, Wave, Laplace)
# - Reduce domain complexity
```

#### Issue: "NotImplementedError: Not implemented" when solving
**Solution:**
- This PDE type doesn't have a closed-form symbolic solution
- Try a simpler version of the PDE
- Use standard PDEs (Heat, Wave, Laplace) for guaranteed solutions

---

### User Interface Issues

#### Issue: Page layout broken
**Solution:**
```bash
# Clear Django cache
python manage.py shell
>>> from django.core.cache import cache
>>> cache.clear()

# Or delete compiled files
find . -type d -name __pycache__ -exec rm -r {} +

# Restart server
python manage.py runserver
```

#### Issue: Pagination not working
**Solution:**
```bash
# Check URL parameters are correct
# Should be: ?page=2 not ?page_num=2

# Verify PaginationMixin is used
paginate_by = 10
```

#### Issue: Delete/Edit buttons not appearing
**Solution:**
```bash
# Check user permissions (especially in admin)
# Make sure you're logged in as superuser

# Or check template syntax
{% if user.is_superuser %}
    <!-- Admin options -->
{% endif %}
```

---

### Admin Panel Issues

#### Issue: Can't login to admin panel
**Solution:**
```bash
# Create new superuser
python manage.py createsuperuser

# Reset password for existing user
python manage.py changepassword username

# Check admin middleware is enabled in settings.py
'django.contrib.auth.middleware.AuthenticationMiddleware'
```

#### Issue: Models not appearing in admin
**Solution:**
```bash
# Check admin.py registration:
from django.contrib import admin
from .models import PDESolution

@admin.register(PDESolution)
class PDESolutionAdmin(admin.ModelAdmin):
    pass
```

#### Issue: Saving object gives permission denied
**Solution:**
```bash
# Make sure you're logged in
# Check user has staff status
# Or give explicit permissions via Django shell
```

---

### Performance Issues

#### Issue: Page loads slowly
**Solution:**
```bash
# Check database query count (debug toolbar)
pip install django-debug-toolbar

# Optimize queries in views.py
# Use select_related() for ForeignKeys
# Use prefetch_related() for reverse relations

# Enable caching
python manage.py shell
>>> from django.core.cache import cache
>>> cache.set('key', value, timeout=300)
```

#### Issue: High memory usage
**Solution:**
```python
# In settings.py:
# Reduce Gunicorn workers
# Limit query results
# Use pagination (already implemented)

# Clear old solutions if database is large
PDESolution.objects.filter(
    created_at__lt=timezone.now() - timedelta(days=30)
).delete()
```

---

### Deployment Issues

#### Issue: "ModuleNotFoundError" on production server
**Solution:**
```bash
# Install Python dependencies in production environment
pip install -r requirements.txt

# Check Python version matches
python --version  # Should be 3.8+

# Activate correct virtual environment
source /var/www/pde-solver/venv/bin/activate
```

#### Issue: 502 Bad Gateway (Nginx)
**Solution:**
```bash
# Check if Gunicorn is running
sudo systemctl status pde-solver

# Restart Gunicorn
sudo systemctl restart pde-solver

# Check logs
sudo journalctl -u pde-solver -f

# Verify Nginx config
sudo nginx -t
sudo systemctl restart nginx
```

#### Issue: ALLOWED_HOSTS error
**Solution:**
```python
# In settings.py:
ALLOWED_HOSTS = ['your-domain.com', 'www.your-domain.com', 'localhost']

# Or use environment variable:
ALLOWED_HOSTS = os.getenv('ALLOWED_HOSTS', '').split(',')
```

---

### Email Configuration Issues

#### Issue: Email not sending
**Solution:**
```python
# In settings.py, check EMAIL backend:
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'your-email@gmail.com'
EMAIL_HOST_PASSWORD = 'your-app-password'  # Not regular password!

# Test email
python manage.py shell
>>> from django.core.mail import send_mail
>>> send_mail('Test', 'Message', 'from@example.com', ['to@example.com'])
```

---

### Git Issues

#### Issue: "fatal: not a git repository"
**Solution:**
```bash
# Initialize git in directory
cd /home/georstar/myRepos/PDE-Webapp
git init

# Or clone existing repo
git clone <repo-url>
```

#### Issue: Merge conflicts
**Solution:**
```bash
# See conflicts
git status

# Edit conflicted files manually
# Then stage and commit
git add .
git commit -m "Resolve conflicts"

# Or abort merge
git merge --abort
```

---

### Testing Issues

#### Issue: Tests fail with "ModuleNotFoundError"
**Solution:**
```bash
# Make sure all dependencies are installed
pip install -r requirements.txt

# Run tests with verbose output
python manage.py test -v 2

# Run specific test
python manage.py test pde_solver.tests.PDESolverTestCase
```

#### Issue: Database locked during tests
**Solution:**
```bash
# Django creates test database
# Usually cleans up automatically
# If stuck, restart shell:
exit()
python manage.py test
```

---

## 📋 Diagnostic Checklist

When something goes wrong, check:

- [ ] Is virtual environment activated?
- [ ] Are all dependencies installed? (`pip install -r requirements.txt`)
- [ ] Is database migrated? (`python manage.py migrate`)
- [ ] Are you using correct Python version? (3.8+)
- [ ] Is port 8000 available?
- [ ] Are CSRF cookies enabled in browser?
- [ ] Is JavaScript enabled?
- [ ] Have you cleared browser cache?
- [ ] Are there error messages in console? (Browser F12 → Console)
- [ ] Check Django logs in terminal
- [ ] Verify .env file has correct settings

---

## 📚 Getting Help

1. **Check Documentation**
   - README.md - Full documentation
   - QUICKSTART.md - Setup guide
   - DEPLOYMENT.md - Production guide

2. **Review Examples**
   - tests.py - Usage examples
   - solver.py - Solver documentation
   - views.py - View examples

3. **Debug Tips**
   - Use `python manage.py shell` for debugging
   - Check `db.sqlite3` with SQLite browser
   - Review Django logs in terminal
   - Use browser developer tools (F12)

4. **Common Resources**
   - Django Docs: https://docs.djangoproject.com/
   - SymPy Docs: https://docs.sympy.org/
   - Bootstrap Docs: https://getbootstrap.com/docs/

---

## 🆘 Emergency Recovery

If everything breaks:

```bash
# Backup current state
cp -r /home/georstar/myRepos/PDE-Webapp backup/

# Reset to clean state
rm db.sqlite3
rm -rf pde_solver/__pycache__
python manage.py migrate
python manage.py createsuperuser

# Restart from scratch
rm -rf venv/
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

---

**Last Updated**: January 14, 2026
**Version**: 1.0.0
