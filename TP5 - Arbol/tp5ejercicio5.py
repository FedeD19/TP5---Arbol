from tree import BinaryTree


def inorden(nodo, accion):
    if nodo is not None:
        inorden(nodo.left, accion)
        accion(nodo)
        inorden(nodo.right, accion)


def inorden_descendente(nodo, accion):
    if nodo is not None:
        inorden_descendente(nodo.right, accion)
        accion(nodo)
        inorden_descendente(nodo.left, accion)


def contar_nodos(nodo):
    if nodo is None:
        return 0
    return 1 + contar_nodos(nodo.left) + contar_nodos(nodo.right)


def contar_heroes(nodo):
    if nodo is None:
        return 0
    actual = 1 if nodo.other_values['is_hero'] else 0
    return actual + contar_heroes(nodo.left) + contar_heroes(nodo.right)


def buscar_por_proximidad(nodo, texto, encontrados):
    if nodo is not None:
        buscar_por_proximidad(nodo.left, texto, encontrados)
        if texto.casefold() in nodo.value.casefold():
            encontrados.append(nodo.value)
        buscar_por_proximidad(nodo.right, texto, encontrados)


def corregir_nombre(arbol, nombre_incorrecto, nombre_correcto):
    nodo = arbol.search(nombre_incorrecto)
    if nodo is None or arbol.search(nombre_correcto) is not None:
        return False
    datos = dict(nodo.other_values)
    arbol.delete_node(nombre_incorrecto)
    arbol.insert_node(nombre_correcto, datos)
    return True


def crear_bosque(arbol):
    heroes = BinaryTree()
    villanos = BinaryTree()

    def separar(nodo):
        destino = heroes if nodo.other_values['is_hero'] else villanos
        destino.insert_node(nodo.value, dict(nodo.other_values))

    inorden(arbol.root, separar)
    return heroes, villanos



arbol = BinaryTree()

#Se carga a Doctor Strange con un error intencional para resolver el punto e.
personajes = [
    ('Iron Man', True), ('Captain America', True),
    ('Captain Marvel', True), ('Black Widow', True),
    ('Hulk', True), ('Thor', True), ('Hawkeye', True),
    ('Scarlet Witch', True), ('Spider-Man', True),
    ('Black Panther', True), ('Doctor Strang', True),
    ('Ant-Man', True), ('Wasp', True), ('Falcon', True),
    ('Winter Soldier', True), ('Shang-Chi', True),
    ('Thanos', False), ('Ultron', False), ('Hela', False),
    ('Killmonger', False), ('Red Skull', False),
    ('Ronan', False), ('Green Goblin', False),
    ('Mysterio', False), ('Vulture', False),
]

#a True significa héroe; False significa villano
for nombre, es_heroe in personajes:
        arbol.insert_node(nombre, {'is_hero': es_heroe})

#b Villanos ordenados alfabéticamente
print('\nb) Villanos (A-Z):')
inorden(arbol.root, lambda nodo: print(nodo.value)
    if not nodo.other_values['is_hero'] else None)

#c Superhéroes cuyos nombres empiezan con C
print('\nc) Héroes que comienzan con C:')
inorden(arbol.root, lambda nodo: print(nodo.value)
    if nodo.other_values['is_hero'] and nodo.value.startswith('C') else None)

#d Cantidad total de héroes
print('\nd) Cantidad de héroes:', contar_heroes(arbol.root))

#e Búsqueda aproximada y modificación de la clave
print('\ne) Búsqueda por proximidad de "Strang":')
coincidencias = []
buscar_por_proximidad(arbol.root, 'Strang', coincidencias)
print('Coincidencias:', coincidencias)
if len(coincidencias) == 1:
    if corregir_nombre(arbol, coincidencias[0], 'Doctor Strange'):
        print('Nombre corregido: Doctor Strange')

#f Héroes ordenados de Z a A
print('\nf) Héroes (Z-A):')
inorden_descendente(arbol.root, lambda nodo: print(nodo.value)
    if nodo.other_values['is_hero'] else None)

#g Separar el árbol original en dos árboles nuevos
heroes, villanos = crear_bosque(arbol)
print('\ng.I) Cantidad de nodos en cada árbol:')
print('Héroes:', contar_nodos(heroes.root))
print('Villanos:', contar_nodos(villanos.root))

print('\ng.II) Árbol de héroes (A-Z):')
inorden(heroes.root, lambda nodo: print(nodo.value))
print('\ng.II) Árbol de villanos (A-Z):')
inorden(villanos.root, lambda nodo: print(nodo.value))