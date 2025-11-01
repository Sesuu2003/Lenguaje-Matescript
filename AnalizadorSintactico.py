
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

# tree.create_node("Program", 1, data=DatosNodo("<Program>", "program"))  # root node
def Inicializar():
   
   tree = Tree()
   with open('productoMatrices.txt', 'r', encoding='utf-8') as f:
      contenido = f.read()

   tokens = analizador_lexico(contenido)
   tokens_invertido = tokens[::-1]
   estado = "En proceso"
   pila = []

   tree.create_node(tag="Program",identifier= 1, data= DatosNodo("<Program>", tokens[0][1]))

   pila.append ("$")
   pila.append(tree.get_node(1)) # Cargar la 

   tuplaLexica = tokens_invertido.pop()
   idPadre = 1
   idNodo = 2

   # Obtengo la primera COLUMNA de la TAS c/ los nombres de las VARIABLES
   variables = [v for v in df.index[0:] if pd.notna(v) and str(v).strip() != ''] #Devuelve todas las variables excepto las casillas vacias o NaN

   # Obtengo la primera FILA de la TAS c/ los nombres de los TERMINALES
   terminales = df.columns[0:].tolist()  
   #print(terminales)
   return tree, variables, terminales, idPadre, idNodo, tuplaLexica, estado, pila, tokens_invertido
 
def searchNodo(idPadre, tag, tree, variables):
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
 
def nodoCreate(pila,idNodo,idPadre, variable, terminales, tuplaLexica,tree):
   elem = df.at[variable,tuplaLexica[0]]
   elem = elem.split()
   elem = [e.replace('"',"").replace("“","").replace("”","") for e in elem if e != "epsilon"]
   #print(elem)
   for e in (elem):
      if e in terminales:
         lexema_actual = ""
      else: 
         lexema_actual = tuplaLexica[1]
      tree.create_node(tag=e, identifier=idNodo, parent=idPadre, data=DatosNodo(e ,lexema_actual)) 
      #print(e ,tuplaLexica[1], idNodo)
      #input()
      idNodo+=1
   
   hijos = tree.children(idPadre)
   
   for h in hijos[::-1]:       
      pila.append(h)
      
   return pila

# print(tokens_invertido)

def AnalizadorPredictivo():

   tree, variables, terminales, idPadre, idNodo, tuplaLexica, estado, pila, tokens_invertido = Inicializar()

   while estado == "En proceso" and len(pila) > 0:
      componente = pila.pop()
      #print(componente.data.simbologramatical, ' ', componente.data.lexema)
      if componente == "$":
         if not tokens_invertido:
               estado = "Éxito"
               exportar_arbol(tree)
               print(estado)
         else:
               print("Error: tokens sobrantes después de vaciar la pila.")
               estado = "Error"
               print(estado,'  ',componente.data.simbologramatical,' ',tuplaLexica[0])
         continue  #Salta a la próxima iteracion

      elif componente.data.simbologramatical in variables:
         if not pd.isna(df.at[componente.data.simbologramatical, tuplaLexica[0]]):
               idPadre = searchNodo(idPadre, componente.tag, tree, variables)
               nodoCreate(pila, idNodo, idPadre, componente.data.simbologramatical,terminales, tuplaLexica,tree)
               listNodos = tree.all_nodes()
               idNodo = listNodos[-1].identifier + 1
         else:
               estado = "Error por componente inválido 'Campo NaN'"
               print(estado,'  ',componente.data.simbologramatical,' ',tuplaLexica[0])

      elif componente.data.simbologramatical == 'epsilon':
         continue

      elif componente.data.simbologramatical in terminales:
         if not (componente.data.simbologramatical == tuplaLexica[0]):
               estado = 'Error por componente léxico inválido según la gramática'
               print(estado,'  ',componente.data.simbologramatical,' ',tuplaLexica[0])
         else:
               # Asigno el lexema correcto al terminal
               componente.data.lexema = tuplaLexica[1]

               # Solo hago pop si quedan más tokens
               if tokens_invertido:
                  tuplaLexica = tokens_invertido.pop()

      else:
         print(componente.data.simbologramatical, 'Componente ERRÁTICO', componente.data.lexema, 'Lo que hay en la pila', tuplaLexica[0])
         estado = "Error"
         print(estado,'  ',componente.data.simbologramatical,' ',tuplaLexica[0])
                  
   #tree.show(sorting=False)   
   return  tree

##tree = AnalizadorPredictivo()
# print(estado)
# print("Árbol final")
# print(tokens)

