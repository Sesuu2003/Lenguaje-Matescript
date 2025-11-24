from enum import Enum  # TAS Panda
import pandas as pd

#CONS
MaxSim=200
FinArch=1 #0

#TYPE

# Terminales y variables
# TipoSimboloGramatical=[Tid,Tcreal,cad,Twhile,Tif,Tvar,punto,Tpycom,coma,dospuntos,menos,mas,pesos,error]

# FileOfChar= file of char;
class TELemTS:
    def _init_(self, complex, Lexema):
        self.complex = complex
        self.Lexema =  Lexema

class TablaDeSimbolos:
    def _init_(self):
        self.elem = [None] * MaxSim
        self.cant = 0

def LeerCar(Fuente, control):
    if control < len(Fuente):
        car = Fuente[control]
        control += 1
    else:
        car = FinArch
    return car, control

# Automatas

class Sigma(Enum):
    LETRA = "Letra"
    DIGITO = "Digito"
    CESPECIAL = "Caracter especial"
    OPREL = "OpRel"
    OPARITMETICO = "OpAritmetico"
    COMILLAS = "Comillas"
    PUNTO = "Punto"
    OTRO = "Otro"

# Definir caracteres especiales permitidos
CARACTERES_ESPECIALES = {'_','@','#', '$', '%', '&','¿','?','¡', '!','|','°',' '}  
OPERADORES_RELACIONALES = {'>','<','='}
OPERADORES_ARITMETICOS = {'-','+','*','/','^'}
def car_a_simb(car):
    if car == '"':
        return Sigma.COMILLAS.value    
    elif car.isalpha():
        return Sigma.LETRA.value
    elif car.isdigit():
        return Sigma.DIGITO.value
    elif car in CARACTERES_ESPECIALES:
        return Sigma.CESPECIAL.value
    elif car in OPERADORES_RELACIONALES:
        return Sigma.OPREL.value
    elif car in OPERADORES_ARITMETICOS:
        return Sigma.OPARITMETICO.value
    elif car == '.':
        return Sigma.PUNTO.value
    else:
        return Sigma.OTRO.value

#  Definir cada Sigma y car_a_simb
class SigmaString(Enum):
    OTRO = "Otro"
    COMILLAS = 'Comillas'          

class SigmaEntero(Enum):
     DIGITO = "Digito"
     OTRO = "Otro"
     
class SigmaFloat(Enum):
     DIGITO = "Digito"
     PUNTO = "Punto"
     OTRO = "Otro"
     
class SigmaOpRel(Enum):
    OPREL = "OpRel"
    OTRO = "Otro"
    
def esEntero(cadena:str) -> bool:
    q0 = 0
    F = {1}
    
    # Q = {0,1,2} 
    Delta = {
        (0, SigmaEntero.DIGITO.value): 1,
        (0, SigmaEntero.OTRO.value): 2,
        
        (1, SigmaEntero.DIGITO.value): 1,
        (1, SigmaEntero.OTRO.value): 2,
        
    }
    estado_actual = q0
    i = 0
    while estado_actual != 2 and not(i > len(cadena)-1):
        simbolo = car_a_simb(cadena[i])
        if simbolo != SigmaEntero.DIGITO.value:
            simbolo = SigmaEntero.OTRO.value
        estado_actual = Delta.get((estado_actual,simbolo),estado_actual)
        i +=1
        
    return estado_actual in F

def esString(cadena:str) -> bool:
    q0 = 0
    F = {4}
    
    # Q = {0,1,2,3,4}
    Delta = {
        (0, SigmaString.COMILLAS.value):1,
        (0, SigmaString.OTRO.value): 2,
        
        (1, Sigma.COMILLAS.value):4,
        (1, Sigma.OTRO.value): 3,
        
        (3, SigmaString.OTRO.value):3,
        (3, Sigma.COMILLAS.value):4,
        
        (4, Sigma.COMILLAS.value):2,
        (4, Sigma.OTRO.value):2,
        
    }
    
    estado_actual = q0
    i=0
    while estado_actual !=2 and not(i> len(cadena) -1):
        simbolo = car_a_simb(cadena[i])
        if simbolo != SigmaString.COMILLAS.value:
            simbolo = SigmaString.OTRO.value
        estado_actual = Delta.get((estado_actual,simbolo),estado_actual)
        i +=1
    return estado_actual in F

def esConstReal(cadena:str) -> bool:
    q0 = 0
    F = {4}
    
    # Q = {0,1,2,3,4}
    Delta = {
        (0, SigmaFloat.DIGITO.value): 1,
        (0, SigmaFloat.PUNTO.value): 2,
        (0, SigmaFloat.OTRO.value): 2,
        
        (1, SigmaFloat.DIGITO.value): 1,
        (1, SigmaFloat.OTRO.value): 2,
        (1, SigmaFloat.PUNTO.value): 3,

        (3, SigmaFloat.OTRO.value):2,
        (3, SigmaFloat.PUNTO.value):2,
        (3, SigmaFloat.DIGITO.value):4,
        
        (4, SigmaFloat.OTRO.value):2,
        (4, SigmaFloat.PUNTO.value):2,
        (4, SigmaFloat.DIGITO.value):4
        
    }
    
    estado_actual = q0
    i=0
    while (estado_actual !=2) and (i<= len(cadena)-1):
        simbolo = car_a_simb(cadena[i])
        if (simbolo != SigmaFloat.PUNTO.value) and (simbolo != SigmaFloat.DIGITO.value):
            simbolo = SigmaFloat.OTRO.value
        estado_actual = Delta.get((estado_actual,simbolo),estado_actual)
        i +=1
    return estado_actual in F
    
def esOpRel(cadena:str) -> bool:
    q0 = 0
    F = {1,2,3}
    # Q = {0,1,2,3,4,5}
    Delta = {
        (0, "="):4,
        (0, ">"): 1,
        (0, "<"): 2,
        
        (4, "="):3,
        (4, ">"):5,
        (4, "<"):5,
        
        (1, "="):3,
        (1, "<"):5,
        (1, ">"):5,
        
        (2, ">"):3,
        (2, "="):3,
        (2, "<"):5,
    }
    
    estado_actual = q0   
    
    i=0
    while estado_actual !=5 and not(i> len(cadena) -1): 
        simbolo = (cadena[i])
        if not (simbolo  in OPERADORES_RELACIONALES): 
            #simbolo = SigmaOpRel.OTRO.value
            estado_actual = 5
        else:
            estado_actual = Delta.get((estado_actual,simbolo),estado_actual)
        i += 1
    return estado_actual in F

# CODIGO FUNCION ANALIZADOR LEXICO 

PALABRAS_CLAVE = {"program","var","begin","end","if","else","then","while","do","not","or","and","traspone","tam","rd","wrt","array","float"}

diccionario_simbolos = {
    ",": "coma",
    ".": "punto",
    ";": "puntoycoma",
    "=": "assignOp",
    ":": "dosPuntos",
    "+": "mas",
    "-": "menos",
    "^": "circunflejo",
    "(": "parentesisIzq",
    ")": "parentesisDer",
    "{": "llaveIzq",
    "}": "llaveDer",
    "[": "corcheteIzq",
    "]":  "corcheteDer",
    "/": "barra",
    "*": "producto"
}

def es_identificador(cadena):
    return cadena[0].isalpha() and all(c.isalnum() or c == '_' for c in cadena)

def clasificar_lexema(lexema):
    if lexema in PALABRAS_CLAVE:
        return (lexema)
    elif esEntero(lexema):
        return ("int")
    elif esConstReal(lexema):
        return ("const")  
    elif esString(lexema):
        return ("string")
    elif esOpRel(lexema):
        return ("relOp")
    elif es_identificador(lexema):
        return ("id")
    elif lexema == "=":
        return ("assignOp")
    else:
        return ("ERROR")

def analizador_lexico(fuente): 
    tokens = []
    lexema = ""
    i = 0
    while i < len(fuente):
        c = fuente[i]
        
        if '"' in lexema:    
            lexema += c
            i += 1
            if c == '"':
                tokens.append([clasificar_lexema(lexema),lexema])
                lexema = ""
            continue

        if c in OPERADORES_RELACIONALES:
            if lexema and lexema not in OPERADORES_RELACIONALES:
                tokens.append([clasificar_lexema(lexema), lexema])
                lexema = ""
            lexema += c
            i += 1
            # Verificar si el siguiente carácter también es operador
            if i < len(fuente) and fuente[i] in OPERADORES_RELACIONALES:
                continue  # Esperar para formar operador de 2 chars
            else:
                # Agregar el operador (1 o 2 caracteres)
                tokens.append([clasificar_lexema(lexema), lexema])
                lexema = ""
                continue

        if c.isspace():
            i += 1
            if lexema:
                tokens.append([clasificar_lexema(lexema),lexema])
                lexema = ""
            continue

        if lexema and lexema[-1] == "." and c == ".":     
            tokens.append([clasificar_lexema(lexema[:-1]), lexema]) 
            tokens.append(["puntopunto",lexema])
            lexema = ""
            i+=1
            continue

        if lexema.isdigit() and c == ".":  
            lexema += c
            i += 1
            continue 
        
        if c in diccionario_simbolos: 
            if lexema:
                tokens.append([clasificar_lexema(lexema),lexema])
                lexema = ""                
            tokens.append([diccionario_simbolos[c],c])
            i += 1
            continue

        if c.isalnum() or c == '_' or c == '"':
            lexema += c
            i += 1
        else:
            if lexema:
                tokens.append([clasificar_lexema(lexema),lexema])
                lexema = ""
            i += 1

    if lexema:
        tokens.append([clasificar_lexema(lexema),lexema])

    return tokens

