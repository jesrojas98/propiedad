from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Propiedad, ImagenPropiedad
from login.models import corredor
from .forms import PropiedadForm
from propietarios.models import propietario
from login.utils import login_required_session
import cloudinary.uploader
from django.db import transaction

#======================================================================================================
@login_required_session
def propiedad_mostrar(request):
    propiedades = Propiedad.objects.all()
    return render(request, 'mostrar_propiedad.html', {'propiedades': propiedades})
#======================================================================================================
@login_required_session
def propiedad_registrar(request):
    message = ''
    propietarios = propietario.objects.all()

    if request.method == 'POST':
        form = PropiedadForm(request.POST, request.FILES)
        if form.is_valid():
            with transaction.atomic():  # Asegurar consistencia
                propiedad = form.save()
                
                # Subir imágenes a Cloudinary
                subir_imagenes_cloudinary(request, propiedad)
                
            return redirect('propiedad:mostrar_propiedad')
        else:
            print("Errores del formulario:", form.errors.as_json())
            message = 'Hubo un error al registrar la propiedad.'

    else:
        form = PropiedadForm()

    return render(request, 'agregar_propiedad.html', {
        'form': form,
        'message': message,
        'propietarios': propietarios
    })

def subir_imagenes_cloudinary(request, propiedad):
    """
    Función para subir múltiples imágenes a Cloudinary y asociarlas a una propiedad
    """
    imagenes_subidas = request.FILES.getlist('imagenes')
    
    for idx, imagen in enumerate(imagenes_subidas):
        try:
            # Subir imagen a Cloudinary
            resultado = cloudinary.uploader.upload(
                imagen,
                folder=f"propiedades/{propiedad.id}",  # Organizar por propiedad
                transformation=[
                    {'width': 1200, 'height': 900, 'crop': 'limit'},  # Redimensionar
                    {'quality': 'auto'},  # Optimización automática
                    {'fetch_format': 'auto'}  # Formato automático (WebP cuando sea posible)
                ]
            )
            
            # Crear objeto ImagenPropiedad con la información de Cloudinary
            ImagenPropiedad.objects.create(
                propiedad=propiedad,
                imagen=resultado['public_id'],  # Cloudinary public_id
                cloudinary_public_id=resultado['public_id'],
                orden=idx,
                es_portada=(idx == 0)  # Primera imagen como portada
            )
            
        except Exception as e:
            print(f"Error subiendo imagen {idx}: {str(e)}")
            # Continuar con las demás imágenes aunque una falle


#======================================================================================================
@login_required_session
def propiedad_registrar_casa(request):
    message = ''
    propietarios = propietario.objects.all()
    user_id = request.session.get("user_id")

    if request.method == 'POST':
        form = PropiedadForm(request.POST, request.FILES)
        if form.is_valid():
            with transaction.atomic():
                propiedad = form.save(commit=False)
                
                # Asignar corredor y tipo
                try:
                    propiedad.id_corredor_encargado = corredor.objects.get(id=user_id)
                except corredor.DoesNotExist:
                    messages.error(request, "No se encontró el corredor autenticado.")
                    return redirect('login:login')
                
                propiedad.tipo_propiedad = "Casa"
                propiedad.save()
                form.save_m2m()

                # 🔥 Subir imágenes a Cloudinary
                subir_imagenes_cloudinary(request, propiedad)

            messages.success(request, "Casa registrada correctamente.")
            return redirect('propiedad:mostrar_propiedad')
        else:
            print("Errores del formulario:", form.errors.as_json())
            message = 'Hubo un error al registrar la casa.'

    else:
        form = PropiedadForm()

    return render(request, 'casa.html', {
        'form': form,
        'message': message,
        'propietarios': propietarios
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
            subir_imagenes_cloudinary(request, propiedad)

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
            subir_imagenes_cloudinary(request, propiedad)

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
            subir_imagenes_cloudinary(request, propiedad)

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
            subir_imagenes_cloudinary(request, propiedad)

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
            subir_imagenes_cloudinary(request, propiedad)

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
            subir_imagenes_cloudinary(request, propiedad)

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
            subir_imagenes_cloudinary(request, propiedad)

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
    propiedad = get_object_or_404(Propiedad, id=id)
    message = ''
    user_id = request.session.get("user_id")
    corredor_actual = get_object_or_404(corredor, id=user_id)

    if request.method == 'POST':
        if 'eliminar_imagen' in request.POST:
            imagen_id = request.POST.get('eliminar_imagen')
            imagen = get_object_or_404(ImagenPropiedad, id=imagen_id)
            
            # 🔥 Eliminar de Cloudinary
            if imagen.cloudinary_public_id:
                try:
                    cloudinary.uploader.destroy(imagen.cloudinary_public_id)
                except Exception as e:
                    print(f"Error eliminando imagen de Cloudinary: {e}")
            
            imagen.delete()
            messages.success(request, 'Imagen eliminada exitosamente.')
            return redirect('propiedad:modificar_propiedad', id=id)
        else:
            form = PropiedadForm(request.POST, request.FILES, instance=propiedad)

            # Guardar valores originales
            valor_original_nueva = propiedad.nueva
            valor_original_posee_casa = propiedad.posee_casa
            valor_original_tipo_propiedad = propiedad.tipo_propiedad

            if form.is_valid():
                with transaction.atomic():
                    # Mantener valores originales si no se modifican
                    if not form.cleaned_data.get("nueva"):
                        form.instance.nueva = valor_original_nueva
                    if not form.cleaned_data.get("posee_casa"):
                        form.instance.posee_casa = valor_original_posee_casa
                    if 'tipo_propiedad' not in form.cleaned_data or not form.cleaned_data.get('tipo_propiedad'):
                        form.instance.tipo_propiedad = valor_original_tipo_propiedad

                    propiedad.id_corredor_encargado = corredor_actual

                    # 🔥 Subir nuevas imágenes a Cloudinary
                    if request.FILES.getlist('imagenes'):
                        subir_imagenes_cloudinary(request, propiedad)

                    form.save()

                messages.success(request, 'Propiedad modificada exitosamente.')
                return redirect('propiedad:mostrar_propiedad')
            else:
                messages.error(request, 'Hubo un error al modificar la propiedad.')
                print("Errores del formulario:", form.errors)

    else:
        form = PropiedadForm(instance=propiedad)

    # ... resto del contexto igual que antes ...
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
        'range_15': range(1, 16),
        'range_3': range(1, 4),
        'tipo_propiedad': propiedad.tipo_propiedad
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