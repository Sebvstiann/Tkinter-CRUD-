import mysql.connector

# Conexión a la base de datos MySQL
def get_db_connection():
    conn = mysql.connector.connect(
        host="localhost",  # Cambia esto si es necesario
        user="root",  # Cambia esto si es necesario
        password="2001",  # Cambia esto si es necesario
        database="gestion_inventario"  # Nombre de la base de datos
    )
    return conn

# Función para obtener todas las categorías
def obtener_categorias():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM categorias')
    categorias = cursor.fetchall()
    cursor.close()
    conn.close()
    return categorias  # Devuelve todos los registros de categorías

# Función para obtener productos filtrados por categoría
def obtener_productos_por_categoria(categoria_id=None):
    conn = get_db_connection()
    cursor = conn.cursor()
    if categoria_id:
        cursor.execute('SELECT * FROM productos WHERE categoria_id = %s', (categoria_id,))
    else:
        cursor.execute('SELECT * FROM productos')
    productos = cursor.fetchall()
    cursor.close()
    conn.close()
    return productos

# Función para agregar un producto
def agregar_producto(nombre, descripcion, precio, cantidad, categoria_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO productos (nombre, descripcion, precio, cantidad, categoria_id) VALUES (%s, %s, %s, %s, %s)",
        (nombre, descripcion, precio, cantidad, categoria_id)
    )
    conn.commit()  # Confirmar cambios
    cursor.close()
    conn.close()

# Función para actualizar un producto
def actualizar_producto(id, nombre, descripcion, precio, cantidad, categoria_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        "UPDATE productos SET nombre = %s, descripcion = %s, precio = %s, cantidad = %s, categoria_id = %s WHERE id = %s",
        (nombre, descripcion, precio, cantidad, categoria_id, id)
    )
    conn.commit()  # Confirmar cambios
    cursor.close()
    conn.close()

# Función para eliminar un producto
def eliminar_producto(id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM productos WHERE id = %s", (id,))
    conn.commit()  # Confirmar cambios
    cursor.close()
    conn.close()

