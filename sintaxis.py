#
# Sofia Recinos Dorst  A01657055
# Ulrich Nuño Tapia  A00821805

from curses import ERR
from distutils.log import ERROR
import ply.yacc as yacc

# Get the token map from the lexer.  This is required.
from lexico import tokens

#Vector Polaco
VP = []
OpStack = []
VarStack = []

#Cuadruplos
PilaO = []
PilaTipos = []
PilaSaltos = []
Cuadruplos = []

#########################################
#1D(Operator(arrnum))-> 0-+, 1--, 2-/, 3-*,4- >, 5- <, 6- >=, 7- <=, 8- !=, 9- ==
#2D(operand)-> 0-int, 1-float, 2-char, 3-string, 4-bool
#3D(Operand)-> 0-int, 1-float, 2- char, 3-string, 4-bool
#R(Resultant type)->0-int, 1-float, 2- char,3-string, 4-bool, 5- error
semantico = [
#+
[[0, 1, 5, 5, 5], [1, 1, 5, 5, 5], [5, 5, 2, 3, 5], [5, 5, 3, 3, 5], [5, 5, 5, 5, 5]],
#-
[[0, 1, 5, 5, 5], [1, 1, 5, 5, 5], [5, 5, 5, 5, 5], [5, 5, 5, 5, 5], [5, 5, 5, 5, 5]],
#/
[[0, 1, 5, 5, 5], [1, 1, 5, 5, 5], [5, 5, 5, 5, 5], [5, 5, 5, 5, 5], [5, 5, 5, 5, 5]],
#*
[[0, 1, 5, 5, 5], [1, 1, 5, 5, 5], [5, 5, 5, 5, 5], [5, 5, 5, 5, 5], [5, 5, 5, 5, 5]],
#>
[[4, 4, 5, 5, 5], [4, 4, 5, 5, 5], [5, 5, 5, 5, 5], [5, 5, 5, 5, 5], [5, 5, 5, 5, 5]],
#<
[[4, 4, 5, 5, 5], [4, 4, 5, 5, 5], [5, 5, 5, 5, 5], [5, 5, 5, 5, 5], [5, 5, 5, 5, 5]],
#>=
[[4, 4, 5, 5, 5], [4, 4, 5, 5, 5], [5, 5, 5, 5, 5], [5, 5, 5, 5, 5], [5, 5, 5, 5, 5]],
#<=
[[4, 4, 5, 5, 5], [4, 4, 5, 5, 5], [5, 5, 5, 5, 5], [5, 5, 5, 5, 5], [5, 5, 5, 5, 5]],
#!=
[[4, 4, 4, 4, 4], [4, 4, 4, 4, 4], [4, 4, 4, 4, 4], [4, 4, 4, 4, 4], [4, 4, 4, 4, 4]],
#==
[[4, 4, 4, 4, 4], [4, 4, 4, 4, 4], [4, 4, 4, 4, 4], [4, 4, 4, 4, 4], [4, 4, 4, 4, 4]]
]

type_dict = {
    "INTT": 0,
    "FLOATT": 1,
    "CHARR": 2,
    "STRINGG": 3,
    "TRUE": 4,
    "FALSE": 4
}

#1D(Operator(arrnum))-> 0-+, 1--, 2-/, 3-*,4- >, 5- <, 6- >=, 7- <=, 8- !=, 9- ==
oper_dict = {
    "+": 0,
    "-": 1,
    "/": 2,
    "*": 3,
    ">": 4,
    "<": 5,
    ">=": 6,
    "<=": 7,
    "!=": 8,
    "==": 9
}

def get_id(type, value):
    return "id"+str(value), type_dict[type]

def next_temp():
    return 1

var_table = {
    "main" : []
}

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

def p_decfuncion(p):
    'decfuncion : FUNCTION tipo ID LPAREN parametro RPAREN bloque'
    p[0] = p[1]
    
def p_parametro(p):
    """parametro : tipo decid parametros
                | empty"""
    p[0] = p[1]

def p_parametros(p):
    """parametros : COMA tipo decid parametros
                | empty"""
    
def p_decid(p):
    'decid : ID decarreglo'
    p[0] = p[1]

def p_decarreglo:
    """decarreglo : LBRAQUET INTT RBRAQUET decarreglo
                | empty"""

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
    '''funcyvar : decfuncion
                | decvariable'''
    p[0] = p[1]

    
def p_instruccion(p):
    """instruccion : decvariable
                | condicion
                | asignacion_usofuncion
                | loop
                | bloque
                | return"""
    p[0] = p[1]
    
def p_decvariable(p):
    'decvariable : tipo ids PUNTOYCOMA'
    for v in p[2]:
        var_table['main'].append({'name' : v,
                                'type' : p[1]})
    p[0] = p[1]


def p_ids(p):
    'ids: decid variosids'
    p[0] = p[2].append()

def p_variosids(p):
    """ids : COMA ids
            | empty"""
    if p[1] == None:
        p[0] = []
    else:
        p[0] = p[2]

        
def p_condicion_parte1(p):
    'condicion_parte1 : IF LPAREN expresion RPAREN'
    condicion = PilaO[-1]
    PilaO.pop()
    tipo_c = PilaTipos[-1]
    PilaTipos.pop()
    if tipo_c != 4:
        print("ERROR!! la expresion en el if no es boolena")
    else:
        Cuadruplos.append(['gotoF', condicion,"_", "_"])
        PilaSaltos.append(len(Cuadruplos)-1)
    p[0] = p[1]

def p_condicion(p):
    'condicion :  condicion_parte1 bloque bloqueelse'
    destino = PilaSaltos[-1]
    PilaSaltos.pop()
    Cuadruplos[destino][3] = len(Cuadruplos)
    p[0] = p[1]


def p_bloqueelse(p):
    """bloqueelse : ELSE bloque
            | empty"""
    Falso = PilaSaltos[-1]
    PilaSaltos.pop()
    Cuadruplos.append(["goto","_","_","_"])
    PilaSaltos.append(len(Cuadruplos)-1)
    Cuadruplos[Falso][3] = len(Cuadruplos)
    p[0] = p[1]

def p_while_1(p):
    'while_1 : WHILE'
    PilaSaltos.append(len(Cuadruplos))
    p[0] = p[1]

def p_while_2(p):
    'while_2 : LPAREN expresion RPAREN'
    tipo_c = PilaTipos[-1]
    PilaTipos.pop()
    if tipo_c != 0 or tipo_c != 1:
        print("ERROR!! la expresion en el if no es numerico")
    Cuadruplos.append(['gotoF', PilaO[-1], " ", '_'])
    PilaO.pop()
    PilaSaltos.append(len(Cuadruplos)-1)
    p[0] = p[1]

def p_while(p):
    'while : while_1 while_2 bloque'
    Salida = PilaSaltos[-1]
    PilaSaltos.pop()
    Regreso = PilaSaltos[-1]
    PilaSaltos.pop()
    Cuadruplos.append('goto', " ", " ", Regreso)
    Cuadruplos[Salida][3] = len(Cuadruplos)
    p[0] = p[1]

def p_asignacion_usofuncion(p):
    'asignacion_usofuncion : ID asiguso'
    p[0] = p[1]
    
def p_asiguso(p):
    """asiguso : asignacion 
            | usofuncion"""
    p[0] = p[1]
    
def p_asignacion(p):
    'asignacion : IGUAL expresion PUNTOYCOMA'
    p[0] = p[1]
    
def p_usofuncion(p):
    'usofuncion : LPAREN expresiones RPAREN PUNTOYCOMA'
    p[0] = p[1]
    
def p_expresiones(p):
    """expresiones : expresion expresionesvarias
            | empty"""
    p[0] = p[1]
    
def p_expresionesvarias(p):
    """expresionesvarias : COMA expresion expresionesvarias
            | empty"""
    p[0] = p[1]    

def p_tipo(p):
    '''type : INT
            | FLOAT
            | CHAR
            | BOOL
            | STRING'''    

def p_return(p):
    'return : RETURN expresion PUNTOYCOMA'
    p[0] = p[1]



"""
def p_for(p):
    'for : FOR LPAREN id asignacion expresion PUNTOYCOMA expresion RPAREN bloque'
    #Esto va justo después del for, en id
    PilaSaltos.append(len(Cuadruplos)-1)
    tipo_c = PilaTipos[-1]
    PilaTipos.pop()
    if tipo_c != 0 or tipo_c != 1:
        print("ERROR!! la expresion en el if no es numerico")

    #Esto por expresion1
    expresion = PilaO[-1]
    PilaO.pop()
    tipo_c = PilaTipos[-1]
    PilaTipos.pop()
    if tipo_c != 0 or tipo_c != 1:
        print("ERROR!! la expresion en el if no es numerico")
    else:
        vcontrol = PilaO[-1]
        tipo_control = PilaTipos[-1]
        tipo_res = ['=', tipo_control, tipo_c]
        if tipo_res == ERROR:
            print("ERROR!! Los tipos de variables no coinciden")
        else:
            Cuadruplos.append(['=', expresion, vcontrol])

    #esto despues de segunda expresion
    tipo_c = PilaTipos[-1]
    PilaTipos.pop()
    if tipo_c != 0 or tipo_c != 1:
        print("ERROR!! la expresion en el if no es numerico")
    else:
        vfinal = vcontrol
        expresion = PilaO[-1]
        PilaO.pop()
        Cuadruplos.append(['=', expresion, ' ', vfinal])
        Cuadruplos.append('MENORQUE', vcontrol, vfinal, 'T'+expresion)
        PilaSaltos.append(len(Cuadruplos)-1)
        Cuadruplos.append(['gotoF', 'T'+expresion, ' ', '_'])
        PilaSaltos.append(len(Cuadruplos)-1)

    #fin de la expresion
    Cuadruplos.append(['PLUS', vcontrol, 1, 'T'+(expresion + vfinal)])
    Cuadruplos.append(['=', 'T'+(expresion + vfinal), ' ', vcontrol])
    Cuadruplos.append(['=', 'T'+(expresion + vfinal), ' ', PilaO[-1]])
    Cuadruplos.append(['goto', PilaSaltos[-1]])
    PilaSaltos.pop()
    Cuadruplos[PilaSaltos[-1]][3] = len(Cuadruplos)
    PilaO.pop()
    PilaTipos.pop()
"""

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
    """m_escritura : COMA expresion resultado
                | empty"""
    if p[0] == ',':
        Cuadruplos.append(['print', " ", " ", PilaO[-1]])
        PilaO.pop()
    p[0] = p[1]

def p_expresion(p):
    'expresion : expresion_2 posexp'
    p[0] = p[1]

def p_expresion_2(p):
    'expresion_2 : exp'
    if OpStack[-1] == ">" or OpStack[-1] == "<" or OpStack[-1] == "!":
        operDer = OpStack[-1]
        OpStack.pop()
        tipoDer = PilaTipos[-1]
        PilaTipos.pop()
        operIzq = OpStack[-1]
        OpStack.pop()
        tipoIzq = PilaTipos[-1]
        PilaTipos.pop()
        operador = OpStack[-1]
        OpStack.pop()
        tipoRes = semantico[tipoIzq, tipoDer, oper_dict[operador]]
        if tipoRes != 5:
            result = next_temp()
            Cuadruplos.append([operador, operIzq, operDer, result])
            PilaO.append(result)
            PilaTipos.append(tipoRes)
        else:
            print("Error, El tipo de operador esta cuacho")
    p[0] = p[1]

def p_posexp(p):
    """posexp : symexp exp
            | empty"""
    p[0] = p[1]

def p_symexp(p):
    """symexp : MAYORQUE
            | MENORQUE | DIFERENT """
    OpStack.append(p[1].value)
    p[0] = p[1]

def p_exp(p):
    'exp : exp_2 mexp'
    p[0] = p[1]

def p_exp_2(p):
    'exp_2 : termino'
    if OpStack[-1] == "+" or OpStack[-1] == "-":
        operDer = OpStack[-1]
        OpStack.pop()
        tipoDer = PilaTipos[-1]
        PilaTipos.pop()
        operIzq = OpStack[-1]
        OpStack.pop()
        tipoIzq = PilaTipos[-1]
        PilaTipos.pop()
        operador = OpStack[-1]
        OpStack.pop()
        tipoRes = semantico[tipoIzq, tipoDer, oper_dict[operador]]
        if tipoRes != 5:
            result = next_temp()
            Cuadruplos.append([operador, operIzq, operDer, result])
            PilaO.append(result)
            PilaTipos.append(tipoRes)
        else:
            print("Error, El tipo de operador esta cuacho")
    p[0] = p[1]

def p_mexp(p):
    """mexp : sumres exp
            | empty"""
    p[0] = p[1]

def p_sumres(p):
    """sumres : PLUS 
            | MINUS"""
    OpStack.append(p[1].value)
    p[0] = p[1]

def p_termino(p):
    'termino : termino_2 mtermino'
    p[0] = p[1]

def p_termino_2(p):
    'termino_2: factor'
    if OpStack[-1] == "*" or OpStack[-1] == "/":
        operDer = OpStack[-1]
        OpStack.pop()
        tipoDer = PilaTipos[-1]
        PilaTipos.pop()
        operIzq = OpStack[-1]
        OpStack.pop()
        tipoIzq = PilaTipos[-1]
        PilaTipos.pop()
        operador = OpStack[-1]
        OpStack.pop()
        tipoRes = semantico[tipoIzq, tipoDer, oper_dict[operador]]
        if tipoRes != 5:
            result = next_temp()
            Cuadruplos.append([operador, operIzq, operDer, result])
            PilaO.append(result)
            PilaTipos.append(tipoRes)
        else:
            print("Error, El tipo de operador esta cuacho")
    p[0] = p[1]

def p_mtermino(p):
    """mtermino : multdiv termino
                | empty"""
    p[0] = p[1]

def p_multdiv(p):
    """multdiv : TIMES
            | DIVIDE"""
    OpStack.append(p[1].value)
    p[0] = p[1]

def p_factor(p):
    """factor : LPAREN expresion RPAREN
            | sumresvac var_cte"""
    if p[1].value == "-":
        pass
    p[0] = p[1]

def p_sumresvac(p):
    """sumresvac : sumres
                | empty"""
    p[0] = p[1]

def p_var_cte(p):
    """var_cte : usoid
                | INTT
                | FLOATT
                | usofuncion"""
    PilaO.append[get_id(p[1].type, p[1].value)]
    p[0] = p[1]

def p_usoid(p):
    'usoid : ID usoid2'
    p[0] = p[1]

def p_usoid2(p):
    """usoid2 : PUNTO ID usoid3 usoid2
                | empty"""
    p[0] = p[1]

def p_usoid3(p):
    """usoid3 : LPAREN fvarsu RPAREN
                | empty"""
    p[0] = p[1]

def p_empty(p):
    'empty :'
    p[0] = None

start = 'programa'

def p_error(p):
    print("Syntax error")

parser = yacc.yacc(debug = True) 

while True:
   try:
       s = input('calc > ')
   except EOFError:
       break
   if not s: continue
   result = parser.parse(s)
   print(result)
