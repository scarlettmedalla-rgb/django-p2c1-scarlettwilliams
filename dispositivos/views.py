# dispositivos/views.py
from django.shortcuts import render
from .services import cargar_dispositivos

def inicio(request):
  contexto = {
    "sistema": "EcoEnergy",
    "mensaje": "Monitoreo energético responsable",
    "asignatura": "Programación Back End",
  }
  return render(request,"dispositivos/inicio.html",contexto,)

# dispositivos/views.py
def catalogo(request):
  dispositivos = cargar_dispositivos()
  activos = sum(
    1 for item in dispositivos
      if item["estado"] == "Activo"
  )
  contexto = {
  "dispositivos": dispositivos,
  "total": len(dispositivos),
  "total_activos": activos,
  }
  return render(
      request, "dispositivos/catalogo.html", contexto
  )


#crear un metodo que muestre un dispositivo por ruta que seria dispositivo/1 deberia cargar un dispositivo y si es distinto a 1 dispositivo no encontrado