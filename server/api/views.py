from django.http import JsonResponse
from cobranza.models import (
    ListaCobroDetalle2022, ListaCobroDetalle2023,
    ListaCobroDetalle2024, ListaCobroDetalle2025
)
from django.db.models import Sum, F, ExpressionWrapper, DecimalField, Count
from django.db.models.functions import ExtractMonth

def collection_stats(request):
    def get_yearly_stats(model):
        return (
            model.objects
            .annotate(
                month=ExtractMonth('fechaCobroBanco'),
                efficiency=ExpressionWrapper(
                    F('montoCobrado') * 100.0 / F('montoCobrar'),
                    output_field=DecimalField()
                )
            )
            .values('month')
            .annotate(
                total_cobrado=Sum('montoCobrado'),
                total_por_cobrar=Sum('montoCobrar'),
                promedio_eficiencia=Sum('efficiency') / Count('id')
            )
            .order_by('month')
        )

    stats = {
        '2022': list(get_yearly_stats(ListaCobroDetalle2022)),
        '2023': list(get_yearly_stats(ListaCobroDetalle2023)),
        '2024': list(get_yearly_stats(ListaCobroDetalle2024)),
        '2025': list(get_yearly_stats(ListaCobroDetalle2025))
    }

    return JsonResponse(stats)