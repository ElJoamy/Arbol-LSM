# LSMTree

## Descripción

LSMTree (Log-Structured Merge Tree) es una estructura de datos que se utiliza para implementar una base de datos de clave-valor. Esta implementación de LSMTree en Python proporciona un mecanismo eficiente para almacenar y recuperar datos de manera persistente.

La LSMTree consta de dos componentes principales: la memtable y las SSTables (Sorted String Tables). La memtable es una estructura en memoria que almacena las claves y los valores temporalmente. A medida que la memtable se llena y alcanza un umbral de tamaño, se realiza una escritura en disco en forma de una SSTable. Las SSTables son archivos en disco que contienen las claves y los valores ordenados.

## Funcionalidades

La implementación de LSMTree en Python proporciona las siguientes funcionalidades:

- `__init__(self, threshold=100, compression=True, db_path='./my_database')`: Es el método de inicialización de la clase. Se encarga de configurar los parámetros iniciales del LSMTree, como el umbral de tamaño de la memtable, la opción de compresión y la ruta del directorio de la base de datos.

- `put(self, key, value, ttl=None)`: Inserta una clave y su valor asociado en el LSMTree. Opcionalmente, se puede especificar un tiempo de vida (ttl) en segundos para la clave.

- `get(self, key)`: Obtiene el valor asociado a una clave en el LSMTree. Devuelve el valor si la clave existe y es válida, de lo contrario devuelve None.

- `flush_memtable(self)`: Transfiere los datos de la memtable a las SSTables y realiza la fusión si es necesario.

- `index_memtable(self)`: Indexa las claves de la memtable para mantener el mapeo con las SSTables.

- `persist_sstables(self)`: Guarda las SSTables en disco y actualiza la ubicación de la base de datos.

- `load_sstables(self)`: Carga las SSTables existentes en disco en la memoria.

- `save_to_disk(self, filepath)`: Guarda el LSMTree en disco utilizando pickle.

- `load_from_disk(filepath)`: Carga un LSMTree desde un archivo utilizando pickle.

- `close(self)`: Guarda las SSTables en disco y limpia las variables del LSMTree.

## Configuración

La clase LSMTree se puede configurar con los siguientes parámetros en su constructor:

- `threshold` (opcional): Umbral de tamaño de la memtable antes de que se active la escritura en disco. El valor predeterminado es 100.

- `compression` (opcional): Indica si se debe comprimir el valor almacenado en disco. El valor predeterminado es True.

- `db_path` (opcional): Ruta del directorio de la base de datos. El valor predeterminado es './my_database'.

## Uso

El archivo [lsm_tree.py](/lsm_tree.py) contiene la implementación de la clase LSMTree.

El archivo [tests.py](/tests.py) contiene un ejemplos de uso de la clase LSMTree y sus funcionalidades.

Recuerda implementar las variables de entorno en el archivo [.env](/.env) antes de ejecutar el archivo [tests.py](/tests.py).

Y no olvides instalar el archivo [requirements.txt](/requirements.txt) antes de ejecutar el archivo [tests.py](/tests.py).

A continuación se muestra un ejemplo básico de cómo utilizar la clase LSMTree:

```python
# Crear una instancia de LSMTree
lsm_tree = LSMTree()

# Insertar datos en el LSMTree
lsm_tree.put('clave1', 'valor1')
lsm_tree.put('clave2', 'valor2', ttl=60)

# Obtener datos del LSMTree
valor1 = lsm_tree.get('clave1')  # Devuelve 'valor1'
valor2 = lsm_tree.get('clave2')  # Devuelve 'valor2'
valor3 = lsm_tree.get('clave3')  # Devuelve None

# Guardar el LSMTree en disco
lsm_tree.save_to_disk('lsm_tree.pickle')

# Cargar el LSMTree desde disco
lsm_tree = LSMTree.load_from_disk('lsm_tree.pickle')

# Cerrar el LSMTree
lsm_tree.close()
```

## Dependencias

Esta implementación de LSMTree en Python depende de las siguientes bibliotecas externas:

- `time`: Para el manejo de tiempo y tiempo de vida (TTL).
- `pickle`: Para guardar y cargar el LSMTree en disco.
- `sortedcontainers`: Para ordenar los diccionarios de la memtable y las SSTables.
- `zlib`: Para la compresión de valores almacenados en disco.
- `os`: Para crear y mover directorios.
- `shutil`: Para eliminar y mover directorios.

Asegúrate de instalar estas dependencias antes de utilizar la implementación de LSMTree.
Puedes instalar las dependencias con el siguiente comando:
```bash
pip install -r requirements.txt
```

## Mejoras y consideraciones adicionales

Además de las funcionalidades mencionadas, se sugieren las siguientes mejoras y consideraciones adicionales para fortalecer y mejorar la implementación de un árbol LSM:

1. Compresión de datos en disco: Utilizar la biblioteca `zlib` para comprimir los valores almacenados en disco puede reducir el espacio de almacenamiento y mejorar la eficiencia en la lectura y escritura de datos.

2. Time To Live (TTL): Implementar un mecanismo de tiempo de vida para las claves, donde las claves expiradas se eliminen automáticamente. Esto es útil para el manejo de datos temporales o con una vida útil limitada.

3. Limpieza y eliminación de datos obsoletos: Agregar un mecanismo para eliminar los datos obsoletos en las SSTables, ya sea basado en el tiempo de vida (TTL) o en alguna política de eliminación específica. Esto ayudará a ahorrar espacio en disco y mantener la integridad de los datos.

4. Optimización de la fusión de SSTables: Considerar estrategias de fusión más eficientes, como la fusión por niveles o la fusión diferencial, para reducir el tiempo y los recursos requeridos durante la fusión de SSTables.

Recuerda que estas mejoras y consideraciones adicionales no son estrictamente requeridas, pero pueden mejorar la funcionalidad y el rendimiento general de un árbol LSM.
Estas mejoras ya están implementadas en el codigo de este repositorio. 

## Configuración del archivo .env

El archivo `.env` es un archivo de configuración que se utiliza para almacenar variables de entorno en un formato clave-valor. En el contexto de la implementación de LSMTree, se utiliza para definir la ruta del directorio de la base de datos y la ubicación del archivo de respaldo del LSMTree.

El archivo `.env` debe tener las siguientes variables:

- `DB_PATH`: La ruta del directorio de la base de datos donde se guardarán las SSTables. Puedes proporcionar una ruta absoluta o relativa al directorio actual. El valor predeterminado es `./my_database/`.

- `FILEPATH`: La ubicación completa del archivo de respaldo del LSMTree. Esto se utiliza para guardar y cargar el LSMTree utilizando el método `save_to_disk` y `load_from_disk`. El valor predeterminado es `${DB_PATH}lsm_tree.pkl`.

Puedes ajustar los valores de estas variables según tus preferencias y requisitos.

Asegúrate de crear un archivo `.env` en el mismo directorio que tu script de Python y asegúrate de que las variables estén configuradas correctamente antes de ejecutar el código.

Aquí hay un ejemplo de cómo podría verse un archivo `.env`:

```
DB_PATH=./my_database/
FILEPATH=${DB_PATH}lsm_tree.pkl
```

En este ejemplo, el directorio de la base de datos se establece en `./my_database/` y el archivo de respaldo del LSMTree se ubicará en `${DB_PATH}lsm_tree.pkl`.

Recuerda que debes asegurarte de tener la biblioteca `python-dotenv` instalada para poder cargar y utilizar las variables del archivo `.env`. Puedes instalarla con el siguiente comando:

```bash
pip install python-dotenv
```

## Contribuciones
Si deseas contribuir en el proyectopuedes enviarme un mensaje a 
[gmail](mailto:joamysalguero1@gmail.com)
o por linkedin
[linkedin](https://www.linkedin.com/in/joamy5902/)