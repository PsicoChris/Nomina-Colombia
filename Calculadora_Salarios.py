salario = int(input("ingresa tu salario"))


salario_minimo = 1160000
auxilio_transporte = 140606
uvt = 42412
base_impuestos = float(salario/uvt)
ibc = (salario*40)/100
salud_pension = 28.5/100
cotizacion = ibc*salud_pension
salario_cotizado = salario-cotizacion


tipo_de_salario = int(input("Ingresa 1 para salario nominal y 2 para salario por prestación de servicios"))



if ibc < 1160000:
    ibc = 1160000
else:
    ibc = ibc



if tipo_de_salario == 2:
    if base_impuestos <= 95:
        print("El impuesto es de 0%")
        print("Su salario final es: ")
        print(salario_cotizado)
    elif base_impuestos > 95 and base_impuestos <= 150: 
        salario_final = salario_cotizado - (salario*0.19) - (uvt*10)
        print("El Impuesto es del 19% + 10 UVts")
        print("Su salario es: ")
        print(salario_final)
    elif base_impuestos > 150 and base_impuestos <= 360:
        salario_final = salario_cotizado - (salario*0.28) - (uvt*10)
        print("El Impuesto es del 28% + 10 UVts")
        print("Su salario es: ")
        print(salario_final)
    elif base_impuestos > 360 and base_impuestos <= 640:
        salario_final = salario_cotizado - (salario*0.33) - (uvt*69)
        print("El Impuesto es del 33% + 69 UVts")
        print("Su salario es: ")
        print(salario_final)
    elif base_impuestos > 640 and base_impuestos <= 945:
        salario_final = salario_cotizado - (salario*0.35) - (uvt*162)
        print("El Impuesto es del 35% + 162 UVts")
        print("Su salario es: ")
        print(salario_final)
    elif base_impuestos > 945 and base_impuestos <= 2300:
        salario_final = salario_cotizado - (salario*0.37) - (uvt*268)
        print("El Impuesto es del 37% + 268 UVts")
        print("Su salario es: ")
        print(salario_final)
    else:
        salario_final = salario_cotizado - (salario*0.39) - (uvt*770)
        print("El Impuesto es del 39% +770 UVTs")
        print("Su salario es: ")
        print(salario_final)

elif tipo_de_salario == 1:
    if base_impuestos <= 95:
        print("El impuesto es de 0%")
        print("Su salario final es: ")
        print(salario_cotizado)
    elif base_impuestos > 95 and base_impuestos <= 150: 
        salario_final = salario_cotizado - (salario*0.19) - (uvt*10)
        print("El Impuesto es del 19% + 10 UVts")
        print("Su salario es: ")
        print(salario_final)
    elif base_impuestos > 150 and base_impuestos <= 360:
        salario_final = salario_cotizado - (salario*0.28) - (uvt*10)
        print("El Impuesto es del 28% + 10 UVts")
        print("Su salario es: ")
        print(salario_final)
    elif base_impuestos > 360 and base_impuestos <= 640:
        salario_final = salario_cotizado - (salario*0.33) - (uvt*69)
        print("El Impuesto es del 33% + 69 UVts")
        print("Su salario es: ")
        print(salario_final)
    elif base_impuestos > 640 and base_impuestos <= 945:
        salario_final = salario_cotizado - (salario*0.35) - (uvt*162)
        print("El Impuesto es del 35% + 162 UVts")
        print("Su salario es: ")
        print(salario_final)
    elif base_impuestos > 945 and base_impuestos <= 2300:
        salario_final = salario_cotizado - (salario*0.37) - (uvt*268)
        print("El Impuesto es del 37% + 268 UVts")
        print("Su salario es: ")
        print(salario_final)
    else:
        salario_final = salario_cotizado - (salario*0.39) - (uvt*770)
        print("El Impuesto es del 39% +770 UVTs")
        print("Su salario es: ")
        print(salario_final)
else:
    print("ESTA ESE NÚMERO EN LAS OPCIONES O QUE GONO*****")



print(ibc)
