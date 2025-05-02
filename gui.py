import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
from database import obtener_productos_por_categoria, agregar_producto, actualizar_producto, eliminar_producto, get_db_connection  # Asegúrate de tener las importaciones correctas

class InventarioApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Sistema de Gestión de Inventario")
        self.root.geometry("800x600")
        
        # Cambiar el color de fondo del root
        self.root.configure(bg="#f0f0f0")  # Fondo gris claro

        # Crear un menú de navegación
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)

        # Menú de Archivo
        file_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Archivo", menu=file_menu)
        file_menu.add_command(label="Salir", command=self.root.quit)

        # Menú de Edición
        edit_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Editar", menu=edit_menu)
        edit_menu.add_command(label="Actualizar", command=self.actualizar_producto)

        # Crear los widgets después de configurar el menú
        self.create_widgets()

    def create_widgets(self):
        # Filtro de categoría
        self.label_categoria = tk.Label(self.root, text="Filtrar por Categoría:", bg="#f0f0f0", font=("Arial", 12))
        self.label_categoria.grid(row=0, column=0, padx=10, pady=50, sticky="w")

        # Combo de categorías
        self.combo_categoria = ttk.Combobox(self.root, width=30)  # Aumenta el width del combo
        self.combo_categoria['values'] = self.obtener_categorias()  # Obtener categorías de la base de datos
        self.combo_categoria.current(0)  # Selecciona la primera categoría por defecto
        self.combo_categoria.grid(row=0, column=1, padx=10, pady=50, sticky="w")
        self.combo_categoria.bind("<<ComboboxSelected>>", self.ver_productos)

        # Barra de búsqueda
        self.search_entry = tk.Entry(self.root, width=40, font=("Arial", 12))  # Aumenta el width para agrandar la barra de búsqueda
        self.search_entry.grid(row=0, column=2, padx=10, pady=10)

        # Botón de búsqueda
        self.search_button = tk.Button(self.root, text="Buscar", command=self.buscar_producto, bg="#87CEEB", fg="white", font=("Arial", 12, "bold"), width=15, height=1)  # Aumenta el width y height
        self.search_button.grid(row=0, column=3, padx=10, pady=10)

        # Frame para los botones 
        frame_botones = tk.Frame(self.root, bg="#f0f0f0")
        frame_botones.grid(row=1, column=0, columnspan=4, pady=20, padx=10)

        # Botones
        self.btn_agregar = tk.Button(frame_botones, text="Agregar Producto", command=self.agregar_producto, bg="#4CAF50", fg="white", font=("Arial", 12, "bold"), height=2, width=20)
        self.btn_agregar.grid(row=0, column=0, padx=10, pady=10)

        self.btn_actualizar = tk.Button(frame_botones, text="Actualizar Producto", command=self.actualizar_producto, bg="#FF9800", fg="white", font=("Arial", 12, "bold"), height=2, width=20)
        self.btn_actualizar.grid(row=0, column=1, padx=10, pady=10)

        self.btn_eliminar = tk.Button(frame_botones, text="Eliminar Producto", command=self.eliminar_producto, bg="#F44336", fg="white", font=("Arial", 12, "bold"), height=2, width=20)
        self.btn_eliminar.grid(row=0, column=2, padx=10, pady=10)

        # Tabla de productos (Treeview)
        self.tree = ttk.Treeview(self.root, columns=("ID", "Nombre", "Descripción", "Precio", "Cantidad", "Categoría"))
        self.tree.heading("#1", text="ID")
        self.tree.heading("#2", text="Nombre")
        self.tree.heading("#3", text="Descripción")
        self.tree.heading("#4", text="Precio")
        self.tree.heading("#5", text="Cantidad")
        self.tree.heading("#6", text="Categoría")

        # Alineación de las columnas
        self.tree.column("#1", anchor="center")
        self.tree.column("#2", anchor="w")
        self.tree.column("#3", anchor="w")
        self.tree.column("#4", anchor="e")
        self.tree.column("#5", anchor="e")
        self.tree.column("#6", anchor="w")

        self.tree.grid(row=2, column=0, columnspan=4, padx=10, pady=20)

        self.ver_productos()  # Inicialmente mostramos todos los productos

    def obtener_categorias(self):
        # Obtener todas las categorías de la base de datos
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT nombre FROM categorias')
        categorias = cursor.fetchall()
        cursor.close()
        conn.close()
        return [categoria[0] for categoria in categorias]

    def ver_productos(self, event=None):
        # Limpiar la tabla
        for row in self.tree.get_children():
            self.tree.delete(row)

        categoria_seleccionada = self.combo_categoria.get()
        categoria_id = self.obtener_id_categoria(categoria_seleccionada)

        productos = obtener_productos_por_categoria(categoria_id)
        for producto in productos:
            self.tree.insert("", "end", values=producto)

    def obtener_id_categoria(self, categoria_nombre):
        # Obtener el ID de la categoría seleccionada
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT id FROM categorias WHERE nombre = %s', (categoria_nombre,))
        categoria_id = cursor.fetchone()[0]
        cursor.close()
        conn.close()
        return categoria_id

    def buscar_producto(self):
        # Buscar producto por nombre
        search_text = self.search_entry.get()
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM productos WHERE nombre LIKE %s", ('%' + search_text + '%',))
        productos = cursor.fetchall()
        cursor.close()
        conn.close()

        for row in self.tree.get_children():
            self.tree.delete(row)
        
        for producto in productos:
            self.tree.insert("", "end", values=producto)

    def agregar_producto(self):
        def agregar():
            nombre = entry_nombre.get()
            descripcion = entry_descripcion.get() if entry_descripcion.get() != "" else "No disponible"  # Asignar valor por defecto si está vacío
            
            # Validación para verificar si el producto ya existe
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM productos WHERE nombre = %s", (nombre,))
            producto_existente = cursor.fetchone()  # Si ya existe un producto con el mismo nombre
            cursor.close()
            conn.close()

            if producto_existente:
                messagebox.showwarning("Advertencia", "Este producto ya existe en el inventario.")
                return
            
            # Validación de precio
            try:
                precio = float(entry_precio.get())
                if precio <= 0:
                    messagebox.showwarning("Advertencia", "El precio debe ser un número positivo.")
                    return
            except ValueError:
                messagebox.showwarning("Advertencia", "El precio debe ser un número válido.")
                return

            # Validación de cantidad
            try:
                cantidad = int(entry_cantidad.get())
                if cantidad < 0:
                    messagebox.showwarning("Advertencia", "La cantidad no puede ser negativa.")
                    return
            except ValueError:
                messagebox.showwarning("Advertencia", "La cantidad debe ser un número entero.")
                return

            # Validación de categoría
            try:
                categoria_id = int(entry_categoria_id.get())
                # Verificar si la categoría existe
                conn = get_db_connection()
                cursor = conn.cursor()
                cursor.execute('SELECT * FROM categorias WHERE id = %s', (categoria_id,))
                categoria_existente = cursor.fetchone()
                cursor.close()
                conn.close()
                if not categoria_existente:
                    messagebox.showwarning("Advertencia", "El ID de categoría no es válido.")
                    return
            except ValueError:
                messagebox.showwarning("Advertencia", "El ID de categoría debe ser un número válido.")
                return

            # Verificar si los campos obligatorios están completos
            if not nombre:  # Nombre no puede estar vacío
                messagebox.showwarning("Advertencia", "El nombre es obligatorio.")
                return

            # Insertar el producto en la base de datos
            agregar_producto(nombre, descripcion, precio, cantidad, categoria_id)
            messagebox.showinfo("Éxito", "Producto agregado correctamente")
            top.destroy()  # Cerrar la ventana emergente
            self.ver_productos()  # Actualizar la tabla de productos

        # Ventana emergente para agregar producto
        top = tk.Toplevel(self.root)
        top.title("Agregar Producto")
        top.geometry("400x400")

        tk.Label(top, text="Nombre").pack()
        entry_nombre = tk.Entry(top)
        entry_nombre.pack()

        tk.Label(top, text="Descripción (Opcional)").pack()  # Descripción es opcional
        entry_descripcion = tk.Entry(top)
        entry_descripcion.pack()

        tk.Label(top, text="Precio").pack()
        entry_precio = tk.Entry(top)
        entry_precio.pack()

        tk.Label(top, text="Cantidad").pack()
        entry_cantidad = tk.Entry(top)
        entry_cantidad.pack()

        tk.Label(top, text="ID de Categoría").pack()
        entry_categoria_id = tk.Entry(top)
        entry_categoria_id.pack()

        tk.Button(top, text="Agregar", command=agregar).pack()

    def actualizar_producto(self):
        selected_item = self.tree.selection()
        if selected_item:
            item_id = self.tree.item(selected_item)["values"][0]
            nombre = self.tree.item(selected_item)["values"][1]
            descripcion = self.tree.item(selected_item)["values"][2]
            precio = self.tree.item(selected_item)["values"][3]
            cantidad = self.tree.item(selected_item)["values"][4]
            categoria_id = self.tree.item(selected_item)["values"][5]

            def actualizar():
                nombre_nuevo = entry_nombre.get()
                descripcion_nueva = entry_descripcion.get() if entry_descripcion.get() != "" else "No disponible"  # Asignar valor por defecto si está vacío

                # Validación para verificar si el producto ya existe (duplicado de nombre)
                conn = get_db_connection()
                cursor = conn.cursor()
                cursor.execute("SELECT * FROM productos WHERE nombre = %s AND id != %s", (nombre_nuevo, item_id))
                producto_existente = cursor.fetchone()  # Verifica si ya existe otro producto con el mismo nombre
                cursor.close()
                conn.close()

                if producto_existente:
                    messagebox.showwarning("Advertencia", "Este producto ya existe en el inventario.")
                    return
                
                # Validación de precio
                try:
                    precio_nuevo = float(entry_precio.get())
                    if precio_nuevo <= 0:
                        messagebox.showwarning("Advertencia", "El precio debe ser un número positivo.")
                        return
                except ValueError:
                    messagebox.showwarning("Advertencia", "El precio debe ser un número válido.")
                    return

                # Validación de cantidad
                try:
                    cantidad_nueva = int(entry_cantidad.get())
                    if cantidad_nueva < 0:
                        messagebox.showwarning("Advertencia", "La cantidad no puede ser negativa.")
                        return
                except ValueError:
                    messagebox.showwarning("Advertencia", "La cantidad debe ser un número entero.")
                    return

                # Validación de categoría
                try:
                    categoria_id_nueva = int(entry_categoria_id.get())
                    # Verificar si la categoría existe
                    conn = get_db_connection()
                    cursor = conn.cursor()
                    cursor.execute('SELECT * FROM categorias WHERE id = %s', (categoria_id_nueva,))
                    categoria_existente = cursor.fetchone()
                    cursor.close()
                    conn.close()
                    if not categoria_existente:
                        messagebox.showwarning("Advertencia", "El ID de categoría no es válido.")
                        return
                except ValueError:
                    messagebox.showwarning("Advertencia", "El ID de categoría debe ser un número válido.")
                    return

                # Verificar si los campos obligatorios están completos
                if not nombre_nuevo:  # Nombre no puede estar vacío
                    messagebox.showwarning("Advertencia", "El nombre es obligatorio.")
                    return

                # Llamar a la función para actualizar el producto en la base de datos
                actualizar_producto(item_id, nombre_nuevo, descripcion_nueva, precio_nuevo, cantidad_nueva, categoria_id_nueva)
                messagebox.showinfo("Éxito", "Producto actualizado correctamente")
                top.destroy()
                self.ver_productos()  # Actualizar la tabla de productos

            top = tk.Toplevel(self.root)
            top.title("Actualizar Producto")
            top.geometry("400x400")

            tk.Label(top, text="Nombre").pack()
            entry_nombre = tk.Entry(top)
            entry_nombre.insert(0, nombre)
            entry_nombre.pack()

            tk.Label(top, text="Descripción").pack()
            entry_descripcion = tk.Entry(top)
            entry_descripcion.insert(0, descripcion)
            entry_descripcion.pack()

            tk.Label(top, text="Precio").pack()
            entry_precio = tk.Entry(top)
            entry_precio.insert(0, precio)
            entry_precio.pack()

            tk.Label(top, text="Cantidad").pack()
            entry_cantidad = tk.Entry(top)
            entry_cantidad.insert(0, cantidad)
            entry_cantidad.pack()

            tk.Label(top, text="ID de Categoría").pack()
            entry_categoria_id = tk.Entry(top)
            entry_categoria_id.insert(0, categoria_id)
            entry_categoria_id.pack()

            tk.Button(top, text="Actualizar", command=actualizar).pack()

    def eliminar_producto(self):
        selected_item = self.tree.selection()
        if selected_item:
            item_id = self.tree.item(selected_item)["values"][0]
            confirmar = messagebox.askyesno("Confirmación", "¿Estás seguro de eliminar este producto?")
            if confirmar:
                eliminar_producto(item_id)  # Llamar a la función para eliminar
                messagebox.showinfo("Éxito", "Producto eliminado correctamente")
                self.ver_productos()  # Actualizar la tabla
        else:
            messagebox.showwarning("Selección inválida", "Por favor selecciona un producto para eliminar.")

# Crear la ventana principal
root = tk.Tk()
app = InventarioApp(root)

# Ejecutar la aplicación
root.mainloop()
