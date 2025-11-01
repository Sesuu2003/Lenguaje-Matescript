from enum import Enum  

class Sigma(Enum):
    LETRA = "Letra"
    DIGITO = "Digito"
    CESPECIAL = "Caracter especial"
    COMILLAS = "Comillas"
    PUNTO = "Punto"
    OTRO = "Otro"

CARACTERES_ESPECIALES = {'_', '-','@','#', '$', '%', '&', '*','¿','?', '>', '<', '=', '!', '+', '-', '/', '^','|','°',' '}

class SigmaEntero(Enum):
     DIGITO = "Digito"
     OTRO = "Otro"

def car_a_simb(car):    
    if car.isalpha():
        return Sigma.LETRA.value
    elif car.isdigit():
        return Sigma.DIGITO.value
    elif car in CARACTERES_ESPECIALES:
        return Sigma.CESPECIAL.value
    elif car == '"':
        return Sigma.COMILLAS.value
    elif car == '.':
        return Sigma.PUNTO.value
    else:
        return Sigma.OTRO.value
        
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

print(esEntero('12'))

