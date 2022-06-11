# Sofia Recinos Dorst  A01657055
# Ulrik Nuño Tapia  A00821805

from sintaxis import *

import sys

if len(sys.argv) != 2:
	print("Falta nombre del archivo")
	exit()

file_name = sys.argv[1]

compila(file_name)


TablaMemoria_globales = {'int' : [0]* DirFunc["global"]["direcciones"]["int"], 
							'float' : [0]* (DirFunc["global"]["direcciones"]["float"] - 250), 
							'string' : [""]* (DirFunc["global"]["direcciones"]["string"] - 500), 
							'bool' : [False]* (DirFunc["global"]["direcciones"]["bool"] - 750),
							'arr' : [-1]* (DirFunc["global"]["direcciones"]["arr"] - 5000)}


TablaMemoria_tempGlobales = {'int' : [0]* (DirFunc["global"]["direcciones_temporales"]["int"]-2000), 
							'float' : [0]* (DirFunc["global"]["direcciones_temporales"]["float"] - 2250), 
							'string' : [""]* (DirFunc["global"]["direcciones_temporales"]["string"] - 2500), 
							'bool' : [False]* (DirFunc["global"]["direcciones_temporales"]["bool"] - 2750)}

pilaTablaMemoria_Locales = [] 
pilaTablaMemoria_Locales_temp = [] 
PilaFunciones = [ ]
PilaPosiciones = [ ]

Cuadruplos = []


with open(file_name+'.geist','r') as filegeist:   
 while(True):  
  
  line = filegeist.readline()
  if not line:
   break;
  line = line.strip()[1:-1]
  line_parts = line.split(', ')
  cuadruplo_final = []
  for i in line_parts:
    if i[0] == "'":
      cuadruplo_final.append(i[1:-1])
    else:
      cuadruplo_final.append(int(i))
  Cuadruplos.append(cuadruplo_final)
  


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

def get_tipo_dir(direccion):
	numero_tipo = direccion%1000
	if numero_tipo < 250 :
		return "int" 
	elif numero_tipo < 500 :
		return "float" 
	elif numero_tipo < 750 :
		return "string" 
	elif numero_tipo < 1000 :
		return "bool" 

def get_posicion_dir(direccion):
	numero_posicion = direccion%1000
	if numero_posicion < 250 :
		return numero_posicion 
	elif numero_posicion < 500 :
		return numero_posicion - 250
	elif numero_posicion < 750 :
		return numero_posicion - 500
	elif numero_posicion < 1000 :
		return numero_posicion - 750

def get_element(direccion):
	tipo_memoria = direccion//1000
	tipo = get_tipo_dir(direccion)
	posicion = get_posicion_dir(direccion)
	if tipo_memoria == 0 :
		return TablaMemoria_globales[tipo][posicion]
	if tipo_memoria == 1 :
		return pilaTablaMemoria_Locales[-1][tipo][posicion]
	if tipo_memoria == 2 :
		return TablaMemoria_tempGlobales[tipo][posicion]
	if tipo_memoria == 3 :
		return pilaTablaMemoria_Locales_temp[-1][tipo][posicion]
	if tipo_memoria == 4 :
		return TablaMemoria_CTEs[tipo][posicion]
	if tipo_memoria == 5 :
                if direccion-5000 < 250:
                    return get_element(TablaMemoria_globales['arr'][direccion-5000])
                else:
                    #print("real::", pilaTablaMemoria_Locales[-1]['arr'][direccion-5250])
                    return get_element(pilaTablaMemoria_Locales[-1]['arr'][direccion-5250])

def assign_value(direccion, value):
	tipo_memoria = direccion//1000
	tipo = get_tipo_dir(direccion)
	posicion = get_posicion_dir(direccion)

	if tipo_memoria == 0 :
		TablaMemoria_globales[tipo][posicion] = value
	if tipo_memoria == 1 :
		pilaTablaMemoria_Locales[-1][tipo][posicion] = value
	if tipo_memoria == 2 :
		TablaMemoria_tempGlobales[tipo][posicion] = value
	if tipo_memoria == 3 :
		#print(pilaTablaMemoria_Locales_temp[-1],[tipo],[posicion])
		pilaTablaMemoria_Locales_temp[-1][tipo][posicion] = value
	if tipo_memoria == 4 :
		TablaMemoria_CTEs[tipo][posicion] = value 
	if tipo_memoria == 5 :
                if direccion-5000 < 250:
                    assign_value(TablaMemoria_globales['arr'][direccion-5000], value) #1007
                else:
                    #print("real:::", pilaTablaMemoria_Locales[-1]['arr'][direccion-5250])
                    assign_value(pilaTablaMemoria_Locales[-1]['arr'][direccion-5250], value)

#Para arreglos
def direct_assign_value(direccion, value):
	tipo_memoria = direccion//1000
	tipo = get_tipo_dir(direccion)
	posicion = get_posicion_dir(direccion)

	if tipo_memoria == 0 :
		TablaMemoria_globales[tipo][posicion] = value
	if tipo_memoria == 1 :
		pilaTablaMemoria_Locales[-1][tipo][posicion] = value
	if tipo_memoria == 2 :
		TablaMemoria_tempGlobales[tipo][posicion] = value
	if tipo_memoria == 3 :
		#print(pilaTablaMemoria_Locales_temp[-1],[tipo],[posicion])
		pilaTablaMemoria_Locales_temp[-1][tipo][posicion] = value
	if tipo_memoria == 4 :
		TablaMemoria_CTEs[tipo][posicion] = value 
	if tipo_memoria == 5 :
		if direccion-5000 < 250:
			TablaMemoria_globales['arr'][direccion-5000] = int(value) #80
		else:
			#print(pilaTablaMemoria_Locales[-1]['arr'][direccion-5250])
			#print(int(value))
			pilaTablaMemoria_Locales[-1]['arr'][direccion-5250] = int(value)


def assign_parametro(direccion, value):
	tipo_memoria = direccion//1000
	tipo = get_tipo_dir(direccion)
	posicion = get_posicion_dir(direccion)

	if tipo_memoria == 0 :
		TablaMemoria_globales[tipo][posicion] = value
	if tipo_memoria == 1 :
		sig_TablaMemoria_Locales[tipo][posicion] = value
	if tipo_memoria == 2 :
		TablaMemoria_tempGlobales[tipo][posicion] = value
	if tipo_memoria == 3 :
		sig_TablaMemoria_Locales_temp[tipo][posicion] = value
	if tipo_memoria == 4 :
		TablaMemoria_CTEs[tipo][posicion] = value 
	if tipo_memoria == 5 :
                if direccion-5000 < 250:
                    return get_element(TablaMemoria_globales['arr'][direccion-5000])
                else:
                    return get_element(sig_TablaMemoria_Locales['arr'][direccion-5250])


sig_TablaMemoria_Locales = { }
sig_TablaMemoria_Locales_temp = { }
sig_funcion = ""

def Era(nameFunction):
	global sig_funcion
	global sig_TablaMemoria_Locales
	global sig_TablaMemoria_Locales_temp
	info_funcion = DirFunc[nameFunction]
	sig_TablaMemoria_Locales = {'int' : [0]*(info_funcion["direcciones"]["int"]-1000), 
    								'float' : [0]*(info_funcion["direcciones"]["float"]-1250), 
    								'string' : [""]*(info_funcion["direcciones"]["string"]-1500), 
    								'bool' : [False]*(info_funcion["direcciones"]["bool"]-1750) ,
    								'arr' : [0]*(info_funcion["direcciones"]["arr"]-5250)}

	sig_TablaMemoria_Locales_temp = {'int' : [0]*(info_funcion["direcciones_temporales"]["int"]-3000) , 
    								'float' : [0]*(info_funcion["direcciones_temporales"]["float"]-3250), 
    								'string' : [""]*(info_funcion["direcciones_temporales"]["string"]-3500), 
    								'bool' : [False]*(info_funcion["direcciones_temporales"]["bool"]-3750)}
	PilaFunciones.append(nameFunction)



def GoSub():
	global sig_funcion
	pilaTablaMemoria_Locales.append(sig_TablaMemoria_Locales)
	pilaTablaMemoria_Locales_temp.append(sig_TablaMemoria_Locales_temp)
	

posicion = 0 
Era("main")
GoSub()

while True:
	instruccion = Cuadruplos[posicion]
	#print(instruccion)
	if instruccion[0] == "+":
		# + , OpIzq, OpDer, Direccion_Destino
		try:
			assign_value(instruccion[3], get_element(instruccion[1]) + get_element(instruccion[2]))
			posicion += 1
		except Exception as e:
			print(e)
			exit()

	elif instruccion[0] == "Dir+ValDirecto":
		# Dir+ValDirecto , OpIzq, OpDer(Directo), Direccion_Destino
		try:
			direct_assign_value(instruccion[3], get_element(instruccion[1]) + instruccion[2])
			posicion += 1
		except Exception as e:
			print(e)
			exit()

	elif instruccion[0] == "Dir*ValDirecto":
		# Dir*ValDirecto , OpIzq, OpDer(Directo), Direccion_Destino
		try:
			assign_value(instruccion[3], get_element(instruccion[1]) * instruccion[2])
			posicion += 1
		except Exception as e:
			print(e)
			exit()

	elif instruccion[0] == "-":
		# - , OpIzq, OpDer, Direccion_Destino
		try:
			assign_value(instruccion[3], get_element(instruccion[1]) - get_element(instruccion[2]))
			posicion += 1
		except Exception as e:
			print(e)
			exit()
	elif instruccion[0] == "*":
		# * , OpIzq, OpDer, Direccion_Destino
		try:
			assign_value(instruccion[3], get_element(instruccion[1]) * get_element(instruccion[2]))
			posicion += 1
		except Exception as e:
			print(e)
			exit()
	elif instruccion[0] == "/":
		# / , OpIzq, OpDer, Direccion_Destino
		try:
			assign_value(instruccion[3], get_element(instruccion[1]) / get_element(instruccion[2]))
			posicion += 1
		except Exception as e:
			print(e)
			exit()
	elif instruccion[0] == "<":
		# < , OpIzq, OpDer, Direccion_Destino
		try:
			assign_value(instruccion[3], get_element(instruccion[1]) < get_element(instruccion[2]))
			posicion += 1
		except Exception as e:
			print(e)
			exit()
	elif instruccion[0] == ">":
		# > , OpIzq, OpDer, Direccion_Destino
		try:
			assign_value(instruccion[3], get_element(instruccion[1]) > get_element(instruccion[2]))
			posicion += 1
		except Exception as e:
			print(e)
			exit()
	elif instruccion[0] == "==":
		# == , OpIzq, OpDer, Direccion_Destino
		try:
			assign_value(instruccion[3], get_element(instruccion[1]) == get_element(instruccion[2]))
			posicion += 1
		except Exception as e:
			print(e)
			exit()
	elif instruccion[0] == "!=":
		# != , OpIzq, OpDer, Direccion_Destino
		try:
			assign_value(instruccion[3], get_element(instruccion[1]) != get_element(instruccion[2]))
			posicion += 1
		except Exception as e:
			print(e)
			exit()
	elif instruccion[0] == "=":
		# = , Direccion, , Direccion_Destino
		try:
			assign_value(instruccion[3], get_element(instruccion[1]) )
			posicion += 1
		except Exception as e:
			print(e)
			exit()

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
		#GOSUB, name, , Dirini
		PilaPosiciones.append(posicion + 1)
		posicion = instruccion[3]
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
		assign_parametro(info_param["direccion"], get_element(instruccion[1]))
		posicion +=1

	elif instruccion[0] == "VER" :
		#VER, direccion, Liminf, Limsup
		if(get_element(instruccion[1]) < instruccion[2] or get_element(instruccion[1]) > instruccion[3]):
			print("“Error, exceso de dimensiones en el arreglo”")
			exit()
		else:
			posicion += 1

	elif instruccion[0] == "print" :
		print(get_element(instruccion[3]))
		posicion += 1

	elif instruccion[0] == "read" :
		try:
			Nameinput = input("cin>> ")
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
			#print(instruccion, Nameinput)
			assign_value(instruccion[3], Nameinput)
		except Exception as e:
			print(e)
			exit()
		posicion += 1

	elif instruccion[0] == "ENDPROG":
		break;
