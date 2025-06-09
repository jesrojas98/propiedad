from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Propiedad, ImagenPropiedad
from login.models import corredor
from .forms import PropiedadForm
from propietarios.models import propietario
from login.utils import login_required_session

#======================================================================================================
@login_required_session
def propiedad_mostrar(request):
    propiedades = Propiedad.objects.all()
    return render(request, 'mostrar_propiedad.html', {'propiedades': propiedades})
#======================================================================================================
@login_required_session
def propiedad_registrar(request):
    message = ''
    propietarios = propietario.objects.all()  # Obtener propietarios para el select

    if request.method == 'POST':
        form = PropiedadForm(request.POST, request.FILES)
        if form.is_valid():
            propiedad = form.save()
            for imagen in request.FILES.getlist('imagenes'):
                ImagenPropiedad.objects.create(propiedad=propiedad, imagen=imagen)
            return redirect('propiedad:mostrar_propiedad')
        else:
            print("Errores del formulario:", form.errors.as_json())
            message = 'Hubo un error al registrar la propiedad.'

    else:
        form = PropiedadForm()

    return render(request, 'agregar_propiedad.html', {
        'form': form,
        'message': message,
        'propietarios': propietarios  # Pasamos propietarios al template
    })

#======================================================================================================
@login_required_session
def propiedad_registrar_casa(request):
    message = ''
    propietarios = propietario.objects.all()  # Obtener propietarios para el select
    user_id = request.session.get("user_id")  # Obtener el ID del corredor autenticado

    if request.method == 'POST':
        form = PropiedadForm(request.POST, request.FILES)
        if form.is_valid():
            propiedad = form.save(commit=False)  # Guarda pero sin ManyToMany aún
            
            # 📌 Asignamos el corredor autenticado a la propiedad
            try:
                propiedad.id_corredor_encargado = corredor.objects.get(id=user_id)
            except corredor.DoesNotExist:
                messages.error(request, "No se encontró el corredor autenticado.")
                return redirect('login:login')
            
            # 📌 Asignamos automáticamente el tipo de propiedad como "casa"
            propiedad.tipo_propiedad = "Casa"

            propiedad.save()  # Guarda la propiedad en la BD
            form.save_m2m()  # Ahora sí guarda los ManyToManyField (otros)

            # 📌 Guardar imágenes de la propiedad
            for imagen in request.FILES.getlist('imagenes'):
                ImagenPropiedad.objects.create(propiedad=propiedad, imagen=imagen)

            messages.success(request, "Propiedad registrada correctamente.")
            return redirect('propiedad:mostrar_propiedad')
        else:
            print("Errores del formulario:", form.errors.as_json())
            message = 'Hubo un error al registrar la propiedad.'

    else:
        form = PropiedadForm()

    return render(request, 'casa.html', {
        'form': form,
        'message': message,
        'propietarios': propietarios  # Pasamos propietarios al template
    })

#======================================================================================================
@login_required_session
def propiedad_registrar_departamento(request):
    message = ''
    propietarios = propietario.objects.all()  # Obtener propietarios para el select
    user_id = request.session.get("user_id")  # Obtener el ID del corredor autenticado

    if request.method == 'POST':
        form = PropiedadForm(request.POST, request.FILES)
        if form.is_valid():
            propiedad = form.save(commit=False)  # Guarda pero sin ManyToMany aún
            
            # 📌 Asignamos el corredor autenticado a la propiedad
            try:
                propiedad.id_corredor_encargado = corredor.objects.get(id=user_id)
            except corredor.DoesNotExist:
                messages.error(request, "No se encontró el corredor autenticado.")
                return redirect('login:login')
            
            # 📌 Asignamos automáticamente el tipo de propiedad como "casa"
            propiedad.tipo_propiedad = "Departamento"

            propiedad.save()  # Guarda la propiedad en la BD
            form.save_m2m()  # Ahora sí guarda los ManyToManyField (otros)

            # 📌 Guardar imágenes de la propiedad
            for imagen in request.FILES.getlist('imagenes'):
                ImagenPropiedad.objects.create(propiedad=propiedad, imagen=imagen)

            messages.success(request, "Departamento registrado correctamente.")
            return redirect('propiedad:mostrar_propiedad')
        else:
            print("Errores del formulario:", form.errors.as_json())
            message = 'Hubo un error al registrar el departamento.'

    else:
        form = PropiedadForm()

    return render(request, 'departamento.html', {
        'form': form,
        'message': message,
        'propietarios': propietarios  # Pasamos propietarios al template
    })

#======================================================================================================
@login_required_session
def propiedad_registrar_oficina(request):
    message = ''
    propietarios = propietario.objects.all()  # Obtener propietarios para el select
    user_id = request.session.get("user_id")  # Obtener el ID del corredor autenticado

    if request.method == 'POST':
        form = PropiedadForm(request.POST, request.FILES)
        if form.is_valid():
            propiedad = form.save(commit=False)  # Guarda pero sin ManyToMany aún

            # 📌 Asignamos el corredor autenticado a la propiedad
            try:
                propiedad.id_corredor_encargado = corredor.objects.get(id=user_id)
            except corredor.DoesNotExist:
                messages.error(request, "No se encontró el corredor autenticado.")
                return redirect('login:login')

            # 📌 Asignamos automáticamente el tipo de propiedad como "casa"
            propiedad.tipo_propiedad = "Oficina"

            propiedad.save()  # Guarda la propiedad en la BD
            form.save_m2m()  # Ahora sí guarda los ManyToManyField (otros)

            # 📌 Guardar imágenes de la propiedad
            for imagen in request.FILES.getlist('imagenes'):
                ImagenPropiedad.objects.create(propiedad=propiedad, imagen=imagen)

            messages.success(request, "Oficina registrada correctamente.")
            return redirect('propiedad:mostrar_propiedad')
        else:
            print("Errores del formulario:", form.errors.as_json())
            message = 'Hubo un error al registrar la oficina.'

    else:
        form = PropiedadForm()

    return render(request, 'oficina.html', {
        'form': form,
        'message': message,
        'propietarios': propietarios  # Pasamos propietarios al template
    })

#======================================================================================================
@login_required_session
def propiedad_registrar_local(request):
    message = ''
    propietarios = propietario.objects.all()  # Obtener propietarios para el select
    user_id = request.session.get("user_id")  # Obtener el ID del corredor autenticado

    if request.method == 'POST':
        form = PropiedadForm(request.POST, request.FILES)
        if form.is_valid():
            propiedad = form.save(commit=False)  # Guarda pero sin ManyToMany aún

            # 📌 Asignamos el corredor autenticado a la propiedad
            try:
                propiedad.id_corredor_encargado = corredor.objects.get(id=user_id)
            except corredor.DoesNotExist:
                messages.error(request, "No se encontró el corredor autenticado.")
                return redirect('login:login')
            
            # 📌 Asignamos automáticamente el tipo de propiedad como "casa"
            propiedad.tipo_propiedad = "Local Comercial"

            propiedad.save()  # Guarda la propiedad en la BD
            form.save_m2m()  # Ahora sí guarda los ManyToManyField (otros)

            # 📌 Guardar imágenes de la propiedad
            for imagen in request.FILES.getlist('imagenes'):
                ImagenPropiedad.objects.create(propiedad=propiedad, imagen=imagen)

            messages.success(request, "Local comercial registrado correctamente.")
            return redirect('propiedad:mostrar_propiedad')
        else:
            print("Errores del formulario:", form.errors.as_json())
            message = 'Hubo un error al registrar el local comercial.'

    else:
        form = PropiedadForm()

    return render(request, 'local_comercial.html', {
        'form': form,
        'message': message,
        'propietarios': propietarios  # Pasamos propietarios al template
    })

#======================================================================================================
@login_required_session
def propiedad_registrar_bodega(request):
    message = ''
    propietarios = propietario.objects.all()  # Obtener propietarios para el select
    user_id = request.session.get("user_id")  # Obtener el ID del corredor autenticado

    if request.method == 'POST':
        form = PropiedadForm(request.POST, request.FILES)
        if form.is_valid():
            propiedad = form.save(commit=False)  # Guarda pero sin ManyToMany aún

            # 📌 Asignamos el corredor autenticado a la propiedad
            try:
                propiedad.id_corredor_encargado = corredor.objects.get(id=user_id)
            except corredor.DoesNotExist:
                messages.error(request, "No se encontró el corredor autenticado.")
                return redirect('login:login')
            
            # 📌 Asignamos automáticamente el tipo de propiedad como "casa"
            propiedad.tipo_propiedad = "Bodega"

            propiedad.save()  # Guarda la propiedad en la BD
            form.save_m2m()  # Ahora sí guarda los ManyToManyField (otros)

            # 📌 Guardar imágenes de la propiedad
            for imagen in request.FILES.getlist('imagenes'):
                ImagenPropiedad.objects.create(propiedad=propiedad, imagen=imagen)

            messages.success(request, "Bodega registrada correctamente.")
            return redirect('propiedad:mostrar_propiedad')
        else:
            print("Errores del formulario:", form.errors.as_json())
            message = 'Hubo un error al registrar la bodega.'

    else:
        form = PropiedadForm()

    return render(request, 'bodega.html', {
        'form': form,
        'message': message,
        'propietarios': propietarios  # Pasamos propietarios al template
    })

#======================================================================================================
@login_required_session
def propiedad_registrar_industrial(request):
    message = ''
    propietarios = propietario.objects.all()  # Obtener propietarios para el select
    user_id = request.session.get("user_id")  # Obtener el ID del corredor autenticado

    if request.method == 'POST':
        form = PropiedadForm(request.POST, request.FILES)
        if form.is_valid():
            propiedad = form.save(commit=False)  # Guarda pero sin ManyToMany aún

            # 📌 Asignamos el corredor autenticado a la propiedad
            try:
                propiedad.id_corredor_encargado = corredor.objects.get(id=user_id)
            except corredor.DoesNotExist:
                messages.error(request, "No se encontró el corredor autenticado.")
                return redirect('login:login')
            
            # 📌 Asignamos automáticamente el tipo de propiedad como "casa"
            propiedad.tipo_propiedad = "Local Industrial"

            propiedad.save()  # Guarda la propiedad en la BD
            form.save_m2m()  # Ahora sí guarda los ManyToManyField (otros)

            # 📌 Guardar imágenes de la propiedad
            for imagen in request.FILES.getlist('imagenes'):
                ImagenPropiedad.objects.create(propiedad=propiedad, imagen=imagen)

            messages.success(request, "Propiedad industrial registrada correctamente.")
            return redirect('propiedad:mostrar_propiedad')
        else:
            print("Errores del formulario:", form.errors.as_json())
            message = 'Hubo un error al registrar la propiedad industrial.'

    else:
        form = PropiedadForm()

    return render(request, 'industrial.html', {
        'form': form,
        'message': message,
        'propietarios': propietarios  # Pasamos propietarios al template
    })

#======================================================================================================
@login_required_session
def propiedad_registrar_terreno(request):
    message = ''
    propietarios = propietario.objects.all()  # Obtener propietarios para el select
    user_id = request.session.get("user_id")  # Obtener el ID del corredor autenticado

    if request.method == 'POST':
        form = PropiedadForm(request.POST, request.FILES)
        if form.is_valid():
            propiedad = form.save(commit=False)  # Guarda pero sin ManyToMany aún

            # 📌 Asignamos el corredor autenticado a la propiedad
            try:
                propiedad.id_corredor_encargado = corredor.objects.get(id=user_id)
            except corredor.DoesNotExist:
                messages.error(request, "No se encontró el corredor autenticado.")
                return redirect('login:login')
            
            # 📌 Asignamos automáticamente el tipo de propiedad como "casa"
            propiedad.tipo_propiedad = "Terreno"

            propiedad.save()  # Guarda la propiedad en la BD
            form.save_m2m()  # Ahora sí guarda los ManyToManyField (otros)

            # 📌 Guardar imágenes de la propiedad
            for imagen in request.FILES.getlist('imagenes'):
                ImagenPropiedad.objects.create(propiedad=propiedad, imagen=imagen)

            messages.success(request, "Terreno registrado correctamente.")
            return redirect('propiedad:mostrar_propiedad')
        else:
            print("Errores del formulario:", form.errors.as_json())
            message = 'Hubo un error al registrar el terreno.'

    else:
        form = PropiedadForm()

    return render(request, 'terreno.html', {
        'form': form,
        'message': message,
        'propietarios': propietarios  # Pasamos propietarios al template
    })

#======================================================================================================

@login_required_session
def propiedad_registrar_parcela(request):
    message = ''
    propietarios = propietario.objects.all()  # Obtener propietarios para el select
    user_id = request.session.get("user_id")  # Obtener el ID del corredor autenticado

    if request.method == 'POST':
        form = PropiedadForm(request.POST, request.FILES)
        if form.is_valid():
            propiedad = form.save(commit=False)  # No guarda aún en la base de datos

            # 📌 Asignar el corredor autenticado a la propiedad
            try:
                propiedad.id_corredor_encargado = corredor.objects.get(id=user_id)
            except corredor.DoesNotExist:
                messages.error(request, "No se encontró el corredor autenticado.")
                return redirect('login:login')
            
            # 📌 Asignamos automáticamente el tipo de propiedad como "casa"
            propiedad.tipo_propiedad = "Parcela"

            propiedad.save()  # Ahora sí guarda en la base de datos

            # 📌 Guardar imágenes asociadas
            for imagen in request.FILES.getlist('imagenes'):
                ImagenPropiedad.objects.create(propiedad=propiedad, imagen=imagen)

            messages.success(request, "Parcela registrada correctamente.")
            return redirect('propiedad:mostrar_propiedad')
        else:
            print("Errores del formulario:", form.errors.as_json())
            message = 'Hubo un error al registrar la parcela.'

    else:
        form = PropiedadForm()

    return render(request, 'parcela.html', {
        'form': form,
        'message': message,
        'propietarios': propietarios  # Pasamos propietarios al template
    })


#===============================================================================================
@login_required_session
def propiedad_modificar(request, id):
    """Vista para modificar una propiedad y asignarle el corredor encargado."""

    propiedad = get_object_or_404(Propiedad, id=id)
    message = ''

    # 📌 Obtener el corredor actual desde la base de datos  
    user_id = request.session.get("user_id")
    corredor_actual = get_object_or_404(corredor, id=user_id)  

    if request.method == 'POST':
        if 'eliminar_imagen' in request.POST:
            imagen_id = request.POST.get('eliminar_imagen')
            imagen = get_object_or_404(ImagenPropiedad, id=imagen_id)
            imagen.imagen.delete()  # 📌 Eliminar el archivo físico de la imagen
            imagen.delete()  # 📌 Eliminar la entrada en la base de datos
            messages.success(request, 'Imagen eliminada exitosamente.')
            return redirect('propiedad:modificar_propiedad', id=id)
        else:
            form = PropiedadForm(request.POST, request.FILES, instance=propiedad)

            # Guardar los valores originales antes de que el formulario los modifique
            valor_original_nueva = propiedad.nueva
            valor_original_posee_casa = propiedad.posee_casa
            valor_original_tipo_propiedad = propiedad.tipo_propiedad  # Guardar el tipo de propiedad original

            if form.is_valid():
                # 📌 Mantener valores originales si no se modifican
                if not form.cleaned_data.get("nueva"):
                    form.instance.nueva = valor_original_nueva
                if not form.cleaned_data.get("posee_casa"):
                    form.instance.posee_casa = valor_original_posee_casa
                
                # 📌 Preservar el tipo de propiedad original
                # Verificar si el campo tipo_propiedad está en el formulario y si está vacío
                if 'tipo_propiedad' not in form.cleaned_data or not form.cleaned_data.get('tipo_propiedad'):
                    form.instance.tipo_propiedad = valor_original_tipo_propiedad

                # 📌 Asignar el corredor encargado a la propiedad
                propiedad.id_corredor_encargado = corredor_actual

                # 📌 Guardar imágenes adicionales
                for imagen in request.FILES.getlist('imagenes'):
                    ImagenPropiedad.objects.create(propiedad=propiedad, imagen=imagen)

                form.save()
                messages.success(request, 'Propiedad modificada exitosamente.')
                return redirect('propiedad:mostrar_propiedad')
            else:
                messages.error(request, 'Hubo un error al modificar la propiedad.')
                print("Errores del formulario:", form.errors)  # Añadir para depuración

    else:
        form = PropiedadForm(instance=propiedad)

    regiones_disponibles = [
        "Metropolitana", "Antofagasta", "Araucanía", "Arica y Parinacota", 
        "Atacama", "Aysén", "Bernardo Ohiggins", "Biobío", "Coquimbo", 
        "Los Lagos", "Los Ríos", "Magallanes", "Maule", "Ñuble", 
        "Tarapacá", "Valparaíso"
    ]

    context = {
        'form': form,
        'message': message,
        'propiedad': propiedad,
        'propietarios': propietario.objects.all(),
        'regiones': regiones_disponibles,
        'region_seleccionada': propiedad.region if propiedad.region else "",
        'comuna': propiedad.comuna or "",
        'calle': propiedad.calle or "",
        'numero_calle': propiedad.numero_calle or "",
        'numero_casa': propiedad.numero_casa or "",
        'dormitorios_seleccionado': int(propiedad.dormitorios) if propiedad.dormitorios else None,
        'banios_seleccionado': int(propiedad.banios) if propiedad.banios else None,
        'estacionamiento_seleccionado': int(propiedad.estacionamiento) if propiedad.estacionamiento else None,
        'bodegas_seleccionado': int(propiedad.bodegas) if propiedad.bodegas else None,
        'pisos_seleccionado': int(propiedad.pisos) if propiedad.pisos else None,
        'otros': list(propiedad.otros.values_list('id', flat=True)),
        'range_15': range(1, 16),  # Rango de 1 a 15 para iterar en el template
        'range_3': range(1, 4),  # Rango de 1 a 3 para los pisos
        'tipo_propiedad': propiedad.tipo_propiedad  # Añadir el tipo de propiedad al contexto
    }

    return render(request, 'modificar_propiedad.html', context)

#======================================================================================================
@login_required_session
def propiedad_eliminar(request, id):
    propiedad = get_object_or_404(Propiedad, id=id)
    if request.method == 'POST':
        propiedad.delete()
        messages.success(request, 'Propiedad eliminada exitosamente, volviendo a lista de propiedades.')
        return redirect('propiedad:mostrar_propiedad')
    return render(request, 'eliminar_propiedad.html', {'propiedad': propiedad})
#======================================================================================================
@login_required_session
def propiedad_descripcion(request, id):
    propiedad = get_object_or_404(Propiedad, id=id)
    return render(request, 'descripcion_propiedad.html', {'propiedad': propiedad})