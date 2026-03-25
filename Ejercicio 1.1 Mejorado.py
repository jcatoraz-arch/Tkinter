import tkinter as tk

ventana = tk.Tk()
ventana.title("Calculadora")
ventana.geometry("325x330")

pantalla = tk.Entry(ventana, width=18, font=("Arial", 24))
pantalla.grid(row=0, column=0, columnspan=4)

def agregar_numero(valor):
    actual = pantalla.get()
    pantalla.delete(0, tk.END)
    pantalla.insert(0, actual + str(valor))

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

numeros = [
    [1,2,3],
    [4,5,6],
    [7,8,9]
]

for fila in range(3):
    for columna in range(3):
        numero = numeros[fila][columna]
        crear_boton(str(numero), fila + 1, columna, lambda n=numero: agregar_numero(n))

botones = [
    ("0",4,1, lambda: agregar_numero(0)),
    ("+",1,3, lambda: agregar_numero("+")),
    ("-",2,3, lambda: agregar_numero("-")),
    ("*",3,3, lambda: agregar_numero("*")),
    ("/",4,3, lambda: agregar_numero("/")),
    ("C",4,0, limpiar),
    ("=",4,2, calcular)
]

for texto, fila, columna, comando in botones:
    crear_boton(texto, fila, columna, comando)

ventana.mainloop()