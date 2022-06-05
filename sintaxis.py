#
# Sofia Recinos Dorst  A01657055
# Ulrik Nuño Tapia  A00821805

from re import U
import ply.yacc as yacc
import sys
from pprint import pprint

# Get the token map from the lexer.  This is required.
from lexico import tokens

OpStack = []

#Cuadruplos
Cuadruplos = []
# goto al main, principio del programa
Cuadruplos.append(["goto", " ", "main" , " "])


#Pilas
PilaO = []
PilaTipos = []
PilaSaltos = []
PilaIDs = []


PilaDims = []

# Directorio de funciones
# Globales: 0 - 2000
#   int 0 - 250
#   float 250-500
#   string 500 - 750
#   bool 750-1000
#Locales: 1000 - 2000
#   int 1000-1250
#   float 1250 - 1500
#   string 1500 - 1750
#   bool 1750 - 2000
#Temporales 2000 - 4000
#   Globales 2000 - 3000
#     int 2000-2250
#     float 2250 - 2500
#     string 2500 - 2750
#     bool 2750 - 3000
#   Locales
#     int 3000-3250
#     float 3250 - 3500
#     string 3500 - 3750
#     bool 3750 - 4000
#CTEs 4000 - 5000
#   int 4000 - 4250
#   float 4250 - 4500
#   string 4500 - 4750
#   bool 4750 - 4752
#Arreglos Globales 5000-5250
#Arreglos Locales 5250-5500
#########################################


direcciones_CTEs = {'int' : 4001 , 'float' : 4250, 'string' : 4500, 'bool' : 4750}

TablaMemoria_CTEs = {'int' : [-1] , 'float' : [ ], 'string' : [ ], 'bool' : [True,False]}

direcciones_Arreglos = {'Arr' : 5001}

semantico = {
    "int" : {
        "+": {
            "int" : "int",
            "float" : "float",
            "bool" : "error",
            "string" : "error"
        },
        "-": {
            "int" : "int",
            "float" : "float",
            "bool" : "error",
            "string" : "error"
        },
        "/": {
            "int" : "int",
            "float" : "float",
            "bool" : "error",
            "string" : "error"
        },
        "*": {
            "int" : "int",
            "float" : "float",
            "bool" : "error",
            "string" : "error"
        },
        ">": {
            "int" : "bool",
            "float" : "bool",
            "bool" : "error",
            "string" : "error"
        },
         "<": {
            "int" : "bool",
            "float" : "bool",
            "bool" : "error",
            "string" : "error"
        },
         "!=": {
            "int" : "bool",
            "float" : "bool",
            "bool" : "error",
            "string" : "error"
        },
         "==": {
            "int" : "bool",
            "float" : "bool",
            "bool" : "error",
            "string" : "error"
        },
         "=": {
            "int" : "int",
            "float" : "error",
            "bool" : "error",
            "string" : "error"
        },
    }, 
    "float" : {
        "+": {
            "int" : "float",
            "float" : "float",
            "bool" : "error",
            "string" : "error"
        },
        "-": {
            "int" : "float",
            "float" : "float",
            "bool" : "error",
            "string" : "error"
        },
        "/": {
            "int" : "float",
            "float" : "float",
            "bool" : "error",
            "string" : "error"
        },
        "*": {
            "int" : "float",
            "float" : "float",
            "bool" : "error",
            "string" : "error"
        },
        ">": {
            "int" : "bool",
            "float" : "bool",
            "bool" : "error",
            "string" : "error"
        },
         "<": {
            "int" : "bool",
            "float" : "bool",
            "bool" : "error",
            "string" : "error"
        },
         "!=": {
            "int" : "bool",
            "float" : "bool",
            "bool" : "error",
            "string" : "error"
        },
         "==": {
            "int" : "bool",
            "float" : "bool",
            "bool" : "error",
            "string" : "error"
        },
         "=": {
            "int" : "float",
            "float" : "float",
            "bool" : "error",
            "string" : "error"
        },

    },
    "string" : {
        "+": {
            "int" : "error",
            "float" : "error",
            "bool" : "error",
            "string" : "string"
        },
        "-": {
            "int" : "error",
            "float" : "error",
            "bool" : "error",
            "string" : "error"
        },
        "/": {
            "int" : "error",
            "float" : "error",
            "bool" : "error",
            "string" : "error"
        },
        "*": {
            "int" : "error",
            "float" : "error",
            "bool" : "error",
            "string" : "error"
        },
        ">": {
            "int" : "error",
            "float" : "error",
            "bool" : "error",
            "string" : "error"
        },
         "<": {
            "int" : "error",
            "float" : "error",
            "bool" : "error",
            "string" : "error"
        },
         "!=": {
            "int" : "error",
            "float" : "error",
            "bool" : "error",
            "string" : "bool"
        },
         "==": {
            "int" : "error",
            "float" : "error",
            "bool" : "error",
            "string" : "bool"
        },
         "=": {
            "int" : "error",
            "float" : "error",
            "bool" : "error",
            "string" : "string"
        },
    },
     "bool" : {
        "+": {
            "int" : "error",
            "float" : "error",
            "bool" : "error",
            "string" : "error"
        },
        "-": {
            "int" : "error",
            "float" : "error",
            "bool" : "error",
            "string" : "error"
        },
        "/": {
            "int" : "error",
            "float" : "error",
            "bool" : "error",
            "string" : "error"
        },
        "*": {
            "int" : "error",
            "float" : "error",
            "bool" : "error",
            "string" : "error"
        },
        ">": {
            "int" : "error",
            "float" : "error",
            "bool" : "error",
            "string" : "error"
        },
         "<": {
            "int" : "error",
            "float" : "error",
            "bool" : "error",
            "string" : "error"
        },
         "!=": {
            "int" : "error",
            "float" : "error",
            "bool" : "bool",
            "string" : "error"
        },
         "==": {
            "int" : "error",
            "float" : "error",
            "bool" : "bool",
            "string" : "error"
        },
         "=": {
            "int" : "error",
            "float" : "error",
            "bool" : "bool",
            "string" : "error"
        },
    },
}

#ASIGNACIÓN DE DIRECCIONES DE MEMORIA PARA LA MAQUINA VIRTUAL
 

# VARIABLES GLOBALES
NombreFunc = "global"
TipoFunc = "global"

UltimoTipo = "void"

def next_temp(tipo_var):
    global NombreFunc
    dir_temp = DirFunc[NombreFunc]["direcciones_temporales"][tipo_var]
    DirFunc[NombreFunc]["direcciones_temporales"][tipo_var] += 1
    return dir_temp


def next_arr():
    global NombreFunc
    dir_temp = DirFunc[NombreFunc]["direcciones"]['arr']
    DirFunc[NombreFunc]["direcciones"]['arr'] += 1
    return dir_temp

#Variables que guardan info sobre el programa global
nombreProg = "global"
tipoProg = "global"
DirInicio = 0
tamProg = 0

DirFunc = {
    "global" : {"nombre" : nombreProg , "tipo" : tipoProg, "DirIni" : DirInicio,
                "tamano" : tamProg , "var_table" : {},
                "direcciones" : {'int' : 0 , 'float' : 250, 'string' : 500, 'bool' : 750, 'arr' : 5000},
                "direcciones_temporales" : {'int' : 2000 , 'float' : 2250, 'string' : 2500, 'bool' : 2750}
                }
}

def get_ID_info(n_id):
    global NombreFunc
    if n_id not in DirFunc[NombreFunc]["var_table"] :
        if n_id not in DirFunc["global"]["var_table"] :
            return False 
        return DirFunc["global"]["var_table"][n_id]
 
    else :
        return DirFunc[NombreFunc]["var_table"][n_id]

def p_programa(p):
    'programa : START programa1 main END'
    p[0] = p[1] 

def p_main(p):
    'main : main_migaja1 MAIN LPAREN RPAREN bloque main_migaja2'
    Cuadruplos.append(["ENDPROG", " " , " ", " "])
    p[0] = p[1] 

def p_main_migaja1(p):
    'main_migaja1 : '
    global NombreFunc
    global TipoFunc

    NombreFunc = "main"
    TipoFunc = "void"

    DirFunc["main"]={"nombre" : "main" , "tipo" : "void", "DirIni" : len(Cuadruplos),
                    "var_table" : {}, "local_table" : [], "NumParam" : 0, 
                    "NumVars" : 0, "NumTemp" : 0,
                    "direcciones": {'int' : 1000 , 'float' : 1250, 'string' : 1500, 'bool' : 1750, 'arr' : 5250},
                    "direcciones_temporales": {'int' : 3000 , 'float' : 3250, 'string' : 3500, 'bool' : 3750}}
    Cuadruplos[0][3] = len(Cuadruplos)

def p_main_migaja2(p):
    'main_migaja2 :  '
    global NombreFunc
    global TipoFunc

    NombreFunc = "global"
    TipoFunc = "global"
    

def p_programa1(p):
    """programa1 : programa2 programa1
                  | empty"""
    p[0] = p[1]

def p_programa2(p):
    """programa2 : decfuncion 
                    | instruccion  
                    | clase"""
    p[0] = p[1]

#voy a ir agregando param x param en lugar de todos de un solo :)
# 1 migaja menos
def p_decfuncion(p):
    'decfuncion : FUNCTION decfuncion_migaja1 LPAREN parametro RPAREN decfuncion_migaja2 bloque'
    global NombreFunc
    global TipoFunc

    if TipoFunc != "void" :
        if DirFunc[NombreFunc]["tiene_return"] != True :
            print ("Error, no hay return en la función", NombreFunc)
            sys.exit()

    #Libera
    NombreFunc = "global"
    
    TipoFunc = "global"

    Cuadruplos.append(["ENDFUNC", " " , " " , " "])

    p[0] = p[1]

# NECESITO leer la variable
def p_decfuncion_migaja1(p):

    'decfuncion_migaja1 : tipoFuncion ID'
    global NombreFunc
    global TipoFunc

    if p[2] in DirFunc:
        print("Error, la funcion ", p[2], "ya había sido declarada")
        sys.exit()
    else:
        NombreFunc = p[2]
        TipoFunc = p[1]

        DirFunc[p[2]]={"nombre" : p[2] , "tipo" : p[1], "DirIni" : len(Cuadruplos),
                     "var_table" : {}, "local_table" : [], "NumParam" : 0, 
                     "NumVars" : 0, "NumTemp" : 0, "tiene_return" : False,
                     "direcciones": {'int' : 1000 , 'float' : 1250, 'string' : 1500, 'bool' : 1750, 'arr' : 5250},
                     "direcciones_temporales": {'int' : 3000 , 'float' : 3250, 'string' : 3500, 'bool' : 3750}}
        if p[1] != "void" :
            DirFunc["global"]["var_table"][p[2]] = {'nombre' : p[2],
                                                    'tipo' : p[1],
                                                    'direccion' : DirFunc["global"]["direcciones"][p[1]]}
            DirFunc["global"]["direcciones"][p[1]] += 1
    p[0] = p[1]  


# NECESITO leer la variable
def p_decfuncion_migaja2(p):
    'decfuncion_migaja2 : '

    global NombreFunc 

    DirFunc[NombreFunc]["NumParam"] = len(DirFunc[NombreFunc]["local_table"])
    DirFunc[NombreFunc]["NumVars"] = len(DirFunc[NombreFunc]["var_table"])


#Se agrego void en una funcion de tipos diferentes xq no se acepta void como tipo para variable
def p_tipoFuncion(p):
    """tipoFuncion : tipo
                    | VOID """
    p[0] = p[1]

# Agrega migaja para ir agregando param x param en la current local table de func
def p_parametro(p):
    """parametro : parametro_migaja1 parametros 
                    | empty"""
    p[0] = p[1]


# NECESITO leer la variable
def p_parametro_migaja1(p):
    'parametro_migaja1 : guarda_tipo decid'

    global NombreFunc
    global TipoFunc
    
    if (p[2][1] != "["):
        if p[2][0] in DirFunc[NombreFunc]["var_table"] :
            print("Error, el parametro ", p[2][0], "ya había sido declarado")
            sys.exit()
        else :
            DirFunc[NombreFunc]["var_table"][p[2][0]] = {'nombre' : p[2][0],
                                                      'tipo' : UltimoTipo,
                                                      'direccion' : DirFunc[NombreFunc]["direcciones"][UltimoTipo]}
            DirFunc[NombreFunc]["local_table"].append({'nombre' : p[2][0],
                                                       'tipo' : UltimoTipo,
                                                       'direccion' : DirFunc[NombreFunc]["direcciones"][UltimoTipo]})
            DirFunc[NombreFunc]["direcciones"][UltimoTipo] += 1
    else:
        print("Error, No se pueden recibir arreglos como parametros de funciones")
    p[0] = p[1]


def p_guarda_tipo(p):
    'guarda_tipo : tipo'
    global UltimoTipo
    UltimoTipo = p[1]
    p[0] = p[1]

def p_parametros(p):
    """parametros : COMA parametro_migaja1 parametros 
                    | empty"""
    p[0] = p[1]


def p_decid(p):
    'decid : decid_migaja1 decarreglo'
    p[0] = (PilaIDs[-1], p[2])
    PilaIDs.pop()

def p_decid_migaja1(p):
    'decid_migaja1 : ID'
    PilaIDs.append(p[1])
    p[0] = p[1]

def p_decarreglo(p):
    """decarreglo : decarreglo_migaja1 decarreglo_migaja2 decarreglo_migaja3
                    | empty"""
    p[0] = p[1]

def p_decarreglo_migaja3(p):
     "decarreglo_migaja3 : "
     global NombreFunc
     global UltimoTipo
     info_id = get_ID_info(PilaIDs[-1])
     Offset = 0
     size = info_id["R"]
     for nodo in info_id["Nodos"]:
         nodo["m"] = info_id["R"] / (nodo["LimSup"] - nodo["LimInf"] + 1)
         info_id["R"] = nodo["m"]
         Offset += nodo["LimInf"] * nodo["m"]
     K = Offset
     info_id["Nodos"][-1]["m"] = - K
     info_id["size"] = size
     info_id["Virtual_address"] = info_id["direccion"]
     DirFunc[NombreFunc]["direcciones"][UltimoTipo] += size


def p_decarreglo_migaja2(p):
    "decarreglo_migaja2 : LBRAQUET decarreglo_migaja4 RBRAQUET masdecarreglos"

def p_masdecarreglos(p):
    """masdecarreglos : masdecarreglo_migaja3 LBRAQUET decarreglo_migaja4 RBRAQUET masdecarreglos
                   | empty """

def p_decarreglo_migaja1(p):
    "decarreglo_migaja1 : "
    global UltimoTipo
    var_name = PilaIDs[-1]
    DirFunc[NombreFunc]["var_table"][var_name]={'nombre' : var_name,
                                'tipo' : UltimoTipo,
                                'direccion' : DirFunc[NombreFunc]["direcciones"][UltimoTipo]
                                }
    info_id = DirFunc[NombreFunc]["var_table"][var_name]
    info_id["isArray"] = True
    info_id["dim"] = 1
    info_id["R"] = 1
    info_id["Nodos"] = [{"LimInf": 0,
                             "LimSup": 0,
                             "m": 0}]
    p[0] = "["

def p_decarreglo_migaja4(p):
    "decarreglo_migaja4 : INTT"
    info_id = get_ID_info(PilaIDs[-1])
    info_id["Nodos"][-1]["LimSup"] = p[1]
    info_id["R"] *= (p[1] - 0 + 1)

    p[0] = p[1]

def p_masdecarreglo_migaja3(p):
    "masdecarreglo_migaja3 : "
    info_id = get_ID_info(PilaIDs[-1])
    info_id["dim"] += 1
    info_id["Nodos"].append({"LimInf": 0,
                             "LimSup": 0,
                             "m": 0})

def p_clase(p):
    'clase : CLASS ID bloqueclase'
    p[0] = p[1]

def p_bloqueclase(p):
    'bloqueclase : LCORCHETE funcyvarrec RCORCHETE'
    p[0] = p[1]

def p_funcyvarrec(p):
    """funcyvarrec : funcyvar funcyvarrec 
                    | empty"""
    p[0] = p[1]

def p_funcyvar(p):
    """funcyvar : decfuncion 
                | decvariable"""
    p[0] = p[1]
    
def p_instruccion(p):
    """instruccion : decvariable
                | condicion
                | asignacion_usofuncion
                | while
                | bloque
                | return
                | lectura
                | escritura"""
    p[0] = p[1]

def p_decvariable(p):
    'decvariable : guarda_tipo ids PUNTOYCOMA'
    global UltimoTipo
    global NombreFunc
    for var_name, is_arr in p[2]:
        if is_arr != "[":
            if var_name in DirFunc[NombreFunc]["var_table"]:
                print("Error, la variable", var_name, "ya había sido declarada")
            else:
                DirFunc[NombreFunc]["var_table"][var_name]={'nombre' : var_name,
                                                            'tipo' : UltimoTipo,
                                                            'direccion' : DirFunc[NombreFunc]["direcciones"][UltimoTipo]
                                                            }
                DirFunc[NombreFunc]["direcciones"][UltimoTipo] += 1
    p[0] = p[1]

def p_ids(p):
    'ids : decid variosids'
    p[2].append(p[1])
    p[0] = p[2]

def p_variosids(p):
    """variosids : COMA ids 
            | empty"""
    if p[1] == None:
        p[0] = []
    else:
        p[0] = p[2]

        
def p_condicion_migaja1(p):
    'condicion_migaja1 : '
    condicion = PilaO[-1]
    PilaO.pop()
    tipo_c = PilaTipos[-1]
    PilaTipos.pop()

    if tipo_c != "bool":
        print("ERROR!! la expresion en el if no es boolena")
    else:
        Cuadruplos.append(['gotoF', condicion," ", "_"])
        PilaSaltos.append(len(Cuadruplos)-1)

def p_condicion(p):
    'condicion :  IF LPAREN expresion RPAREN condicion_migaja1 bloque bloqueelse'
    destino = PilaSaltos[-1]
    PilaSaltos.pop()
    Cuadruplos[destino][3] = len(Cuadruplos)
    p[0] = p[1]


def p_bloqueelse(p):
    """bloqueelse : ELSE bloqueelse_migaja1 bloque
                    | empty"""
    
    p[0] = p[1]

def p_bloqueelse_migaja1(p):
    'bloqueelse_migaja1 : '
    Falso = PilaSaltos[-1]
    PilaSaltos.pop()
    Cuadruplos.append(["goto"," "," ","_"])
    PilaSaltos.append(len(Cuadruplos)-1)
    Cuadruplos[Falso][3] = len(Cuadruplos)

def p_while_migaja1(p):
    'while_migaja1 : '
    PilaSaltos.append(len(Cuadruplos))

def p_while_migaja2(p):
    'while_migaja2 : '
    tipo_c = PilaTipos[-1]
    PilaTipos.pop()
    if tipo_c != "bool":
        print("ERROR!! la expresion en el while no es booleano")
    Cuadruplos.append(['gotoF', PilaO[-1], " ", '_'])
    PilaO.pop()
    PilaSaltos.append(len(Cuadruplos)-1)

def p_while(p):
    'while : WHILE while_migaja1  LPAREN expresion RPAREN while_migaja2 bloque'
    Salida = PilaSaltos[-1]
    PilaSaltos.pop()
    Regreso = PilaSaltos[-1]
    PilaSaltos.pop()
    Cuadruplos.append(['goto', " ", " ", Regreso])
    Cuadruplos[Salida][3] = len(Cuadruplos)
    p[0] = p[1]

def p_asignacion_usofuncion(p):
    'asignacion_usofuncion : asignacion_usofuncion_migaja1 asiguso'
    PilaIDs.pop()
    p[0] = p[1]

def p_asignacion_usofuncion_migaja1(p):
    'asignacion_usofuncion_migaja1 : ID'
    PilaIDs.append(p[1])
    p[0] = p[1]

#MIGAJA1 DE LLAMADA: VERIFICA QUE LA FUNCION EXISTA EN DIRFUNC
#PROBLEMAS:
# 1.Necesitamos saber si es uso funcion antes de buscar el ID en el dirFunc porque 
# si es asignacion el ID no reprenta una funcion 
# USOFUNCION: Funcion(x);
# ASIGNACION: x = (3 * 4(funcion(x)))
# 2. En la parte del codigo donde nos dice si es uso funcion o asignaciion no tenemos el ID
# SOLUCION:
# Variable global que nos diga cual es el current ID
# OTRO PROBLEMAAAAA!!!! :(((((
# Funcion1 (x,funcion2(y))
# currentID = funcion1
# currentID = funcion2
# SOLUCION:
# Pila de IDs


def p_asiguso(p):
    """asiguso : asignacion
                | usofuncion"""
    p[0] = p[1]
    
def p_asignacion(p):
    'asignacion : asignacion_migaja1 IGUAL expresion PUNTOYCOMA'
    id_info = get_ID_info(PilaIDs[-1])
    tipo_c = PilaTipos[-1]
    PilaTipos.pop()
    Tipo_id = PilaTipos[-1]
    PilaTipos.pop()
    if semantico[Tipo_id]["="][tipo_c] != "error" : 
        Cuadruplos.append(['=', PilaO[-1], " ", PilaO[-2]])
    else :
        print("Error no se puede realizar esta asignacion")
    PilaO.pop()
    PilaO.pop()
    p[0] = p[1]

def p_asignacion_migaja1(p):
    """asignacion_migaja1 : arreglos
                    | empty"""
    id_info = get_ID_info(PilaIDs[-1])
    if id_info == False :
        print("Error, la variable", PilaIDs[-1],"no existe ")
    elif p[1] is None:
        PilaO.append(id_info["direccion"])
        PilaTipos.append(id_info["tipo"])



def p_usofuncion(p):
    'usofuncion : usofuncion_migaja1 LPAREN usofuncion_migaja2 RPAREN PUNTOYCOMA'
    Cuadruplos.append(["GOSUB", PilaIDs[-1] , " " , DirFunc[PilaIDs[-1]]["DirIni"]])
    p[0] = p[1]

def p_usofuncion_migaja1(p):
    'usofuncion_migaja1 : '

    if PilaIDs[-1] not in DirFunc :
        print ("Error, esa función no ha sido declarada")
    else: 
        if DirFunc[PilaIDs[-1]]["tipo"] != "void" :
            print ("ERROR, la funcion", PilaIDs[-1] , "no tiene donde regresar su valor")
        Cuadruplos.append(["ERA", " " , " ", PilaIDs[-1]])
    
def p_usofuncion_migaja2(p):
    'usofuncion_migaja2 : expresiones'
    if len(p[1]) != len(DirFunc[PilaIDs[-1]]["local_table"]):
        print("Error, no tiene el numero correcto de parametros para la funcion")
    else:
        for i in range(len(p[1])):
            tipo_declaracion = DirFunc[PilaIDs[-1]]["local_table"][i]["tipo"]
            tipo_uso = p[1][i]["tipo"]
            if semantico[tipo_declaracion]["="][tipo_uso] != "error":
                Cuadruplos.append(["PARAM", p[1][i]["nombre"], " ", i])
            else:
                print("Error, asignacion a parametro de tipo incompatible")

def p_expresiones(p):
    """expresiones : expresion expresionesvarias
                    | empty"""
    if p[1] is not None :
        p[2].insert(0, {"tipo" : PilaTipos[-1], "nombre" : PilaO[-1]})
        p[0] = p[2]
        PilaTipos.pop()
        PilaO.pop()
    else :
        p[0] = [ ]
    
def p_expresionesvarias(p):
    """expresionesvarias : COMA expresion expresionesvarias
            | empty"""
    if p[1] is not None :
        p[3].insert(0, {"tipo" : PilaTipos[-1], "nombre" : PilaO[-1]})
        p[0] = p[3]
        PilaTipos.pop()
        PilaO.pop()
    else:
        p[0] = []

def p_tipo(p):
    """tipo : INT 
            | FLOAT
            | BOOL 
            | STRING"""
    p[0] = p[1]

def p_return(p):
    'return : RETURN expresion PUNTOYCOMA'
    global NombreFunc
    global TipoFunc

    tipo_c = PilaTipos[-1]
    Resultado_expresion = PilaO[-1]
    PilaTipos.pop()
    PilaO.pop()
    id_info = DirFunc["global"]["var_table"][NombreFunc]
    if TipoFunc == "void":
        print ("error, funciones de tipo void no poseen return")
    else:
        DirFunc[NombreFunc]["tiene_return"] = True

    if semantico[id_info["tipo"] ]["="][tipo_c] != "error" : 
        Cuadruplos.append(['=', Resultado_expresion, " ", id_info["direccion"]])
    else :
        print("Error el return no es el mismo tipo de la funcion")

    Cuadruplos.append(["ENDFUNC", " " , " " , " "])
    
    p[0] = p[1]

def p_bloque(p):
    'bloque : LCORCHETE instrucciones RCORCHETE'
    p[0] = p[1]

def p_instrucciones(p):
    """instrucciones : instruccion instrucciones 
                        | empty"""
    p[0] = p[1]


def p_escritura(p):
    'escritura : PRINT LPAREN expresion escritura_migaja1 resultado RPAREN PUNTOYCOMA'
    p[0] = p[1]

def p_escritura_migaja1(p):
    'escritura_migaja1 : '
    Cuadruplos.append(['print', " ", " ", PilaO[-1]])
    PilaO.pop()
    PilaTipos.pop()

def p_resultado(p):
    """resultado : COMA expresion escritura_migaja1 resultado 
                    | empty"""
    p[0] = p[1]

def p_lectura(p):
    'lectura : READ LPAREN lecturaid RPAREN PUNTOYCOMA'
    Cuadruplos.append(['read', " ", " ", PilaO[-1]])
    PilaO.pop()
    PilaTipos.pop()
    p[0] = p[1]

def p_lecturaid(p):
    'lecturaid : lecturaid_migaja1 varids'
    if p[2] is None:
        id_info = get_ID_info(PilaIDs[-1])
        if id_info != False:
            PilaO.append(id_info["direccion"])
            PilaTipos.append(id_info["tipo"])
        else:
            print("Error, la variable", PilaIDs[-1], "no existe")
    p[0] = p[1]

def p_lecturaid_migaja1(p) :
    'lecturaid_migaja1 : ID'
    PilaIDs.append(p[1])

def p_varids(p):
    """varids : arreglos 
                    | empty"""
    p[0] = p[1]

def p_arreglos(p):
    'arreglos : arreglos_migaja1 arreglos2'
    info_id = get_ID_info(PilaIDs[-1])
    Aux1 = PilaO[-1]
    PilaO.pop()
    Dir_Pos_Arr = next_temp("int")
    Cuadruplos.append(["+2", Aux1, int(info_id["Nodos"][-1]["m"]), Dir_Pos_Arr])
    Dir_Pos_Arr_Final = next_arr()
    Cuadruplos.append(["+2", Dir_Pos_Arr, info_id["direccion"], Dir_Pos_Arr_Final])
    PilaO.append(Dir_Pos_Arr_Final)
    PilaTipos.append(info_id["tipo"])
    PilaDims.pop()
    OpStack.pop()
    p[0] = '['

def p_arreglos2(p):
    'arreglos2 : LBRAQUET expresion arreglos_migaja2 RBRAQUET masarreglos'


def p_arreglos_migaja1(p):
    "arreglos_migaja1 : "
    dim = 1
    PilaDims.append([PilaIDs[-1], dim])
    OpStack.append("[")

def p_arreglos_migaja2(p):
    "arreglos_migaja2 : "
    info_id = get_ID_info(PilaIDs[-1])
 
    if info_id["isArray"]:
        curr_dim = PilaDims[-1][1] 
        Nodo = info_id["Nodos"][curr_dim - 1]
        Cuadruplos.append(["VER", PilaO[-1], Nodo["LimInf"], Nodo["LimSup"]])
        if curr_dim < info_id["dim"]:
            if PilaTipos[-1] != "int":
                print("ERROR, las dimensiones de los arreglos deben de ser enteras")
            aux = PilaO[-1]
            PilaO.pop()
            s1m1 = next_temp("int")
            Cuadruplos.append(["*2", aux , int(Nodo["m"]), s1m1])
            PilaO.append(s1m1)

        if(curr_dim > 1):
            aux2 = PilaO[-1]
            PilaO.pop()
            aux1 = PilaO[-1]
            PilaO.pop()
            val_k = next_temp("int")
            Cuadruplos.append(["+", aux1 , aux2, val_k])
            PilaO.append(val_k)
    else:
        print("ERROR, el arreglo debe tener dimensiones enteras")

def p_masarreglos(p):
    """masarreglos : masarreglos_migaja1 arreglos2
                     | empty"""
    p[0] = p[1]

def p_masarreglos_migaja1(p):
    'masarreglos_migaja1 : '
    info_id = get_ID_info(PilaIDs[-1])
    PilaDims[-1][1] += 1

def p_expresion(p):
    'expresion : aritmetica expresion_migaja comparitmetica'
    exps_validas = [">", "<", "!=", "=="]
    if len(OpStack) > 0 and OpStack[-1] in exps_validas:
        operDer = PilaO[-1]
        PilaO.pop()
        tipoDer = PilaTipos[-1]
        PilaTipos.pop()
        operIzq = PilaO[-1]
        PilaO.pop()
        tipoIzq = PilaTipos[-1]
        PilaTipos.pop()
        operador = OpStack[-1]
        OpStack.pop()

        tipoRes = semantico[tipoIzq][operador][tipoDer]
        if tipoRes != "error":
            result = next_temp(tipoRes)
            Cuadruplos.append([operador, operIzq, operDer, result])
            PilaO.append(result)
            PilaTipos.append(tipoRes)
        else:
            print("Error, El tipo de operador es incorrecto")
    p[0] = "exp"

def p_expresion_migaja(p):
    'expresion_migaja : '

def p_comparitmetica(p):
    """comparitmetica : comparadores aritmetica
                        | empty"""
    p[0] = p[1]

def p_comparadores(p):
    """comparadores : MAYORQUE
                    | MENORQUE 
                    | DIFERENT IGUAL
                    | IGUAL IGUAL """
    op = p[1]
    if op == "=" or op == "!":
        op += "="
    OpStack.append(op)
    p[0] = p[1]

def p_aritmetica(p):
    'aritmetica : termino aritmetica_migaja aritmetica2'
    p[0] = p[1]

def p_aritmetica_migaja(p):
    'aritmetica_migaja : '
    if len(OpStack) > 0 and (OpStack[-1] == "+" or OpStack[-1] == "-"):
        operDer = PilaO[-1]
        PilaO.pop()
        tipoDer = PilaTipos[-1]
        PilaTipos.pop()
        operIzq = PilaO[-1]
        PilaO.pop()
        tipoIzq = PilaTipos[-1]
        PilaTipos.pop()
        operador = OpStack[-1]
        OpStack.pop()
        tipoRes = semantico[tipoIzq][operador][tipoDer]
        if tipoRes != "error":
            result = next_temp(tipoRes)
            Cuadruplos.append([operador, operIzq, operDer, result])
            PilaO.append(result)
            PilaTipos.append(tipoRes)
        else:
            print("Error, El tipo de operador es incorrecto")

def p_aritmetica2(p):
    """aritmetica2 : sumres aritmetica
                    | empty"""
    p[0] = p[1]

def p_sumres(p):
    """sumres : PLUS 
                | MINUS"""
    OpStack.append(p[1])
    p[0] = p[1]

def p_termino(p):
    'termino : factor termino_migaja ari'
    p[0] = p[1]

def p_termino_migaja(p):
    'termino_migaja : '
    if len(OpStack) > 0 and (OpStack[-1] == "*" or OpStack[-1] == "/"):
        operDer = PilaO[-1]
        PilaO.pop()
        tipoDer = PilaTipos[-1]
        PilaTipos.pop()
        operIzq = PilaO[-1]
        PilaO.pop()
        tipoIzq = PilaTipos[-1]
        PilaTipos.pop()
        operador = OpStack[-1]
        OpStack.pop()
        tipoRes = semantico[tipoIzq][operador][tipoDer]
        if tipoRes != "error":
            result = next_temp(tipoRes)
            Cuadruplos.append([operador, operIzq, operDer, result])
            PilaO.append(result)
            PilaTipos.append(tipoRes)
        else:
            print("Error, El tipo de operador es incorrecto")

def p_ari(p):
    """ari : multdiv termino
            | empty"""
    p[0] = p[1]

def p_multdiv(p):
    """multdiv : TIMES
                | DIVIDE"""
    OpStack.append(p[1])
    p[0] = p[1]

def p_factor(p):
    """factor : LPAREN factor_migaja expresion RPAREN
                | posneg variable"""
    if p[1] == "-":
        operDer = PilaO[-1]
        PilaO.pop()
        tipoDer = PilaTipos[-1]
        PilaTipos.pop()
        

        tipoRes = semantico["int"]["*"][tipoDer]
        if tipoRes != "error":
            result = next_temp(tipoRes)
            Cuadruplos.append(["*", 4000, operDer, result])
            PilaO.append(result)
            PilaTipos.append(tipoRes)
        else:
            print("Error, El tipo de operador es incorrecto")


    if p[1] == '(' and len(OpStack) > 0 and OpStack[-1] == '(':
        OpStack.pop()
    p[0] = p[1]

def p_factor_migaja(p):
    'factor_migaja : '
    OpStack.append('(')


def p_posnegc(p):
    """posneg : sumres
                | empty"""
    if p[1] is not None:
        OpStack.pop()
    p[0] = p[1]

def p_variable(p):
    """variable : usoid 
                | intt
                | floatt
                | booll
                | stringg """
    #PilaO.append[get_id(p[1].tipo, p[1].value)]
    p[0] = p[1]

def p_intt(p):
    'intt : INTT'
    PilaO.append(direcciones_CTEs["int"])
    PilaTipos.append("int")
    TablaMemoria_CTEs["int"].append(p[1])
    direcciones_CTEs["int"] += 1
    p[0] = p[1]

def p_floatt(p):
    'floatt : FLOATT'
    PilaO.append(direcciones_CTEs["float"])
    PilaTipos.append("float")
    TablaMemoria_CTEs["float"].append(p[1])
    direcciones_CTEs["float"] += 1
    p[0] = p[1]


def p_booll(p):
    """booll : TRUE
        | FALSE"""
    PilaO.append(p[1])
    PilaTipos.append("bool")
    if p[1] == "true" :
        PilaO.append(4750)
    else  :
        PilaO.append(4751)
    p[0] = p[1]

def p_stringg(p):
    'stringg : STRINGG'
    PilaO.append(direcciones_CTEs["string"])
    PilaTipos.append("string")
    TablaMemoria_CTEs["string"].append(p[1])
    direcciones_CTEs["string"] += 1
    p[0] = p[1]


def p_usoid(p):
    'usoid : usoid_migaja1 arrfunc punto'
    if p[2] is None and p[3] is  None:
        id_info = get_ID_info(p[1])
        if id_info != False:
            PilaO.append(id_info["direccion"])
            tipo = id_info["tipo"]
            PilaTipos.append(tipo)
        else:
            print("Error, la variable", p[1], "No ha sido declarada")
    PilaIDs.pop()
    OpStack.pop()
    p[0] = p[1]

def p_usoid_migaja1(p):
    'usoid_migaja1 : ID'
    PilaIDs.append(p[1])
    OpStack.append('ID')
    p[0] = p[1]

def p_punto(p):
    """punto : PUNTO usoid 
                | empty"""
    p[0] = p[1]

def p_arrfunc(p):
    """arrfunc :  arreglos 
                | funciones 
                | empty"""
    p[0] = p[1]

def p_funciones(p):
    'funciones : funciones_migaja1 LPAREN usofuncion_migaja2 RPAREN'
    Cuadruplos.append(["GOSUB", PilaIDs[-1] , " " , DirFunc[PilaIDs[-1]]["DirIni"]])
    function_info = DirFunc["global"]["var_table"][PilaIDs[-1]]
    direccion_temporal = next_temp(function_info["tipo"])
    Cuadruplos.append(["=", function_info["direccion"],"" , direccion_temporal])
    PilaO.append(direccion_temporal)
    PilaTipos.append(function_info["tipo"])
    p[0] = '('

def p_funciones_migaja1(p):
    'funciones_migaja1 : '

    if PilaIDs[-1] not in DirFunc :
        print ("Error, esa función no ha sido declarada")
    else: 
        if DirFunc[PilaIDs[-1]]["tipo"] == "void" :
            print ("ERROR, la funcion", PilaIDs[-1] , "no regresa valor")
        Cuadruplos.append(["ERA", " " , " ", PilaIDs[-1]])

def p_empty(p):
    'empty :'
    p[0] = None

start = 'programa'

def p_error(p):
    print("Syntax error")

def compila(file_name):
    parser = yacc.yacc(debug = True) 
    code_file = open(file_name+".zeit", "r")
    code_lines = code_file.read()
    result = parser.parse(code_lines)
    print(result)
    if result:
        #print("Si funciona!")
        pprint(Cuadruplos)
        codigo_objeto = open(file_name+".geist","w")
        Cuadruplos_strings = []
        for c in Cuadruplos:
            Cuadruplos_strings.append(str(c)+'\n')
        codigo_objeto.writelines(Cuadruplos_strings)
        codigo_objeto.close()
    else:
        print("Error en sintaxis")

