from django.db.models import Count, Q
from django.db.models.functions import TruncMonth
from .models import Post


def obter_metricas_dashboard(pagina, qs_posts=None):
    # Garante o isolamento de dados por página antes de qualquer agregação
    base = qs_posts if qs_posts is not None else Post.objects.filter(pagina=pagina)

    # Indicadores totais (KPIs) calculados em consulta única
    kpis = base.aggregate(
        total_posts=Count('id'),
        publicados=Count('id', filter=Q(status='publicado')),
        rascunhos=Count('id', filter=Q(status='rascunho')),
        autores_ativos=Count('autor', distinct=True),
    )

    # Ranking dos 5 autores com maior volume de publicações
    ranking_autores = list(
        base.values('autor__username', 'autor__first_name')
        .annotate(total=Count('id'))
        .order_by('-total')[:5]
    )

    # Série temporal agrupada por mês e ordenada cronologicamente
    por_mes_qs = (
        base.annotate(mes=TruncMonth('criado_em'))
        .values('mes')
        .annotate(total=Count('id'))
        .order_by('mes')
    )
    por_mes = [
        {'mes': item['mes'].strftime('%m/%Y'), 'total': item['total']}
        for item in por_mes_qs
        if item['mes'] is not None
    ]

    # Distribuição quantitativa por status
    distribuicao_status = list(
        base.values('status')
        .annotate(total=Count('id'))
        .order_by('-total')
    )

    return {
        'kpis': kpis,
        'ranking_autores': ranking_autores,
        'por_mes': por_mes,
        'distribuicao_status': distribuicao_status,
    }