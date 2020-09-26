import csv #importamos la librería csv
with open("synergy_logistics_database.csv","r" ) as archivo_csv:#Primero cargamos el archivo que vamos a utilizar
    desicion=0 #declaramos una variable que nos ayudará llevar el control de lo quiera hacer el usuario
    while desicion!="5": #estructura while para saber que querrá hacer el usuario
        desicion=input("""Bienvenido, por favor elige una de las siguentes opciones: 
        1. Porporción del valor total de las exportaciones e importaciones año con año
        2. Tops 10 de rutas por exportaciones e importaciones
        3. Tops 3 de medios de transporte por exportaciones e importaciones
        4. Listados de países con el 80% de las exportaciones e importaciones
        5. Salir
        """)#print para mostrar al usuario las opciones que puede llebvar a cabo
        def funcion_proyecto(filtro1,valor_filtro1,filtro2,valor_filtro2,llave,base_dict,orden): #creamos función para que mida 3 métricas de acuerdo a la llave que ingresemos
            #Explicación de los parámetros:
            #filtro1= Se indica el campo sobre el que se aplicará el valor del filtro 1
            #valor_filtro1= Se indica el valor del que querremos obtener resultados 
            #filtro2= análogo a filtro1
            #valor_filtro2= análogo a valor_filtro1
            #llave: aquí se ingresará una función lambda que indicará como vamos a agrupar nuestros datos de acuerdo al nombre de las columnas, por ejemplo lambda x:x["origin"]+x["year"] indica que se agruparan los datos por orígen y año
            #base_dict= es la base sobre la que se trabajará
            #orden: se calculan 3 métricas, número de operaciones, su valor total y su valor promedio, si en orden se pone 0 ordenará de mayor a menor de acuerdo al número de operaciones, si se pone 1 hará lo mismo pero por valor total de las operaciones y con 2 por su valor promedio 
        
            archivo_csv.seek(0) #cada vez que se usa la función, regresa el respectivo archivo a la posición 0
            conjunto=set() #creamos un conjunto para no tener elementos duplicados en las llaves 
            informacion_rutas=dict()#diccionario donde guardaremos la información recabada del archivo
            tamaño=0 #bandera que medirá cuantas llaves diferentes tenemos
            for linea in base_dict: #for para recorrer todas las líneas del archivo
                if linea[filtro1]==valor_filtro1 or linea[filtro2]==valor_filtro2: #condición para saber si querremos toda la información, solo exportaciones o solo importaciones
                    conjunto.add(llave(linea)) #agregamos la llave, de acuerdo a lo indicado en los parámetros, si es que esa llave no se ha agregado ya
                    if len(conjunto)==tamaño and len(informacion_rutas)!=0:#si el conjunto no está vacío y no se han agregado nuevas llaves, se hace la siguiente instrucción
                        informacion_rutas[llave(linea)][0]+=1 #sumamos uno a la cantidad de operaciones en la respectiva llave
                        informacion_rutas[llave(linea)][1]+=float(linea["total_value"]) #sumamos su respectivo valor total, del registro en turno
                        informacion_rutas[llave(linea)][2]=informacion_rutas[llave(linea)][1]/informacion_rutas[llave(linea)][0]#actualizamos el promedio del valor de las operaciones con los datos obtenidos anteriormente
                    else:#si es la primer llave o una nueva se ejecuta la siguiente instrucción
                        informacion_rutas[llave(linea)]=[1,float(linea["total_value"]),float(linea["total_value"])]#se ingresa 1 al número de operaciones, el valor total de la operación respectiva al registro en turno y el mismo valor para el promedio 
                        tamaño+=1#nuestra bandera suma uno para indicar que ese es el número de llaves hasta el momento
            sorted_informacion_rutas = sorted(informacion_rutas.items(), key=lambda x: x[1][orden], reverse=True) #ordenamos la información obtenida de acuerdo al parámetro "orden", que tiene que ser ingresado por el usuario
            return [sorted_informacion_rutas,informacion_rutas]#la función devuelve la lista ordenada
        total_exportaciones_por_año=dict(funcion_proyecto(filtro1="direction", valor_filtro1="Exports", filtro2="direction", valor_filtro2="Exports",orden=0,llave=lambda linea:linea["year"],base_dict=csv.DictReader(archivo_csv))[0])
        total_importaciones_por_año=dict(funcion_proyecto(filtro1="direction", valor_filtro1="Imports", filtro2="direction", valor_filtro2="Imports",orden=0,llave=lambda linea:linea["year"],base_dict=csv.DictReader(archivo_csv))[0])
        #En las dos líneas anteriores obtenemos el valor total de las operaciones por cada año, con la función creada
        if desicion=="1": #Si el usuario elige 1 se imprimirá la proporción de ingresos totales hechos por las exportaciones e importaciones por cada año
            for año in ["2015", "2016","2017","2018","2019","2020"]: 
                    print("")
                    print("Para el año ", año) 
                    print("Exportaciones ", 100*total_exportaciones_por_año[año][1]/(total_exportaciones_por_año[año][1]+total_importaciones_por_año[año][1]))
                    print("Importaciones ", 100*total_importaciones_por_año[año][1]/(total_exportaciones_por_año[año][1]+total_importaciones_por_año[año][1]))
        elif desicion=="2": #si el usuario elige 2 se imprimirán los top 10 de rutas de acuerdo a las 3 métricas calculadas, filtrado por año, importaciones y exportaciones
            consigna1_exportaciones_top10flujo=funcion_proyecto(filtro1="direction", valor_filtro1="Exports", filtro2="direction", valor_filtro2="Exports",orden=0,llave=lambda linea:linea["origin"]+"-"+ linea["destination"]+" "+linea["year"],base_dict=csv.DictReader(archivo_csv))
            consigna1_exportaciones_top10total_value=funcion_proyecto(filtro1="direction", valor_filtro1="Exports", filtro2="direction", valor_filtro2="Exports",orden=1,llave=lambda linea:linea["origin"]+"-"+ linea["destination"]+" "+linea["year"],base_dict=csv.DictReader(archivo_csv))
            consigna1_exportaciones_top10promedio=funcion_proyecto(filtro1="direction", valor_filtro1="Exports", filtro2="direction", valor_filtro2="Exports",orden=2,llave=lambda linea:linea["origin"]+"-"+ linea["destination"]+" "+linea["year"],base_dict=csv.DictReader(archivo_csv))
            consigna1_importaciones_top10flujo=funcion_proyecto(filtro1="direction", valor_filtro1="Imports", filtro2="direction", valor_filtro2="Imports",orden=0,llave=lambda linea:linea["origin"]+"-"+ linea["destination"]+" "+linea["year"],base_dict=csv.DictReader(archivo_csv))
            consigna1_importaciones_top10total_value=funcion_proyecto(filtro1="direction", valor_filtro1="Imports", filtro2="direction", valor_filtro2="Imports",orden=1,llave=lambda linea:linea["origin"]+"-"+ linea["destination"]+" "+linea["year"],base_dict=csv.DictReader(archivo_csv))
            consigna1_importaciones_top10promedio=funcion_proyecto(filtro1="direction", valor_filtro1="Imports", filtro2="direction", valor_filtro2="Imports",orden=2,llave=lambda linea:linea["origin"]+"-"+ linea["destination"]+" "+linea["year"],base_dict=csv.DictReader(archivo_csv))
            importaciones_por_año=dict(funcion_proyecto(filtro1="direction", valor_filtro1="Imports", filtro2="direction", valor_filtro2="Imports",orden=0,llave=lambda linea:linea["year"],base_dict=csv.DictReader(archivo_csv))[0])
            for año in ["2015", "2016","2017","2018","2019","2020"]:
                print("")
                print("Para el año ", año)
                print("(Clave, [número de operaciones, valor total de las operaciones, valor promedio de las operaciones])")
                for nombre_top10, resultados in zip(["Top 10 por número de exportaciones", "Top 10 por valor total de exportaciones", "Top 10 por promedio del valor total de exportaciones", "Top 10 por número de importaciones", "Top 10 por valor total de importaciones", "Top 10 por promedio del valor total de importaciones"],
                                                   [consigna1_exportaciones_top10flujo[0],consigna1_exportaciones_top10total_value[0],consigna1_exportaciones_top10promedio[0],consigna1_importaciones_top10flujo[0],consigna1_importaciones_top10total_value[0],consigna1_importaciones_top10promedio[0]]): 
                    print("")
                    print(nombre_top10)
                    contador=0
                    for resultado in resultados:
                        if contador==10:
                            break
                        if resultado[0][len(resultado[0])-4:len(resultado[0])]==año:
                            print(resultado)
                            contador+=1
        elif desicion=="3": #si el usuario elige 3 se imprimirán los top 3 de medios de transporte de acuerdo a las 3 métricas calculadas, filtrado por año, importaciones y exportaciones
            consigna2_exportaciones_top3flujo=funcion_proyecto(filtro1="direction", valor_filtro1="Exports", filtro2="direction", valor_filtro2="Exports",orden=0,llave=lambda linea:linea["transport_mode"]+" "+linea["year"],base_dict=csv.DictReader(archivo_csv))
            consigna2_exportaciones_top3total_value=funcion_proyecto(filtro1="direction", valor_filtro1="Exports", filtro2="direction", valor_filtro2="Exports",orden=1,llave=lambda linea:linea["transport_mode"]+" "+linea["year"],base_dict=csv.DictReader(archivo_csv))
            consigna2_exportaciones_top3promedio=funcion_proyecto(filtro1="direction", valor_filtro1="Exports", filtro2="direction", valor_filtro2="Exports",orden=2,llave=lambda linea:linea["transport_mode"]+" "+linea["year"],base_dict=csv.DictReader(archivo_csv))
            consigna2_importaciones_top3flujo=funcion_proyecto(filtro1="direction", valor_filtro1="Imports", filtro2="direction", valor_filtro2="Imports",orden=0,llave=lambda linea:linea["transport_mode"]+" "+linea["year"],base_dict=csv.DictReader(archivo_csv))
            consigna2_importaciones_top3total_value=funcion_proyecto(filtro1="direction", valor_filtro1="Imports", filtro2="direction", valor_filtro2="Imports",orden=1,llave=lambda linea:linea["transport_mode"]+" "+linea["year"],base_dict=csv.DictReader(archivo_csv))
            consigna2_importaciones_top3promedio=funcion_proyecto(filtro1="direction", valor_filtro1="Imports", filtro2="direction", valor_filtro2="Imports",orden=2,llave=lambda linea:linea["transport_mode"]+" "+linea["year"],base_dict=csv.DictReader(archivo_csv))
            
            
            for año in ["2015", "2016","2017","2018","2019","2020"]:
                print("")
                print("Para el año ", año)
                print("[Clave, número de operaciones, valor total de las operaciones, valor promedio de las operaciones, proporción del valor total de las operaciones en el año]")
                tipo=1
                for nombre_top3, resultados in zip(["Top 3 por número de exportaciones", "Top 3 por valor total de exportaciones", "Top 3 por promedio del valor total de exportaciones", "Top 3 por número de importaciones", "Top 3 por valor total de importaciones", "Top 3 por promedio del valor total de importaciones"],
                                                    [consigna2_exportaciones_top3flujo[0],consigna2_exportaciones_top3total_value[0],consigna2_exportaciones_top3promedio[0],consigna2_importaciones_top3flujo[0],consigna2_importaciones_top3total_value[0],consigna2_importaciones_top3promedio[0]]):
                    print("")
                    print(nombre_top3) 
                    contador=0
                    if tipo <4:
                        total=total_exportaciones_por_año
                    else:
                        total=total_importaciones_por_año
                    for resultado in resultados:
                        if contador==3:
                            break
                        if resultado[0][len(resultado[0])-4:len(resultado[0])]==año:
                            print("[",resultado[0],", ",resultado[1][0],", ",resultado[1][1],", ",resultado[1][2],", ",resultado[1][1]/int(total[año][1]),"]")
                            contador+=1
                    tipo+=1
        elif desicion=="4":   #si el usuario elige 4 se mostrarán los países de origen que representen el 80% del valor total de los ingresos, filtrado por año, exportaciones e importaciones
            consigna3_exportaciones_80porciento=funcion_proyecto(filtro1="direction", valor_filtro1="Exports", filtro2="direction", valor_filtro2="Exports",orden=1,llave=lambda linea:linea["origin"]+" "+linea["year"],base_dict=csv.DictReader(archivo_csv))
            consigna3_importaciones_80porciento=funcion_proyecto(filtro1="direction", valor_filtro1="Imports", filtro2="direction", valor_filtro2="Imports",orden=1,llave=lambda linea:linea["origin"]+" "+linea["year"],base_dict=csv.DictReader(archivo_csv))
            
            for año in ["2015", "2016","2017","2018","2019","2020"]:
                print("")
                print("Para el año ", año)
                print("País   proporción")
                for top_80porciento, resultados,total in zip(["Países con 80% de las exportaciones", "Países con 80% de las importaciones"], 
                                                    [consigna3_exportaciones_80porciento[0],consigna3_importaciones_80porciento[0]],[total_exportaciones_por_año, total_importaciones_por_año]):
                    print("")
                    print(top_80porciento)
                    proporcion=0
                    for resultado in resultados:
                        if proporcion>=.8:
                            break
                        if resultado[0][len(resultado[0])-4:len(resultado[0])]==año:
                            print(resultado[0][0:len(resultado[0])-4], " ", float(100*resultado[1][1]/int(total[año][1])),"%")
                            proporcion+=resultado[1][1]/int(total[año][1])
        elif desicion=="5":#si el usuario elige 5 lo sacará del programa
            continue
        else: #si no ingresa ningún valor de los anteriores se imprimirá el siguiente mensaje
            print("Respuesta no válida. Recuerda no poner espacios en tu respuesta y solo ingresar el número de la opción que deseas")
        print("")
        
        
        
        

        
            