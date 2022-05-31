# Sofia Recinos Dorst  A01657055
# Ulrich Nuño Tapia  A00821805

from sintaxis import Cuadruplos
from sintaxis import DirFunc
from sintaxis import TablaMemoria_CTEs

TablaMemoria_globales = {'int' : [ ] , 'float' : [ ], 'string' : [ ], 'bool' : [ ]}
TablaMemoria_tempGlobales = {'int' : [ ] , 'float' : [ ], 'string' : [ ], 'bool' : [ ]}

pilaTablaMemoria_Locales = [] 
pilaTablaMemoria_Locales_temp = [] 

PilaFunciones = []

PilaPosiciones = [ ]

print(Cuadruplos)

def get_tipo_dir(direccion):

def get_element(direccion):



def assign_value(direccion, value):
	


sig_TablaMemoria_Locales = { }
sig_TablaMemoria_Locales_temp = { }
sig_funcion = ""

def Era(nameFunction):
	global sig_funcion
	info_funcion = DirFunc[nameFunction]
    sig_TablaMemoria_Locales = {'int' : [0]*(info_funcion[direcciones]["int"]-1000) , 
    								'float' : [0]*(info_funcion[direcciones]["float"]-1250), 
    								'string' : [" "]*[0]*(info_funcion[direcciones]["string"]-1500), 
    								'bool' : [0]*(info_funcion[direcciones]["bool"]-1750)}

    sig_TablaMemoria_Locales_temp = {'int' : [0]*(info_funcion[direcciones]["int"]-3000) , 
    								'float' : [0]*(info_funcion[direcciones]["float"]-3250), 
    								'string' : [" "]*[0]*(info_funcion[direcciones]["string"]-3500), 
    								'bool' : [0]*(info_funcion[direcciones]["bool"]-3750)}
    sig_funcion = nameFunction

def GoSub():
	global sig_funcion
    pilaTablaMemoria_Locales.append(sig_TablaMemoria_Locales)
    pilaTablaMemoria_Locales_temp.append(sig_TablaMemoria_Locales_temp)
    PilaFunciones.append(sig_funcion)


posicion = 0 

while True:
	instruccion = Cuadruplos[posicion]
	if instruccion[0] == "+":
		# + , OpIzq, OpDer, Direccion_Destino
		try:
			assign_value(instruccion[3], get_element(instruccion[1]) + get_element(instruccion[2]))
			posicion += 1
		except exception as e:
			print(e)
	
	elif instruccion[0] == "-":
		# - , OpIzq, OpDer, Direccion_Destino
		try:
			assign_value(instruccion[3], get_element(instruccion[1]) - get_element(instruccion[2]))
			posicion += 1
		except exception as e:
			print(e)

	elif instruccion[0] == "*":
		# * , OpIzq, OpDer, Direccion_Destino
		try:
			assign_value(instruccion[3], get_element(instruccion[1]) * get_element(instruccion[2]))
			posicion += 1
		except exception as e:
			print(e)

	elif instruccion[0] == "/":
		# / , OpIzq, OpDer, Direccion_Destino
		try:
			assign_value(instruccion[3], get_element(instruccion[1]) / get_element(instruccion[2]))
			posicion += 1
		except exception as e:
			print(e)

	elif instruccion[0] == "goto":
		# goto , , , Cuadruplo
		posicion = instruccion[3]

	elif instruccion[0] == "gotoF":
		# gotoF , condicion, , Cuadruplo
		if get_element(instruccion[1]):
			posicion += 1
		else:
			posicion = instruccion[3]

	elif instruccion[0] == "gotoT" :
		# gotoT , condicion, , Cuadruplo
		if get_element(instruccion[1]) :
			posicion = instruccion[3]
		else:
			posicion += 1

	elif instruccion[0] == "GOSUB" :
		#GOSUB, , , name
		PilaPosiciones.append(posicion + 1)
		posicion = DirFunc[instruccion[3]]["DirIni"]
		GoSub()

	elif instruccion[0] == "ERA" :
		#ERA, , , name
		Era(instruccion[3])
		posicion += 1

	elif instruccion[0] == "ENDFUNC" :
		#ENDFUNC, , , 
		PilaFunciones.pop()
		pilaTablaMemoria_Locales.pop()
		pilaTablaMemoria_Locales_temp.pop()
		posicion = PilaPosiciones[-1]
		PilaPosiciones.pop()

	elif instruccion[0] == "PARAM" :
		#PARAM, direccion, , # Param
		info_funcion = DirFunc[PilaFunciones[-1]]
		info_param = info_funcion["local_table"][instruccion[3]]
		assign_value(info_param["direccion"], get_element(instruccion[1]))
		posicion +=1

	elif instruccion[0] == "print" :
		print(get_element[instruccion[3]])
		posicion += 1

	elif instruccion[0] == "read" :
		try:
			Nameinput = input()
			tipo_dir = get_tipo_dir(instruccion[3])
			if tipo_dir == "int":
				Nameinput = int(Nameinput)
			elif tipo_dir == "float":
				Nameinput = float(Nameinput)
			elif tipo_dir == "bool":
				if Nameinput == "false":
					Nameinput = False
				elif Nameinput == "true":
					Nameinput = True
				else:
					print("Error")
					Nameinput = False
			assign_value(instruccion[3], Nameinput)
		except exception as e:
			print(e)
		posicion += 1
























