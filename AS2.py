from AnalizadorLexico import analizador_lexico
from treelib import Node, Tree
from arbol import exportar_arbol

import pandas as pd

df = pd.read_csv('TAS FINAL.csv', index_col=0, header=0, skip_blank_lines=True)

class DatosNodo(object):
    def __init__(self, simbolo, lexema):
        self.simbologramatical = simbolo
        self.lexema = lexema

tree = Tree()

with open('codigo.txt', 'r', encoding='utf-8') as f:
    contenido = f.read()

tokens = analizador_lexico(contenido)
tokens_invertido = tokens[::-1]
estado = "En proceso"
pila = []

tree.create_node(tag="Program", identifier=1, data=DatosNodo("<Program>", tokens[0][1]))

pila.append("$")
pila.append(tree.get_node(1))

variables = [v for v in df.index[0:] if pd.notna(v) and str(v).strip() != '']
terminales = df.columns[0:].tolist()

def searchNodo(idPadre, tag):
    hojas = tree.leaves()[::-1]
    i = 0
    encontrado = False
    while (encontrado == False) and (tag in variables) and (i < len(hojas)):
        if (tag == hojas[i].tag):
            idPadre = hojas[i].identifier
            encontrado = True
        i += 1
    return idPadre

def nodoCreate(pila, idNodo, idPadre, variable, tuplaLexica):
    elem = df.at[variable, tuplaLexica[0]]
    elem = elem.split()
    elem = [e.replace('"', "").replace("“", "").replace("”", "") for e in elem if e != "epsilon"]
    print(elem)

    for e in elem:
        if e in terminales:
            lexema_actual = None  # El lexema real se asigna después cuando se hace match
        else:
            lexema_actual = tuplaLexica[1]
        tree.create_node(tag=e, identifier=idNodo, parent=idPadre, data=DatosNodo(e, lexema_actual))
        idNodo += 1

    hijos = tree.children(idPadre)
    for h in hijos[::-1]:
        pila.append(h)

    return pila

print(tokens_invertido)
tuplaLexica = tokens_invertido.pop()
idPadre = 1
idNodo = 2

while estado == "En proceso" and len(pila) > 0:
    componente = pila.pop()

    if componente == "$":
        if not tokens_invertido:
            estado = "Éxito"
        else:
            print("Error: tokens sobrantes después de vaciar la pila.")
            estado = "Error"
        continue  #Salta a la próxima iteracion

    elif componente.data.simbologramatical in variables:
        if not pd.isna(df.at[componente.data.simbologramatical, tuplaLexica[0]]):
            idPadre = searchNodo(idPadre, componente.tag)
            nodoCreate(pila, idNodo, idPadre, componente.data.simbologramatical, tuplaLexica)
            listNodos = tree.all_nodes()
            idNodo = listNodos[-1].identifier + 1
        else:
            estado = "Error por componente inválido 'Campo NaN'"

    elif componente.data.simbologramatical == 'epsilon':
        continue

    elif componente.data.simbologramatical in terminales:
        if not (componente.data.simbologramatical == tuplaLexica[0]):
            estado = 'Error por componente léxico inválido según la gramática 1'
        else:
            # Asigno el lexema correcto al terminal
            componente.data.lexema = tuplaLexica[1]

            # Solo hago pop si quedan más tokens
            if tokens_invertido:
                tuplaLexica = tokens_invertido.pop()

    else:
        print(componente.data.simbologramatical, 'Componente ERRÁTICO')
        estado = "Error"

print(estado)
print("Árbol final")

tree.show(sorting=False)
exportar_arbol(tree)
print(tokens)
