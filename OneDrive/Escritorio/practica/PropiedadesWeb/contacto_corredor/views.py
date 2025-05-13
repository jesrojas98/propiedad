from django.shortcuts import render, redirect , get_object_or_404
from django.contrib import messages
from .models import contacto_propietario
from login.models import corredor
from .forms import contactoForm
from login.utils import login_required_session
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from .models import contacto_interesado
from operaciones.models import Publicacion
from .forms import ContactoInteresadoForm

#=======================================================================================================
def contactar_corredor(request):
    message = ''
    contactos = contacto_propietario.objects.all()
    corredores = corredor.objects.all()
    form = contactoForm()  

    if request.method == 'POST':
        form = contactoForm(request.POST)
        if form.is_valid():
            contacto = form.save()
            message = 'Mensaje enviado exitosamente.'
            form = contactoForm(instance=contacto) 
        else:
            print("Error en el formulario:", form.errors)  
            message = 'Revise los campos del formulario.'

    return render(request, 'contactar_corredor.html', {
        'form': form, 
        'contactos': contactos, 
        'corredores': corredores, 
        'message': message
    })
#=======================================================================================================
@login_required_session
def contactos_a_corredor(request):
    user_id = request.session.get("user_id")

    if not user_id:
        messages.error(request, "No tienes permisos para ver estos contactos.")
        return redirect("login:login")  

    # Filtrar solo los contactos de propietarios asignados al corredor autenticado
    contactos_propietarios_v = contacto_propietario.objects.filter(corredor_id=user_id)

    # Filtrar solo los contactos de interesados asignados al corredor autenticado
    contactos_interesados_v = contacto_interesado.objects.filter(corredor_id=user_id)

    # Si no tiene contactos, mandar mensaje de advertencia
    if not contactos_propietarios_v.exists() and not contactos_interesados_v.exists():
        messages.warning(request, "No tienes contactos asignados actualmente.")

    return render(
        request,
        'contactos_a_corredor.html',
        {
            'contactos_propietarios': contactos_propietarios_v,
            'contactos_interesados': contactos_interesados_v
        }
    )

#=======================================================================================================
def contacto_interesado_view(request, publicacion_id):
    publicacion = get_object_or_404(Publicacion, id=publicacion_id)

    if request.method == "POST":
        form = ContactoInteresadoForm(request.POST)
        if form.is_valid():
            contacto = form.save(commit=False)
            contacto.id_publicacion = publicacion  # Asigna la publicación seleccionada
            contacto.corredor = publicacion.id_corredor_encargado  # Asigna el corredor de la publicación
            contacto.save()
            messages.success(request, "¡Tu mensaje ha sido enviado! El corredor te contactará pronto.")
            return redirect("operaciones:inicio")  # Redirige a la lista de publicaciones
        else:
            messages.error(request, "Hubo un error en el formulario, revisa los campos.")

    else:
        form = ContactoInteresadoForm()

    return render(request, "contacto_interesado.html", {"form": form, "publicacion": publicacion})

#=======================================================================================================
@login_required_session
def detalle_contacto(request, id, tipo_contacto):
    user_id = request.session.get("user_id")

    if tipo_contacto == "propietario":
        contacto = contacto_propietario.objects.filter(id=id, corredor_id=user_id).first()
    elif tipo_contacto == "interesado":
        contacto = contacto_interesado.objects.filter(id=id, corredor_id=user_id).first()
    else:
        messages.error(request, "Tipo de contacto no válido.")
        return redirect("contacto_corredor:contactos_a_corredor")

    if not contacto:
        messages.error(request, "No tienes permisos para ver este contacto o no existe.")
        return redirect("contacto_corredor:contactos_a_corredor")

    # Si es un contacto de interesado, traer la publicación
    publicacion = contacto.id_publicacion if tipo_contacto == "interesado" else None

    return render(request, "detalle_contacto.html", {
        "contacto": contacto,
        "tipo_contacto": tipo_contacto,
        "publicacion": publicacion
    })
