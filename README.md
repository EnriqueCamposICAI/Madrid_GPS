# Madrid_GPS
Python 3.10.0

Este programa tiene integrado un GPS del mapa de Madrid. En él podrás insertar un origen y destino en el ayuntamiento de Madrid y te buscará la ruta más corta por distancia y por tiempo. 

Hay que tener varias cosas en cuenta a la hora de ejecutar el programa:
  - Lo primero es que es una aproximación. Las distancias y tiempos son medidas de forma que no es 100% ajustado a la realidad. De hecho, las velocidades permitidas en       cada vía e incluso las direcciones (por todas las calles se permite ir en ambos sentidos) son tomadas propias. 
  - Hay que tener en cuenta que los datos de las direcciones y cruces (los dos csv necesarios para ejecutar el programa) no contienen toda la información sobre el           callejero de Madrid. Es decir, solamente se pueden buscar calles y direcciones que estén en dichos csv. Para el caso de las direcciones tenemos la gran mayoría de       calles, pero las calles tenemos el problema de que no están todos los cruces, por lo que hay que tener esto en cuenta. 
  - El archivo grafo.py es una librería similar a NetworkX, pero realizada a mano. Tiene las funciones adaptadas a las necesidades del archivo GPS.py. 

# Cómo buscar direcciones

Para buscar direcciones hay que seguir estos pasos. Más o menos están explicados en el propio archivo, pero para despejar dudas. 
  1. Escoger si se quiere buscar por distancia más corta o menor tiempo
  2. Insertar el nombre completo de la calle de origen (Calle de ... , Carretera de ...)
  3. Seleccionar si el numeral de la calle es de tipo NUM (número) o KM (kilómetro). Esto generalemente será NUM para las calles, avenidas, caminos... y KM para              autovías, autopistas y algunas carreteras
  4. Insertar el número
  5. Si tiene algo extra que ingresar, metalo en extra (como portal B o EXT o INT en caso de autopistas)
  6. Repetir los pasos para la dirección de destino. 
  
Después de realizar esto, el programa mostrará los pasos a seguir en el terminal y mediante un mapa, las direcciones a seguir. 
