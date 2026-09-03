preguntas evaluacion parte 2
1. El recorrido empieza en el archivo urls.py, donde la URL (/resumen-zonas/) atrapa el clic del usuario y lo dirige a la View (la función llamada "resumen_zonas" en el archivo views.py). 
Dentro de esa View, Python carga los archivos, hace las sumas y empaqueta todos los resultados en un diccionario llamado contexto (context). Finalmente, la View envía ese contexto al Template (el archivo resumen_zonas.html), el cual toma esos datos y los acomoda en la tabla y las tarjetas para mostrárselos al usuario en su pantalla. 

2. Esto se encuentra en el archivo views.py, específicamente dentro de la función resumen_zonas. 
Funciona usando un ciclo (un for) que revisa la lista de dispositivos uno por uno. Si el dispositivo pertenece a la zona que se está revisando en ese momento, el código le suma un 1 al contador de dispositivos (cantidad_disp_zona += 1) y le suma los kilowatts del dispositivo al acumulador de consumo de esa zona (consumo_zona += dispositivo['consumo_kwh']).

3. La condición que utilicé compara el consumo con el límite mediante un simple if consumo_zona <= limite:. Cuando una zona no tiene ningún dispositivo guardado, su contador de consumo nunca suma nada y se queda en 0. Como el 0 siempre es menor que el límite de la zona, el código pasa por la condición de forma exitosa y le asigna automáticamente el estado "DENTRO DEL LÍMITE" con color verde.
