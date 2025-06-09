from django.shortcuts import render, get_object_or_404 , redirect
from .models import corredor
from .forms import CorredorLoginForm, RegistroUsuarioForm, CambiarContraseniaForm
from django.core.mail import send_mail
from django.contrib.auth.hashers import make_password, check_password
from django.contrib import messages
from .utils import login_required_session
from operaciones.models import Publicacion
from contacto_corredor.models import contacto_interesado
from django.db.models import Sum
from operaciones.models import OperacionVenta 
from comisiones.models import Comision, Egresos
import json


#=======================================================================================================
# Vista de login

def Corredor_logear(request):
    message = ''
    form = CorredorLoginForm()   

    if request.method == 'POST': # Si se envió el formulario
        correo = request.POST.get('correo')
        clave = request.POST.get('contrasenia')

        if correo and clave:
            try:
                user = corredor.objects.get(correo=correo)

                if check_password(clave, user.contrasenia):
                    request.session['user_id'] = user.id
                    request.session['user_email'] = user.correo
                    request.session['user_name'] = user.nombre
                    print("Usuario logeado:", request.session['user_name'])  # Debug

                    return redirect('login:dashboard')  # Redirige solo si está autenticado
                else:
                    message = 'Clave o contraseña incorrectas'
            except corredor.DoesNotExist:
                message = 'Usuario no existe'

    return render(request, 'login.html', {'form': form, 'message': message})


#=======================================================================================================

# Vista de registro de corredor
def Corredor_registrar(request):
    form = RegistroUsuarioForm()  # Instancia vacía del formulario
    Corredor_v = corredor.objects.all()
    
    if request.method == 'POST':
        form = RegistroUsuarioForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login:login')  # Redirigir al login después de registro exitoso
        else:
            # Los errores se manejarán en el template automáticamente
            pass
    
    return render(request, 'registrar.html', {'form': form, 'corredores': Corredor_v})

#=======================================================================================================
# Vista de solitud de recuperación de contraseña
def solicitar_recuperacion(request):
    message = ''
    form = CorredorLoginForm()   
    Corredor_v = corredor.objects.all()

    if request.method == "POST":
        correo = request.POST.get("correo")
        
        try:
            user = corredor.objects.get(correo=correo)
            user.generar_token()  # Generamos el token de recuperación
            
            enlace = f"http://127.0.0.1:8000/login/cambiar_contrasenia/{user.reset_token}/"

            send_mail(
                "Recuperación de contraseña en PropiedadesWeb",
                f"Haz clic en el siguiente enlace para restablecer tu contraseña: {enlace}",
                "mensajeriapropiedadesweb@gmail.com",
                [correo],
                fail_silently=False,
            )

            message = "Correo enviado con éxito"
        except corredor.DoesNotExist:
            message = "Correo no registrado"
    
    return render(request, 'solicitar_recuperacion.html', {'form': form, 'corredores': Corredor_v, 'message': message})

#=======================================================================================================
# Vista para cambiar la contraseña
def cambiar_contrasenia(request, token):
    #Obtenemos el corredor con el token de recuperación
    Corredor_v = get_object_or_404(corredor, reset_token=token)

    if request.method == "POST":
        form = CambiarContraseniaForm(request.POST)
        if form.is_valid():
            nueva_contrasenia = form.cleaned_data["nueva_contrasenia"]
            # Validamos la contraseña, luego la hasheamos y la guardamos en la BD
            hashed_password = make_password(nueva_contrasenia)
            # Se utiliza update para actualizar la contraseña en la BD y reseteamos el token
            corredor.objects.filter(id=Corredor_v.id).update(
                contrasenia=hashed_password,
                reset_token=None
            )

            messages.success(request, "Contraseña cambiada exitosamente")
            return redirect('login:login')
        else:
            messages.error(request, "Error en el formulario")

    return render(request, "cambiar_contrasenia.html", {'form': CambiarContraseniaForm(),'user': Corredor_v})
#====================================================================================================================== # Asegúrate de importar el modelo correcto
from django.db.models.functions import TruncDate

@login_required_session
def dashboard(request):
    user_id = request.session.get("user_id")

    if not user_id:
        messages.error(request, "No tienes permisos para ver este dashboard.")
        return redirect("login:login")

    # Obtener el mes seleccionado
    mes_seleccionado = request.GET.get("mes")

    # Contar propiedades
    propiedades_en_venta = Publicacion.objects.filter(tipo_publicacion='Venta', estado=True, id_corredor_encargado=user_id).count()
    propiedades_en_arriendo = Publicacion.objects.filter(tipo_publicacion='Arriendo', estado=True, id_corredor_encargado=user_id).count()
    propiedades_vendidas = OperacionVenta.objects.filter(progreso=100, id_corredor=user_id).count()
    consultas_realizadas = contacto_interesado.objects.filter(id_publicacion__id_corredor_encargado=user_id).count()

    # Filtro dinámico para comisiones y egresos
    filtro_mes = {}
    if mes_seleccionado and mes_seleccionado.isdigit():
        filtro_mes["fecha_creacion__month"] = int(mes_seleccionado)

    comisiones_aprobadas_clp = Comision.objects.filter(estado_vale_vista="Aprobado", id_corredor=user_id, **filtro_mes).aggregate(Sum("valor_vale_vista"))["valor_vale_vista__sum"] or 0
    comisiones_retenidas_clp = Comision.objects.filter(estado_vale_vista="Retenido", id_corredor=user_id, **filtro_mes).aggregate(Sum("valor_vale_vista"))["valor_vale_vista__sum"] or 0
    egresos_registrados_clp = Egresos.objects.filter(id_corredor=user_id, **filtro_mes).aggregate(Sum("valor_egreso"))["valor_egreso__sum"] or 0

    # Datos para gráfico dinámico
    if mes_seleccionado:
        # Agrupar egresos por día del mes
        egresos_diarios = Egresos.objects.filter(id_corredor=user_id, **filtro_mes).annotate(fecha_dia=TruncDate("fecha_creacion")).values("fecha_dia").annotate(total_egreso=Sum("valor_egreso")).order_by("fecha_dia")
        egresos_labels = [egreso["fecha_dia"].strftime("%d") for egreso in egresos_diarios]
        egresos_data = [egreso["total_egreso"] for egreso in egresos_diarios]
    else:
        # Mostrar egresos por mes
        meses = range(1, 13)
        egresos_labels = [str(m) for m in meses]
        egresos_data = [Egresos.objects.filter(id_corredor=user_id, fecha_creacion__month=mes).aggregate(Sum("valor_egreso"))["valor_egreso__sum"] or 0 for mes in meses]

    context = {
        'propiedades_en_venta': propiedades_en_venta,
        'propiedades_en_arriendo': propiedades_en_arriendo,
        'propiedades_vendidas': propiedades_vendidas,
        'consultas_realizadas': consultas_realizadas,
        'comisiones_aprobadas_clp': comisiones_aprobadas_clp,
        'comisiones_retenidas_clp': comisiones_retenidas_clp,
        'egresos_registrados_clp': egresos_registrados_clp,
        'meses_json': egresos_labels,
        'egresos_por_mes': egresos_data,
        'mes_seleccionado': mes_seleccionado,
        'egresos_diarios_labels': egresos_labels if mes_seleccionado else [],  # Añadir labels para el gráfico diario
        'egresos_diarios_data': egresos_data if mes_seleccionado else [],  # Añadir data para el gráfico diario
    }

    return render(request, "dashboard.html", context)



#======================================================================================================================
def cerrar_sesion(request):
    request.session.flush() 
    return redirect('login:login') 


