# Django PDE Solver Web Application

A sophisticated web application for solving partial differential equations (PDEs) using Django and SymPy.

## Features

- ✨ **Solve PDEs Symbolically**: Input your PDE and get symbolic solutions
- 📝 **Support for Conditions**: Add boundary and initial conditions
- 💾 **Save Solutions**: Store and access your solutions anytime
- 🔬 **Multiple PDE Types**: Support for Heat, Wave, and Laplace equations
- 📊 **Solution History**: Browse all previously solved PDEs
- 🎨 **Beautiful UI**: Modern Bootstrap 5 interface

## Supported PDE Types

- **Heat Equation**: ∂u/∂t = α·∂²u/∂x²
- **Wave Equation**: ∂²u/∂t² = c²·∂²u/∂x²
- **Laplace Equation**: ∂²u/∂x² + ∂²u/∂y² = 0

## Installation

### Prerequisites
- Python 3.8+
- pip or conda

### Step 1: Clone the repository
```bash
cd /home/georstar/myRepos/PDE-Webapp
```

### Step 2: Create a virtual environment
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### Step 3: Install dependencies
```bash
pip install -r requirements.txt
```

### Step 4: Run migrations
```bash
python manage.py migrate
```

### Step 5: Create a superuser (optional, for admin panel)
```bash
python manage.py createsuperuser
```

### Step 6: Run the development server
```bash
python manage.py runserver
```

Visit `http://localhost:8000` in your browser to access the application.

## Usage

### Solving a PDE

1. Go to the **Solve PDE** page
2. Enter your PDE using standard notation:
   - `u_t` for ∂u/∂t
   - `u_x` for ∂u/∂x
   - `u_xx` for ∂²u/∂x²
   - `u_xy` for ∂²u/∂x∂y

3. Optionally add:
   - **Boundary Conditions**: e.g., `u(0,t) = 0, u(L,t) = 0`
   - **Initial Conditions**: e.g., `u(x,0) = sin(x), u_t(x,0) = 0`

4. Click **Solve PDE** to get the solution

### Examples

#### Heat Equation
```
Equation: u_t = u_xx
Boundary Conditions: u(0,t) = 0, u(1,t) = 0
Initial Conditions: u(x,0) = sin(pi*x)
```

#### Wave Equation
```
Equation: u_tt = u_xx
Boundary Conditions: u(0,t) = 0, u(1,t) = 0
Initial Conditions: u(x,0) = sin(pi*x), u_t(x,0) = 0
```

## Project Structure

```
PDE-Webapp/
├── manage.py                 # Django management script
├── requirements.txt          # Python dependencies
├── pde_project/             # Main project configuration
│   ├── settings.py          # Django settings
│   ├── urls.py              # URL routing
│   ├── wsgi.py              # WSGI config
│   └── asgi.py              # ASGI config
├── pde_solver/              # PDE solver app
│   ├── models.py            # Database models
│   ├── views.py             # View logic
│   ├── forms.py             # Form definitions
│   ├── urls.py              # App URL routing
│   ├── solver.py            # PDE solver engine
│   └── admin.py             # Django admin config
├── templates/               # HTML templates
│   ├── base.html            # Base template
│   └── pde_solver/
│       ├── home.html        # Home page
│       ├── solver.html      # PDE solver form
│       ├── solution_list.html   # Solutions list
│       └── solution_detail.html # Solution details
└── db.sqlite3               # SQLite database
```

## Technologies Used

- **Backend**: Django 4.2
- **Mathematics**: SymPy 1.12
- **Frontend**: Bootstrap 5
- **Database**: SQLite (development) / PostgreSQL (production)
- **Server**: Gunicorn

## API Endpoints

### REST API
- `POST /api/solve/` - Solve a PDE (AJAX endpoint)

### Web Views
- `GET /` - Home page
- `GET /solve/` - PDE solver form
- `POST /solve/` - Submit and solve PDE
- `GET /solutions/` - List all solutions
- `GET /solution/<id>/` - View solution details
- `GET /admin/` - Django admin panel (requires authentication)

## Configuration

### Settings File
Edit `pde_project/settings.py` to:
- Change `DEBUG = False` for production
- Update `ALLOWED_HOSTS`
- Configure database settings
- Set `SECRET_KEY` securely in production

### Environment Variables
Create a `.env` file:
```bash
DEBUG=True
SECRET_KEY=your-secret-key-here
ALLOWED_HOSTS=localhost,127.0.0.1
DATABASE_URL=sqlite:///db.sqlite3
```

## Performance Considerations

- **PDE Solver Timeout**: Set to 30 seconds (configurable in settings)
- **Database**: SQLite for development, PostgreSQL for production
- **Caching**: Can be added for frequently solved PDEs

## Limitations

- Complex nonlinear PDEs may not have closed-form solutions
- Numerical methods are not currently implemented
- Some PDEs may timeout if they're computationally intensive

## Future Enhancements

- [ ] Numerical solution methods (Finite Difference, Finite Element)
- [ ] Graphical visualization of solutions
- [ ] Support for systems of PDEs
- [ ] Import/Export solutions (PDF, CSV)
- [ ] User accounts and solution sharing
- [ ] LaTeX rendering for equations
- [ ] Solution validation and error bounds
- [ ] Performance optimization with caching

## Troubleshooting

### PDE not solving
- Check the notation: use `u_t`, `u_x`, `u_xx` etc.
- Ensure the PDE is properly formatted
- Some complex PDEs may not have closed-form solutions

### Port already in use
```bash
python manage.py runserver 8001  # Use a different port
```

### Database errors
```bash
python manage.py migrate
python manage.py makemigrations
```

## Contributing

Contributions are welcome! Please:
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## License

This project is open source and available under the MIT License.

## Support

For issues, questions, or suggestions, please create an issue on the repository.

## Author

Created as a demonstration of Django, SymPy, and mathematical problem-solving.