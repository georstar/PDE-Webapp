from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, DetailView, CreateView
from django.urls import reverse_lazy
from django.contrib import messages
from django.http import JsonResponse
from .models import PDESolution
from .forms import PDEInputForm
from .solver import PDESolver, COMMON_SOLUTIONS
import logging

logger = logging.getLogger(__name__)


class PDESolverView(CreateView):
    """View for solving PDEs"""
    model = PDESolution
    form_class = PDEInputForm
    template_name = 'pde_solver/solver.html'
    success_url = reverse_lazy('solution_list')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['common_solutions'] = COMMON_SOLUTIONS
        context['recent_solutions'] = PDESolution.objects.all()[:5]
        return context
    
    def form_valid(self, form):
        """Solve the PDE when form is submitted"""
        equation = form.cleaned_data['equation']
        boundary_conditions = form.cleaned_data.get('boundary_conditions', '')
        initial_conditions = form.cleaned_data.get('initial_conditions', '')
        
        # Solve the PDE
        result = PDESolver.solve_pde(
            equation,
            boundary_conditions,
            initial_conditions
        )
        
        # Save the solution
        form.instance.solution = result['solution']
        form.instance.method_used = result['method']
        
        messages.success(self.request, 'PDE solved successfully!')
        return super().form_valid(form)


class SolutionListView(ListView):
    """View to list all saved PDE solutions"""
    model = PDESolution
    template_name = 'pde_solver/solution_list.html'
    context_object_name = 'solutions'
    paginate_by = 10


class SolutionDetailView(DetailView):
    """View to display detailed solution"""
    model = PDESolution
    template_name = 'pde_solver/solution_detail.html'
    context_object_name = 'solution'


def solve_pde_api(request):
    """API endpoint for solving PDEs (AJAX)"""
    if request.method == 'POST':
        equation = request.POST.get('equation', '')
        boundary_conditions = request.POST.get('boundary_conditions', '')
        initial_conditions = request.POST.get('initial_conditions', '')
        
        if not equation:
            return JsonResponse({'status': 'error', 'message': 'Equation is required'}, status=400)
        
        try:
            result = PDESolver.solve_pde(
                equation,
                boundary_conditions,
                initial_conditions
            )
            return JsonResponse(result)
        except Exception as e:
            logger.error(f"Error solving PDE: {str(e)}")
            return JsonResponse({
                'status': 'error',
                'message': f'Error solving PDE: {str(e)}'
            }, status=500)
    
    return JsonResponse({'status': 'error', 'message': 'Only POST requests allowed'}, status=405)


def home(request):
    """Home page view"""
    context = {
        'total_solutions': PDESolution.objects.count(),
        'recent_solutions': PDESolution.objects.all()[:3],
        'common_solutions': COMMON_SOLUTIONS,
    }
    return render(request, 'pde_solver/home.html', context)
