import time                  #libreria para ocupar funciones de tiempo
from time import sleep       #Modulo para impementar retardos 
import pickle                #libreria para serializar objetos 

import board                 #libreria para manejar el protocolo i2c 
import adafruit_adxl34x      #libreria para leer el sensor adxl 

import json                  #libreria para manejar cadenas de ddatos en formato json  

import sys                   #libreria para tener acceso a funciones del sistema 
import numpy as np           #libreria para manipular datos en forma de arreglos o matrices
import matplotlib.pyplot as plt    #libreria para implementar gráficos

import paho.mqtt.client as paho     #libreria para implementar el protocolo mqtt
broker="broker.emqx.io"             #definición del bloker publico
port=1883                           #puerto de acceso al broker

from mpu6050 import mpu6050         #libreria para leer el sensor mpu6050   
sensor1 = mpu6050(0x69)             #definición de un objeto del sensor mpu6050 con direccion 0x69
sensor2 = mpu6050(0x68)             #definición de un objeto del sensor mpu6050 con direccion 0x68 

v_1 = np.array([0.0])               #definición de arreglo para almacenar datos de la posicion x sensor 1
v_2 = np.array([0.0])               #definición de arreglo para almacenar datos de la posicion y sensor 1
v_3 = np.array([0.0])               #definición de arreglo para almacenar datos de la posicion z sensor 1
v_4 = np.array([0.0])               #definición de arreglo para almacenar datos de la posicion x sensor 2
v_5 = np.array([0.0])               #definición de arreglo para almacenar datos de la posicion y sensor 2
v_6 = np.array([0.0])               #definición de arreglo para almacenar datos de la posicion z sensor 2
v_7 = np.array([0.0])               #definición de arreglo para almacenar datos de la posicion x sensor 3
v_8 = np.array([0.0])               #definición de arreglo para almacenar datos de la posicion y sensor 3
v_9 = np.array([0.0])               #definición de arreglo para almacenar datos de la posicion z sensor 3
frecuenciahz = np.array([0.0])      #definición de arreglo para almacenar el historial de datos de frecuencias  

i2c = board.I2C()                            #definicón del objeto para manejar el protocolo i2c
acelero = adafruit_adxl34x.ADXL345(i2c)      #definición de un objeto del sensor adxl  

def on_publish(client,userdata,result):      #definición de la función para publicar en el broker a traves de mqtt
    print("data published \n")
    pass


def Calibracion(acel):                        #definición de la función de calibracion para el sensor mpu6050
    x_ac = 0                                  #valores iniciales de las variables x, y y z
    y_ac = 0
    z_ac = 0

    for x in range(2):                        #se toma la lectura de 2 valores para establecer un promedio  
        #print(y_ac)
        x_ac = x_ac + acel.get('x')
        y_ac = y_ac + acel.get('y')
        z_ac = z_ac + acel.get('z')
    
    x_p = x_ac/2                              #se toma el promedio de las lecturas del acelerometro en los ejes x, y, z
    y_p = y_ac/2
    z_p = z_ac/2
 
    return(x_p, y_p, z_p)                     #Retorno de los valores x, y, z

def cal_adx():                                 #Función de calibracion para el sensor adxl

    x_ac_adx = 0                               #valores iniciales de las variables x, y y z
    y_ac_adx = 0
    z_ac_adx = 0
    for x in range(2):
                                                                     #se toma la lectura de 2 valores para establecer un promedio 
        x_ac_adx_d, y_ac_adx_d, z_ac_adx_d = acelero.acceleration
        x_ac_adx = x_ac_adx + x_ac_adx_d
        y_ac_adx = y_ac_adx + y_ac_adx_d
        z_ac_adx = z_ac_adx + z_ac_adx_d
        
    x_p_adx = x_ac_adx/2                                             #se toma el promedio de las lecturas del acelerometro en los ejes x, y, z
    y_p_adx = y_ac_adx/2
    z_p_adx = z_ac_adx/2

    return(x_p_adx, y_p_adx, z_p_adx)          #Retorno de los valores x, y, z

while True:                                    #comienzo del bucle principal
    
    contador = 0                               #contador de toma de muesgtras
    base_temp = time.time()                    #se realiza la medición del tiempo actual 
    while contador < 799:                      #mientras el numero de muestras tomado sea menor a 799  
        #base_temp = time.time()               #se realiza la medición del tiempo actual para determinar la duración de un ciclo de muestreo      
        of_x1, of_y1, of_z1 = Calibracion(sensor1.get_accel_data())          #eliminacion del offset del sensor 1
        of_x2, of_y2, of_z2 = Calibracion(sensor2.get_accel_data())          #eliminacion del offset del sensor 2
        of_x3, of_y3, of_z3 = cal_adx()                                      #eliminacion del offset del sensor 3


        acele1 = sensor1.get_accel_data()                                    #toma de lecturas del sensor 1
        x_a_1=acele1.get('x')-of_x1                                          #aceleración en x del sensor 1
        #y_a_1=acele1.get('y')-of_y1                                         #aceleración en y del sensor 1
        #z_a_1=acele1.get('z')-of_z1                                         #aceleración en z del sensor 1

        acele2 = sensor2.get_accel_data()                                    #toma de lecturas del sensor 2
        x_a_2=acele2.get('x')-of_x2                                          #aceleración en x del sensor 2
        #y_a_2=acele2.get('y')-of_y2                                         #aceleración en y del sensor 2
        #z_a_2=acele2.get('z')-of_z2                                         #aceleración en z del sensor 2
    
        x_ac_adx_d, y_ac_adx_d, z_ac_adx_d = acelero.acceleration            #toma de lecturas del sensor 3
        x_a_3=x_ac_adx_d-of_x3                                               #aceleración en x del sensor 3                                              
        #y_a_3=y_ac_adx_d-of_y3                                              #aceleración en y del sensor 3
        #z_a_3=z_ac_adx_d-of_z3                                              #aceleración en z del sensor 3
        
        v_1 = np.append(v_1, x_a_1)                                          #almacenamiento en un vector de la aceleración en x del sensor 1
        #v_2 = np.append(v_2, y_a_1)                                         #almacenamiento en un vector de la aceleración en y del sensor 1 
        #v_3 = np.append(v_3, z_a_1)                                         #almacenamiento en un vector de la aceleración en z del sensor 1
        v_4 = np.append(v_4, x_a_2)                                          #almacenamiento en un vector de la aceleración en x del sensor 2
        #v_5 = np.append(v_5, y_a_2)                                         #almacenamiento en un vector de la aceleración en y del sensor 2
        #v_6 = np.append(v_6, z_a_2)                                         #almacenamiento en un vector de la aceleración en z del sensor 2
        v_7 = np.append(v_7, x_a_3)                                          #almacenamiento en un vector de la aceleración en x del sensor 3
        #v_8 = np.append(v_8, y_a_3)                                         #almacenamiento en un vector de la aceleración en y del sensor 3
        #v_9 = np.append(v_9, z_a_3)                                         #almacenamiento en un vector de la aceleración en z del sensor 3
        
        #print("")                                                           #impresion de la lectura actual en cada uno de los tres sensores
        #print(x_a_1)                                                        #aceleracion en x sensor 1
        #print(y_a_1)                                                        #aceleracion en y sensor 1
        #print(z_a_1)                                                        #aceleracion en z sensor 1
        #print(x_a_2)                                                        #aceleracion en x sensor 2 
        #print(y_a_2)                                                        #aceleracion en y sensor 2
        #print(z_a_2)                                                        #aceleracion en z sensor 2
        #print(x_a_3)                                                        #aceleracion en x sensor 3
        #print(y_a_3)                                                        #aceleracion en y sensor 3
        #print(z_a_3)                                                        #aceleracion en z sensor 3
        #print("")    
        
        time.sleep(0.000001)                                                 #Retardo de 1 us
        contador = contador+1                                                #incremento de ciclo de muestreo
        #base_temp_2 = time.time()                                           #Medición de tiempo final de un ciclo de muestreo
        #print(base_temp_2-base_temp)                                        #Impresion del tiempo requerido para muestrear un ciclo
        
    base_temp_2 = time.time()                                                #Se almacena el tiempo que tarda en ejecutar 800 ciclos
    print(base_temp_2-base_temp)                                             #Se imprime el tiempo que tarda en ejecutar 800 ciclos
    np.savetxt('acelerometro_101.txt', v_1, fmt = '%.4e')                    #Se almacenan los datos de la aceleracion x del sensor 1 
    #np.savetxt('acelerometro_102.txt', v_2, fmt = '%.4e')                   #Se almacenan los datos de la aceleracion y del sensor 1 
    #np.savetxt('acelerometro_103.txt', v_3, fmt = '%.4e')                   #Se almacenan los datos de la aceleracion z del sensor 1 
    np.savetxt('acelerometro_104.txt', v_4, fmt = '%.4e')                    #Se almacenan los datos de la aceleracion x del sensor 2 
    #np.savetxt('acelerometro_105.txt', v_5, fmt = '%.4e')                   #Se almacenan los datos de la aceleracion y del sensor 2  
    #np.savetxt('acelerometro_106.txt', v_6, fmt = '%.4e')                   #Se almacenan los datos de la aceleracion z del sensor 2 
    np.savetxt('acelerometro_107.txt', v_7, fmt = '%.4e')                    #Se almacenan los datos de la aceleracion x del sensor 3 
    #np.savetxt('acelerometro_108.txt', v_8, fmt = '%.4e')                   #Se almacenan los datos de la aceleracion y del sensor 3  
    #np.savetxt('acelerometro_109.txt', v_9, fmt = '%.4e')                   #Se almacenan los datos de la aceleracion z del sensor 3 
    print("Datos capturados")
    print("Pausa")
    time.sleep(1)                                                            #retardo de 1 seg
    
    F = np.loadtxt('acelerometro_101.txt')                                   #Se leen los datos de aceleracion del eje x del sensor 1
    N = F.size                                                               #Se determina la longitud del vector F
    T=(base_temp_2-base_temp)/800                                            #Se establece el periodo de muestreo
    y_f = np.fft.fft(F)                                                      #Se obtiene la transformada de fourier 
    x_f = np.linspace(0.0, 1.0/(2.0*T), N//2)                                #Se determina los valores del eje horizontal
    y_f_amplitud = 2.0/N * np.abs(y_f[:N//2])                                #Se determina la amplitud de frecuencias (eje vertical) 
    
    #plt.plot(x_f, y_f_amplitud)                                             #Se configura la grafica grafica para la aceleracion x en el sensor 1
    #plt.show()                                                              #Se muestra la aceleracion x del sensor 1 

    max_value_1 = np.max(y_f_amplitud)                                       #Se determina el maximo valor del vector de frecuencias del eje x del sensor 1 
    print('El valor maximo del array es:', max_value_1)                      #Se imprime el valor maximo  
    frecuencia_1 = x_f[np.where(y_f_amplitud == max(y_f_amplitud))]          #Se determina el valor de la frecuencia que tiene el valor maximo
    print('La frecuencia registrada es de:',frecuencia_1[0])                 #Se imprime el valor de maximo frecuancia 
    time.sleep(0.5)                                                          #Retardo de 0.5 seg 
    
    '''
    F = np.loadtxt('acelerometro_102.txt')                                   #Se leen los datos de aceleracion del eje y del sensor 1
    N = F.size                                                               #Se determina la longitud del vector F
    T = 1.0 / 200.0                                                          #Se establece el periodo de muestreo
    y_f = np.fft.fft(F)                                                      #Se obtiene la transformada de fourier 
    x_f = np.linspace(0.0, 1.0/(2.0*T), N//2)                                #Se determina los valores del eje horizontal
    y_f_amplitud = 2.0/N * np.abs(y_f[:N//2])                                #Se determina la amplitud de frecuencias (eje vertical) 

    max_value_2 = np.max(y_f_amplitud)                                       #Se determina el maximo valor del vector de frecuencias del eje x del sensor 1
    print('El valor maximo del array es:', max_value_2)                      #Se imprime el valor maximo
    frecuencia_2 = x_f[np.where(y_f_amplitud == max(y_f_amplitud))]          #Se determina el valor de la frecuencia que tiene el valor maximo 
    print('La frecuencia registrada es de:',frecuencia_2[0])                 #Se imprime el valor de maximo frecuancia 
    time.sleep(0.5)                                                          #Retardo de 0.5 seg
    '''
    '''
    F = np.loadtxt('acelerometro_103.txt')                                   #Se leen los datos de aceleracion del eje z del sensor 1
    N = F.size                                                               #Se determina la longitud del vector F
    T = 1.0 / 200.0                                                          #Se establece el periodo de muestreo
    y_f = np.fft.fft(F)                                                      #Se obtiene la transformada de fourier 
    x_f = np.linspace(0.0, 1.0/(2.0*T), N//2)                                #Se determina los valores del eje horizontal
    y_f_amplitud = 2.0/N * np.abs(y_f[:N//2])                                #Se determina la amplitud de frecuencias (eje vertical)

    max_value_3 = np.max(y_f_amplitud)                                       #Se determina el maximo valor del vector de frecuencias del eje y del sensor 1
    print('El valor maximo del array es:', max_value_3)                      #Se imprime el valor maximo
    frecuencia_3 = x_f[np.where(y_f_amplitud == max(y_f_amplitud))]          #Se determina el valor de la frecuencia que tiene el valor maximo 
    print('La frecuencia registrada es de:',frecuencia_3[0])                 #Se imprime el valor de maximo frecuencia 
    time.sleep(0.5)                                                          #Retardo de 0.5 seg
    '''
    
    F = np.loadtxt('acelerometro_104.txt')                                   #Se leen los datos de aceleracion del eje x del sensor 2
    N = F.size                                                               #Se determina la longitud del vector F
    #T = 1.0 / 60.0                                                          #Se establece el periodo de muestreo
    T=(base_temp_2-base_temp)/800                                            #Se establece el periodo de muestreo 
    y_f = np.fft.fft(F)                                                      #Se obtiene la transformada de fourier
    x_f = np.linspace(0.0, 1.0/(2.0*T), N//2)                                #Se determina los valores del eje horizontal
    y_f_amplitud = 2.0/N * np.abs(y_f[:N//2])                                #Se determina la amplitud de frecuencias (eje vertical)   
    
    #plt.plot(x_f, y_f_amplitud)                                             #Se configura la grafica grafica para la aceleracion x en el sensor 2
    #plt.show()                                                              #Se muestra la aceleracion x del sensor 2

    max_value_4 = np.max(y_f_amplitud)                                       #Se determina el maximo valor del vector de frecuencias del eje x del sensor 2
    print('El valor maximo del array es:', max_value_4)                      #Se imprime el valor maximo
    frecuencia_4 = x_f[np.where(y_f_amplitud == max(y_f_amplitud))]          #Se determina el valor de la frecuencia que tiene el valor maximo 
    print('La frecuencia registrada es de:',frecuencia_4[0])                 #Se imprime el valor de maximo frecuencia 
    time.sleep(0.5)                                                          #Retardo de 0.5 seg
    
    '''
    F = np.loadtxt('acelerometro_105.txt')                                   #Se leen los datos de aceleracion del eje y del sensor 2
    N = F.size                                                               #Se determina la longitud del vector F
    T = 1.0 / 200.0                                                          #Se establece el periodo de muestreo
    y_f = np.fft.fft(F)                                                      #Se obtiene la transformada de fourier
    x_f = np.linspace(0.0, 1.0/(2.0*T), N//2)                                #Se determina los valores del eje horizontal 
    y_f_amplitud = 2.0/N * np.abs(y_f[:N//2])                                #Se determina la amplitud de frecuencias (eje vertical)

    max_value_5 = np.max(y_f_amplitud)                                       #Se determina el maximo valor del vector de frecuencias del eje y del sensor 2
    print('El valor maximo del array es:', max_value_5)                      #Se imprime el valor maximo
    frecuencia_5 = x_f[np.where(y_f_amplitud == max(y_f_amplitud))]          #Se determina el valor de la frecuencia que tiene el valor maximo
    print('La frecuencia registrada es de:',frecuencia_5[0])                 #Se imprime el valor de maximo frecuencia
    time.sleep(0.5)                                                          #Retardo de 0.5 seg 
    '''
    '''
    F = np.loadtxt('acelerometro_106.txt')                                   #Se leen los datos de aceleracion del eje z del sensor 2
    N = F.size                                                               #Se determina la longitud del vector F
    T = 1.0 / 200.0                                                          #Se establece el periodo de muestreo 
    y_f = np.fft.fft(F)                                                      #Se obtiene la transformada de fourier
    x_f = np.linspace(0.0, 1.0/(2.0*T), N//2)                                #Se determina los valores del eje horizontal  
    y_f_amplitud = 2.0/N * np.abs(y_f[:N//2])                                #Se determina la amplitud de frecuencias (eje vertical)

    max_value_6 = np.max(y_f_amplitud)                                       #Se determina el maximo valor del vector de frecuencias del eje z del sensor 2
    print('El valor maximo del array es:', max_value_6)                      #Se imprime el valor maximo 
    frecuencia_6 = x_f[np.where(y_f_amplitud == max(y_f_amplitud))]          #Se determina el valor de la frecuencia que tiene el valor maximo
    print('La frecuencia registrada es de:',frecuencia_6[0])                 #Se imprime el valor de maximo frecuencia
    time.sleep(0.5)                                                          #Retardo de 0.5 seg 
    '''
    
    F = np.loadtxt('acelerometro_107.txt')                                   #Se leen los datos de aceleracion del eje x del sensor 3
    N = F.size                                                               #Se determina la longitud del vector F
    #T = 1.0 / 60.0                                                          #Se establece el periodo de muestreo
    T=(base_temp_2-base_temp)/800                                            #Se establece el periodo de muestreo
    y_f = np.fft.fft(F)                                                      #Se obtiene la transformada de fourier
    x_f = np.linspace(0.0, 1.0/(2.0*T), N//2)                                #Se determina los valores del eje horizontal
    y_f_amplitud = 2.0/N * np.abs(y_f[:N//2])                                #Se determina la amplitud de frecuencias (eje vertical)
    
    #plt.plot(x_f, y_f_amplitud)                                             #Se configura la grafica grafica para la aceleracion x en el sensor 2
    #plt.show()                                                              #Se muestra la aceleracion x del sensor 2

    max_value_7 = np.max(y_f_amplitud)                                       #Se determina el maximo valor del vector de frecuencias del eje x del sensor 3
    print('El valor maximo del array es:', max_value_7)                      #Se imprime el valor maximo 
    frecuencia_7 = x_f[np.where(y_f_amplitud == max(y_f_amplitud))]          #Se determina el valor de la frecuencia que tiene el valor maximo
    print('La frecuencia registrada es de:',frecuencia_7[0])                 #Se imprime el valor de maximo frecuencia 
    time.sleep(0.5)                                                          #Retardo de 0.5 seg
    
    '''
    F = np.loadtxt('acelerometro_108.txt')                                   #Se leen los datos de aceleracion del eje y del sensor 3
    N = F.size                                                               #Se determina la longitud del vector F
    T = 1.0 / 200.0                                                          #Se establece el periodo de muestreo
    y_f = np.fft.fft(F)                                                      #Se obtiene la transformada de fourier
    x_f = np.linspace(0.0, 1.0/(2.0*T), N//2)                                #Se determina los valores del eje horizontal
    y_f_amplitud = 2.0/N * np.abs(y_f[:N//2])                                #Se determina la amplitud de frecuencias (eje vertical) 

    max_value_8 = np.max(y_f_amplitud)                                       #Se determina el maximo valor del vector de frecuencias del eje y del sensor 3
    print('El valor maximo del array es:', max_value_8)                      #Se imprime el valor maximo 
    frecuencia_8 = x_f[np.where(y_f_amplitud == max(y_f_amplitud))]          #Se determina el valor de la frecuencia que tiene el valor maximo
    print('La frecuencia registrada es de:',frecuencia_8[0])                 #Se imprime el valor de maximo frecuencia
    time.sleep(0.5)                                                          #Retardo de 0.5 seg
    '''
    '''
    F = np.loadtxt('acelerometro_109.txt')                                   #Se leen los datos de aceleracion del eje z del sensor 3
    N = F.size                                                               #Se determina la longitud del vector F
    T = 1.0 / 200.0                                                          #Se establece el periodo de muestreo
    y_f = np.fft.fft(F)                                                      #Se obtiene la transformada de fourier
    x_f = np.linspace(0.0, 1.0/(2.0*T), N//2)                                #Se determina los valores del eje horizontal
    y_f_amplitud = 2.0/N * np.abs(y_f[:N//2])                                #Se determina la amplitud de frecuencias (eje vertical) 

    max_value_9 = np.max(y_f_amplitud)                                       #Se determina el maximo valor del vector de frecuencias del eje z del sensor 3
    print('El valor maximo del array es:', max_value_9)                      #Se imprime el valor maximo
    frecuencia_9 = x_f[np.where(y_f_amplitud == max(y_f_amplitud))]          #Se determina el valor de la frecuencia que tiene el valor maximo
    print('La frecuencia registrada es de:',frecuencia_9[0])                 #Se imprime el valor de maximo frecuencia
    time.sleep(0.5)                                                          #Retardo de 0.5 seg
    '''
    
    temperatura1 = sensor1.get_temp()                                        #obtencion de la temperatura del sensor 1
    temperatura2 = sensor2.get_temp()                                        #obtencion de la temperatura del sensor 2
    
    client1= paho.Client("control1")                                         #Se crea u objeto ciente
    client1.on_publish = on_publish                                          #Se llama a la funion publish
    client1.connect(broker,port)                                             #Se establece la conexion con el broker
    
    dict = [{"sensor":"Sensor1", "temperatura": temperatura1, "frecuencia": frecuencia_1[0], "amplitud": max_value_1},    #Se determina el diccionario a enviar
            {"sensor":"Sensor2", "temperatura": 0,            "frecuencia": frecuencia_4[0], "amplitud": max_value_4},
            {"sensor":"Sensor3", "temperatura": temperatura2, "frecuencia": frecuencia_7[0], "amplitud": max_value_7}]
    s=pickle.dumps(dict)                                                     #se desserializa del dato dict
    #print(s)                                                                #se imprime el dato s 
    d=pickle.loads(s)                                                        #se serializa el dato s en ascii
    print(d)                                                                 #Se imprime el dato d
    
    ret= client1.publish("vibraciones", json.dumps(d))                       #Se envían los datos al broker   
        
    frecuenciahz = np.append(frecuenciahz, frecuencia_1[0])                  #Se construye el vector de frecuencias
    np.savetxt('frecuencias.txt', frecuenciahz, fmt = '%.4e')                #Se almacena el vector de frecuencias en un txt
    time.sleep(5)                                                            #Retardo de 5 seg
