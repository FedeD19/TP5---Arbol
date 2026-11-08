from tree import BinaryTree

CRIATURAS = [
    ('Ceto', None), ('Tifón', 'Zeus'),
    ('Equidna', 'Argos Panoptes'), ('Dino', None),
    ('Pefredo', None), ('Enio', None), ('Escila', None),
    ('Caribdis', None), ('Euríale', None), ('Esteno', None),
    ('Medusa', 'Perseo'), ('Ladón', 'Heracles'),
    ('Águila del Cáucaso', None), ('Quimera', 'Belerofonte'),
    ('Hidra de Lerna', 'Heracles'), ('León de Nemea', 'Heracles'),
    ('Esfinge', 'Edipo'), ('Dragón de la Cólquida', None),
    ('Cerbero', None), ('Cerda de Cromión', 'Teseo'),
    ('Ortro', 'Heracles'), ('Toro de Creta', 'Teseo'),
    ('Jabalí de Calidón', 'Atalanta'), ('Carcinos', None),
    ('Gerión', 'Heracles'), ('Cloto', None),
    ('Láquesis', None), ('Átropos', None),
    ('Minotauro de Creta', 'Teseo'), ('Harpías', None),
    ('Argos Panoptes', 'Hermes'), ('Aves del Estínfalo', None),
    ('Talos', 'Medea'), ('Sirenas', None),
    ('Pitón', 'Apolo'), ('Cierva de Cerinea', None),
    ('Basilisco', None), ('Jabalí de Erimanto', None),
]

def inorden(nodo, accion):
    if nodo is not None:
        inorden(nodo.left, accion)
        accion(nodo)
        inorden(nodo.right, accion)

def mostrar_criatura(nodo):
    info = nodo.other_values
    print(f"{nodo.value} - derrotada por: {info['derrotado_por'] or '-'}")

def mostrar_datos(nodo):
    if nodo is None:
        print('Criatura no encontrada.')
        return
    info = nodo.other_values
    print('Nombre:', nodo.value)
    print('Derrotada por:', info['derrotado_por'] or '-')
    print('Descripción:', info['descripcion'] or '-')
    print('Capturada por:', info['capturada'] or '-')


def listar_por_derrotador(arbol, heroe):
    inorden(arbol.root, lambda nodo: print(nodo.value)
            if nodo.other_values['derrotado_por'] == heroe else None)


def listar_no_derrotadas(arbol):
    inorden(arbol.root, lambda nodo: print(nodo.value)
            if nodo.other_values['derrotado_por'] is None else None)


def ranking_derrotadores(arbol):
    contador = {}

    def acumular(nodo):
        nombre = nodo.other_values['derrotado_por']
        if nombre is not None:
            contador[nombre] = contador.get(nombre, 0) + 1

    inorden(arbol.root, acumular)
    ranking = sorted(contador.items(), key=lambda par: (-par[1], par[0]))
    for nombre, cantidad in ranking[:3]:
        print(f'{nombre}: {cantidad} criatura(s)')


def buscar_coincidencia(arbol, texto):
    coincidencias = []

    def evaluar(nodo):
        if texto.casefold() in nodo.value.casefold():
            coincidencias.append(nodo)

    inorden(arbol.root, evaluar)
    return coincidencias


def cambiar_nombre(arbol, anterior, nuevo):
    nodo = arbol.search(anterior)
    if nodo is None or arbol.search(nuevo) is not None:
        return False
    datos = dict(nodo.other_values)
    arbol.delete_node(anterior)
    arbol.insert_node(nuevo, datos)
    return True



arbol = BinaryTree()

# Se usa value para el nombre, y other_values para los demás atributos.
for nombre, derrotador in CRIATURAS:
    arbol.insert_node(nombre, {
        'derrotado_por': derrotador,
        'descripcion': '',
        'capturada': None,
    })

#a Inorden de criaturas y derrotadores
print('\na) Criaturas ordenadas alfabéticamente:')
inorden(arbol.root, mostrar_criatura)

#b Permitir cargar/modificar la descripción de una criatura
print('\nb) Se carga la descripción de Talos.')
talos = arbol.search('Talos')
if talos is not None:
    talos.other_values['descripcion'] = 'Autómata de bronce que protegía la isla de Creta.'

#c Mostrar toda la información de Talos
print('\nc) Datos de Talos:')
mostrar_datos(arbol.search('Talos'))

#d Los 3 personajes con más victorias
print('\nd) Tres personajes que derrotaron más criaturas:')
ranking_derrotadores(arbol)

#e Criaturas derrotadas por Heracles
print('\ne) Criaturas derrotadas por Heracles:')
listar_por_derrotador(arbol, 'Heracles')

#f Criaturas sin derrotador registrado
print('\nf) Criaturas que no han sido derrotadas:')
listar_no_derrotadas(arbol)

#g El campo 'capturada' está incluido desde la inserción
print('\ng) Cada nodo contiene un campo "capturada" (inicialmente None).')

#h Registrar cuatro capturas por Heracles
print('\nh) Registrar capturas realizadas por Heracles:')
for nombre in ('Cerbero', 'Toro de Creta',
    'Cierva de Cerinea', 'Jabalí de Erimanto'):
    nodo = arbol.search(nombre)
    if nodo is not None:
        nodo.other_values['capturada'] = 'Heracles'
        print(nombre)

#i Búsqueda parcial por coincidencia
print('\ni) Buscar nombres que contienen "de":')
for nodo in buscar_coincidencia(arbol, 'de'):
    print(nodo.value)

#j Eliminar dos criaturas
print('\nj) Eliminar Basilisco y Sirenas:')
for nombre in ('Basilisco', 'Sirenas'):
    eliminado, _ = arbol.delete_node(nombre)
    print(nombre, 'eliminado' if eliminado is not None else 'no encontrado')

#k Marcar como derrotadas por Heracles a las aves
print('\nk) Actualizar Aves del Estínfalo:')
nodo = arbol.search('Aves del Estínfalo')
if nodo is not None:
    nodo.other_values['derrotado_por'] = 'Heracles'
    nodo.other_values['descripcion'] = 'Heracles derrotó a varias aves del Estínfalo.'
    mostrar_datos(nodo)

#l Renombrar la criatura sin romper el orden del ABB
print('\nl) Renombrar Ladón:')
if cambiar_nombre(arbol, 'Ladón', 'Dragón Ladón'):
    print('Ladón -> Dragón Ladón')

#m Recorrer por nivel
print('\nm) Listado del árbol por nivel:')
arbol.by_level()

#n Mostrar criaturas capturadas (no necesariamente derrotadas) por Heracles
print('\nn) Criaturas capturadas por Heracles:')
inorden(arbol.root, lambda nodo: print(nodo.value)
    if nodo.other_values['capturada'] == 'Heracles' else None)