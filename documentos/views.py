from django.shortcuts import render, redirect,get_object_or_404
from django.contrib import messages
from .forms import DocumentosForm
from .models import Documento, Propiedad

def registrar_docu_venta(request, propiedad_id):
    """Registra un documento y lo asocia automáticamente a la propiedad seleccionada."""
    propiedad = get_object_or_404(Propiedad, id=propiedad_id)
    message = ''

    if request.method == 'POST':
        form = DocumentosForm(request.POST, request.FILES)
        if form.is_valid():
            documento = form.save(commit=False)
            documento.id_propiedad = propiedad  # Asociamos la propiedad seleccionada
            documento.save()
            messages.success(request, 'Documento registrado exitosamente.')
            return redirect('documentos:mostrar_documentos', propiedad_id=propiedad_id)
        else:
            messages.error(request, 'Hubo un error al registrar el documento.')
    else:
        form = DocumentosForm()

    return render(request, 'docu_venta.html', {
        'form': form,
        'message': message,
        'propiedad': propiedad  # Pasamos la propiedad al template
    })


def documento_mostrar(request, propiedad_id):
    """Muestra solo los documentos de la propiedad seleccionada."""
    propiedad = get_object_or_404(Propiedad, id=propiedad_id)
    documentos = Documento.objects.filter(id_propiedad=propiedad)

    return render(request, 'mostrar_documentos.html', {
        'documentos': documentos,
        'propiedad': propiedad
    })
