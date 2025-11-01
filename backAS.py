
from AnalizadorLexico import analizador_lexico
from treelib import Node, Tree
from arbol import exportar_arbol

import pandas as pd
df = pd.read_csv('TAS FINAL.csv', index_col=0, header=0, skip_blank_lines=True)  # Reemplaza 'archivo.csv' con la ruta de tu archivo
#print(df.head())  # Muestra las primeras 5 filas del DataFrame
#print(df.at['<Program>','program'])

class DatosNodo(object): 
        def __init__(self, simbolo, lexema): 
            self.simbologramatical = simbolo
            self.lexema = lexema
tree = Tree()

# tree.create_node("Program", 1, data=DatosNodo("<Program>", "program"))  # root node

with open('codigo.txt', 'r', encoding='utf-8') as f:
    contenido = f.read()

tokens = analizador_lexico(contenido)
tokens_invertido = tokens[::-1]
estado = "En proceso"
pila = []

tree.create_node(tag="Program",identifier= 1, data= DatosNodo("<Program>", tokens[0][1]))

pila.append ("$")
pila.append(tree.get_node(1)) # Cargar la pila

# Obtengo la primera COLUMNA de la TAS c/ los nombres de las VARIABLES
variables = [v for v in df.index[0:] if pd.notna(v) and str(v).strip() != ''] #Devuelve todas las variables excepto las casillas vacias o NaN

# Obtengo la primera FILA de la TAS c/ los nombres de los TERMINALES
terminales = df.columns[0:].tolist()  
print(terminales)

def searchNodo(idPadre, tag):
   hojas = tree.leaves()[::-1]
   i = 0
   encontrado = False
   while (encontrado == False) and (tag in variables) and (i < len(hojas)): 
      if (tag == hojas[i].tag):
         idPadre = hojas[i].identifier
         encontrado = True 
      i +=1
      # Es el id (variable) al que se le asignarán los nodos hijos de la derivación
   return idPadre
 
def nodoCreate(pila,idNodo,idPadre, variable, tuplaLexica):
   elem = df.at[variable,tuplaLexica[0]]
   elem = elem.split()
   elem = [e.replace('"',"").replace("“","").replace("”","") for e in elem if e != "epsilon"]
   print(elem)
   for e in (elem):
      tree.create_node(tag=e, identifier=idNodo, parent=idPadre, data=DatosNodo(e ,tuplaLexica[1])) 
      idNodo+=1
   
   hijos = tree.children(idPadre)
   
   for h in hijos[::-1]:       
      pila.append(h)
      
   return pila

tuplaLexica = tokens_invertido.pop()
idPadre = 1
idNodo = 2

while estado == "En proceso": 
   
   componente = pila.pop() 
   if (componente.data.simbologramatical in variables):  # Pregunta si es variable
      if not(pd.isna(df.at[componente.data.simbologramatical,tuplaLexica[0]])) :
         idPadre = searchNodo(idPadre, componente.tag)
         nodoCreate(pila,idNodo,idPadre,componente.data.simbologramatical,tuplaLexica)
         listNodos = tree.all_nodes()
         idNodo = (listNodos[-1].identifier + 1)
      else: estado = "Error por componente inválido 'Campo NaN'"
   elif componente.data.simbologramatical == 'epsilon':
      continue     
             
   elif componente.data.simbologramatical in terminales and tokens_invertido:   # Pregunta si es terminal
      if not(componente.data.simbologramatical == tuplaLexica[0]):  # Compara si el terminal es igual al del Analizador Lexico
         estado = 'Error por componente léxico inválido segun la gramática 1'
      else:
         componente.data.lexema = tuplaLexica[1]
         tuplaLexica = tokens_invertido.pop()
          
   elif pila.pop() == "$" :
         estado = "Éxito"
   else: 
         print(componente.data.simbologramatical, 'Componente ERRÁTICO') 
         estado = "Error"  # Si no, error

print(estado)

print("Árbol final")

tree.show(sorting=False)
exportar_arbol(tree)
print(tokens)
