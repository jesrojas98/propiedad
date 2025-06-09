from django.shortcuts import render, redirect, get_object_or_404
from .models import Publicacion, OperacionVenta, Mindicador
from propiedad.models import Propiedad, ImagenPropiedad
from .forms import OperacionVentaForm
from documentos.models import Documento
from .forms import PublicacionForm
from django.contrib import messages
from django.http import JsonResponse
from login.models import corredor
from login.utils import login_required_session
import logging
from django.http import JsonResponse
import requests


logger = logging.getLogger(__name__)

#========================================================================================================================
def inicio(request):
    return render(request, "inicio.html")
#========================================================================================================================
from django.shortcuts import render
from django.db.models import Q

def publicaciones(request):
    # Obtener todas las publicaciones activas
    publicaciones = Publicacion.objects.filter(estado=True).order_by('-fecha_creacion')
    
    # Separar publicaciones en categorías
    publicaciones_destacadas = publicaciones.filter(destacada=True)
    publicaciones_venta = publicaciones.filter(tipo_publicacion__iexact="Venta")
    publicaciones_arriendo = publicaciones.filter(tipo_publicacion__iexact="Arriendo")
    
    # Asignar imagen a cada publicación en todas las categorías
    publicaciones_destacadas = asignar_imagen(publicaciones_destacadas)
    publicaciones_venta = asignar_imagen(publicaciones_venta)
    publicaciones_arriendo = asignar_imagen(publicaciones_arriendo)
    
    return render(request, "publicaciones.html", {
        "publicaciones_destacadas": publicaciones_destacadas,
        "publicaciones_venta": publicaciones_venta,
        "publicaciones_arriendo": publicaciones_arriendo
    })
#========================================================================================================================
def publicaciones_filtradas(request):
    # Obtener parámetros de búsqueda básicos
    tipo_publicacion = request.GET.get('tipo_publicacion', '')
    tipo_propiedad = request.GET.get('tipo_propiedad', '')
    ubicacion = request.GET.get('ubicacion', '')
    
    # Obtener parámetros de búsqueda avanzados
    dormitorios = request.GET.get('dormitorios', '')
    banios = request.GET.get('banios', '')
    estacionamiento = request.GET.get('estacionamiento', '')
    tipo_valor = request.GET.get('tipo_valor', '')
    precio_min = request.GET.get('precio_min', '')
    precio_max = request.GET.get('precio_max', '')
    
    # Iniciar con todas las publicaciones activas
    publicaciones = Publicacion.objects.filter(estado=True).order_by('-fecha_creacion')
    
    # Aplicar filtros básicos
    # Filtrar por tipo de publicación (Venta/Arriendo)
    if tipo_publicacion:
        publicaciones = publicaciones.filter(tipo_publicacion=tipo_publicacion)
    
    # Filtrar por ubicación (buscar en comuna, ciudad o calle)
    if ubicacion:
        publicaciones = publicaciones.filter(
            Q(id_propiedad__comuna__icontains=ubicacion) | 
            Q(id_propiedad__region__icontains=ubicacion) | 
            Q(id_propiedad__calle__icontains=ubicacion) |
            Q(id_propiedad__sector__icontains=ubicacion)
        )
    
    # Aplicar filtros avanzados
    # Filtrar por tipo de propiedad
    if tipo_propiedad:
        publicaciones = publicaciones.filter(
            Q(titulo__icontains=tipo_propiedad) | 
            Q(descripcion__icontains=tipo_propiedad)
        )
    
    # Filtrar por número mínimo de dormitorios
    if dormitorios:
        publicaciones = publicaciones.filter(id_propiedad__dormitorios__gte=dormitorios)
    
    # Filtrar por número mínimo de baños
    if banios:
        publicaciones = publicaciones.filter(id_propiedad__banios__gte=banios)
    
    # Filtrar por número mínimo de estacionamientos
    if estacionamiento:
        publicaciones = publicaciones.filter(id_propiedad__estacionamiento__gte=estacionamiento)
    
    # Filtrar por tipo de valor (CLP/UF)
    if tipo_valor:
        publicaciones = publicaciones.filter(tipo_valor=tipo_valor)
    
    # Filtrar por rango de precios
    if precio_min:
        publicaciones = publicaciones.filter(valor__gte=precio_min)
    
    if precio_max:
        publicaciones = publicaciones.filter(valor__lte=precio_max)
    
    # Asignar imágenes a los resultados filtrados
    publicaciones_filtradas = asignar_imagen(publicaciones)
    
    return render(request, "publicaciones_filtradas.html", {
        "publicaciones_filtradas": publicaciones_filtradas
    })

def asignar_imagen(publicaciones):
    for publicacion in publicaciones:
        primera_imagen = ImagenPropiedad.objects.filter(propiedad=publicacion.id_propiedad).first()
        publicacion.imagen_url = primera_imagen.imagen.url if primera_imagen else "/static/img/default.jpg"
    return publicaciones

def detalle_publicacion(request, publicacion_id):
    publicacion = Publicacion.objects.get(id=publicacion_id, estado=True)
    imagenes = ImagenPropiedad.objects.filter(propiedad=publicacion.id_propiedad)
    
    return render(request, "detalle_publicacion.html", {
        "publicacion": publicacion,
        "imagenes": imagenes
    })
#========================================================================================================================
@login_required_session
def editar_publicacion(request, publicacion_id):
    publicacion = get_object_or_404(Publicacion, id=publicacion_id)

    if request.method == "POST":
        form = PublicacionForm(request.POST, request.FILES, instance=publicacion)
        if form.is_valid():
            instancia = form.save(commit=False)
            instancia.titulo = instancia.id_propiedad.titulo  # Mantener el título de la propiedad
            
            # Actualizar la descripción de la propiedad con la nueva descripción de la publicación
            instancia.id_propiedad.descripcion = instancia.descripcion
            instancia.id_propiedad.save()  # Guardar cambios en la propiedad

            instancia.save()  # Guardar cambios en la publicación
            messages.success(request, "¡Publicación editada con éxito!")
            return redirect("operaciones:lista_publicaciones")  # Redirige a la lista de publicaciones
        else:
            messages.error(request, "Hubo un error en el formulario, revisa los campos.")
    else:
        form = PublicacionForm(instance=publicacion)

    return render(request, "editar_publicacion.html", {"form": form, "publicacion": publicacion})

#========================================================================================================================
@login_required_session
def lista_publicaciones(request):
    """ Vista para listar solo las publicaciones del corredor autenticado """
    user_id = request.session.get("user_id")  # Obtener el ID del corredor autenticado

    # Filtrar las publicaciones solo del corredor autenticado
    publicaciones = Publicacion.objects.filter(id_corredor_encargado_id=user_id).order_by('-fecha_creacion')

    # Obtener la primera imagen asociada a cada propiedad
    for publicacion in publicaciones:
        primera_imagen = ImagenPropiedad.objects.filter(propiedad=publicacion.id_propiedad).first()
        publicacion.imagen_url = primera_imagen.imagen.url if primera_imagen else "/static/img/default.jpg"

    return render(request, "lista_publicaciones.html", {"publicaciones": publicaciones})

#========================================================================================================================


@login_required_session
def cambiar_estado_publicacion(request, publicacion_id):
    publicacion = get_object_or_404(Publicacion, id=publicacion_id)
    publicacion.estado = not publicacion.estado  # Alterna el estado
    publicacion.save()
    return JsonResponse({"success": True, "estado": publicacion.estado})

from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from .models import Publicacion

@login_required_session
def destacar_publicacion(request, publicacion_id):
    if request.method == "POST":
        publicacion = get_object_or_404(Publicacion, id=publicacion_id)
        publicacion.destacada = not publicacion.destacada  # Cambia el estado
        publicacion.save()

        return JsonResponse({"success": True, "destacada": publicacion.destacada})
    
    return JsonResponse({"success": False})

#========================================================================================================================

@login_required_session
def crear_publicacion(request):
    if request.method == "POST":
        form = PublicacionForm(request.POST, request.FILES)
        if form.is_valid():
            try:
                id_propiedad = form.cleaned_data.get("id_propiedad")
                if not id_propiedad:
                    messages.error(request, "Debes seleccionar una propiedad válida.")
                    return render(request, "crear_publicacion.html", {"form": form})

                publicacion = form.save(commit=False)
                publicacion.titulo = id_propiedad.titulo 

                if not publicacion.descripcion or not publicacion.descripcion.strip():
                    publicacion.descripcion = id_propiedad.descripcion  

                user_id = request.session.get("user_id")
                if not user_id:
                    messages.error(request, "No se encontró la sesión del usuario.")
                    return redirect("operaciones:crear_publicacion")

                try:
                    publicacion.id_corredor_encargado = corredor.objects.get(id=user_id)
                except corredor.DoesNotExist:
                    messages.error(request, "No se encontró el corredor autenticado.")
                    return redirect("operaciones:crear_publicacion")

                publicacion.save()
                
                messages.success(request, "¡Publicación creada con éxito!")
                return redirect("operaciones:lista_publicaciones")

            except Exception as e:
                logger.error(f"Error al guardar la publicación: {str(e)}")
                messages.error(request, f"Ocurrió un error inesperado: {str(e)}")
        else:
            messages.error(request, "Hubo un error en el formulario, revisa los campos.")
    
    else:
        form = PublicacionForm()
        form.fields["id_propiedad"].queryset = Propiedad.objects.all() 

    return render(request, "crear_publicacion.html", {"form": form})


#========================================================================================================================

def detalle_publicacion(request, id):
    publicacion = get_object_or_404(Publicacion, id=id)

    # Obtener todas las imágenes de la propiedad asociada a la publicación
    imagenes = ImagenPropiedad.objects.filter(propiedad=publicacion.id_propiedad)

    return render(request, 'detalle_publicacion.html', {
        'publicacion': publicacion,
        'imagenes': imagenes
    })

#========================================================================================================================

@login_required_session
def listado_operaciones(request):
    """Lista todas las operaciones de venta y permite editarlas desde la lista"""

    operaciones = OperacionVenta.objects.all().order_by('-fecha_creacion_operacion')

    if request.method == "POST":
        operacion_id = request.POST.get("operacion_id")
        operacion = get_object_or_404(OperacionVenta, id=operacion_id)

        # Asigna los valores desde el formulario si existen
        operacion.estado_antecedentes = request.POST.get("estado_antecedentes", operacion.estado_antecedentes)
        operacion.estado_agendamiento = request.POST.get("estado_agendamiento", operacion.estado_agendamiento)
        operacion.estado_cierre_negocio = request.POST.get("estado_cierre_negocio", operacion.estado_cierre_negocio)
        operacion.estado_promesa = request.POST.get("estado_promesa", operacion.estado_promesa)
        operacion.estado_escritura = request.POST.get("estado_escritura", operacion.estado_escritura)
        operacion.estado_inscripcion = request.POST.get("estado_inscripcion", operacion.estado_inscripcion)
        operacion.estado_entrega = request.POST.get("estado_entrega", operacion.estado_entrega)

        # Calcular progreso automático
        operacion.progreso = calcular_progreso(operacion)

        operacion.save()  # Guarda los cambios en la BD
        messages.success(request, "Operación actualizada correctamente.")

        return redirect("operaciones:listado_operaciones")  # Redirige para evitar reenvío del formulario

    # Agregar progreso al contexto de cada operación
    for operacion in operaciones:
        operacion.progreso = calcular_progreso(operacion)

    context = {
        'operaciones': operaciones,
        'ESTADO_ANTECEDENTES_CHOICES': OperacionVenta.ESTADO_ANTECEDENTES_CHOICES,
        'ESTADO_AGENDAMIENTO_CHOICES': OperacionVenta.ESTADO_AGENDAMIENTO_CHOICES,
        'ESTADO_NEGOCIO_CHOICES': OperacionVenta.ESTADO_NEGOCIO_CHOICES,
        'ESTADO_PROMESA_CHOICES': OperacionVenta.ESTADO_PROMESA_CHOICES,
        'ESTADO_ESCRITURA_CHOICES': OperacionVenta.ESTADO_ESCRITURA_CHOICES,
        'ESTADO_INSCRIPCION_CHOICES': OperacionVenta.ESTADO_INSCRIPCION_CHOICES,
        'ESTADO_ENTREGA_CHOICES': OperacionVenta.ESTADO_ENTREGA_CHOICES,
    }

    return render(request, 'listado_operaciones.html', context)


def calcular_progreso(operacion):
    """Calcula el progreso de la operación en base a los estados."""
    
    # Lista de estados a evaluar
    estados = [
        operacion.estado_antecedentes,
        operacion.estado_agendamiento,
        operacion.estado_cierre_negocio,
        operacion.estado_promesa,
        operacion.estado_escritura,
        operacion.estado_inscripcion,
        operacion.estado_entrega,
    ]

    total_fases = len(estados)
    progreso_total = 0  # Variable para acumular el progreso

    # Definir pesos de avance por tipo de estado
    avance_completo = 1 
    avance_medio = 0.5   
    sin_avance = 0       

    for estado in estados:
        if estado in ["ANULADA", "RECHAZADA", "OMITIDA"]:
            progreso_total += sin_avance  # No suma
        elif estado == "PRESENTADA":
            progreso_total += avance_medio  # Suma la mitad
        elif estado in ["REALIZADA", "ACEPTADA", "ENTREGADA"]:  
            progreso_total += avance_completo  # Suma completo

    # Calcular porcentaje final
    progreso = round((progreso_total / total_fases) * 100) if total_fases > 0 else 0
    return progreso




#========================================================================================================================

@login_required_session
def crear_operacion_venta(request, propiedad_id):
    """Vista para registrar una nueva operación de venta permitiendo seleccionar la propiedad."""

    # Obtener el corredor autenticado
    user_id = request.session.get("user_id")
    corredor_actual = get_object_or_404(corredor, id=user_id)

    # Validar que la propiedad seleccionada pertenece al corredor
    propiedad = get_object_or_404(Propiedad, id=propiedad_id, id_corredor_encargado=corredor_actual)

    if request.method == "POST":
        form = OperacionVentaForm(request.POST)
        if form.is_valid():
            operacion = form.save(commit=False)

            # Filtrar documentos de la propiedad seleccionada
            documentos = Documento.objects.filter(id_propiedad=propiedad)

            if not documentos.exists():
                messages.error(request, "La propiedad seleccionada no tiene documentos asociados.")
                return render(request, "crear_operacion_venta.html", {
                    "form": form,
                    "propiedad": propiedad,
                    "mostrar_boton_documento": True  # Variable para el botón de registrar documento
                })

            # Asignamos los valores correctos a la operación
            operacion.id_documento = documentos.first()
            operacion.id_corredor = corredor_actual  
            operacion.id_propiedad = propiedad  
            operacion.comision_operacion = int(operacion.valor_operacion * 0.04)  # 4% de comisión

            # Guardamos la operación
            operacion.save()

            messages.success(request, "Operación de venta registrada con éxito.")
            return redirect("operaciones:listado_operaciones")
        else:
            messages.error(request, "Hubo un error en el formulario. Revisa los datos ingresados.")
    else:
        form = OperacionVentaForm()

    return render(request, "crear_operacion_venta.html", {
        "form": form,
        "propiedad": propiedad,
        "mostrar_boton_documento": False  # No mostrar el botón por defecto
    })


#========================================================================================================================
@login_required_session
def eliminar_operacion(request, operacion_id):
    """Elimina una operación de venta."""
    
    operacion = get_object_or_404(OperacionVenta, id=operacion_id)
    
    if request.method == "POST":
        operacion.delete()
        messages.success(request, "Operación eliminada correctamente.")
        return redirect('operaciones:listado_operaciones')

    return render(request, 'eliminar_operacion.html', {'operacion': operacion})

#========================================================================================================================

# Función para obtener el valor de la UF desde la API
def obtener_uf():
    url = "https://mindicador.cl/api/uf"
    response = requests.get(url)
    
    if response.status_code == 200:
        data = response.json()
        # Obtener el valor de la UF del último día
        valor_uf = data['serie'][0]['valor']  # Obtiene el valor de la UF
        return valor_uf
    else:
        return None

# Función para calcular el pago mensual
def calcular_pago_mensual(principal, tasa_interes_anual, plazo_anos, valor_uf, unidad_moneda):
    # Si la unidad de moneda es UF, multiplicamos por el valor de la UF
    if unidad_moneda == 'uf':
        principal = principal * valor_uf  # Convertimos el principal a CLP

    tasa_mensual = tasa_interes_anual / 12 / 100  # Convertimos la tasa anual a mensual
    num_pagos = plazo_anos * 12  # Número total de pagos (meses)
    cuota_mensual = principal * (tasa_mensual * (1 + tasa_mensual) ** num_pagos) / ((1 + tasa_mensual) ** num_pagos - 1)
    return cuota_mensual

# Vista para procesar el formulario y calcular los pagos, obtener la UF
def simular_credito(request):
    cuota_mensual = None  # Inicializamos la cuota mensual como None
    pagos = []
    total_pagado = 0
    pago_intereses_total = 0
    pago_principal_total = 0
    indicador_resultado = None  # Variable para almacenar el valor de la UF
    unidad_moneda = 'clp'  # Valor predeterminado para la unidad de moneda
    principal = 0
    
    # Obtenemos el valor de la UF desde la API
    valor_uf = obtener_uf()

    if request.method == 'POST':
        # Obtenemos la unidad de moneda seleccionada
        unidad_moneda = request.POST.get('unidad_moneda', 'clp')

        principal = request.POST.get('principal')
        plazo_anos = request.POST.get('plazo_anos')
        tasa_interes_anual = request.POST.get('tasa_interes_anual')

        if principal and plazo_anos and tasa_interes_anual:
            try:
                principal = float(principal)  # Convertimos el valor principal a float
                plazo_anos = int(plazo_anos)  # Convertimos el plazo a años a int
                tasa_interes_anual = float(tasa_interes_anual)  # Convertimos la tasa a float

                # Calculamos la cuota mensual usando la función
                cuota_mensual = calcular_pago_mensual(principal, tasa_interes_anual, plazo_anos, valor_uf, unidad_moneda)

                # Convertimos el principal a UF si es necesario para los cálculos
                saldo_pendiente = principal * valor_uf if unidad_moneda == 'uf' else principal  # Convertimos a UF solo si se seleccionó UF

                # Simulación de los pagos mensuales
                for mes in range(1, plazo_anos * 12 + 1):
                    # Calculamos los intereses del mes
                    interes_mes = saldo_pendiente * (tasa_interes_anual / 100 / 12)
                    # El pago principal es la cuota mensual menos los intereses
                    pago_principal = cuota_mensual - interes_mes
                    saldo_pendiente -= pago_principal

                    pagos.append({
                        'mes': mes,
                        'interes_mes': round(interes_mes, 2),
                        'pago_principal': round(pago_principal, 2),
                        'saldo_pendiente': round(saldo_pendiente, 2)
                    })
                # Convertimos el pago principal total a CLP si es necesario
                pago_principal_total = principal * valor_uf if unidad_moneda == 'uf' else principal  # Convertir a CLP si está en UF

                # Resumen final en CLP
                total_pagado = cuota_mensual * plazo_anos * 12
                pago_intereses_total = total_pagado - pago_principal_total

                
                

            except ValueError:
                return render(request, 'credito.html', {'error': 'Por favor, ingrese valores válidos.'})
        else:
            return render(request, 'credito.html', {'error': 'Por favor, complete todos los campos.'})

    # Retorna los resultados a la misma página
    return render(request, 'credito.html', {
        'cuota_mensual': round(cuota_mensual, 2) if cuota_mensual else None,
        'pagos': pagos,
        'total_pagado': round(total_pagado, 2),
        'pago_intereses_total': round(pago_intereses_total, 2),
        'pago_principal_total': round(pago_principal_total, 2),  # Muestra el principal total siempre en CLP
        'valor_uf': round(valor_uf, 2) if valor_uf else None,
        'unidad_moneda': unidad_moneda,
        'principal': principal  # Muestra siempre el valor del principal en CLP
    })
#========================================================================================================================