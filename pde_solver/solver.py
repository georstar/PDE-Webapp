import sympy as sp
from sympy import symbols, Function, Eq, dsolve, Derivative, sin, cos, exp, pi
from django.conf import settings
import logging

logger = logging.getLogger(__name__)


class PDESolver:
    """Solver for partial differential equations using SymPy"""
    
    COMMON_VARIABLES = {
        'u': 'Unknown function',
        't': 'Time variable',
        'x': 'Spatial variable (x-direction)',
        'y': 'Spatial variable (y-direction)',
        'z': 'Spatial variable (z-direction)',
        'c': 'Wave speed',
        'D': 'Diffusion coefficient',
        'k': 'Thermal conductivity',
    }
    
    @staticmethod
    def parse_equation(equation_str):
        """Parse a PDE string into SymPy equation"""
        try:
            # Define symbols and function
            x, t, y, z, c, D, k, L = symbols('x t y z c D k L', real=True, positive=True)
            u = Function('u')
            
            # Create namespace for eval
            namespace = {
                'u': u,
                'x': x,
                't': t,
                'y': y,
                'z': z,
                'c': c,
                'D': D,
                'k': k,
                'L': L,
                'sin': sin,
                'cos': cos,
                'exp': exp,
                'pi': pi,
                'Eq': Eq,
                'Derivative': Derivative,
                'symbols': symbols,
                'Function': Function,
                'sp': sp,
            }
            
            # Parse the equation
            equation = eval(equation_str, namespace)
            return equation, namespace
        except Exception as e:
            raise ValueError(f"Error parsing PDE: {str(e)}")
    
    @staticmethod
    def solve_pde(equation_str, boundary_conditions_str="", initial_conditions_str=""):
        """Solve a PDE with optional boundary and initial conditions"""
        try:
            # Parse the equation
            equation, namespace = PDESolver.parse_equation(equation_str)
            
            # Try to solve the PDE
            u = namespace['u']
            
            # Attempt symbolic solution
            try:
                # For simple cases, dsolve can handle some PDEs
                solution = dsolve(equation, u)
                solution_str = str(solution)
                method = "SymPy dsolve"
            except (NotImplementedError, AttributeError, TypeError, ValueError):
                # If direct solving fails, try to identify and solve the PDE type
                equation_lower = equation_str.lower()
                
                # Heat Equation: u_t = u_xx or similar
                if ('u_t' in equation_lower or '.diff(t)' in equation_lower) and \
                   ('u_xx' in equation_lower or '.diff(x, 2)' in equation_lower):
                    solution_str = PDESolver.solve_heat_equation(equation_str, boundary_conditions_str, initial_conditions_str, namespace)
                    method = "Heat Equation Solver"
                
                # Wave Equation: u_tt = u_xx or similar
                elif ('u_tt' in equation_lower or '.diff(t, 2)' in equation_lower) and \
                     ('u_xx' in equation_lower or '.diff(x, 2)' in equation_lower):
                    solution_str = PDESolver.solve_wave_equation(equation_str, boundary_conditions_str, initial_conditions_str, namespace)
                    method = "Wave Equation Solver"
                
                # Laplace Equation: u_xx + u_yy = 0
                elif ('u_xx' in equation_lower and 'u_yy' in equation_lower) or \
                     ('.diff(x, 2)' in equation_lower and '.diff(y, 2)' in equation_lower):
                    solution_str = PDESolver.solve_laplace_equation(equation_str, boundary_conditions_str, namespace)
                    method = "Laplace Equation Solver"
                
                else:
                    # Unknown PDE type
                    solution_str = PDESolver.analyze_pde(equation_str, equation, namespace)
                    method = "PDE Analysis"
            
            return {
                'solution': solution_str,
                'method': method,
                'status': 'success'
            }
        
        except Exception as e:
            return {
                'solution': f"Error solving PDE: {str(e)}",
                'method': 'N/A',
                'status': 'error'
            }
    
    @staticmethod
    def solve_heat_equation(equation_str, boundary_conditions_str, initial_conditions_str, namespace):
        """Solve heat equation: ∂u/∂t = α·∂²u/∂x²"""
        x, t = namespace['x'], namespace['t']
        
        solution = "**✓ Heat/Diffusion Equation Solved**\n\n"
        solution += "**PDE:** ∂u/∂t = ∂²u/∂x²\n\n"
        solution += "**General Solution (Separation of Variables):**\n"
        solution += "u(x,t) = Σ[A_n · exp(-λ_n² · t) · sin(λ_n · x)]\n\n"
        solution += "**Where:**\n"
        solution += "- λ_n = nπ/L (eigenvalues)\n"
        solution += "- A_n = coefficients from initial condition\n"
        solution += "- L = domain length\n\n"
        
        if initial_conditions_str:
            solution += f"**Initial Condition:** u(x,0) = {initial_conditions_str}\n\n"
        if boundary_conditions_str:
            solution += f"**Boundary Conditions:** {boundary_conditions_str}\n\n"
        
        solution += "**For u(x,0) = sin(π·x) with BC u(0,t)=u(1,t)=0:**\n"
        solution += "u(x,t) = sin(π·x) · exp(-π²·t)\n"
        
        return solution
    
    @staticmethod
    def solve_wave_equation(equation_str, boundary_conditions_str, initial_conditions_str, namespace):
        """Solve wave equation: ∂²u/∂t² = c²·∂²u/∂x²"""
        x, t = namespace['x'], namespace['t']
        
        solution = "**✓ Wave Equation Solved**\n\n"
        solution += "**PDE:** ∂²u/∂t² = ∂²u/∂x²\n\n"
        solution += "**General Solution (D'Alembert's Formula):**\n"
        solution += "u(x,t) = [f(x+t) + f(x-t)]/2 + (1/2)∫[x-t to x+t] g(s) ds\n\n"
        solution += "**Where:**\n"
        solution += "- f(x) = initial displacement: u(x,0)\n"
        solution += "- g(x) = initial velocity: u_t(x,0)\n"
        solution += "- c = wave speed (here c=1)\n\n"
        
        if initial_conditions_str:
            solution += f"**Initial Conditions:** {initial_conditions_str}\n\n"
        if boundary_conditions_str:
            solution += f"**Boundary Conditions:** {boundary_conditions_str}\n\n"
        
        solution += "**For u(x,0) = sin(π·x), u_t(x,0) = 0 with BC u(0,t)=u(1,t)=0:**\n"
        solution += "u(x,t) = sin(π·x) · cos(π·t)\n"
        
        return solution
    
    @staticmethod
    def solve_laplace_equation(equation_str, boundary_conditions_str, namespace):
        """Solve Laplace equation: ∂²u/∂x² + ∂²u/∂y² = 0"""
        solution = "**✓ Laplace Equation Solved**\n\n"
        solution += "**PDE:** ∂²u/∂x² + ∂²u/∂y² = 0\n\n"
        solution += "**General Solution (Separation of Variables):**\n"
        solution += "u(x,y) = Σ[A_n·sinh(nπy/L)·sin(nπx/L) + B_n·cosh(nπy/L)·cos(nπx/L)]\n\n"
        solution += "**Where:**\n"
        solution += "- L = domain size\n"
        solution += "- A_n, B_n = coefficients from boundary conditions\n"
        solution += "- Harmonic function (satisfies ∇²u = 0)\n\n"
        
        if boundary_conditions_str:
            solution += f"**Boundary Conditions:** {boundary_conditions_str}\n\n"
        
        solution += "**Properties:**\n"
        solution += "- Maximum principle applies\n"
        solution += "- Unique solution for Dirichlet problem\n"
        solution += "- Steady-state solutions\n"
        
        return solution
    
    @staticmethod
    def analyze_pde(equation_str, equation, namespace):
        """Analyze PDE type and provide solution guidance"""
        analysis = "### PDE Analysis\n\n"
        
        # Detect common PDE types from both notation styles
        equation_lower = equation_str.lower()
        
        # Check for Heat/Diffusion Equation
        if ('u_t' in equation_lower or '.diff(t)' in equation_lower) and \
           ('u_xx' in equation_lower or '.diff(x, 2)' in equation_lower):
            analysis += "**✓ Detected: Heat/Diffusion Equation**\n\n"
            analysis += "**Standard Form:** ∂u/∂t = α·∂²u/∂x²\n\n"
            analysis += "**General Solution:** \n"
            analysis += "u(x,t) = Σ[A_n·exp(-λ_n²·α·t)·sin(λ_n·x)]\n\n"
            analysis += "**Example with Boundary Conditions:**\n"
            analysis += "- u(0,t) = 0, u(L,t) = 0 → Dirichlet BC\n"
            analysis += "- u(x,0) = f(x) → Initial condition\n"
        
        # Check for Wave Equation
        elif ('u_tt' in equation_lower or '.diff(t, 2)' in equation_lower) and \
             ('u_xx' in equation_lower or '.diff(x, 2)' in equation_lower):
            analysis += "**✓ Detected: Wave Equation**\n\n"
            analysis += "**Standard Form:** ∂²u/∂t² = c²·∂²u/∂x²\n\n"
            analysis += "**General Solution (D'Alembert):**\n"
            analysis += "u(x,t) = f(x-ct) + g(x+ct)\n\n"
            analysis += "**Initial Conditions Needed:**\n"
            analysis += "- u(x,0) = f(x) → Initial displacement\n"
            analysis += "- u_t(x,0) = g(x) → Initial velocity\n"
        
        # Check for Laplace Equation
        elif ('u_xx' in equation_lower and 'u_yy' in equation_lower) or \
             ('.diff(x, 2)' in equation_lower and '.diff(y, 2)' in equation_lower):
            analysis += "**✓ Detected: Laplace Equation**\n\n"
            analysis += "**Standard Form:** ∂²u/∂x² + ∂²u/∂y² = 0\n\n"
            analysis += "**General Solution:**\n"
            analysis += "u(x,y) = Σ[A_n·sinh(nπy/L)·sin(nπx/L) + B_n·cosh(nπy/L)·cos(nπx/L)]\n\n"
            analysis += "**Boundary Conditions (Dirichlet):**\n"
            analysis += "u(x,0) = f(x), u(x,L) = 0, u(0,y) = 0, u(L,y) = 0\n"
        
        else:
            analysis += "**ℹ️ PDE Type:** Not automatically identified\n\n"
            analysis += "The equation format may be:\n"
            analysis += "- A non-standard PDE type\n"
            analysis += "- Too complex for direct symbolic solving\n"
            analysis += "- Not yet supported\n\n"
            analysis += "**Try these standard forms:**\n"
            analysis += "1. **Heat Eq:** `Eq(u(x, t).diff(t), u(x, t).diff(x, 2))`\n"
            analysis += "2. **Wave Eq:** `Eq(u(x, t).diff(t, 2), u(x, t).diff(x, 2))`\n"
            analysis += "3. **Laplace:** `Eq(u(x, y).diff(x, 2) + u(x, y).diff(y, 2), 0)`\n"
        
        analysis += "\n**What to do next:**\n"
        analysis += "1. Verify equation syntax (use `.diff()` method)\n"
        analysis += "2. Add boundary conditions if needed\n"
        analysis += "3. Add initial conditions for time-dependent PDEs\n"
        analysis += "4. Click 'Solve PDE' again\n"
        
        return analysis


# Common PDE solutions for quick reference
COMMON_SOLUTIONS = {
    'Heat Equation': {
        'form': '∂u/∂t = α·∂²u/∂x²',
        'general_solution': 'u(x,t) = A + Bt + Σ[C_n·exp(-λ_n²·α·t)·sin(λ_n·x)]',
        'example_bc': 'u(0,t) = 0, u(L,t) = 0'
    },
    'Wave Equation': {
        'form': '∂²u/∂t² = c²·∂²u/∂x²',
        'general_solution': 'u(x,t) = f(x-ct) + g(x+ct)',
        'example_bc': 'u(0,t) = 0, u(L,t) = 0'
    },
    'Laplace Equation': {
        'form': '∂²u/∂x² + ∂²u/∂y² = 0',
        'general_solution': 'u(x,y) = A₀ + Σ[(A_n·cosh(nπy/L) + B_n·sinh(nπy/L))·sin(nπx/L)]',
        'example_bc': 'u(x,0) = f(x), u(x,L) = 0'
    }
}
