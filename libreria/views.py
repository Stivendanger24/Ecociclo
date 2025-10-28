from django.contrib.auth import authenticate, login as auth_login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
import requests
from django.contrib import messages
from django.db.models import Q 
from django.contrib.auth.views import LoginView
from .models import Producto
from .forms import ProductoForm

# Vista de inicio
def inicio(request):
    return render(request, 'paginas/inicio.html')

# Login usando el sistema de autenticación por defecto de Django
# No necesitas definir un login manualmente si usas la vista por defecto
class CustomLoginView(LoginView):
    template_name = 'paginas/login.html'  # Apunta a tu plantilla personalizada

# Vista para logout
def logout_view(request):
    logout(request)
    return redirect('login')

@login_required(login_url='login')
def profile(request):
    return render(request, 'productos/index.html')

# Vista protegida para productos
@login_required(login_url='login')
def productos(request):
    # Obtener todos los productos
    productos = Producto.objects.all()

    # Hacer una solicitud GET al microservicio Flask para obtener la fecha y hora actuales
    try:
        response = requests.get('http://127.0.0.1:5000/api/get-current-datetime')
        response.raise_for_status()  # Levanta un error si la respuesta no es exitosa
        datetime_data = response.json()  # Convierte la respuesta JSON a un diccionario
    except requests.exceptions.RequestException as e:
        datetime_data = None
        print(f"Error al conectar con el microservicio: {e}")

    # Pasa los productos y la fecha y hora al template
    return render(request, 'productos/index.html', {
        'productos': productos,
        'datetime_data': datetime_data
    })

@login_required(login_url='login')
def crear(request):
    formulario = ProductoForm(request.POST or None, request.FILES or None)
    if formulario.is_valid():
        formulario.save()
        return redirect('productos')
    return render(request, 'productos/crear.html', {'formulario': formulario})

@login_required(login_url='login')
def editar(request, id):
    producto = Producto.objects.get(id=id)
    formulario = ProductoForm(request.POST or None, request.FILES or None, instance=producto)
    if formulario.is_valid() and request.POST:
        formulario.save()
        return redirect('productos')
    return render(request, 'productos/editar.html', {'formulario': formulario})

@login_required(login_url='login')
def nosotros(request):
    return render(request, 'paginas/nosotros.html')

@login_required(login_url='login')
def eliminar(request, id):
    producto = Producto.objects.get(id=id)
    producto.delete()
    return redirect('productos')
