   # ------------------------------------------------------------
# calclex.py
#
# tokenizer for a simple expression evaluator for
# numbers and +,-,*,/
#
# Sofia Recinos Dorst  A01657055
# Ulrich Nuño Tapia  A00821805
# ------------------------------------------------------------

import ply.lex as lex

reserved = {
   'start' : 'START',
   'if' : 'IF',
   'else' : 'ELSE',
   'while' : 'WHILE',
   'class' : 'CLASS',
   'void' : 'VOID',
   'print' : 'PRINT',
   'read' : 'READ',
   'function' : 'FUNCTION',
   'int' : 'INT',
   'float' : 'FLOAT',
   'string' : 'STRING',
   'bool' : 'BOOL',
   'true' : 'TRUE',
   'false' : 'FALSE',
   'return' : 'RETURN',
   'end' : 'END'

}


# List of token names.   This is always required
tokens = [
   'PLUS',
   'MINUS',
   'TIMES',
   'DIVIDE',
   'LPAREN',
   'RPAREN',
   'ID',
   'PUNTOYCOMA',
   'LBRAQUET',
   'RBRAQUET',
   'LCORCHETE',
   'RCORCHETE',
   'COMA',
   'PUNTO',
   'DIFERENT',
   'MENORQUE',
   'MAYORQUE',
   'IGUAL',
   'STRINGG',
   'FLOATT',
   'INTT'
   

] + list(reserved.values())

# Regular expression rules for simple tokens
t_PLUS    = r'\+'
t_MINUS   = r'-'
t_TIMES   = r'\*'
t_DIVIDE  = r'/'
t_LPAREN  = r'\('
t_RPAREN  = r'\)'
t_PUNTOYCOMA = r'\;'
t_LBRAQUET = r'\['
t_RBRAQUET = r'\]'
t_LCORCHETE = r'\{'
t_RCORCHETE = r'\}'
t_COMA = r'\,'
t_PUNTO = r'\.'
t_DIFERENT = r'\!'
t_MENORQUE = r'\<'
t_MAYORQUE = r'\>'
t_IGUAL = r'\='
t_STRINGG = r'\".*?\"'


# Check for reserved words
def t_FLOATT(t):
    r'[0-9]*\.[0-9]+'
    t.value = float(t.value)  
    return t

def t_INTT(t):
    r'[0-9]+'
    t.value = int(t.value)  
    return t

    # Check for reserved words
def t_ID(t):
    r'[a-zA-Z_][a-zA-Z_0-9]*'
    t.type = reserved.get(t.value,'ID')    
    return t

# Define a rule so we can track line numbers
def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

# A string containing ignored characters (spaces and tabs)
t_ignore  = ' \t'

# Error handling rule
def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)

# Build the lexer
lexer = lex.lex()

# Test it out 1
data = '''
3 + 4 * 10
  + -20 *2.34
  "hola no se"
'''

#Test it out 2
data2 = '''
start
int x ;
x = 1 ;
while(x < 2)
{
    int y ;
    y = 1 ;
}
end
'''

# Give the lexer some input
lexer.input(data)
lexer.input(data2)

# Tokenize
while True:
    tok = lexer.token()
    if not tok:
        break      # No more input
    print(tok)
