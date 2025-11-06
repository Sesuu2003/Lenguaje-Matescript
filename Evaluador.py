from typing import Dict
import sys
import numpy as np

from AnalizadorSintactico import AnalizadorPredictivo

class valorEstado(object):
    def __init__(self, tipoVar, valores): 
            self.tipo = tipoVar
            self.contenido = valores
#contenido = Real
#contenido = (Fila, Columna, valor)

# una func. por cada var. de la gramática

## Alexis

# <C>::= “,” “const” <C> | epsilon
def vC(arbol, NodoActual,listaValores):
    hijos = arbol.children(NodoActual.identifier)
    if hijos:
        listaValores.append(float(hijos[1].data.lexema))
        return vC(arbol,hijos[2],listaValores)
    else:
        return listaValores

# <ColList>::= “const” <C>
def vColList(arbol, NodoActual,listaValores):
    hijos = arbol.children(NodoActual.identifier)
    listaValores.append(float(hijos[0].data.lexema))
    return vC(arbol,hijos[1],listaValores)

# <Row>::= “[“ <ColList> ”]”
def vRow(arbol, NodoActual, listaValores):
    hijos = arbol.children(NodoActual.identifier)
    listaCol = []
    listaCol = vColList(arbol,hijos[1],listaCol)
    listaValores.append(listaCol)
    return listaValores

# <R>::=  “,” <Row> <R>| epsilon
def vR(arbol, NodoActual, listaValores):
    hijos = arbol.children(NodoActual.identifier)
    if hijos:
        listaValores = vRow(arbol, hijos[1],listaValores)
        return vR(arbol, hijos[2],listaValores)
    else:
        return listaValores

# <ident>::= ”[“ <ColList>“]” | epsilon
def vIdent(arbol, NodoActual, estado,lexema):
    hijos = arbol.children(NodoActual.identifier)
    if hijos:
        listaValores = []
        subIndices = vColList(arbol, hijos[1],listaValores)
        valor = estado[lexema].contenido[subIndices[0],subIndices[1]]
        operador = valorEstado("float",valor)
        return operador 
    else:
        operador = valorEstado(estado[lexema].tipo, estado[lexema].contenido)
        return operador

# <Arraydef> ::= “array” ”[” "int" “, “ "int" “]”
def vArrayDef(arbol,nodoActual):
    hijos = arbol.children(nodoActual.identifier)
    return int(hijos[2].data.lexema),int(hijos[4].data.lexema)

# <Type>::= <Arraydef> | “float”
def vType(arbol,NodoActual,estado,lexema):
    hijos = arbol.children(NodoActual.identifier)
    if hijos[0].data.simbologramatical == '<Arraydef>':
        filas, columnas = vArrayDef(arbol,hijos[0])
        estado[lexema] = valorEstado("array", np.zeros((filas,columnas),dtype = float))
    else:
        estado[lexema] = valorEstado("float", 0.0)  # Asignar tipo float al identificador
    return estado

# <wrtDec> ::= epsilon | “,”<contwrt>
def vWrtDec(arbol, NodoActual,estado):
    hijos = arbol.children(NodoActual.identifier)
    if hijos:
        contenido = vContWrite(arbol,hijos[1],estado) 
    return estado

# <contwrt> ::= <AE> <wrtDec> | “string” <wrtDec>
def vContWrite(arbol,NodoActual,estado):
    hijos = arbol.children(NodoActual.identifier)
    if hijos[0].data.simbologramatical == "<AE>":
        valorAE = vAE(arbol,hijos[0],estado).contenido
        print(valorAE)
        contenidoWRT = vWrtDec(arbol,hijos[1],estado) 
        #contenidoWRT += vWrtDec(arbol,hijos[1],estado) 
    else:
        cadena_recortada = hijos[0].data.lexema[1:-1]
        print(cadena_recortada)
        contenidoWRT = vWrtDec(arbol,hijos[1],estado)
   
    return estado

# <Write> ::= “wrt” ”(“ <contwrt> “)” 
def vWrite(arbol,NodoActual,estado):
    hijos = arbol.children(NodoActual.identifier)
    contenidoWRT= ""
    contenidoWRT = vContWrite(arbol,hijos[2],estado)
    return estado

# <STR>::= “string” “,” | epsilon
def vSTR(arbol, NodoActual):
    hijos = arbol.children(NodoActual.identifier)
    if hijos:
        return hijos[0].data.lexema
    else:
        return ""

# <Read> ::= “rd” ”(“ <STR> "id" ”)”
def vRead(arbol,NodoActual,estado):

    hijos = arbol.children(NodoActual.identifier)
    str = vSTR(arbol,hijos[2])
    valorIngresado = input(str)
    id = hijos[3].data.lexema
    estado[id].contenido = float(valorIngresado)
    return estado

## ------------ Victoria ------------------

# <RowList>::= <Row> <R> 
def vRowList(arbol,NodoActual,listaValores):
    hijos = arbol.children(NodoActual.identifier)
    listaValores = []
    listaValores = vRow(arbol,hijos[0],listaValores)
    return vR(arbol,hijos[1],listaValores)

# <matConst>::= “[“ <RowList> “]”
def vMatConst(arbol,NodoActual,estado):
    hijos = arbol.children(NodoActual.identifier)
    listaValores = []
    return vRowList(arbol,hijos[1],listaValores)

# <Primary> ::=  “id”<ident> | "(" <AE> ")" | “const” | “traspone” ”(” ”id” “)” | “tam” ”(“ “id” “[” “int” “]” “)” | <matConst> | “-” <Primary>
def vPrimary(arbol, NodoActual, estado):
    hijos = arbol.children(NodoActual.identifier)
    #print(hijos[0].data.simbologramatical,' ',hijos[0].data.lexema)
    if hijos[0].data.simbologramatical == "id":                     
        operador = vIdent(arbol,hijos[1],estado,hijos[0].data.lexema) 
    elif  hijos[0].data.lexema == "(":
        operador = vAE(arbol,hijos[1],estado)

    elif hijos[0].data.simbologramatical == "const":
        valor = float(hijos[0].data.lexema)
        operador = valorEstado("float",valor)

    elif hijos[0].data.simbologramatical == "traspone":
        id = hijos[2].data.lexema  # Lexema del hijo 2 (id)
        valor = estado[id].contenido
        operador =  ("array",valor.T) # LLAMAR A FUNCIÓN TRASPONE
        
    elif hijos[0].data.simbologramatical == "tam":
        id = hijos[2].data.lexema  # Lexema del hijo 2 (id)
        #np.shape[0] par columnas y [1] para filas
        if hijos[4].data.lexema in [0,1]:
            valor= estado[id].contenido.shape[hijos[4].data.lexema]
            operador = valorEstado("float",valor) # LLAMAR A FUNCIÓN TAMANIO    
        else:
            sys.exit("Error: Tamaño de matriz no válido")
        #TODO completar tamaño de matriz
        
    elif  hijos[0].data.lexema == "-":
        operador = vPrimary(arbol,hijos[1], estado)
        operador.contenido = (operador.contenido)*(-1)
    else: 
        matriz = vMatConst(arbol,hijos[0],estado)
        operador = valorEstado("array",matriz)
    return operador

# <FactorDec> ::= epsilon | “^” <Factor>
def vFactorDec(arbol,NodoActual, estado, op1):
    hijos = arbol.children(NodoActual.identifier)
    if hijos:
        op2 = vFactor(arbol,hijos[1],estado)
        if (op1.tipo == "array" and op2.tipo == "array"):
            try:
                valor = op1.contenido**op2.contenido
                res = valorEstado("array",valor)
            except:
                sys.exit("Error: Tamaño de matrices incompatibles")
        elif (op1.tipo != op2.tipo):
            valor = op1.contenido**op2.contenido
            res = valorEstado("array",valor)
        else:
            res = valorEstado("float",valor)
    else:
        res = op1
    return res

# <Factor> ::= <Primary> <FactorDec> 
def vFactor(arbol, NodoActual, estado):
    hijos = arbol.children(NodoActual.identifier)
    op1=vPrimary(arbol,hijos[0],estado)
    res=vFactorDec(arbol,hijos[1],estado, op1)
    return res

# <TermDec> ::= epsilon | “*”<Term> | “/”<Term>
def vTermDec(arbol,NodoActual, estado, op1):                    
    hijos = arbol.children(NodoActual.identifier)
    if not hijos:  # Si la operación no sigue
        return op1 
    elif hijos[0].data.lexema == "*": 
        op2 = vTerm(arbol,hijos[1], estado)
        if op1.tipo == "array" and op2.tipo == "array":
            try:
                contenido = op1.contenido @ op2.contenido
                res = valorEstado("array",contenido)
            except TypeError as e:
                sys.exit(f"Error en '*' por tipos incompatibles: {e}")
        else:
                if op1.tipo != op2.tipo:
                    contenido = op1.contenido * op2.contenido
                    res = valorEstado("array",contenido)
                else:
                    contenido = op1.contenido * op2.contenido
                    res = valorEstado("float",contenido)
    else: 
         op2 = vTerm(arbol,hijos[1], estado)
         if op1.tipo == "float" and op1.tipo == op2.tipo:
                contenido = op1.contenido / op2.contenido
                res = valorEstado("float",contenido) 
         else:
            sys.exit("Error: No se pueden dividir matrices")
    return res

#<AEDec> ::= epsilon | ”+” <AE> | ”-” <AE>  
def vAEDec(arbol,NodoActual, estado,op1):                       
    hijos = arbol.children(NodoActual.identifier)
    if not hijos:  # Si la operación no sigue
        return op1 
    elif hijos[0].data.lexema == "+": 
        op2 = vAE(arbol,hijos[1], estado)
        # Preguntar el tipo de dato 
        # Suponiendo que se permite entre dos float o dos matrices del mismo tamaño
        if op1.tipo == op2.tipo:
            # En las matrices preguntar si son iguales las dimensiones
            if (op1.tipo == "array" and op1.contenido.shape == op2.contenido.shape) or (op1.tipo == "float"):    
                contenido = op1.contenido + op2.contenido
                res = valorEstado(op1.tipo,contenido) 
            else:  
                sys.exit("Error en '+' por matrices de dimensiones incompatibles")
        else: 
            sys.exit("Error en '+' po|r tipos incompatibles") # El programa se corta, con un código de error. Verificar en una lista de errores
    else: 
        op2 = vAE(arbol,hijos[1], estado)
        if op1.tipo == op2.tipo:
            if (op1.tipo == "array" and op1.contenido.shape == op2.contenido.shape) or (op1.tipo == "float"):    
                contenido = op1.contenido - op2.contenido
                res = valorEstado(op1.tipo,contenido) 
            else:  
                sys.exit("Error en '-' por matrices de dimensiones incompatibles")
        else: 
            sys.exit("Error en '-' por tipos incompatibles")
    return res

#<Term> ::= <Factor> <TermDec>
def vTerm(arbol, NodoActual, estado):
    hijos = arbol.children(NodoActual.identifier)
    op1 = vFactor(arbol,hijos[0], estado)
    if len(hijos) < 2:
        return op1
    else:
         return vTermDec(arbol,hijos[1], estado, op1)

#<AE> ::= <Term> <AEDec>
def vAE(arbol,NodoActual,estado):
    hijos = arbol.children(NodoActual.identifier) # como separar el -
    op1 = vTerm(arbol,hijos[0], estado) # Primer operando
    #res = vAEDec(arbol,hijos[1], estado, op1)
    #print(res.tipo,' ',res.contenido)
    return vAEDec(arbol,hijos[1], estado, op1)

def opRelacionales(op1,opRel,op2):
    if opRel == '==':
        res = (op1.contenido == op2.contenido)
    elif opRel == '!=':
        res = (op1.contenido != op2.contenido)
    elif opRel == '<':
        res = (op1.contenido < op2.contenido)
    elif opRel == '>':
        res = (op1.contenido > op2.contenido)
    elif opRel == '<=':
        res = (op1.contenido <= op2.contenido)
    else:
        res = (op1.contenido >= op2.contenido)
    return res 

# <FactorCond>::= “not” <FactorCond> | <AE> ”relOp” <AE>  | “{“ <Condicion> “}”
def vFactorCond(arbol, NodoActual, estado):
    hijos = arbol.children(NodoActual.identifier)
    if hijos[0].data.lexema == "not":
        res = not(vFactorCond(arbol,hijos[1], estado))
    elif hijos[0].data.lexema == "{":
        res = vCondicion(arbol,hijos[1], estado)
    else:
        op1 = vAE(arbol,hijos[0], estado) 
        op2 = vAE(arbol,hijos[2], estado)
        try:
            res = opRelacionales(op1,hijos[1].data.lexema,op2)
        except ValueError:
            print("Error por tipos de operandos incompatibles")
    return res

# <TermDecCond>::= epsilon | “and” <TermCond> 
def vTermDecCond(arbol,NodoActual, estado, res):
    hijos = arbol.children(NodoActual.identifier)
    if hijos:
        resTerm = vTermCond(arbol,hijos[1], estado)
        return (res and resTerm)
    else:
        return res 

# <TermCond>:= <FactorCond> <TermDecCond>
def vTermCond(arbol, NodoActual, estado):
    hijos = arbol.children(NodoActual.identifier)
    res = vFactorCond(arbol,hijos[0], estado) 
    return vTermDecCond(arbol, hijos[1], estado, res)

# ------------------------ Ulises ----------------------------

#<CDec>::= epsilon | “or” <Condicion>
def vCDec(arbol, NodoActual, estado,res):
    hijos = arbol.children(NodoActual.identifier)
    if hijos:
        resCond = vCondicion(arbol,hijos[1], estado)  # Lexema del hijo 2 (Condicion)
        return (res or resCond)
    else:
        return res

#<Cycle> ::= “while”  <Condicion> “do” <body> “end”
def vCycle(arbol, NodoActual, estado):
    hijos = arbol.children(NodoActual.identifier)
    valorCondicional = vCondicion(arbol,hijos[1], estado)
    iteracion = 0
    # ✓ WHILE REAL: Repite hasta que la condición sea False
    while valorCondicional:
        estado = vBody(arbol, hijos[3], estado)
        valorCondicional = vCondicion(arbol,hijos[1], estado)
        iteracion += 1
    return estado

#<CondDec> ::= “end” | “else” <body> “end” 
def vCondDec(arbol, NodoActual, estado):
    hijos = arbol.children(NodoActual.identifier)
    if hijos[0].data.lexema == "end":
        return estado  # No hay cambios en el estado
    elif hijos[0].data.lexema == "else":
        return vBody(arbol,hijos[1], estado) # Procesar el cuerpo del else
    
#<Condicion>::= <TermCond> <CDec>
def vCondicion(arbol, NodoActual, estado):
    hijos = arbol.children(NodoActual.identifier)
    res = vTermCond(arbol,hijos[0], estado)  # Lexema del hijo 1 (TermCond)
    return vCDec(arbol,hijos[1], estado,res) # Lexema del hijo 2 (CDec)

#<Conditional> ::= “if” <Condicion> “then” <body> <CondDec> 
def vConditional(arbol, NodoActual, estado):
    hijos = arbol.children(NodoActual.identifier)
    valorCondicion = vCondicion(arbol,hijos[1], estado)
    if valorCondicion:
        return vBody(arbol,hijos[3], estado)
    else:
        return vCondDec(arbol,hijos[4],estado)
   
#<Expresion>::=  "assignOp" <AE> | ”[“ <AE> “,” <AE> “]” "assignOp" <AE>
def vExpresion(arbol, NodoActual, estado, lexema):
    hijos = arbol.children(NodoActual.identifier)
    if hijos[0].data.simbologramatical == "assignOp":
        valorAE = vAE(arbol,hijos[1], estado)
        if valorAE.tipo == "array":
            estado[lexema].contenido = np.array(valorAE.contenido)
        else:    
            estado[lexema].contenido = valorAE.contenido
    else: #segunda producción
        Fila = int(vAE(arbol,hijos[1], estado).contenido)
        Columna = int(vAE(arbol,hijos[3], estado).contenido)
        Valor = vAE(arbol,hijos[6], estado).contenido               # REVISAR C/ MATRICES
        estado[lexema].contenido[Fila,Columna] = Valor
    return estado

#<Assign> ::= "id" <Expresion> 
def vAssign(arbol, NodoActual, estado):
    hijos = arbol.children(NodoActual.identifier)
    lexema = hijos[0].data.lexema  # Lexema del hijo 1 (id)
    return vExpresion(arbol,hijos[1], estado, lexema)  # Lexema del hijo 2 (Expresion)

#<Sent> ::= <Assign> | <Read> | <Write> | <Cycle> | <Conditional>
def vSent(arbol,NodoActual, estado):
    hijos = arbol.children(NodoActual.identifier)
    if hijos[0].tag == '<Assign>' :
        estado = vAssign(arbol,hijos[0], estado)
    elif hijos[0].tag == '<Read>':
        estado = vRead(arbol,hijos[0], estado)
    elif hijos[0].tag == '<Write>':
        estado = vWrite(arbol,hijos[0], estado)
    elif hijos[0].tag == '<Cycle>':
        estado = vCycle(arbol,hijos[0], estado)
    elif hijos[0].tag == '<Conditional>':
        estado = vConditional(arbol,hijos[0], estado)
    return estado

#<bodyDec>::= <body> | epsilon
def vBodyDec(arbol,NodoActual, estado):
    hijos = arbol.children(NodoActual.identifier)
    if hijos:  # Si hay hijos, es decir, si hay un cuerpo
        estado = vBody(arbol,hijos[0], estado)  # Lexema del hijo 1 (body)
    return estado

#<body>::= <Sent> “;” <bodyDec>
def vBody(arbol,NodoActual,estado):
    hijos = arbol.children(NodoActual.identifier)
    estado = vSent(arbol,hijos[0], estado)  # Lexema del hijo 1 (Sent)
      # Lexema del hijo 3 (bodyDec)
    return vBodyDec(arbol,hijos[2], estado)

# <Variable>::= <VarDec> | epsilon
def vVariable(arbol,NodoActual,estado):
    hijos = arbol.children(NodoActual.identifier)
    if hijos:  # Si hay hijos, es decir, si hay una variable
        estado = vVarDec(arbol,hijos[0], estado)  # Lexema del hijo 1 (VarDec)
    return estado

#<VarDec> ::= “id” “:” <Type> “;” <Variable>
def vVarDec(arbol,NodoActual,estado):
    hijos = arbol.children(NodoActual.identifier)
    #valorTipo= vType(arbol_3, estado)
    estado = vType(arbol,hijos[2],estado,hijos[0].data.lexema)  # Lexema del hijo 1 (id)
    # Lexema del hijo 3 (Variable)
    return vVariable(arbol,hijos[4], estado)

#<VarDef> ::= “var” <VarDec> | epsilon
def vVarDef(arbol,NodoActual, estado):
    # analizar qué hijo produjo VarDef para saber qué llamar
    # raiz = arbol.root
    hijos = arbol.children(NodoActual.identifier)
    if hijos :
        estado = vVarDec(arbol,hijos[1], estado)
    return estado
    
# <Program> ::= “program” ”Id” ”;” <VarDef> “begin” <body>  “end” “.”
def vProgram(arbol, estado):
  #hijos = raiz.successors(arbol.root)
  hijos= arbol.children(arbol.root)
  estado = vVarDef(arbol,hijos[3], estado) # pasar el 4° hijo de Program 
  vBody(arbol,hijos[5], estado)
  return True

#arbol = analizador_predictivo(tree) #pasar fuente

estado:Dict[str, valorEstado] = {}  #dicc de var de fuente y sus valores actuales clave(nombre), tipo, valor, cant.colum y filas (matriz)
#generar registro
arbol = AnalizadorPredictivo()
vProgram(arbol, estado)

