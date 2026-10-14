from django.shortcuts import render, redirect, get_object_or_404
from django.core.paginator import Paginator
from .models import Reporte
from .forms import ReporteForm


def lista_reportes(request):
    qs = Reporte.objects.select_related(
        'tipo', 'area', 'responsable'
    ).order_by('-fecha_creacion')

    paginator = Paginator(qs, 10)  # 10 reportes por página
    reportes = paginator.get_page(request.GET.get('page'))

    return render(
        request,
        'reportes/lista.html',
        {'reportes': reportes}
    )


def crear_reporte(request):
    if request.method == 'POST':  # el usuario envió el formulario
        form = ReporteForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect('reportes:lista')

    else:
        # GET: mostrar el formulario vacío
        form = ReporteForm()

    return render(
        request,
        'reportes/formulario.html',
        {
            'form': form,
            'titulo': 'Nuevo reporte'
        }
    )


def editar_reporte(request, pk):
    reporte = get_object_or_404(Reporte, pk=pk)

    if request.method == 'POST':
        form = ReporteForm(request.POST, instance=reporte)

        if form.is_valid():
            form.save()
            return redirect('reportes:lista')

    else:
        form = ReporteForm(instance=reporte)

    return render(
        request,
        'reportes/formulario.html',
        {
            'form': form,
            'titulo': f'Editar reporte {reporte.codigo}'
        }
    )


def eliminar_reporte(request, pk):
    reporte = get_object_or_404(Reporte, pk=pk)

    if request.method == 'POST':
        # llega solo si el usuario pulsó "Aceptar"
        reporte.delete()

    return redirect('reportes:lista')

# Create your views here.
