from django.shortcuts import render, get_object_or_404, redirect
from .forms import RegistroPropietario , EditarPropietario
from .models import propietario
from propiedad.models import Propiedad  # Ajusta según el nombre exacto de tu app
from django.contrib import messages
from login.utils import login_required_session

# Create your views here.
@login_required_session
def registrar_propietario(request):
    form = RegistroPropietario()
    propietarios = propietario.objects.all()
    message = ""

    if request.method == 'POST':
        form = RegistroPropietario(request.POST)
        if form.is_valid():
            form.save()
            message = 'Propietario registrado con éxito'
            return redirect("propiedad:agregar_propiedad")
        else:
            message = 'Corrige los errores en el formulario'

    return render(request, 'registrar_propietarios.html', {
        'form': form,
        'propietarios': propietarios,  # Corrección: La variable debe llamarse 'propietarios' para evitar confusión
        'message': message
    })


#------------------------------------------------------------------------------------------------------------------------------------------
@login_required_session
def listado_propietarios(request):
    propietarios_v = propietario.objects.all()
    return render(request, 'lista_propietarios.html', {'propietarios': propietarios_v})

#------------------------------------------------------------------------------------------------------------------------------------------
@login_required_session
def editar_propietario(request, id):
    propietario_v = get_object_or_404(propietario, id=id)

    if request.method == "POST":
        form = EditarPropietario(request.POST, instance=propietario_v)
        if form.is_valid():
            form.save()
            # Aquí agregamos 'propietarios:' antes de 'lista_propietarios'
            return redirect('propietarios:lista_propietarios')
    else:
        form = EditarPropietario(instance=propietario_v)

    return render(request, 'editar_propietario.html', {'form': form , 'propietario': propietario_v})

#------------------------------------------------------------------------------------------------------------------------------------------
@login_required_session
def eliminar_propietario(request, id):
    propietario_v = get_object_or_404(propietario, id=id)

    if request.method == 'POST':
        try:
            # Eliminar todas las propiedades asociadas primero
            Propiedad.objects.filter(id_propietario=propietario_v).delete()
            
            # Luego eliminar el propietario
            propietario_v.delete()
            
            messages.success(request, "Propietario y sus propiedades eliminados exitosamente")
            return redirect('propietarios:lista_propietarios')
        except Exception as e:
            messages.error(request, f"Error al eliminar: {str(e)}")
            return redirect('propietarios:eliminar_propietario', id=propietario_v.id)
    else:
        return render(request, 'eliminar_propietario.html', {'propietario': propietario_v})