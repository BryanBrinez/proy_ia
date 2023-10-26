import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk, ImageOps
import algoritmo_busqueda
import time

cuadro_width = 400
cuadro_height = 300
celda_width = 0  # Inicialmente establece las variables en 0
celda_height = 0

# Crea una lista para mantener referencias a las imágenes cargadas
imagenes_cargadas = []
#cuadro = None  # Define cuadro como una variable global

def cargar_matriz():
    archivo = filedialog.askopenfilename(filetypes=[("Archivos de Texto", "*.txt")])
    
    if archivo:
        matriz = cargar_matriz_desde_archivo(archivo)
        
        # Elimina todos los widgets dentro del cuadro antes de mostrar la nueva matriz
        for widget in cuadro.winfo_children():
            widget.grid_forget()
        
        # Luego, muestra la matriz en el cuadro
        mostrar_matriz(matriz)
        
        # Llama al algoritmo de búsqueda
        camino, cost = algoritmo_busqueda.buscar_camino(matriz)
        #print("este es el costo final ", costo_total)
        
        if camino:
            # Mueve el personaje paso a paso en el camino
            mover_personaje(camino,cost)
            # Muestra el costo acumulado
            
        else:
            messagebox.showinfo("Mensaje", "No se encontró un camino válido.")

def cargar_matriz_desde_archivo(archivo):
    matriz = []
    with open(archivo, "r") as f:
        for linea in f:
            fila = [int(numero) for numero in linea.strip().split()]
            matriz.append(fila)
    return matriz

def mostrar_matriz(matriz):
    num_filas = len(matriz)
    num_columnas = len(matriz[0])
    
    # Elimina cualquier imagen existente de Coraje en el cuadro
    for widget in cuadro.winfo_children():
        widget.grid_forget()
    
    # Asigna los valores a las variables globales
    global celda_width
    global celda_height
    celda_width = cuadro_width / num_columnas
    celda_height = cuadro_height / num_filas

    for i in range(num_filas):
        for j in range(num_columnas):
            imagen_numero = matriz[i][j]
            imagen = cargar_imagen(imagen_numero, celda_width, celda_height)
            label = tk.Label(cuadro, image=imagen)
            label.image = imagen  # Mantiene una referencia a la imagen
            label.grid(row=i, column=j)
            imagenes_cargadas.append(imagen)  # Agrega la imagen a la lista de referencias

def cargar_imagen(numero, width, height):
    # Debes cargar las imágenes correspondientes según el número
    # Por ejemplo, puedes tener una lista de rutas a las imágenes y seleccionar la adecuada
    if numero == 1:
        imagen = Image.open("images/coraje.png")
    elif numero == 2:
        imagen = Image.open("images/muriel.png")
    elif numero == 3:
        imagen = Image.open("images/gato.png")
    elif numero == 4:
        imagen = Image.open("images/amo_malvado.png")
    elif numero == 0:
        imagen = Image.open("images/espacio_blanco.png")
        imagen = ImageOps.expand(imagen, border=2, fill="black")
    elif numero == 6:
        imagen = Image.open("images/pared.png")
    else:
        imagen = Image.open("images/imagen_default.png")

    # Redimensiona la imagen para que se ajuste al tamaño de la celda
    imagen = imagen.resize((int(width), int(height)))
    
    imagen = ImageTk.PhotoImage(imagen)
    
    return imagen

def mostrar_costo(costo):
    # Actualiza la etiqueta de costo acumulado con el valor proporcionado
    label_costo.config(text=f"Costo Acumulado: {costo}")
    label_costo.place(relx=0.5, y=30, anchor="center")


def estilizar_costo_label():
    # Establecer una fuente personalizada y más grande
    fuente = ("Arial", 14, "bold")

    # Estilo de la etiqueta
    label_costo["font"] = fuente
    label_costo["bg"] = "pink"  # Color de fondo rosa claro
    label_costo["fg"] = "white"  # Color de texto blanco
    label_costo["padx"] = 20  # Relleno horizontal
    label_costo["pady"] = 10  # Relleno vertical
    label_costo["borderwidth"] = 0  # Eliminamos el borde ya que el canvas lo manejará

    # Canvas para el fondo redondeado
    canvas = tk.Canvas(root, bg="pink", bd=0, highlightthickness=0, relief='ridge')
    canvas.place(relx=0.5, y=20, anchor="center")
    # Se asume que el tamaño del canvas es 240x40, pero puedes ajustarlo según tus necesidades
    canvas.create_rectangle(10, 10, 230, 30, fill="pink", outline="pink", width=2, smooth=True)

    # Colocar la etiqueta de costo en el Canvas
    label_costo.pack(pady=20)  # Espacio superior e inferior
    canvas.create_window(120, 20, window=label_costo)



def obtener_imagen_de_color(width, height, color="#FFD700"):  # Usé un color dorado como ejemplo
    """Devuelve una imagen de un color específico del tamaño proporcionado."""
    imagen = Image.new('RGB', (int(width), int(height)), color=color)
    return ImageTk.PhotoImage(imagen)

def resaltar_camino(fila, columna, color="#FFD700"):  # Usé un color dorado como ejemplo
    imagen_color = obtener_imagen_de_color(celda_width, celda_height, color)
    label_color = tk.Label(cuadro, image=imagen_color)
    label_color.image = imagen_color
    label_color.grid(row=fila, column=columna)

def mover_personaje(camino,cost):
    if camino is None:
        messagebox.showinfo("Mensaje", "No se encontró un camino válido.")
        return

    costo_total = 0  # Inicializa el costo acumulado
    costos = list(reversed(cost))

    for i in range(1, len(camino)):
        fila_anterior, columna_anterior = camino[i - 1]
        fila_actual, columna_actual = camino[i]

        

        # Mueve a Coraje en la interfaz gráfica
        imagen_coraje = cargar_imagen(1, celda_width, celda_height)
        label_coraje = tk.Label(cuadro, image=imagen_coraje)
        label_coraje.image = imagen_coraje
        label_coraje.grid(row=fila_actual, column=columna_actual)

        resaltar_camino(fila_anterior, columna_anterior)
        # Borra la imagen anterior de Coraje
        label_anterior = cuadro.grid_slaves(row=fila_anterior, column=columna_anterior)[0]
        label_anterior.grid_forget()

        # Actualiza el costo acumulado en la etiqueta
        costo_total = costos[i]  # Suma el costo del paso actual
        label_costo.config(text=f"Costo Acumulado: {costo_total}")

        

        # Espera un corto tiempo para mostrar el movimiento
        cuadro.update()
        time.sleep(0.5)

        # Actualiza el costo acumulado en la etiqueta
        label_costo.config(text=f"Costo Acumulado: {costo_total}")


root = tk.Tk()
root.title("Matriz de Imágenes")

# Establece un tamaño fijo para la ventana (por ejemplo, 800x400 píxeles)
root.geometry("800x500")

# Cuadro que indica la ubicación de la matriz (centrado)
cuadro_width = 400
cuadro_height = 300
cuadro = tk.Frame(root, width=cuadro_width, height=cuadro_height, bd=1, relief="solid")
cuadro.place(relx=0.5, rely=0.5, anchor="center")

# Etiqueta para mostrar el costo acumulado
label_costo = tk.Label(root, text="Costo Acumulado: N/A", padx=20, pady=10) 
label_costo.place()


cargar_button = tk.Button(root, text="Cargar Matriz desde Archivo", command=cargar_matriz)
cargar_button.pack(side="right", padx=10, pady=10)
estilizar_costo_label()

root.mainloop()
