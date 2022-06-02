arreglo= [{"hola": 3}, {"2": 2}]

def fun ():
    return arreglo [0]
dicc = fun()
dicc["dos"] = 2
print(arreglo)

for n in arreglo:
    n["nuevo"] = "si"

print(arreglo)
