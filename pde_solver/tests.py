"""
Tests for the PDE Solver application.
To run: python manage.py test
"""

from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from pde_solver.models import PDESolution
from pde_solver.solver import PDESolver
from pde_solver.forms import PDEInputForm


class PDESolverTestCase(TestCase):
    """Test PDE solver engine"""
    
    def test_heat_equation_parsing(self):
        """Test parsing of heat equation"""
        equation_str = "Eq(Derivative(u(x, t), t), Derivative(u(x, t), x, 2))"
        equation, namespace = PDESolver.parse_equation(equation_str)
        self.assertIsNotNone(equation)
    
    def test_wave_equation_parsing(self):
        """Test parsing of wave equation"""
        equation_str = "Eq(Derivative(u(x, t), t, 2), Derivative(u(x, t), x, 2))"
        equation, namespace = PDESolver.parse_equation(equation_str)
        self.assertIsNotNone(equation)
    
    def test_invalid_equation(self):
        """Test handling of invalid equations"""
        with self.assertRaises(ValueError):
            PDESolver.parse_equation("invalid equation syntax")
    
    def test_solve_pde_returns_dict(self):
        """Test that solve_pde returns correct format"""
        result = PDESolver.solve_pde(
            "Eq(Derivative(u(x, t), t), Derivative(u(x, t), x, 2))"
        )
        self.assertIn('solution', result)
        self.assertIn('method', result)
        self.assertIn('status', result)


class PDEModelTestCase(TestCase):
    """Test PDESolution model"""
    
    def setUp(self):
        self.solution = PDESolution.objects.create(
            equation="u_t = u_xx",
            boundary_conditions="u(0,t) = 0, u(L,t) = 0",
            initial_conditions="u(x,0) = sin(pi*x)",
            solution="u(x,t) = sin(pi*x)*exp(-pi^2*t)",
            method_used="Analytical"
        )
    
    def test_solution_creation(self):
        """Test creating a solution"""
        self.assertEqual(self.solution.equation, "u_t = u_xx")
        self.assertIsNotNone(self.solution.created_at)
    
    def test_solution_string_representation(self):
        """Test model string representation"""
        self.assertTrue(str(self.solution).startswith("PDE:"))
    
    def test_solution_ordering(self):
        """Test solutions are ordered by created_at descending"""
        PDESolution.objects.create(
            equation="u_tt = u_xx",
            solution="solution",
            method_used="Analytical"
        )
        solutions = PDESolution.objects.all()
        self.assertEqual(solutions[0].equation, "u_tt = u_xx")


class PDEFormTestCase(TestCase):
    """Test PDEInputForm"""
    
    def test_valid_form(self):
        """Test form with valid data"""
        form_data = {
            'equation': 'u_t = u_xx',
            'boundary_conditions': 'u(0,t) = 0',
            'initial_conditions': 'u(x,0) = sin(x)'
        }
        form = PDEInputForm(data=form_data)
        self.assertTrue(form.is_valid())
    
    def test_required_equation(self):
        """Test that equation is required"""
        form_data = {
            'equation': '',
            'boundary_conditions': 'u(0,t) = 0',
        }
        form = PDEInputForm(data=form_data)
        self.assertFalse(form.is_valid())
    
    def test_optional_conditions(self):
        """Test that conditions are optional"""
        form_data = {
            'equation': 'u_t = u_xx',
            'boundary_conditions': '',
            'initial_conditions': ''
        }
        form = PDEInputForm(data=form_data)
        self.assertTrue(form.is_valid())


class ViewsTestCase(TestCase):
    """Test views and URLs"""
    
    def setUp(self):
        self.client = Client()
        self.solution = PDESolution.objects.create(
            equation="u_t = u_xx",
            solution="solution",
            method_used="Analytical"
        )
    
    def test_home_page(self):
        """Test home page loads"""
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'pde_solver/home.html')
    
    def test_solver_page(self):
        """Test solver page loads"""
        response = self.client.get(reverse('solve_pde'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'pde_solver/solver.html')
    
    def test_solution_list_page(self):
        """Test solution list page"""
        response = self.client.get(reverse('solution_list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "u_t = u_xx")
    
    def test_solution_detail_page(self):
        """Test solution detail page"""
        response = self.client.get(
            reverse('solution_detail', args=[self.solution.pk])
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "u_t = u_xx")
    
    def test_post_solve_pde(self):
        """Test submitting PDE form"""
        form_data = {
            'equation': 'u_t = u_xx',
            'boundary_conditions': '',
            'initial_conditions': ''
        }
        response = self.client.post(reverse('solve_pde'), form_data)
        self.assertEqual(response.status_code, 302)  # Redirect after success
        self.assertEqual(PDESolution.objects.filter(equation='u_t = u_xx').count(), 2)
    
    def test_api_solve_pde_post(self):
        """Test API endpoint for solving PDE"""
        response = self.client.post(
            reverse('solve_pde_api'),
            {
                'equation': 'u_t = u_xx',
                'boundary_conditions': '',
                'initial_conditions': ''
            }
        )
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn('solution', data)
        self.assertIn('method', data)
    
    def test_api_requires_equation(self):
        """Test API returns error without equation"""
        response = self.client.post(
            reverse('solve_pde_api'),
            {'equation': ''}
        )
        self.assertEqual(response.status_code, 400)
    
    def test_api_only_post(self):
        """Test API only accepts POST"""
        response = self.client.get(reverse('solve_pde_api'))
        self.assertEqual(response.status_code, 405)


# Run tests with: python manage.py test
# Run specific test: python manage.py test pde_solver.tests.PDESolverTestCase
# Run with coverage: coverage run --source='pde_solver' manage.py test
#                   coverage report
#                   coverage html
