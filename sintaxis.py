#
# Sofia Recinos Dorst  A01657055
# Ulrich Nuño Tapia  A00821805

from curses import ERR
from distutils.log import ERROR
import ply.yacc as yacc

# Get the token map from the lexer.  This is required.
from lexico import tokens

#Vector Polaco
#VP = []
OpStack = []
#VarStack = []

#Cuadruplos
Cuadruplos = []

#Pilas
PilaO = []
PilaTipos = []
PilaSaltos = []
PilaIDs = []

#########################################

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

id_temp = 0
def next_temp():
    global id_temp
    id_temp += 1
    return "T"+ str(id_temp)

#Variables que guardan info sobre el programa global
nombreProg = "global"
tipoProg = "global"
DirInicio = 0
tamProg = 0

DirFunc = {
    "global" : {"nombre" : nombreProg , "tipo" : tipoProg, "DirIni" : DirInicio,
                "tamano" : tamProg , "var_table" : {}}
}

def get_ID_info(n_id):
    if n_id not in DirFunc[NombreFunc]["var_table"] :
        if n_id not in DirFunc["global"]["var_table"] :
            return False 
        return DirFunc["global"]["var_table"][n_id]
 
    else :
        return DirFunc[NombreFunc]["var_table"][n_id]

def p_programa(p):
    'programa : START programa1 END'
    p[0] = p[1] 

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
    global id_temp
    global NombreFunc
    DirFunc[NombreFunc]["NumTemp"] = id_temp
    id_temp = 0
    #Libera
    NombreFunc = "global"
    global TipoFunc
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
    else:
        NombreFunc = p[2]
        TipoFunc = p[1]

        DirFunc[p[2]]={"nombre" : p[2] , "tipo" : p[1], "DirIni" : len(Cuadruplos),
                     "var_table" : {}, "local_table" : [], "NumParam" : 0, 
                     "NumVars" : 0, "NumTemp" : 0}
        if p[1] is not "void" :
            DirFunc["global"]["var_table"][p[2]] = {'nombre' : p[2],
                                                    'tipo' : p[1]}
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
    'parametro_migaja1 : tipo decid'

    global NombreFunc
    global TipoFunc

    if p[2] in DirFunc[NombreFunc]["var_table"] :
        print("Error, el parametro ", p[2], "ya había sido declarado")
    else :
        DirFunc[NombreFunc]["var_table"][p[2]] = {'nombre' : p[2],
                                                  'tipo' : p[1]}
        DirFunc[NombreFunc]["local_table"].append({'nombre' : p[2],
                                                   'tipo' : p[1]})
    p[0] = p[1]


def p_parametros(p):
    """parametros : COMA parametro_migaja1 parametros 
                    | empty"""
    p[0] = p[1]


def p_decid(p):
    'decid : ID decarreglo'
    p[0] = p[1]

def p_decarreglo(p):
    """decarreglo : LBRAQUET INTT RBRAQUET decarreglo 
                    | empty"""
    p[0] = p[1]

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
    'decvariable : tipo ids PUNTOYCOMA'
    for var_name in p[2]:
        if var_name in DirFunc["global"]["var_table"]:
            print("Error, la variable", var_name, "ya había sido declarada")
        else:
            DirFunc["global"]["var_table"][var_name]={'nombre' : var_name,
                                'tipo' : p[1]}
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
    if semantico[id_info["tipo"]]["="][tipo_c] != "error" : 
        Cuadruplos.append(['=', PilaO[-1], " ", PilaIDs[-1]])
    else :
        print("Error no se puede realizar esta asignacion")
    PilaO.pop()
    p[0] = p[1]

def p_asignacion_migaja1(p):
    'asignacion_migaja1 : '
    id_info = get_ID_info(PilaIDs[-1])
    if id_info == False :
        print("Error, la variable", PilaIDs[-1],"no existe ")



def p_usofuncion(p):
    'usofuncion : usofuncion_migaja1 LPAREN usofuncion_migaja2 RPAREN PUNTOYCOMA'
    Cuadruplos.append(["GOSUB", " " , " " , PilaIDs[-1]])
    p[0] = p[1]

def p_usofuncion_migaja1(p):
    'usofuncion_migaja1 : '
    if PilaIDs[-1] not in DirFunc :
        print ("Error, esa función no ha sido declarada")
    else: 
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
                print("Error, los tipos no se pueden operar")

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
    p[0] = p[1]

def p_bloque(p):
    'bloque : LCORCHETE instrucciones RCORCHETE'
    p[0] = p[1]

def p_instrucciones(p):
    """instrucciones : instruccion instrucciones 
                        | empty"""
    p[0] = p[1]


def p_escritura(p):
    'escritura : PRINT LPAREN expresion resultado RPAREN PUNTOYCOMA'
    Cuadruplos.append(['print', " ", " ", PilaO[-1]])
    PilaO.pop()
    p[0] = p[1]

def p_resultado(p):
    """resultado : COMA expresion resultado 
                    | empty"""
    if p[0] == ',':
        Cuadruplos.append(['print', " ", " ", PilaO[-1]])
        PilaO.pop()
    p[0] = p[1]

def p_lectura(p):
    'lectura : READ LPAREN lecturaid RPAREN PUNTOYCOMA'
    Cuadruplos.append(['read', " ", " ", PilaO[-1]])
    PilaO.pop()
    p[0] = p[1]

def p_lecturaid(p):
    'lecturaid : ID  varids'
    PilaO.append(p[1])
    p[0] = p[1]

def p_varids(p):
    """varids : arreglos 
                    | empty"""

def p_arreglos(p):
    'arreglos : LBRAQUET expresion RBRAQUET masarreglos'
    p[0] = p[1]

def p_masarreglos(p):
    """masarreglos : arreglos 
                    | empty"""

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
            result = next_temp()
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
            result = next_temp()
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
            result = next_temp()
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
    #if p[1].value == "-":
    #    pass
    if p[1] == '(' and len(OpStack) > 0 and OpStack[-1] == '(':
        OpStack.pop()
    p[0] = p[1]

def p_factor_migaja(p):
    'factor_migaja : '
    OpStack.append('(')
    p[0] = p[1]


def p_posnegc(p):
    """posneg : sumres
                | empty"""
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
    PilaO.append(p[1])
    PilaTipos.append("int")
    p[0] = p[1]

def p_floatt(p):
    'floatt : FLOATT'
    PilaO.append(p[1])
    PilaTipos.append("float")
    p[0] = p[1]

def p_booll(p):
    """booll : TRUE
        | FALSE"""
    PilaO.append(p[1])
    PilaTipos.append("bool")
    p[0] = p[1]

def p_stringg(p):
    'stringg : STRINGG'
    PilaO.append(p[1])
    PilaTipos.append("string")
    p[0] = p[1]


def p_usoid(p):
    'usoid : usoid_migaja1 arrfunc punto'
    if p[2] is None and p[3] is None:
        PilaO.append(p[1])
        tipo = DirFunc["global"]["var_table"][p[1]]["tipo"]
        PilaTipos.append(tipo)
    PilaIDs.pop()
    p[0] = p[1]

def p_usoid_migaja1(p):
    'usoid_migaja1 : ID'
    PilaIDs.append(p[1])
    p[0] = p[1]

def p_punto(p):
    """punto : PUNTO usoid 
                | empty"""
    p[0] = p[1]

def p_arrfunc(p):
    """arrfunc : arreglos 
                | funciones 
                | empty"""
    p[0] = p[1]

def p_funciones(p):
    'funciones : usofuncion_migaja1 LPAREN usofuncion_migaja2 RPAREN'
    Cuadruplos.append(["GOSUB", " " , " " , PilaIDs[-1]])
    p[0] = p[1]

def p_empty(p):
    'empty :'
    p[0] = None

start = 'programa'

def p_error(p):
    print("Syntax error")

parser = yacc.yacc(debug = True) 

code_file = open("programaTest.txt", "r")
code_lines = code_file.read()
result = parser.parse(code_lines)
print(result)
if result:
    print("Si funciona!")
    print(Cuadruplos)
else:
    print("Error en sintaxis")
