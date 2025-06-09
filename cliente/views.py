from django.shortcuts import get_object_or_404, redirect, render
from django.http import HttpResponse
from .forms import ClienteForm, EditarCliente
from .models import clientes
from login.utils import login_required_session

# Create your views here.

@login_required_session
def Cliente_registrar(request):
    message = ''
    form = ClienteForm()
    Cliente_v = clientes.objects.all()
    
    if request.method == 'POST':
        form = ClienteForm(request.POST)
        if form.is_valid():
            form.save()
            message = 'Cliente registrado'

    
    return render(request, 'add_cliente.html', {'form': form, 'clientes': Cliente_v, 'message': message})

@login_required_session
def listado_cliente(request):
    Cliente_v = clientes.objects.all()
    return render(request, 'mostrar_cliente.html', {'clientes': Cliente_v})

@login_required_session
def editar_cliente(request, id):
    Cliente_v = get_object_or_404(clientes, id=id)

    if request.method == "POST":
        form = EditarCliente(request.POST, instance=Cliente_v)
        if form.is_valid():
            form.save()
            # Aquí agregamos 'cliente:' antes de 'mostrar_cliente'
            return redirect('cliente:listado_cliente')
    else:
        form = EditarCliente(instance=Cliente_v)

    return render(request, 'edit_cliente.html', {'form': form , 'clientes': Cliente_v})

@login_required_session
def eliminar_cliente(request, id):
    Cliente_v = get_object_or_404(clientes, id=id)
    
    if request.method == 'POST':
        Cliente_v.delete()
        return redirect('cliente:listado_cliente')
    
    return render(request, 'eliminar_cliente.html', {'clientes': Cliente_v})


