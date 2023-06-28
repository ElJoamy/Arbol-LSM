from lsm_tree import LSMTree
import time
import os
from dotenv import load_dotenv

# Cargar variables de entorno desde el archivo .env
load_dotenv()

# Crear un LSMTree
lsm_tree = LSMTree()
filepath = os.getenv('FILEPATH')

# Insertar claves y valores en el LSMTree
lsm_tree.put("key1", "value1")
lsm_tree.put("key2", "value2")
lsm_tree.put("key3", "value3")
lsm_tree.put("key4", "value4")

# Obtener valores de claves
value1 = lsm_tree.get("key1")  # Retorna "value1"
value2 = lsm_tree.get("key2")  # Retorna "value2"
value3 = lsm_tree.get("key3")  # Retorna "value3"
value4 = lsm_tree.get("key4")  # Retorna "value4"
value5 = lsm_tree.get("key5")  # Retorna None, ya que la clave no existe

# Imprimir los valores obtenidos
print(value1)  # Imprime "value1"
print(value2)  # Imprime "value2"
print(value3)  # Imprime "value3"
print(value4)  # Imprime "value4"
print(value5)  # Imprime None

# Actualizar un valor existente
lsm_tree.put("key2", "new_value2")
updated_value2 = lsm_tree.get("key2")  # Retorna "new_value2"
print(updated_value2)  # Imprime "new_value2"

# Insertar claves temporales con tiempo de vida
lsm_tree.put("temp_key1", "temp_value1", ttl=4)  # Clave temporal con tiempo de vida de 4 segundos
lsm_tree.put("temp_key2", "temp_value2", ttl=5)  # Clave temporal con tiempo de vida de 5 segundos

time.sleep(3)  # Esperar 15 segundos para que las claves temporales expiren

# Obtener valores de claves temporales expiradas
expired_value1 = lsm_tree.get("temp_key1")  # Retorna None, ya que la clave ha expirado
expired_value2 = lsm_tree.get("temp_key2")  # Retorna None, ya que la clave ha expirado
print(expired_value1)  # Imprime None
print(expired_value2)  # Imprime None

# Guardar el LSMTree en disco
lsm_tree.persist_sstables()
lsm_tree.save_to_disk(filepath)

# Cerrar el LSMTree
# lsm_tree.close()

# Cargar el LSMTree desde el archivo en disco
new_lsm_tree = LSMTree.load_from_disk(filepath)

# Obtener valores de claves desde el LSMTree cargado
loaded_value1 = new_lsm_tree.get("key1")  # Retorna "value1"
loaded_value2 = new_lsm_tree.get("key2")  # Retorna "new_value2"
print(loaded_value1)  # Imprime "value1"
print(loaded_value2)  # Imprime "new_value2"

# Cerrar el LSMTree cargado
#new_lsm_tree.close()a