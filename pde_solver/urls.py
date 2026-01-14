from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('solve/', views.PDESolverView.as_view(), name='solve_pde'),
    path('solutions/', views.SolutionListView.as_view(), name='solution_list'),
    path('solution/<int:pk>/', views.SolutionDetailView.as_view(), name='solution_detail'),
    path('api/solve/', views.solve_pde_api, name='solve_pde_api'),
]
