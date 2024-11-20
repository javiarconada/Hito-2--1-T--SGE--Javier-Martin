

import tkinter as tk
from tkinter import messagebox, ttk, Tk, Toplevel, Label, Button, Entry, END, BOTH, Scrollbar
import mysql.connector
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import random

# Conexión a la base de datos con manejo de excepciones
def conectar_bd():
    try:
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="campusfp",
            database="ENCUESTAS"
        )
        return conn
    except mysql.connector.Error as e:
        messagebox.showerror("Error de conexión", f"No se pudo conectar a la base de datos: {e}")
        return None

# Función para crear registros
def crear_encuesta():
    try:
        # Obtenemos los datos de los campos de entrada
        edad = edad_entry.get()
        sexo = sexo_combobox.get()
        bebidas_semana = bebidas_semana_entry.get()
        cervezas_semana = cervezas_semana_entry.get()
        bebidas_fin_semana = bebidas_fin_semana_entry.get()
        bebidas_destiladas_semana = bebidas_destiladas_semana_entry.get()
        vinos_semana = vinos_semana_entry.get()
        perdidas_control = perdidas_control_entry.get()
        diversion = diversion_combobox.get()
        problemas_digestivos = problemas_digestivos_combobox.get()
        tension_alta = tension_alta_combobox.get()
        dolor_cabeza = dolor_cabeza_combobox.get()

        # Validación de campos obligatorios
        if not edad or not sexo:
            messagebox.showerror("Error", "Los campos Edad y Sexo son obligatorios.")
            return

        # Validación de tipos numéricos
        try:
            edad = int(edad)
            bebidas_semana = int(bebidas_semana) if bebidas_semana else 0
            cervezas_semana = int(cervezas_semana) if cervezas_semana else 0
            bebidas_fin_semana = int(bebidas_fin_semana) if bebidas_fin_semana else 0
            bebidas_destiladas_semana = int(bebidas_destiladas_semana) if bebidas_destiladas_semana else 0
            vinos_semana = int(vinos_semana) if vinos_semana else 0
            perdidas_control = int(perdidas_control) if perdidas_control else 0
        except ValueError:
            messagebox.showerror("Error", "Los campos de edad y cantidades deben ser numéricos.")
            return

        # Conexión a la base de datos
        conn = conectar_bd()
        if not conn:
            return

        cursor = conn.cursor()

        # Insertamos los valores en la tabla ENCUESTA
        query = """
            INSERT INTO ENCUESTA (edad, Sexo, BebidasSemana, CervezasSemana, BebidasFinSemana, BebidasDestiladasSemana, 
            VinosSemana, PerdidasControl, DiversionDependenciaAlcohol, ProblemasDigestivos, TensionAlta, DolorCabeza)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        cursor.execute(query, (edad, sexo, bebidas_semana, cervezas_semana, bebidas_fin_semana, 
                               bebidas_destiladas_semana, vinos_semana, perdidas_control, diversion, 
                               problemas_digestivos, tension_alta, dolor_cabeza))
        conn.commit()

        # Mostramos un mensaje de éxito
        messagebox.showinfo("Éxito", "Encuesta creada correctamente.")
        limpiar_campos()
    except mysql.connector.Error as e:
        messagebox.showerror("Error de base de datos", f"No se pudo completar la operación: {e}")
    finally:
        if conn:
            conn.close()

# Función para limpiar campos
def limpiar_campos():
    edad_entry.delete(0, tk.END)
    sexo_combobox.set('')
    bebidas_semana_entry.delete(0, tk.END)
    cervezas_semana_entry.delete(0, tk.END)
    bebidas_fin_semana_entry.delete(0, tk.END)
    bebidas_destiladas_semana_entry.delete(0, tk.END)
    vinos_semana_entry.delete(0, tk.END)
    perdidas_control_entry.delete(0, tk.END)
    diversion_combobox.set('')
    problemas_digestivos_combobox.set('')
    tension_alta_combobox.set('')
    dolor_cabeza_combobox.set('')

# Función para mostrar encuestas con filtros
def mostrar_encuestas():
    try:
        # Obtener los filtros seleccionados
        edad_filtro = edad_entry.get()
        sexo_filtro = sexo_combobox.get()
        bebidas_semana_filtro = bebidas_semana_entry.get()
        cervezas_semana_filtro = cervezas_semana_entry.get()
        bebidas_fin_semana_filtro = bebidas_fin_semana_entry.get()
        bebidas_destiladas_semana_filtro = bebidas_destiladas_semana_entry.get()
        vinos_semana_filtro = vinos_semana_entry.get()
        perdidas_control_filtro = perdidas_control_entry.get()
        diversion_filtro = diversion_combobox.get()
        problemas_digestivos_filtro = problemas_digestivos_combobox.get()
        tension_alta_filtro = tension_alta_combobox.get()
        dolor_cabeza_filtro = dolor_cabeza_combobox.get()

        conn = conectar_bd()
        if not conn:
            return
        cursor = conn.cursor()

        # Crear la consulta base
        query = "SELECT * FROM ENCUESTA WHERE 1=1"
        params = []

        if edad_filtro.strip():
            query += " AND edad = %s"
            params.append(edad_filtro)
        if sexo_filtro.strip():
            query += " AND Sexo = %s"
            params.append(sexo_filtro)
        if bebidas_semana_filtro.strip():
            query += " AND BebidasSemana = %s"
            params.append(bebidas_semana_filtro)
        if cervezas_semana_filtro.strip():
            query += " AND CervezasSemana = %s"
            params.append(cervezas_semana_filtro)
        if bebidas_fin_semana_filtro.strip():
            query += " AND BebidasFinSemana = %s"
            params.append(bebidas_fin_semana_filtro)
        if bebidas_destiladas_semana_filtro.strip():
            query += " AND BebidasDestiladasSemana = %s"
            params.append(bebidas_destiladas_semana_filtro)
        if vinos_semana_filtro.strip():
            query += " AND VinosSemana = %s"
            params.append(vinos_semana_filtro)
        if perdidas_control_filtro.strip():
            query += " AND PerdidasControl = %s"
            params.append(perdidas_control_filtro)
        if diversion_filtro.strip():
            query += " AND DiversionDependenciaAlcohol = %s"
            params.append(diversion_filtro)
        if problemas_digestivos_filtro.strip():
            query += " AND ProblemasDigestivos = %s"
            params.append(problemas_digestivos_filtro)
        if tension_alta_filtro.strip():
            query += " AND TensionAlta = %s"
            params.append(tension_alta_filtro)
        if dolor_cabeza_filtro.strip():
            query += " AND DolorCabeza = %s"
            params.append(dolor_cabeza_filtro)

        # Ejecutar la consulta
        cursor.execute(query, tuple(params))
        registros = cursor.fetchall()

        # Limpiar la vista anterior
        for item in treeview.get_children():
            treeview.delete(item)

        # Mostrar los registros filtrados
        for row in registros:
            treeview.insert("", "end", values=row)
    except mysql.connector.Error as e:
        messagebox.showerror("Error de base de datos", f"Error al ejecutar la consulta: {e}")
    finally:
        if conn:
            conn.close()



def eliminar_encuesta():
    """Función para eliminar una encuesta por ID."""
    # Crear una nueva ventana para ingresar el ID
    eliminar_ventana = tk.Toplevel(ventana)
    eliminar_ventana.title("Eliminar Encuesta")
    eliminar_ventana.geometry("300x150")

    tk.Label(eliminar_ventana, text="Ingrese el ID de la Encuesta a eliminar:").pack(pady=10)
    id_entry_eliminar = tk.Entry(eliminar_ventana)
    id_entry_eliminar.pack(pady=5)

    def eliminar():
        """Elimina la encuesta con el ID ingresado."""
        id_encuesta = id_entry_eliminar.get()

        # Validar que el ID sea numérico
        if not id_encuesta.isdigit():
            messagebox.showerror("Error", "Debe ingresar un ID numérico válido.")
            return

        # Conexión a la base de datos
        conn = conectar_bd()
        if not conn:
            return

        try:
            cursor = conn.cursor()
            query = "DELETE FROM ENCUESTA WHERE idEncuesta = %s"
            cursor.execute(query, (id_encuesta,))
            conn.commit()

            # Verificar si se eliminó alguna fila
            if cursor.rowcount > 0:
                messagebox.showinfo("Éxito", "Encuesta eliminada correctamente.")
            else:
                messagebox.showerror("Error", "No se encontró ninguna encuesta con ese ID.")
        except mysql.connector.Error as e:
            messagebox.showerror("Error de base de datos", f"No se pudo eliminar la encuesta: {e}")
        finally:
            conn.close()
            eliminar_ventana.destroy()

    # Botón para eliminar la encuesta
    tk.Button(eliminar_ventana, text="Eliminar", command=eliminar).pack(pady=10)

# Función para generar un gráfico dinámico en una nueva ventana
def graficar_datos():
    # Datos ficticios basados en encuestas
    edades = ["18-25", "26-35", "36-45", "46-55", "56+"]
    respuestas = [random.randint(10, 50) for _ in edades]

    # Crear figura
    fig = Figure(figsize=(6, 4), dpi=100)
    ax = fig.add_subplot(111)
    ax.bar(edades, respuestas, color='skyblue')
    ax.set_title("Distribución por Rangos de Edad")
    ax.set_xlabel("Rangos de Edad")
    ax.set_ylabel("Número de Encuestas")

    # Crear una nueva ventana (Toplevel) para mostrar el gráfico
    nueva_ventana = tk.Toplevel(ventana)  # Nueva ventana
    nueva_ventana.title("Gráfico de Encuestas")
    nueva_ventana.geometry("800x600")

    # Mostrar gráfica en la nueva ventana
    canvas = FigureCanvasTkAgg(fig, master=nueva_ventana)
    canvas_widget = canvas.get_tk_widget()
    canvas_widget.pack(fill=tk.BOTH, expand=True)

  
def modificar_encuesta(id_encuesta, edad, sexo, bebidas_semana, cervezas_semana, bebidas_fin_semana,
                        bebidas_destiladas_semana, vinos_semana, perdidas_control, diversion_dependencia_alcohol,
                        problemas_digestivos, tension_alta, dolor_cabeza):
    # Conectar a la base de datos MySQL
    conn = mysql.connector.connect(
        host="localhost",
        user="root",  
        password="campusfp",  
        database="ENCUESTAS"  
    )
    
    cursor = conn.cursor()

    # Consulta para actualizar la encuesta
    query = """
        UPDATE ENCUESTA
        SET 
            edad = %s,
            Sexo = %s,
            BebidasSemana = %s,
            CervezasSemana = %s,
            BebidasFinSemana = %s,
            BebidasDestiladasSemana = %s,
            VinosSemana = %s,
            PerdidasControl = %s,
            DiversionDependenciaAlcohol = %s,
            ProblemasDigestivos = %s,
            TensionAlta = %s,
            DolorCabeza = %s
        WHERE idEncuesta = %s
    """
    
    # Ejecutar la consulta
    cursor.execute(query, (edad, sexo, bebidas_semana, cervezas_semana, bebidas_fin_semana,
                           bebidas_destiladas_semana, vinos_semana, perdidas_control, diversion_dependencia_alcohol,
                           problemas_digestivos, tension_alta, dolor_cabeza, id_encuesta))

    # Confirmar los cambios en la base de datos
    conn.commit()

    # Cerrar la conexión
    cursor.close()
    conn.close()

    print("Encuesta modificada correctamente")

def modificar_encuesta_wrapper():
   
    try:
        # Obtener el ID seleccionado en el TreeView
        id_encuesta = int(treeview.item(treeview.selection()[0])['values'][0])  # Selecciona el ID de la fila

        # Obtener los valores de los campos de entrada
        edad = int(edad_entry.get())
        sexo = sexo_combobox.get()
        bebidas_semana = int(bebidas_semana_entry.get())
        cervezas_semana = int(cervezas_semana_entry.get())
        bebidas_fin_semana = int(bebidas_fin_semana_entry.get())
        bebidas_destiladas_semana = int(bebidas_destiladas_semana_entry.get())
        vinos_semana = int(vinos_semana_entry.get())
        perdidas_control = int(perdidas_control_entry.get())
        diversion_dependencia_alcohol = diversion_combobox.get()
        problemas_digestivos = problemas_digestivos_combobox.get()
        tension_alta = tension_alta_combobox.get()
        dolor_cabeza = dolor_cabeza_combobox.get()

        # Llamar a la función modificar_encuesta con los valores recolectados
        modificar_encuesta(
            id_encuesta, edad, sexo, bebidas_semana, cervezas_semana, bebidas_fin_semana,
            bebidas_destiladas_semana, vinos_semana, perdidas_control, diversion_dependencia_alcohol,
            problemas_digestivos, tension_alta, dolor_cabeza
        )

        # Mostrar un mensaje de éxito
        messagebox.showinfo("Éxito", "Encuesta modificada correctamente.")
    except IndexError:
        messagebox.showerror("Error", "Por favor, selecciona una encuesta del listado para modificar.")
    except ValueError:
        messagebox.showerror("Error", "Por favor, revisa que todos los campos sean válidos.")
    except Exception as e:
        messagebox.showerror("Error", f"Ha ocurrido un error: {e}")
# Refactorización para modularidad en creación de widgets
def crear_label(parent, text, row, column, padx=10, pady=5):
    """Crea un Label en la ventana principal."""
    label = tk.Label(parent, text=text)
    label.grid(row=row, column=column, padx=padx, pady=pady)
    return label

def crear_entry(parent, row, column, padx=10, pady=5):
    """Crea un Entry en la ventana principal."""
    entry = tk.Entry(parent)
    entry.grid(row=row, column=column, padx=padx, pady=pady)
    return entry

def crear_combobox(parent, values, row, column, padx=10, pady=5):
    """Crea un Combobox en la ventana principal."""
    combobox = ttk.Combobox(parent, values=values, state="readonly")
    combobox.grid(row=row, column=column, padx=padx, pady=pady)
    return combobox

columns = ["edad", "sexo", "beb_sem", "cer_sem", "fin_sem", 
           "dest_sem", "vino_sem", "ctrl", "div", "dig", "ten", "dol"]
encabezados = ["Edad", "Sexo", "Beb/sem", "Cer/sem", "Fin/sem",
               "Dest/sem", "Vino/sem", "Ctrl", "Div", "Dig", "Ten", "Dol"]
column_widths = {
    "edad": 50, "sexo": 60, "beb_sem": 70, "cer_sem": 70,
    "fin_sem": 70, "dest_sem": 70, "vino_sem": 70, "ctrl": 50,
    "div": 50, "dig": 50, "ten": 50, "dol": 50
}


# Ventana principal
ventana = tk.Tk()
ventana.title("Sistema de Encuestas")
ventana.geometry("1000x500")

ventana.configure(bg="#f0f8ff")  # Fondo azul claro

# Estilos
style = ttk.Style()
style.theme_use("clam")
style.configure("Treeview", background="#ffffff", foreground="black", fieldbackground="#ffffff")
style.configure("Treeview.Heading", background="#4682b4", foreground="white", font=("Arial", 10, "bold"))
style.map("Treeview", background=[("selected", "#87cefa")])  # Azul claro para selección

# Crear widgets en la ventana principal
edad_label = crear_label(ventana, "Edad", 1, 0)
edad_entry = crear_entry(ventana, 1, 1)
sexo_label = crear_label(ventana, "Sexo", 1, 2)
sexo_combobox = crear_combobox(ventana, ["", "Hombre", "Mujer"], 1, 3)

bebidas_semana_label = crear_label(ventana, "Bebidas por Semana", 2, 0)
bebidas_semana_entry = crear_entry(ventana, 2, 1)
cervezas_semana_label = crear_label(ventana, "Cervezas por Semana", 2, 2)
cervezas_semana_entry = crear_entry(ventana, 2, 3)

bebidas_fin_semana_label = crear_label(ventana, "Bebidas Fin de Semana", 3, 0)
bebidas_fin_semana_entry = crear_entry(ventana, 3, 1)
bebidas_destiladas_semana_label = crear_label(ventana, "Bebidas Destiladas por Semana", 3, 2)
bebidas_destiladas_semana_entry = crear_entry(ventana, 3, 3)

vinos_semana_label = crear_label(ventana, "Vinos por Semana", 4, 0)
vinos_semana_entry = crear_entry(ventana, 4, 1)
perdidas_control_label = crear_label(ventana, "Pérdidas de Control", 4, 2)
perdidas_control_entry = crear_entry(ventana, 4, 3)

diversion_label = crear_label(ventana, "Diversión / Dependencia", 5, 0)
diversion_combobox = crear_combobox(ventana, ["", "Sí", "No"], 5, 1)
problemas_digestivos_label = crear_label(ventana, "Problemas Digestivos", 5, 2)
problemas_digestivos_combobox = crear_combobox(ventana, ["", "Sí", "No"], 5, 3)

tension_alta_label = crear_label(ventana, "Tensión Alta", 6, 0)
tension_alta_combobox = crear_combobox(ventana, ["", "Sí", "No", "No lo sé"], 6, 1)
dolor_cabeza_label = crear_label(ventana, "Dolor de Cabeza", 6, 2)
dolor_cabeza_combobox = crear_combobox(ventana, ["", "Nunca", "Alguna vez", "A menudo", "Muy a menudo"], 6, 3)

# Marco para los botones
botones_frame = tk.Frame(ventana, bg="#f0f8ff")
botones_frame.grid(row=7, column=0, columnspan=4, pady=10)

tk.Button(botones_frame, text="Insertar Encuesta", bg="#4682b4", fg="white", font=("Arial", 10),
          command=crear_encuesta).pack(side="left", padx=5, pady=5)
tk.Button(botones_frame, text="Mostrar Encuestas", bg="#4682b4", fg="white", font=("Arial", 10),
          command=mostrar_encuestas).pack(side="left", padx=5, pady=5)
tk.Button(botones_frame, text="Eliminar Encuesta", bg="#dc143c", fg="white", font=("Arial", 10),
          command=eliminar_encuesta).pack(side="left", padx=5, pady=5)
tk.Button(botones_frame, text="Modificar Encuesta", bg="#4682b4", fg="white", font=("Arial", 10),
          command=modificar_encuesta_wrapper).pack(side="left", padx=5, pady=5)

# Marco para el TreeView y la barra de desplazamiento
frame_treeview = tk.Frame(ventana)
frame_treeview.grid(row=8, column=0, columnspan=4, sticky="nsew", padx=10, pady=10)

scrollbar = Scrollbar(frame_treeview, orient="vertical")
treeview = ttk.Treeview(frame_treeview, columns=columns, show="headings", yscrollcommand=scrollbar.set)
scrollbar.config(command=treeview.yview)

# Posicionar TreeView y Scrollbar
treeview.pack(side="left", fill="both", expand=True)
scrollbar.pack(side="right", fill="y")

# Configuración de encabezados y columnas
for col, encabezado in zip(columns, encabezados):
    treeview.heading(col, text=encabezado)

for col, width in column_widths.items():
    treeview.column(col, width=width)  # Anchos compactos para cada columna


# Botón para gráficos dinámicos
tk.Button(ventana, text="Generar Gráfico", bg="#32cd32", fg="white", font=("Arial", 10),
          command=graficar_datos).grid(row=9, column=0, columnspan=4, pady=10)

# Ajuste del peso para el TreeView
ventana.grid_rowconfigure(8, weight=1)
ventana.grid_columnconfigure(0, weight=1)

ventana.mainloop()
