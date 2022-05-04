#
# Sofia Recinos Dorst  A01657055
# Ulrich Nuño Tapia  A00821805

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
cubo_sintactico = [
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

var_table = {
    "main" : []
}

def p_programa(p):
    'programa : START progvars'
    p[0] = p[1] 

def p_progvars(p):
    """progvars : progvar progvars
                | empty"""
    p[0] = p[1]

def p_progvar(p):
    """progvar : decfuncion 
                | instruccion
                | clase"""
    p[0] = p[1]

def p_instruccion(p):
    """instruccion : vars
                | condicion
                | usofuncion
                | loop
                | bloque
                | return
                | asignacion"""
    p[0] = p[1]

def p_clase(p):
    'clase : CLASS ID bloquec'
    p[0] = p[1]

def p_bloquec(p):
    'bloquec : LCORCHETE cbloquec RCORCHETE'
    p[0] = p[1]

def p_cbloquec(p):
    """cbloquec : cbloquec2 cbloquec
            | empty"""
    p[0] = p[1]

def p_cbloquec2(p):
    '''cbloquec2 : decfuncion
                | vars'''
    p[0] = p[1]

def p_type(p):
    '''type : INT
            | FLOAT
            | CHAR
            | BOOL
            | STRING'''

def p_vars(p):
    'vars : type ID ids'
    var_table['main'].append({'name' : p[2]
                              'type' : p[1]})
    p[0] = p[1]

def p_ids(p):
    """ids : COMA ID ids
            | empty"""
    p[0] = p[1]

def p_return(p):
    'return : RETURN expresion PUNTOYCOMA'
    p[0] = p[1]

def p_decfuncion(p):
    'decfuncion : FUNCTION ID LPAREN fvars RPAREN bloque'
    p[0] = p[1]

def p_usofuncion(p):
    'usofuncion : FUNCTION ID LPAREN fvarsu RPAREN PUNTOYCOMA'
    p[0] = p[1]

def p_fvars(p):
    """fvars : ID ids
            | empty"""
    p[0] = p[1]

def p_fvarsu(p):
    """fvarsu : expresion fvarsus
            | empty"""
    p[0] = p[1]

def p_fvarsus(p):
    """fvarsus : COMA expresion fvarsus
            | empty"""
    p[0] = p[1]

def p_loop(p):
    'loop : FOR LPAREN asignacion expresion PUNTOYCOMA expresion RPAREN bloque'
    p[0] = p[1]

def p_bloque(p):
    'bloque : LCORCHETE instrucciones RCORCHETE'
    p[0] = p[1]

def p_instrucciones(p):
    """instrucciones : instruccion instrucciones
                    | empty"""
    p[0] = p[1]

def p_asignacion(p):
    'asignacion : ID IGUAL expresion PUNTOYCOMA'
    p[0] = p[1]

def p_escritura(p):
    'escritura : PRINT LPAREN pescritura m_escritura RPAREN PUNTOYCOMA'
    p[0] = p[1]

def p_pescritura(p):
    """pescritura : expresion 
        | STRINGG"""
    p[0] = p[1]

def p_m_escritura(p):
    """m_escritura : COMA pescritura m_escritura
                | empty"""
    p[0] = p[1]

def p_expresion(p):
    'expresion : exp posexp'
    p[0] = p[1]

def p_posexp(p):
    """posexp : symexp exp
            | empty"""
    p[0] = p[1]

def p_symexp(p):
    """symexp : MAYORQUE
            | MENORQUE may"""
    p[0] = p[1]

def p_may(p):
    """may : MAYORQUE
        | empty"""
    p[0] = p[1]

def p_exp(p):
    'exp : termino mexp'
    p[0] = p[1]

def p_mexp(p):
    """mexp : sumres exp
            | empty"""
    p[0] = p[1]

def p_sumres(p):
    """sumres : PLUS 
            | MINUS"""
    if OpStack[-1] == 'PLUS' | 'MINUS':
        VP.append(VP[-1])
        VP.pop()
    OpStack.append(p[1])
    p[0] = p[1]

def p_termino(p):
    'termino : factor mtermino'
    p[0] = p[1]

def p_mtermino(p):
    """mtermino : multdiv termino
                | empty"""
    p[0] = p[1]

def p_multdiv(p):
    """multdiv : TIMES
            | DIVIDE"""
     if OpStack[-1] == 'TIMES' | 'DIVIDE':
        VP.append(VP[-1])
        VP.pop()
    OpStack.append(p[1])
    p[0] = p[1]

def p_factor(p):
    """factor : LPAREN expresion RPAREN
            | sumresvac var_cte"""
    p[0] = p[1]

def p_sumresvac(p):
    """sumresvac : sumres
                | empty"""
    p[0] = p[1]

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
    'condicion :  condicion_parte1 bloque else'
    destino = PilaSaltos[-1]
    PilaSaltos.pop()
    Cuadruplos[destino][3] = len(Cuadruplos)
    p[0] = p[1]


def p_else(p):
    """else : ELSE bloque
            | empty"""
    Falso = PilaSaltos[-1]
    PilaSaltos.pop()
    Cuadruplos.append(["goto","_","_","_"])
    PilaSaltos.append(len(Cuadruplos)-1)
    Cuadruplos[Falso][3] = len(Cuadruplos)
    p[0] = p[1]

def p_var_cte(p):
    """var_cte : usoid
                | INTT
                | FLOATT
                | usofuncion"""
    VP.append(p[1])
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
    pass

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