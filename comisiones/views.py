from django.shortcuts import render, get_object_or_404, redirect
from comisiones.models import Comision, Egresos
from comisiones.forms import ComisionForm, EgresosForm
from documentos.models import Documento
from django.contrib import messages
from login.models import corredor 

def listado_vales_vista(request):
    """Vista para listar documentos de tipo 'VALE VISTA' y mostrar si ya tienen una comisión"""
    documentos = Documento.objects.filter(tipo_documento="VALE VISTA")
    
    # Crear un diccionario con documentos que ya tienen comisión
    comisiones_existentes = {comision.id_documento.id: comision for comision in Comision.objects.all()}

    return render(request, "listado_vales_vista.html", {
        "documentos": documentos,
        "comisiones_existentes": comisiones_existentes
    })


def crear_comision(request, documento_id):
    """Vista para registrar una comisión y asignarle el corredor autenticado"""
    documento = get_object_or_404(Documento, id=documento_id)

    # Verificar si ya existe una comisión para este documento
    if Comision.objects.filter(id_documento=documento).exists():
        messages.warning(request, "Ya existe una comisión para este Vale Vista.")
        return redirect("comisiones:listado_vales_vista")  

    if request.method == "POST":
        form = ComisionForm(request.POST)
        if form.is_valid():
            comision = form.save(commit=False)
            comision.id_propiedad = documento.id_propiedad
            comision.id_documento = documento

            # Obtener el corredor desde la sesión (o desde request.user si usas autenticación Django)
            user_id = request.session.get("user_id")  # Si guardas el ID del corredor en sesión
            
            try:
                comision.id_corredor = corredor.objects.get(id=user_id)
            except corredor.DoesNotExist:
                messages.error(request, "No se encontró el corredor autenticado.")
                return redirect("comisiones:listado_vales_vista")

            # Guardar la comisión con el corredor asignado
            comision.save()
            
            messages.success(request, "Comisión creada exitosamente.")
            return redirect("comisiones:listado_vales_vista")  
    else:
        form = ComisionForm()

    return render(request, "crear_comision.html", {"form": form, "documento": documento})

def crear_egreso(request):
    form = EgresosForm(request.POST)
    if form.is_valid():
        egreso = form.save(commit=False)
        user_id = request.session.get("user_id")
        try:
            egreso.id_corredor = corredor.objects.get(id=user_id)
        except corredor.DoesNotExist:
            messages.error(request, "No se encontró el corredor autenticado.")
            return redirect("comisiones:listado_vales_vista")
        egreso.save()
        messages.success(request, 'Egreso creado exitosamente.')
        return redirect("login:dashboard")
    else:
        form = EgresosForm()
    return render(request, "crear_egreso.html", {"form": form})


def editar_comision(request, comision_id):
    """Vista para editar una comisión existente"""
    comision = get_object_or_404(Comision, id=comision_id)

    if request.method == "POST":
        form = ComisionForm(request.POST, instance=comision)
        if form.is_valid():
            form.save()
            messages.success(request, "Comisión actualizada exitosamente.")
            return redirect("comisiones:listado_vales_vista")  
    else:
        form = ComisionForm(instance=comision)

    return render(request, "editar_comision.html", {"form": form, "comision": comision})

def eliminar_comision(request, comision_id):
    """Vista para eliminar una comisión"""
    comision = get_object_or_404(Comision, id=comision_id)

    if request.method == "POST":
        comision.delete()
        messages.success(request, "Comisión eliminada correctamente.")
        return redirect("comisiones:listado_vales_vista")

    return render(request, "eliminar_comision.html", {"comision": comision})

def listado_comisiones(request):
    """Vista para mostrar la lista de comisiones registradas"""
    comisiones = Comision.objects.select_related("id_propiedad", "id_documento", "id_corredor").all()
    
    return render(request, "listado_comisiones.html", {"comisiones": comisiones})


    
