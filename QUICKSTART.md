# Quick Start Guide - PDE Solver Web App

## 🚀 Get Started in 5 Minutes

### 1. Set up the environment
```bash
cd /home/georstar/myRepos/PDE-Webapp
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 2. Install dependencies
```bash
pip install -r requirements.txt
```

### 3. Initialize the database
```bash
python manage.py migrate
```

### 4. Create admin account (optional)
```bash
python manage.py createsuperuser
```

### 5. Run the server
```bash
python manage.py runserver
```

### 6. Open in browser
Visit: http://localhost:8000

---

## 📝 Example PDEs to Try

### Heat Equation (Diffusion)
- **Equation**: `u_t = u_xx`
- **Boundary**: `u(0,t) = 0, u(1,t) = 0`
- **Initial**: `u(x,0) = sin(pi*x)`

### Wave Equation
- **Equation**: `u_tt = u_xx`
- **Boundary**: `u(0,t) = 0, u(L,t) = 0`
- **Initial**: `u(x,0) = sin(pi*x), u_t(x,0) = 0`

### Laplace Equation
- **Equation**: `u_xx + u_yy = 0`
- **Boundary**: Various boundary conditions

---

## 🎯 Features Overview

| Feature | Description |
|---------|-------------|
| **Solve PDEs** | Input your PDE and get symbolic solutions |
| **Conditions** | Add boundary and initial conditions |
| **History** | All solutions are automatically saved |
| **Admin Panel** | Manage solutions via Django admin at `/admin/` |
| **API** | POST endpoint at `/api/solve/` for AJAX requests |

---

## 📁 Key Files

- `manage.py` - Django management script
- `pde_project/settings.py` - Configuration file
- `pde_solver/solver.py` - PDE solver engine (SymPy based)
- `pde_solver/models.py` - Database models
- `templates/` - HTML templates

---

## 🔧 Useful Commands

```bash
# Run migrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser

# Run development server
python manage.py runserver

# Run on specific port
python manage.py runserver 8001

# Access Django shell
python manage.py shell

# Create backup of database
python manage.py dumpdata > backup.json

# Restore from backup
python manage.py loaddata backup.json
```

---

## ⚠️ Troubleshooting

**Port 8000 already in use?**
```bash
python manage.py runserver 8001
```

**Database errors?**
```bash
python manage.py migrate
python manage.py makemigrations pde_solver
```

**Need to reset the database?**
```bash
rm db.sqlite3
python manage.py migrate
```

---

## 📚 Learning Resources

- [Django Documentation](https://docs.djangoproject.com/)
- [SymPy Documentation](https://docs.sympy.org/)
- [PDE Solver Theory](https://en.wikipedia.org/wiki/Partial_differential_equation)

---

## 🎓 Notation Quick Reference

| Notation | Meaning |
|----------|---------|
| `u` | Unknown function |
| `u_t` | ∂u/∂t (partial derivative with respect to t) |
| `u_x` | ∂u/∂x |
| `u_xx` | ∂²u/∂x² (second derivative) |
| `u_xy` | ∂²u/∂x∂y (mixed derivative) |
| `sin(pi*x)` | sin(πx) |
| `exp(t)` | e^t |

---

## 🐛 Reporting Issues

If you encounter any issues:
1. Check the Django logs in the terminal
2. Visit `/admin/` to view saved solutions
3. Try refreshing the page
4. Review the notation guide for correct PDE format

---

Happy solving! 🔬
