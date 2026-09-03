import json
import os
from django.conf import settings
from django.shortcuts import render
from django.http import Http404

def listar_zonas(request):
    ruta_zonas = os.path.join(settings.BASE_DIR, 'data', 'zonas.json')
    ruta_dispositivos = os.path.join(settings.BASE_DIR, 'data', 'dispositivos.json')
    
    with open(ruta_zonas, 'r', encoding='utf-8') as f:
        zonas = json.load(f)
    with open(ruta_dispositivos, 'r', encoding='utf-8') as f:
        dispositivos = json.load(f)
        
    for zona in zonas:
        cantidad = sum(1 for disp in dispositivos if disp['zona_id'] == zona['id'])
        zona['cantidad_dispositivos'] = cantidad
        
    return render(request, 'dispositivos/listar_zonas.html', {'zonas': zonas})

def detalle_zona(request, zona_id):
    ruta_zonas = os.path.join(settings.BASE_DIR, 'data', 'zonas.json')
    ruta_dispositivos = os.path.join(settings.BASE_DIR, 'data', 'dispositivos.json')
    ruta_categorias = os.path.join(settings.BASE_DIR, 'data', 'categorias.json')
    
    with open(ruta_zonas, 'r', encoding='utf-8') as f:
        zonas = json.load(f)
    with open(ruta_dispositivos, 'r', encoding='utf-8') as f:
        dispositivos = json.load(f)
    with open(ruta_categorias, 'r', encoding='utf-8') as f:
        categorias = json.load(f)
        
    zona_actual = None
    for z in zonas:
        if z['id'] == zona_id:
            zona_actual = z
            break
            
    if not zona_actual:
        raise Http404("La zona solicitada no existe")

    dispositivos_zona = []
    consumo_total = 0
    
    for disp in dispositivos:
        if disp['zona_id'] == zona_id:
            cat_nombre = "Sin Categoría"
            for c in categorias:
                if c['id'] == disp['categoria_id']:
                    cat_nombre = c['nombre']
                    break
            
            disp['categoria_nombre'] = cat_nombre
            disp['categoria'] = cat_nombre
            disp['nombre_categoria'] = cat_nombre
            
            dispositivos_zona.append(disp)
            consumo_total += disp['consumo_kwh']
            
    cantidad_disp = len(dispositivos_zona)
    zona_actual['cantidad_dispositivos'] = cantidad_disp
            
    limite = zona_actual['limite_kwh']
    if consumo_total <= limite:
        estado_texto = "NORMAL"
        estado_clase = "success"
    else:
        estado_texto = "ALERTA"
        estado_clase = "danger"

    context = {
        'zona': zona_actual,
        'dispositivos': dispositivos_zona,
        'consumo_total': consumo_total,
        
        'estado_texto': estado_texto,
        'estado_clase': estado_clase,
        'estado': estado_texto,
        
        'cantidad_dispositivos': cantidad_disp,
        'total_dispositivos': cantidad_disp
    }
    
    return render(request, 'dispositivos/detalle_zona.html', context)

def resumen_zonas(request):
    ruta_zonas = os.path.join(settings.BASE_DIR, 'data', 'zonas.json')
    ruta_dispositivos = os.path.join(settings.BASE_DIR, 'data', 'dispositivos.json')
    
    with open(ruta_zonas, 'r', encoding='utf-8') as f:
        zonas = json.load(f)
    with open(ruta_dispositivos, 'r', encoding='utf-8') as f:
        dispositivos = json.load(f)
        
    total_zonas = len(zonas)
    total_dispositivos = len(dispositivos)
    consumo_total_general = 0
    lista_resumen = []
    
    for zona in zonas:
        cantidad_disp_zona = 0
        consumo_zona = 0
        
        for dispositivo in dispositivos:
            if dispositivo['zona_id'] == zona['id']:
                cantidad_disp_zona += 1
                consumo_zona += dispositivo['consumo_kwh']
                consumo_total_general += dispositivo['consumo_kwh']
                
        limite = zona['limite_kwh']
        if consumo_zona <= limite:
            estado_texto = "DENTRO DEL LÍMITE"
            estado_clase = "success"
        else:
            estado_texto = "LÍMITE SUPERADO"
            estado_clase = "danger"
            
        datos_zona = {
            'nombre': zona['nombre'],
            'cantidad_dispositivos': cantidad_disp_zona,
            'consumo_total': consumo_zona,
            'limite': limite,
            'estado_texto': estado_texto,
            'estado_clase': estado_clase,
            'estado': estado_texto
        }
        lista_resumen.append(datos_zona)
        
    context = {
        'resumen_zonas': lista_resumen,
        'total_zonas': total_zonas,
        'total_dispositivos': total_dispositivos,
        'consumo_total_general': consumo_total_general
    }
    
    return render(request, 'resumen_zonas.html', context)