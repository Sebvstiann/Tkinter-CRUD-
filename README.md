# Sistema de Gestión de Inventario con Tkinter y MySQL

Este es un proyecto de escritorio creado en **Python** utilizando **Tkinter** para la interfaz gráfica de usuario (GUI) y **MySQL** para gestionar los datos del inventario. El sistema permite a los usuarios realizar operaciones CRUD (Crear, Leer, Actualizar y Eliminar) sobre productos, con la capacidad de buscar productos por nombre y categoría.

## Funcionalidades

- **Agregar Productos**: Los usuarios pueden añadir productos al inventario con detalles como nombre, descripción, precio, cantidad y categoría.
- **Actualizar Productos**: Permite modificar la información de los productos ya existentes en el inventario.
- **Eliminar Productos**: Elimina productos que ya no están disponibles o que se desea eliminar.
- **Búsqueda de Productos**: Se puede buscar productos por nombre o categoría.
- **Filtro por Categoría**: Los usuarios pueden filtrar los productos según la categoría seleccionada.

## Tecnologías Utilizadas

- **Python**: Lenguaje principal utilizado para el desarrollo de la aplicación.
- **Tkinter**: Biblioteca de Python para crear la interfaz gráfica de usuario (GUI).
- **MySQL**: Base de datos utilizada para almacenar los productos.
- **mysql-connector**: Biblioteca que permite la conexión entre Python y MySQL.

## Requisitos

1. **Python 3.x** instalado en tu máquina.
2. **MySQL** instalado y configurado en tu máquina.
3. La librería **mysql-connector** para conectar Python con MySQL. Puedes instalarla usando el siguiente comando:
   ```bash
   pip install mysql-connector
