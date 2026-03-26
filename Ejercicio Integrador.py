import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
import json
import os

ruta_json = "inventario.json"
inventario = []
contador_id = 1

def cargar_datos():
    global inventario, contador_id
    if os.path.exists(ruta_json):
        try:
            with open(ruta_json, 'r') as f:
                datos = json.load(f)
                inventario = datos.get("productos", [])
                contador_id = datos.get("contador_id", 1)
        except:
            inventario = []
            contador_id = 1
    else:
        inventario = []
        contador_id = 1

def guardar_datos():
    with open(ruta_json, 'w') as f:
        json.dump({"productos": inventario, "contador_id": contador_id}, f, indent=4)

def agregar_producto():
    global contador_id
    
    str_id = entry_id.get()
    nombre = entry_nombre.get()
    precio = entry_precio.get()
    stock = entry_stock.get()
    categoria = combo_categoria.get()
    
    if str_id == "" or nombre == "" or precio == "" or stock == "" or categoria == "":
        messagebox.showerror("Error","Completar todos los campos")
        return
    
    try:
        prod_id = int(str_id)
        prod_precio = float(precio)
        prod_stock = int(stock)
    except ValueError:
        messagebox.showerror("Error","ID y Stock deben ser enteros, Precio debe ser número")
        return

    if any(p["id"] == prod_id for p in inventario):
        messagebox.showerror("Error","El ID ya existe")
        return
    
    producto = {
        "id": prod_id,
        "nombre": nombre,
        "precio": prod_precio,
        "stock": prod_stock,
        "categoria": categoria
    }

    inventario.append(producto)
    if prod_id >= contador_id:
        contador_id = prod_id + 1
    
    guardar_datos()
    actualizar_lista()
    limpiar_campos()

def actualizar_lista(filtro=""):
    for item in arbol.get_children():
        arbol.delete(item)
    
    filtro = filtro.strip().lower()

    if filtro:
        productos_mostrar = [p for p in inventario if filtro in str(p["id"]).lower() or filtro in p["nombre"].lower() or filtro in p["categoria"].lower()]
    else:
        productos_mostrar = list(inventario)

    # Construir árbol jerárquico de categorías
    categoria_tree = {}
    for p in productos_mostrar:
        ruta = p["categoria"].strip()
        if not ruta:
            ruta = "Sin categoría"
        parts = [c.strip() for c in ruta.split("/") if c.strip()]
        if not parts:
            parts = ["Sin categoría"]

        node = categoria_tree
        for part in parts:
            node = node.setdefault(part, {})
        node.setdefault("_productos", []).append(p)

    def insertar_nodo(padre, nodo_dict):
        for clave in sorted(k for k in nodo_dict.keys() if k != "_productos"):
            hijo = arbol.insert(padre, tk.END, text=clave, open=True, tags=("categoria",))
            insertar_nodo(hijo, nodo_dict[clave])
            for p in sorted(nodo_dict[clave].get("_productos", []), key=lambda x: x["id"]):
                arbol.insert(hijo, tk.END, text="", tags=("producto",), values=(p["id"], p["nombre"], f"${p["precio"]}", p["stock"]))

    insertar_nodo("", categoria_tree)


def seleccionar_producto(event):
    seleccion = arbol.selection()
    
    if seleccion:
        item_id = seleccion[0]
        valores = arbol.item(item_id, 'values')
        
        if valores:
            prod_id = int(valores[0])
            producto = next((p for p in inventario if p["id"] == prod_id), None)
            
            if producto:
                entry_id.delete(0, tk.END)
                entry_id.insert(0, producto["id"])

                entry_nombre.delete(0, tk.END)
                entry_nombre.insert(0, producto["nombre"])
                
                entry_precio.delete(0, tk.END)
                entry_precio.insert(0, producto["precio"])
                
                entry_stock.delete(0, tk.END)
                entry_stock.insert(0, producto["stock"])
                
                combo_categoria.set(producto["categoria"])

def actualizar_producto():
    seleccion = arbol.selection()
    
    if not seleccion:
        messagebox.showerror("Error","Seleccionar producto")
        return
    
    item_id = seleccion[0]
    valores = arbol.item(item_id, 'values')
    
    if not valores:
        messagebox.showerror("Error","Debe seleccionar un producto, no una categoría")
        return
    
    try:
        prod_id = int(valores[0])
    except (ValueError, TypeError):
        messagebox.showerror("Error","ID de producto inválido")
        return
    indice = next((i for i, p in enumerate(inventario) if p["id"] == prod_id), None)
    
    if indice is None:
        return
    
    try:
        inventario[indice]["nombre"] = entry_nombre.get()
        inventario[indice]["precio"] = float(entry_precio.get())
        inventario[indice]["stock"] = int(entry_stock.get())
        inventario[indice]["categoria"] = combo_categoria.get()
    except ValueError:
        messagebox.showerror("Error","Datos inválidos")
        return
    
    guardar_datos()
    actualizar_lista()
    limpiar_campos()

def eliminar_producto():
    seleccion = arbol.selection()
    
    if not seleccion:
        messagebox.showerror("Error","Seleccionar producto")
        return
    
    item_id = seleccion[0]
    valores = arbol.item(item_id, 'values')
    
    if not valores:
        messagebox.showerror("Error","Debe seleccionar un producto, no una categoría")
        return
    
    try:
        prod_id = int(valores[0])
    except (ValueError, TypeError):
        messagebox.showerror("Error","ID de producto inválido")
        return
    
    inventario[:] = [p for p in inventario if p["id"] != prod_id]
    
    guardar_datos()
    actualizar_lista()
    limpiar_campos()

def limpiar_campos():
    entry_id.delete(0, tk.END)
    entry_nombre.delete(0, tk.END)
    entry_precio.delete(0, tk.END)
    entry_stock.delete(0, tk.END)
    combo_categoria.set("")

cargar_datos()

ventana = tk.Tk()
ventana.title("Sistema de Inventario")
ventana.geometry("900x500")

frame_left = tk.Frame(ventana, bg="lightgray", padx=10, pady=10)
frame_left.pack(side=tk.LEFT, fill=tk.BOTH, expand=False)

tk.Label(frame_left, text="Panel de Opciones", font=("Arial", 12, "bold"), bg="lightgray").pack(pady=10)

tk.Label(frame_left, text="ID", bg="lightgray").pack(anchor="w")
entry_id = tk.Entry(frame_left, width=25)
entry_id.pack(pady=5)

tk.Label(frame_left, text="Nombre", bg="lightgray").pack(anchor="w")
entry_nombre = tk.Entry(frame_left, width=25)
entry_nombre.pack(pady=5)

tk.Label(frame_left, text="Precio", bg="lightgray").pack(anchor="w")
entry_precio = tk.Entry(frame_left, width=25)
entry_precio.pack(pady=5)

tk.Label(frame_left, text="Stock", bg="lightgray").pack(anchor="w")
entry_stock = tk.Entry(frame_left, width=25)
entry_stock.pack(pady=5)

tk.Label(frame_left, text="Categoría (ej: Comida/Postre/Helados)", bg="lightgray").pack(anchor="w")
combo_categoria = ttk.Combobox(frame_left, width=22, values=["Comida", "Comida/Postre", "Comida/Verduras", "Comida/Frutas", "Bebida", "Otros"])
combo_categoria.pack(pady=5)

tk.Button(frame_left, text="Agregar", command=agregar_producto, bg="green", fg="white", width=25).pack(pady=5)
tk.Button(frame_left, text="Modificar", command=actualizar_producto, bg="blue", fg="white", width=25).pack(pady=5)
tk.Button(frame_left, text="Eliminar", command=eliminar_producto, bg="red", fg="white", width=25).pack(pady=5)
tk.Button(frame_left, text="Guardar", command=guardar_datos, bg="purple", fg="white", width=25).pack(pady=5)
tk.Button(frame_left, text="Limpiar", command=limpiar_campos, bg="orange", fg="white", width=25).pack(pady=5)

frame_right = tk.Frame(ventana, padx=10, pady=10)
frame_right.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

tk.Label(frame_right, text="Productos Guardados", font=("Arial", 12, "bold")).pack(pady=10)

frame_buscar = tk.Frame(frame_right)
frame_buscar.pack(fill=tk.X, pady=5)

tk.Label(frame_buscar, text="Buscar:").pack(side=tk.LEFT)
entry_buscar = tk.Entry(frame_buscar)
entry_buscar.pack(side=tk.LEFT, padx=5, fill=tk.X, expand=True)

def buscar_producto():
    termino = entry_buscar.get().strip()
    actualizar_lista(termino)

def mostrar_todos():
    entry_buscar.delete(0, tk.END)
    actualizar_lista()

btn_buscar = tk.Button(frame_buscar, text="Buscar", command=buscar_producto, bg="lightblue")
btn_buscar.pack(side=tk.LEFT, padx=(0,5))

btn_mostrar = tk.Button(frame_buscar, text="Ver Todos", command=mostrar_todos, bg="lightgreen")
btn_mostrar.pack(side=tk.LEFT)

frame_arbol = tk.Frame(frame_right)
frame_arbol.pack(fill=tk.BOTH, expand=True)

arbol = ttk.Treeview(frame_arbol, height=20, columns=("ID","Nombre","Precio","Stock"), show="tree headings")
arbol.pack(side=tk.LEFT, pady=10, fill=tk.BOTH, expand=True)

scrollbar = ttk.Scrollbar(frame_arbol, orient=tk.VERTICAL, command=arbol.yview)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

arbol.configure(yscrollcommand=scrollbar.set)

arbol.column('#0', width=220)
arbol.heading('#0', text='Categoría / Producto')

arbol.column('ID', width=70, anchor='center')
arbol.heading('ID', text='ID')

arbol.column('Nombre', width=180, anchor='w')
arbol.heading('Nombre', text='Nombre')

arbol.column('Precio', width=80, anchor='e')
arbol.heading('Precio', text='Precio')

arbol.column('Stock', width=80, anchor='center')
arbol.heading('Stock', text='Stock')

arbol.tag_configure("categoria", font=("Arial", 10, "bold"), foreground="blue")
arbol.tag_configure("producto", font=("Arial", 9), foreground="black")

arbol.bind("<<TreeviewSelect>>", seleccionar_producto)

actualizar_lista()

ventana.mainloop()