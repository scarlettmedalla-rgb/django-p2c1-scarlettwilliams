import json
from pathlib import Path
from django.conf import settings
from django.http import Http404
from django.shortcuts import render


def cargar_json(nombre_archivo):
    ruta = settings.BASE_DIR / 'data' / nombre_archivo
    if not ruta.exists():
        return []
    with open(ruta, 'r', encoding='utf-8') as f:
        return json.load(f)

def listar_zonas(request):
    zonas = cargar_json('zonas.json')
    dispositivos = cargar_json('dispositivos.json')

    
    for zona in zonas:
        zona['cantidad_dispositivos'] = sum(1 for d in dispositivos if d.get('zona_id') == zona.get('id'))

    return render(request, 'dispositivos/zonas_listado.html', {'zonas': zonas})

def detalle_zona(request, zona_id):
    zonas = cargar_json('zonas.json')
    categorias = cargar_json('categorias.json')
    dispositivos = cargar_json('dispositivos.json')

    
    zona = next((z for z in zonas if z.get('id') == zona_id), None)
    if not zona:
        
        raise Http404("La zona solicitada no existe.")

   
    mapa_categorias = {c['id']: c['nombre'] for c in categorias}

    dispositivos_zona = []
    consumo_total = 0.0

    for d in dispositivos:
        if d.get('zona_id') == zona_id:
            consumo = float(d.get('consumo_kwh', 0.0))
            consumo_total += consumo
            dispositivos_zona.append({
                'nombre': d.get('nombre'),
                'consumo_kwh': consumo,
                'categoria': mapa_categorias.get(d.get('categoria_id'), 'Sin categoría')
            })

    estado = "ALERTA" if consumo_total > zona.get('limite_kwh', 0.0) else "NORMAL"

    contexto = {
        'zona': zona,
        'dispositivos': dispositivos_zona,
        'consumo_total': round(consumo_total, 2),
        'cantidad_dispositivos': len(dispositivos_zona),
        'estado': estado
    }
    return render(request, 'dispositivos/zona_detalle.html', contexto)