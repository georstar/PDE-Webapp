from django.contrib import admin
from .models import PDESolution


@admin.register(PDESolution)
class PDESolutionAdmin(admin.ModelAdmin):
    list_display = ('equation_preview', 'method_used', 'created_at')
    list_filter = ('method_used', 'created_at')
    search_fields = ('equation', 'solution')
    readonly_fields = ('created_at', 'updated_at')
    fieldsets = (
        ('Equation Details', {
            'fields': ('equation', 'boundary_conditions', 'initial_conditions')
        }),
        ('Solution', {
            'fields': ('solution', 'method_used')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def equation_preview(self, obj):
        return obj.equation[:50] + '...' if len(obj.equation) > 50 else obj.equation
    equation_preview.short_description = 'Equation'
