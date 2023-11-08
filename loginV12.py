# Modulo que se usa para interactuar con el sistema operativo y el sistema de archivos.
import os
# Modulo que se usa para manejar JSON data. JSON (JavaScript Object Notation).
import json
# Modulo que se usan al salir del programa.
import atexit
# Modulo que se usa para manejar el tiempo.
import time

# Matriz para almacenar usuarios.
matriz_user = [[" ", " ", " ", " ", " ", " ", " ", " ", " ", " "],
               [" ", " ", " ", " ", " ", " ", " ", " ", " ", " "],
               [" ", " ", " ", " ", " ", " ", " ", " ", " ", " "],
               [" ", " ", " ", " ", " ", " ", " ", " ", " ", " "],
               [" ", " ", " ", " ", " ", " ", " ", " ", " ", " "],
               [" ", " ", " ", " ", " ", " ", " ", " ", " ", " "],
               [" ", " ", " ", " ", " ", " ", " ", " ", " ", " "],
               [" ", " ", " ", " ", " ", " ", " ", " ", " ", " "],
               [" ", " ", " ", " ", " ", " ", " ", " ", " ", " "],
               [" ", " ", " ", " ", " ", " ", " ", " ", " ", " "]]

# Matriz para almacenar contraseñas.
matriz_pass = [[" ", " ", " ", " ", " ", " ", " ", " "],
               [" ", " ", " ", " ", " ", " ", " ", " "],
               [" ", " ", " ", " ", " ", " ", " ", " "],
               [" ", " ", " ", " ", " ", " ", " ", " "],
               [" ", " ", " ", " ", " ", " ", " ", " "],
               [" ", " ", " ", " ", " ", " ", " ", " "],
               [" ", " ", " ", " ", " ", " ", " ", " "],
               [" ", " ", " ", " ", " ", " ", " ", " "],
               [" ", " ", " ", " ", " ", " ", " ", " "],
               [" ", " ", " ", " ", " ", " ", " ", " "]]

# Nuevas listas para almacenar respuestas de seguridad
respuestas_Ciudad = [[] for _ in range(10)]
respuestas_numero = [[] for _ in range(10)]

# Índice del último usuario registrado
ultimo_indice = -1

# Carpeta donde se almacenan los datos
carpeta_datos = "DATOS"

# Función para limpiar pantalla
def limpiar_pantalla():
    if os.name == "posix":
        # Para sistemas tipo Unix (Linux, macOS)
        os.system("clear")
    else:
        # Para sistemas tipo Windows
        os.system("cls")

# Función para cargar datos desde archivos JSON
def cargar_datos():
    # Declarar las variables que va a usar la funcion como globales para poder modificarlas y usarlas.
    global matriz_user, matriz_pass, respuestas_numero, respuestas_Ciudad, ultimo_indice

    # Trata de abrir los archivos JSON, si no los encuentra crea una matriz vacía.
    try:
        with open(os.path.join(carpeta_datos, "matriz_user.json"), "r") as f:
            matriz_user = json.load(f)
    # Si no se encuentra el archivo, se crea una matriz vacía.
    except FileNotFoundError:
        # Matriz vacía si no se encuentra el archivo
        matriz_user = [[" "] * 10 for _ in range(10)]

    try:
        with open(os.path.join(carpeta_datos, "matriz_pass.json"), "r") as f:
            matriz_pass = json.load(f)
    except FileNotFoundError:
        matriz_pass = [[" "] * 8 for _ in range(10)]  

    try:
        with open(os.path.join(carpeta_datos, "respuestas_numero.json"), "r") as f:
            respuestas_numero = json.load(f)
    except FileNotFoundError:
        respuestas_numero = [[] for _ in range(10)]

    try:
        with open(os.path.join(carpeta_datos, "respuestas_Ciudad.json"), "r") as f:
            respuestas_Ciudad = json.load(f)
    except FileNotFoundError:
        respuestas_Ciudad = [[] for _ in range(10)]

    # Obtener el índice del último usuario registrado
    ultimo_indice = -1
    for i, row in enumerate(matriz_user):
        if "".join(row).strip() != "":
            ultimo_indice = i

    guardar_datos()

# Función para guardar datos en archivos JSON
def guardar_datos():
    # Crea la carpeta si no existe
    os.makedirs(carpeta_datos, exist_ok=True)
    with open(os.path.join(carpeta_datos, "matriz_user.json"), "w") as f:
        json.dump(matriz_user, f)

    with open(os.path.join(carpeta_datos, "matriz_pass.json"), "w") as f:
        json.dump(matriz_pass, f)

    with open(os.path.join(carpeta_datos, "respuestas_numero.json"), "w") as f:
        json.dump(respuestas_numero, f)

    with open(os.path.join(carpeta_datos, "respuestas_Ciudad.json"), "w") as f:
        json.dump(respuestas_Ciudad, f)

# Función para registrar usuario
def registrar():
    global ultimo_indice

    # Verificar si se ha alcanzado el límite de usuarios
    if ultimo_indice == 9:
        print("La matriz está llena. No se pueden registrar más usuarios.")
        time.sleep(1)
        return

    # Solicitar nombre de usuario
    usuario = input("Ingrese su usuario (máximo 10 caracteres): ")

    # Verificar si el usuario ya existe
    if usuario in ["".join(matriz_user[i]).strip() for i in range(ultimo_indice + 1)]:
        print("El usuario ya existe. Intente con un nombre de usuario diferente.")
        time.sleep(1)
        return
    if len(usuario) > 10:
        print("Usuario muy largo\n")
        time.sleep(1)
        return

    # Solicitar contraseña
    contraseña = input("Ingrese su contraseña (obligatoriamente 8 caracteres, una mayúscula, un símbolo y al menos un número): ")

    # Verificar si la contraseña cumple con los requisitos
    if len(contraseña) != 8 or not any(c.isupper() for c in contraseña) or not any(c in "!@#$%^&*()-_+=[]}{|;:'<>,.?/" for c in contraseña) or not any(c.isdigit() for c in contraseña):
        print("La contraseña debe tener 8 caracteres exactos, incluyendo al menos 1 mayúscula, 1 símbolo y 1 número")
        time.sleep(2)
        return

    # Incrementar el índice del último usuario registrado
    ultimo_indice += 1  

    # Almacenar nombre de usuario y contraseña en las matrices correspondientes
    for j, caracter in enumerate(usuario):
        matriz_user[ultimo_indice][j] = caracter

    for j, caracter in enumerate(contraseña):
        matriz_pass[ultimo_indice][j] = caracter

    print("Preguntas de seguridad")
    respuesta_numero = input("¿Cuál es tu número favorito?: ")
    if not respuesta_numero.isdigit():
        print("La respuesta debe ser un número")
        time.sleep(1)
        # Revertir el incremento del índice
        ultimo_indice -= 1
        return
    respuesta_hogar = input("¿Dónde naciste?: ")
    if not respuesta_hogar.isalpha():
        print("La respuesta debe ser una palabra")
        time.sleep(1)
        # Revertir el incremento del índice
        ultimo_indice -= 1
        return

    # Almacenar respuestas de seguridad
    respuestas_numero[ultimo_indice].append(respuesta_numero)
    respuestas_Ciudad[ultimo_indice].append(respuesta_hogar)
    guardar_datos()

# Función para iniciar sesión
def login():
    usuario = input("Ingrese su usuario: ")
    contraseña = input("Ingrese su contraseña: ")

    # Itera sobre las dos listas para checar si el usuario y contraseña coinciden.
    for i in range(ultimo_indice + 1):
        if "".join(matriz_user[i]).strip() == usuario and "".join(matriz_pass[i]).strip() == contraseña:
            print("Inicio de sesión exitoso")
            time.sleep(2)
            submenu()
            return  # Salir de la función si el inicio de sesión es exitoso
    print("Usuario o contraseña incorrectos")
    time.sleep(2)


# Función para el submenu dentro de iniciar sesión
def submenu():
    limpiar_pantalla()
    while True:
        limpiar_pantalla()
        print(".:Bienvenido al sistema de registro de usuarios:.")
        print("1. Ver datos")
        print("2. Cambiar contraseña")
        print("3. Eliminar usuario")
        print("4. Ver ordenamientos")
        print("5. Ver Arboles")
        print("6. Cerrar sesión")

        opcion = input("Ingrese una opción: ")
        if opcion == "1":
            limpiar_pantalla()
            verdatos()

        elif opcion == "2":
            limpiar_pantalla()
            cambiarcontraseña()

        elif opcion == "3":
            limpiar_pantalla()
            eliminarusuario()

        elif opcion == "4":
            limpiar_pantalla()
            ordenamientos()

        elif opcion == "5":
            limpiar_pantalla()
            arboles()
            
        elif opcion == "6":
            return
        else:
            print("Opción inválida")

# Función para ver datos
def verdatos():
    print(".:MATRIZ USUARIO:.")
    for i in range(ultimo_indice + 1):  
        for j in range(10):
            if matriz_user[i][j] != " ":
                print(f"[{matriz_user[i][j]}]", end=" ")
            else:
                print("[ ]", end=" ")
        print()

    print("\n.:MATRIZ CONTRASEÑA:.")
    for i in range(ultimo_indice + 1):
        for j in range(8):
            if matriz_pass[i][j] != " ":
                print(f"[{matriz_pass[i][j]}]", end=" ")
            else:
                print("[ ]", end=" ")
        print()

    print("\nLista de respuestas para número favorito")
    for i in range(ultimo_indice + 1):
        if respuestas_numero[i]:
            print(f"Usuario {i+1}: {respuestas_numero[i]}")
        else:
            print(f"Usuario {i+1}: []")

    print("\nLista de respuestas para lugar de nacimiento")
    for i in range(ultimo_indice + 1):
        if respuestas_Ciudad[i]:
            print(f"Usuario {i+1}: {respuestas_Ciudad[i]}")
        else:
            print(f"Usuario {i+1}: []")
    input("Presione enter para continuar...")
    limpiar_pantalla()

# Función para cambiar contraseña
def cambiarcontraseña():
    global ultimo_indice

    usuario = input("Ingrese su usuario: ")
    
    # Buscar el usuario en la matriz de usuarios
    indice_usuario = None
    for i in range(ultimo_indice + 1):
        if "".join(matriz_user[i]).strip() == usuario:
            indice_usuario = i
            break

    if indice_usuario is not None:
        respuesta_numero = input("Ingrese su número favorito: ")
        respuesta_hogar = input("Ingrese su lugar de nacimiento: ")

        # Verificar si las respuestas coinciden con las almacenadas
        if (
            respuestas_numero[indice_usuario] == [respuesta_numero]
            and respuestas_Ciudad[indice_usuario] == [respuesta_hogar]
        ):
            nueva_contraseña = input("Ingrese su nueva contraseña: ")

            # Verificar la nueva contraseña
            if (
                len(nueva_contraseña) == 8
                and any(c.isupper() for c in nueva_contraseña)
                and any(c in "!@#$%^&*()-_+=[]}{|;:'<>,.?/" for c in nueva_contraseña)
                and any(c.isdigit() for c in nueva_contraseña)
            ):
                matriz_pass[indice_usuario] = list(nueva_contraseña)
                print("Contraseña cambiada con éxito.")
                guardar_datos()
            else:
                print("La nueva contraseña no cumple con los requisitos.")
                time.sleep(1)
                return
                
        else:
            print("Las respuestas de seguridad no coinciden.")
            time.sleep(1)
            return
    else:
        limpiar_pantalla()
        print("Usuario no encontrado.")
        time.sleep(1)
        return
        

# Función para eliminar usuario
def eliminarusuario():
    global ultimo_indice, matriz_user, matriz_pass, respuestas_numero, respuestas_hogar

    usuario_input = input("Ingrese su usuario: ")

    indice_usuario = None
    for i, user in enumerate(matriz_user):  
        if "".join(user).strip() == usuario_input:
            indice_usuario = i
            break

    if indice_usuario is not None:
        respuesta_numero = input("Ingrese su número favorito: ")
        respuesta_Ciudad = input("Ingrese su lugar de nacimiento: ")

        print(f"User's number: {respuesta_numero}")
        print(f"Stored number: {''.join(respuestas_numero[indice_usuario])}")
        print(f"User's city: {respuesta_Ciudad}")
        print(f"Stored city: {''.join(respuestas_Ciudad[indice_usuario])}")

        if (
            ''.join(respuestas_numero[indice_usuario]) == respuesta_numero
            and ''.join(respuestas_Ciudad[indice_usuario]) == respuesta_Ciudad
        ):
            matriz_user.pop(indice_usuario)
            matriz_pass.pop(indice_usuario)
            respuestas_numero.pop(indice_usuario)
            respuestas_Ciudad.pop(indice_usuario)
            ultimo_indice -= 1
            print("Usuario eliminado con éxito")
            guardar_datos()
        else:
            print("Las respuestas de seguridad no coinciden.")
            time.sleep(1)
            return
    else:
        print("Usuario no encontrado.")
        time.sleep(1)
        return


# Función para realizar ordenamientos
def burbuja():
    # Obtiene el input del usuario
    input_str = input('Digite una lista de numeros separados con una " , ": ')
    try:
        # Convierte el input del usuario en una lista de flotantes
        numeros = [float(num_str) for num_str in input_str.split(",")]
    except ValueError:
        print("Error: Por favor, ingrese solo números separados por comas.")
        time.sleep(1)
        limpiar_pantalla()
        burbuja()

    # Contadores de iteraciones, movimientos y consultas
    iteraciones = 0
    movimientos = 0
    consultas = 0

    # Burbuja
    # El ciclo for se repite tantas veces como elementos tenga la lista en caso de que se tenga que mover un elemento de un extremo al otro
    for i in range(len(numeros)):
        # El ciclo for se repite tantas veces como elementos tenga la lista menos 1, ya que se compara un elemento con el siguiente
        for j in range(len(numeros) - 1):
            # Aumenta el contador de consultas
            consultas += 1
            # Compara si el elemento actual es mayor al siguiente
            if numeros[j] > numeros[j + 1]:
                # Cambia los valores de [j] y los numeros[j + 1]
                numeros[j], numeros[j + 1] = numeros[j + 1], numeros[j]
                # Aumenta el contador de movimientos
                movimientos += 1
                # Aumenta el contador de iteraciones
        iteraciones += 1

    print("Lista ordenada: ", numeros)
    print("Iteraciones: ", iteraciones)
    print("Movimientos: ", movimientos)
    print("Consultas: ", consultas)
    input("Prescione enter para continuar...")
    limpiar_pantalla()
    ordenamientos()

# Función para ordenamiento burbuja mejorada

def burbuja_mejorada():
    # Obtiene el input del usuario
    input_str = input('Digite una lista de numeros separados con una " , ": ')
    try:
        # Convierte el input del usuario en una lista de flotantes
        numeros = [float(num_str) for num_str in input_str.split(",")]
    except ValueError:
        print("Error. Por favor digite solo numeros separados por comas.")
        time.sleep(1)
        limpiar_pantalla()
        burbuja_mejorada()
        
    # contador de iteraciones, movimientos y consultas
    iteraciones = 0
    movimientos = 0
    consultas = 0

    # Optimized Bubble sort
    # El ciclo for se repite tantas veces como elementos tenga la lista en caso de que se tenga que mover un elemento de un extremo al otro
    for i in range(len(numeros)):
        # La bandera swapped se inicializa en False al principio de cada iteración, se usa para verificar si se hizo un cambio en la iteración
        swapped = False
        # Este ciclo compara los elementos adjacentes, El -1 -i es para que no se compare el último elemento ya que no tiene un elemento adjacent, y el -i es para que no se compare con los elementos que ya están ordenados
        for j in range(len(numeros) - 1 - i):
            # Aumenta el contador de consultas
            consultas += 1
            # Compara si el elemento actual es mayor al siguiente
            if numeros[j] > numeros[j + 1]:
                # Cambia numeros[j] y numeros[j + 1]
                numeros[j], numeros[j + 1] = numeros[j + 1], numeros[j]
                movimientos += 1
                # Cambia la bandera a True para indicar que se hizo un cambio
                swapped = True
        iteraciones += 1
        # Si no se hizo ningún cambio en la iteración, significa que la lista ya está ordenada y se puede salir del ciclo
        if not swapped:
            break

    print("Lista ordenada: ", numeros)
    print("Iteraciones: ", iteraciones)
    print("Movimientos: ", movimientos)
    print("Consultas: ", consultas)
    input("Prescione enter para continuar...")
    limpiar_pantalla()
    ordenamientos()

# Función para ordenamiento por inserción
def insertSort():
    # Get the input from the user
    input_str = input('Digite una lista de numeros separados con una " , ": ')
    try:
        # Convert the user's input into a list of floats
        numeros = [float(num_str) for num_str in input_str.split(",")]
    except ValueError:
        print("Error. Por favor digite solo numeros separados por comas.")
        time.sleep(1)
        limpiar_pantalla()
        insertSort()

    # Counters for iteraciones, movimientos, and consultas
    iteraciones = 0
    movimientos = 0
    consultas = 0

    # Insertion Sort
    # Este ciclo for pasa por todos los elementos de la lista empezando desde el segundo elemento (index 1)
    for i in range(1, len(numeros)):
        # El elemento actual es el key
        key = numeros[i]
        # El index del elemento previo se almacena en j
        j = i - 1
        # Aumenta el contador de consultas
        consultas += 1
        # Si la key es menor que el elemento de j y/o es negativo se detiene
        while j >= 0 and key < numeros[j]:
            # El elemento de j se mueve al siguiente index
            numeros[j + 1] = numeros[j]
            # Aumenta el contador de movimientos
            movimientos += 1
            # El index de j se decrementa
            j -= 1
        # El key se inserta en el index de j + 1
        numeros[j + 1] = key
        # Aumenta el contador de iteraciones
        iteraciones += 1

    print("Lista ordenada: ", numeros)
    print("Iteraciones: ", iteraciones)
    print("Movimientos", movimientos)
    print("Consultas: ", consultas)
    input("Prescione enter para continuar...") 
    limpiar_pantalla()
    ordenamientos()

# Función para ordenamiento por quick sort
def partition(arr, low, high, movimientos, consultas):
    i = (low-1) 
    pivot = arr[high]  # pivot

    for j in range(low, high):
        consultas += 1
        if arr[j] <= pivot:
            i = i+1
            arr[i], arr[j] = arr[j], arr[i]
            movimientos += 1

    arr[i+1], arr[high] = arr[high], arr[i+1]
    movimientos += 1
    return (i+1, movimientos, consultas)

def quick_sort(arr, low, high, iteraciones, movimientos, consultas):
    if len(arr) == 1:
        return arr
    if low < high:
        pi, movimientos, consultas = partition(arr, low, high, movimientos, consultas)
        iteraciones += 1
        quick_sort(arr, low, pi-1, iteraciones, movimientos, consultas)
        quick_sort(arr, pi+1, high, iteraciones, movimientos, consultas)
    return (arr, iteraciones, movimientos, consultas)


def quick_sort_user_input():
    # Input del usuario.
    input_str = input('Digite una lista de numeros separados con una " , ": ')
    try:
        # Convierte el input del usuario en una lista de flotantes.
        numeros = [float(num_str) for num_str in input_str.split(",")]
    except ValueError:
        print("Error. Por favor digite solo numeros separados por comas.")
        time.sleep(1)
        limpiar_pantalla()
        quick_sort_user_input()

    # Contadores de iteraciones, movimientos y consultas
    iteraciones = 0
    movimientos = 0
    consultas = 0

    # Quick Sort
    numeros, iteraciones, movimientos, consultas = quick_sort(numeros, 0, len(numeros)-1, iteraciones, movimientos, consultas)

    print("Lista ordenada: ", numeros)
    print("Iteraciones: ", iteraciones)
    print("Movimientos", movimientos)
    print("Consultas: ", consultas)
    input("Prescione enter para continuar...")
    limpiar_pantalla()
    ordenamientos()

# Función para ordenamiento por merge sort

def merge_sort(arr, iteraciones, movimientos, consultas):
    if len(arr) > 1:
        mid = len(arr) // 2
        L = arr[:mid]
        R = arr[mid:]

        iteraciones, movimientos, consultas = merge_sort(L, iteraciones, movimientos, consultas)
        iteraciones, movimientos, consultas = merge_sort(R, iteraciones, movimientos, consultas)

        i = j = k = 0

        while i < len(L) and j < len(R):
            consultas += 1
            if L[i] < R[j]:
                arr[k] = L[i]
                i += 1
            else:
                arr[k] = R[j]
                j += 1
            k += 1
            movimientos += 1

        while i < len(L):
            arr[k] = L[i]
            i += 1
            k += 1
            movimientos += 1

        while j < len(R):
            arr[k] = R[j]
            j += 1
            k += 1
            movimientos += 1

        iteraciones += 1

    return iteraciones, movimientos, consultas


def merge_sort_user_input():
    # Get the input from the user
    input_str = input('Digite una lista de numeros separados con una " , ": ')
    try:
        # Convert the user's input into a list of floats
        numeros = [float(num_str) for num_str in input_str.split(",")]
    except ValueError:
        print("Error. Por favor digite solo numeros separados por comas.")
        time.sleep(1)
        limpiar_pantalla()
        merge_sort_user_input()

    # Contadores de iteraciones, movimientos y consultas
    iteraciones = 0
    movimientos = 0
    consultas = 0

    # Merge Sort
    iteraciones, movimientos, consultas = merge_sort(numeros, iteraciones, movimientos, consultas)

    print("Lista ordenada: ", numeros)
    print("Iteraciones: ", iteraciones)
    print("Movimientos", movimientos)
    print("Consultas: ", consultas)
    input("Prescione enter para continuar...")
    limpiar_pantalla()
    ordenamientos()

# Menu de ordenamientos.
def ordenamientos():
    print("Elige uno de los siguientes ordenamientos")
    print("1. Burbuja")
    print("2. Burbuja mejorada")
    print("3. Insert sort")
    print("4. Quick sort")
    print("5. Merge sort")
    print("6. Salir")

    opcion = input("Ingrese una opción: ")

    if opcion == "1":
        limpiar_pantalla()
        burbuja()
        
    elif opcion == "2":
        limpiar_pantalla()
        burbuja_mejorada()
    
    elif opcion == "3":
        limpiar_pantalla()
        insertSort()

    elif opcion =="4":
        limpiar_pantalla()
        quick_sort_user_input()

    elif opcion =="5":
        limpiar_pantalla()
        merge_sort_user_input()
    
    elif opcion == "6":
        limpiar_pantalla()
        submenu()
    
    else:
        print("Opción inválida")
        time.sleep(1)
        ordenamientos()

# Arbol binario.
class Node:
    # Constructor de la clase Node, el constructor es un metodo que se llama cuando un objeto es creado desde la clase
    #  toma los argumentos de data y los asigna a la variable self.data que self es un argumento implicito que se pasa a los metodos y funciones.
    def __init__(self, data):
        # Inicializa los atributos de la clase Node que son left, right y data, los inizialisa en None y data en el argumento data.
        # self.left y self.right son punteros a otros nodos, tambien al declararlos en None se esta diciendo que no apuntan a nada al crearse.
        self.left = None
        self.right = None
        self.data = data

    # Metodo para insertar un nuevo nodo con el valor data.
    def insert(self, data):
        # Checa si el nodo actual tiene un valor asignado, si no, se le asigna el valor data.
        if self.data:
            if data < self.data:
                if self.left is None:
                    self.left = Node(data)
                else:
                    self.left.insert(data)
            elif data > self.data:
                if self.right is None:
                    self.right = Node(data)
                else:
                    self.right.insert(data)
        else:
            self.data = data

    def print_tree(self):
        if self.left:
            self.left.print_tree()
        print(self.data),
        if self.right:
            self.right.print_tree()

# Arbol binario
def arbol_binario():
    # Get the input from the user
    input_str = input('Enter a list of numbers separated by commas: ')
    try:
        # Convert the user's input into a list of integers
        numbers = [int(num_str) for num_str in input_str.split(",")]
    except ValueError:
        print("Error. Por favor digite solo numeros separados por comas.")
        time.sleep(1)
        limpiar_pantalla()
        arbol_binario()
        

    # Create a root node
    root = Node(numbers[0])

    # Insert the rest of the numbers into the tree
    for num in numbers[1:]:
        root.insert(num)

    # Print the tree
    root.print_tree()
    input("Prescione enter para continuar...")
    limpiar_pantalla()
    arboles()

# Arbol AVL.
class Node2:
    def __init__(self, key):
        self.key = key
        self.left = None
        self.right = None
        self.height = 1

class AVLTree:
    def insert(self, root, key):
        if not root:
            return Node2(key)
        elif key < root.key:
            root.left = self.insert(root.left, key)
        else:
            root.right = self.insert(root.right, key)

        root.height = 1 + max(self.getHeight(root.left), self.getHeight(root.right))

        balance = self.getBalance(root)

        if balance > 1:
            if key < root.left.key:
                return self.rightRotate(root)
            else:
                root.left = self.leftRotate(root.left)
                return self.rightRotate(root)

        if balance < -1:
            if key > root.right.key:
                return self.leftRotate(root)
            else:
                root.right = self.rightRotate(root.right)
                return self.leftRotate(root)

        return root

    def leftRotate(self, z):
        y = z.right
        T2 = y.left
        y.left = z
        z.right = T2
        z.height = 1 + max(self.getHeight(z.left), self.getHeight(z.right))
        y.height = 1 + max(self.getHeight(y.left), self.getHeight(y.right))
        return y

    def rightRotate(self, y):
        x = y.left
        T3 = x.right
        x.right = y
        y.left = T3
        y.height = 1 + max(self.getHeight(y.left), self.getHeight(y.right))
        x.height = 1 + max(self.getHeight(x.left), self.getHeight(x.right))
        return x

    def getHeight(self, root):
        if not root:
            return 0
        return root.height

    def getBalance(self, root):
        if not root:
            return 0
        return self.getHeight(root.left) - self.getHeight(root.right)

    def preOrder(self, root):
        if not root:
            return
        print("{0} ".format(root.key), end="")
        self.preOrder(root.left)
        self.preOrder(root.right)

def arbol_avl():
    input_str = input('Digite una lista de numeros separados con una " , ": ')
    try:
        numeros = [int(num_str) for num_str in input_str.split(",")]
    except ValueError:
        print("Error. Por favor digite solo numeros separados por comas.")
        time.sleep(1)
        limpiar_pantalla()
        arbol_avl()

    tree = AVLTree()
    root = None
    for num in numeros:
        root = tree.insert(root, num)

    print("El recorrido previo al pedido del árbol AVL construido es: ")
    tree.preOrder(root)
    print()
    input("Prescione enter para continuar...")
    limpiar_pantalla()
    arboles()

# Menu de arboles.
def arboles():
    print("Elige uno de los siguientes arboles")
    print("1. Arbol binario")
    print("2. Arbol AVL")
    print("3. Salir")

    opcion = input("Ingrese una opción: ")

    if opcion == "1":
        limpiar_pantalla()
        arbol_binario()
        

    elif opcion == "2":
        limpiar_pantalla()
        arbol_avl()
    
    elif opcion == "3":
        print("¡Hasta luego!")
        time.sleep(1)
        exit()
    
    else:
        print("Opción inválida")
        time.sleep(1)
        return

# Menu principal
def main():
    cargar_datos()
    atexit.register(guardar_datos)  # Registrar la función de guardado al salir del programa

    while True:
        limpiar_pantalla()
        print("Bienvenido al sistema de registro de usuarios")
        print("1. Registrar usuario")
        print("2. Iniciar sesión")
        print("3. Salir")

        opcion = input("Ingrese una opción: ")

        if opcion == "1":
            limpiar_pantalla()
            registrar()
        elif opcion == "2":
            limpiar_pantalla()
            login()
        elif opcion == "3":
            print("¡Hasta luego!")
            break
        else:
            print("Opción inválida")
            time.sleep(1)
if __name__ == "__main__": 
    main()