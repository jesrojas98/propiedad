from django.shortcuts import redirect

def login_required_session(view_func):
    """ Decorador para restringir acceso a usuarios autenticados mediante sesión """
    def wrapper(request, *args, **kwargs):
        if 'user_id' not in request.session:
            return redirect('login:login')  # Redirige al login si no está autenticado
        return view_func(request, *args, **kwargs)
    return wrapper
