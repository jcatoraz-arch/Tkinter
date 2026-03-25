import tkinter as tk

ventana = tk.Tk()
ventana.title("Calculadora")
ventana.geometry("325x330")

pantalla = tk.Entry(ventana, width=18, font=("Arial", 24))
pantalla.grid(row=0, column=0, columnspan=4)

def agregar_numero(numero):
    actual = pantalla.get()
    pantalla.delete(0, tk.END)
    pantalla.insert(0, actual + str(numero))

def limpiar():
    pantalla.delete(0, tk.END)

def calcular():
    try:
        resultado = eval(pantalla.get())
        pantalla.delete(0, tk.END)
        pantalla.insert(0, resultado)
    except:
        pantalla.delete(0, tk.END)
        pantalla.insert(0, "Error")

def crear_boton(texto, fila, columna, comando):
    tk.Button(ventana, text=texto, font=("Arial",18), width=5, height=2, command=comando).grid(row=fila, column=columna)

crear_boton("1", 1, 0, lambda: agregar_numero(1))
crear_boton("2", 1, 1, lambda: agregar_numero(2))
crear_boton("3", 1, 2, lambda: agregar_numero(3))
crear_boton("4", 2, 0, lambda: agregar_numero(4))
crear_boton("5", 2, 1, lambda: agregar_numero(5))
crear_boton("6", 2, 2, lambda: agregar_numero(6))
crear_boton("7", 3, 0, lambda: agregar_numero(7))
crear_boton("8", 3, 1, lambda: agregar_numero(8))
crear_boton("9", 3, 2, lambda: agregar_numero(9))
crear_boton("0", 4, 1, lambda: agregar_numero(0))

crear_boton("+", 1, 3, lambda: agregar_numero("+"))
crear_boton("-", 2, 3, lambda: agregar_numero("-"))
crear_boton("*", 3, 3, lambda: agregar_numero("*"))
crear_boton("/", 4, 3, lambda: agregar_numero("/"))

crear_boton("C", 4, 0, limpiar)
crear_boton("=", 4, 2, calcular)

ventana.mainloop()