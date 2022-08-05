import time
from time import sleep
import pickle

import board
import adafruit_adxl34x

import json

import sys
import numpy as np
import matplotlib.pyplot as plt

import paho.mqtt.client as paho
broker="broker.emqx.io"
port=1883

from mpu6050 import mpu6050
sensor1 = mpu6050(0x69)
sensor2 = mpu6050(0x68)

v_1 = np.array([0.0])
v_2 = np.array([0.0])
v_3 = np.array([0.0])
v_4 = np.array([0.0])
v_5 = np.array([0.0])
v_6 = np.array([0.0])
v_7 = np.array([0.0])
v_8 = np.array([0.0])
v_9 = np.array([0.0])
frecuenciahz = np.array([0.0])

i2c = board.I2C()
acelero = adafruit_adxl34x.ADXL345(i2c)

def on_publish(client,userdata,result):             #create function for callback
    print("data published \n")
    pass


def Calibracion(acel):
    x_ac = 0
    y_ac = 0
    z_ac = 0

    for x in range(2):
        #print(y_ac)
        x_ac = x_ac + acel.get('x')
        y_ac = y_ac + acel.get('y')
        z_ac = z_ac + acel.get('z')
    
    x_p = x_ac/2
    y_p = y_ac/2
    z_p = z_ac/2
 
    return(x_p, y_p, z_p)

def cal_adx():

    x_ac_adx = 0
    y_ac_adx = 0
    z_ac_adx = 0
    for x in range(2):
        #acelero = adafruit_adxl34x.ADXL345(i2c)
        x_ac_adx_d, y_ac_adx_d, z_ac_adx_d = acelero.acceleration
        x_ac_adx = x_ac_adx + x_ac_adx_d
        y_ac_adx = y_ac_adx + y_ac_adx_d
        z_ac_adx = z_ac_adx + z_ac_adx_d
        
    x_p_adx = x_ac_adx/2
    y_p_adx = y_ac_adx/2
    z_p_adx = z_ac_adx/2

    return(x_p_adx, y_p_adx, z_p_adx)

while True:
    
    contador = 0
    base_temp = time.time()
    while contador < 799:
        #base_temp = time.time()
        of_x1, of_y1, of_z1 = Calibracion(sensor1.get_accel_data())
        of_x2, of_y2, of_z2 = Calibracion(sensor2.get_accel_data())
        of_x3, of_y3, of_z3 = cal_adx()


        acele1 = sensor1.get_accel_data()
        x_a_1=acele1.get('x')-of_x1
        #y_a_1=acele1.get('y')-of_y1
        #z_a_1=acele1.get('z')-of_z1

        acele2 = sensor2.get_accel_data()
        x_a_2=acele2.get('x')-of_x2
        #y_a_2=acele2.get('y')-of_y2
        #z_a_2=acele2.get('z')-of_z2
    
        x_ac_adx_d, y_ac_adx_d, z_ac_adx_d = acelero.acceleration
        
        x_a_3=x_ac_adx_d-of_x3
        
        #y_a_3=y_ac_adx_d-of_y3
        #z_a_3=z_ac_adx_d-of_z3
        
        v_1 = np.append(v_1, x_a_1)
        #v_2 = np.append(v_2, y_a_1)
        #v_3 = np.append(v_3, z_a_1)
        v_4 = np.append(v_4, x_a_2)
        #v_5 = np.append(v_5, y_a_2)
        #v_6 = np.append(v_6, z_a_2)
        v_7 = np.append(v_7, x_a_3)
        #v_8 = np.append(v_8, y_a_3)
        #v_9 = np.append(v_9, z_a_3)
        #v_7 = np.append(v_7, z_a_3)
        
        
        #print("")
        #print(x_a_1)
        #print(y_a_1)
        #print(z_a_1)
        #print(x_a_2)
        #print(y_a_2)
        #print(z_a_2)
        #print(x_a_3)
        #print(y_a_3)
        #print(z_a_3)
        #print("")    
        
        time.sleep(0.000001)
        contador = contador+1
        #base_temp_2 = time.time()
        #print(base_temp_2-base_temp)
        
    base_temp_2 = time.time()
    print(base_temp_2-base_temp)
    np.savetxt('acelerometro_101.txt', v_1, fmt = '%.4e')
    #np.savetxt('acelerometro_102.txt', v_2, fmt = '%.4e')
    #np.savetxt('acelerometro_103.txt', v_3, fmt = '%.4e')
    np.savetxt('acelerometro_104.txt', v_4, fmt = '%.4e')
    #np.savetxt('acelerometro_105.txt', v_5, fmt = '%.4e')
    #np.savetxt('acelerometro_106.txt', v_6, fmt = '%.4e')
    np.savetxt('acelerometro_107.txt', v_7, fmt = '%.4e')
    #np.savetxt('acelerometro_108.txt', v_8, fmt = '%.4e')
    #np.savetxt('acelerometro_109.txt', v_9, fmt = '%.4e')
    print("Datos capturados")
    print("Pausa")
    time.sleep(1)
    
    F = np.loadtxt('acelerometro_101.txt')
    N = F.size
    #T = 1.0 / 60.0
    T=(base_temp_2-base_temp)/800
    y_f = np.fft.fft(F)
    x_f = np.linspace(0.0, 1.0/(2.0*T), N//2)
    y_f_amplitud = 2.0/N * np.abs(y_f[:N//2])
    
    #plt.plot(x_f, y_f_amplitud)
    #plt.show()

    max_value_1 = np.max(y_f_amplitud)
    print('El valor maximo del array es:', max_value_1)
    frecuencia_1 = x_f[np.where(y_f_amplitud == max(y_f_amplitud))]
    print('La frecuencia registrada es de:',frecuencia_1[0])
    time.sleep(0.5)
    
    '''
    F = np.loadtxt('acelerometro_102.txt')
    N = F.size
    T = 1.0 / 200.0
    y_f = np.fft.fft(F)
    x_f = np.linspace(0.0, 1.0/(2.0*T), N//2)
    y_f_amplitud = 2.0/N * np.abs(y_f[:N//2])

    max_value_2 = np.max(y_f_amplitud)
    print('El valor maximo del array es:', max_value_2)
    frecuencia_2 = x_f[np.where(y_f_amplitud == max(y_f_amplitud))]
    print('La frecuencia registrada es de:',frecuencia_2[0])
    time.sleep(0.5)
    '''
    '''
    F = np.loadtxt('acelerometro_103.txt')
    N = F.size
    T = 1.0 / 200.0
    y_f = np.fft.fft(F)
    x_f = np.linspace(0.0, 1.0/(2.0*T), N//2)
    y_f_amplitud = 2.0/N * np.abs(y_f[:N//2])

    max_value_3 = np.max(y_f_amplitud)
    print('El valor maximo del array es:', max_value_3)
    frecuencia_3 = x_f[np.where(y_f_amplitud == max(y_f_amplitud))]
    print('La frecuencia registrada es de:',frecuencia_3[0])
    time.sleep(0.5)
    '''
    
    F = np.loadtxt('acelerometro_104.txt')
    N = F.size
    #T = 1.0 / 60.0
    T=(base_temp_2-base_temp)/800
    y_f = np.fft.fft(F)
    x_f = np.linspace(0.0, 1.0/(2.0*T), N//2)
    y_f_amplitud = 2.0/N * np.abs(y_f[:N//2])
    
    #plt.plot(x_f, y_f_amplitud)
    #plt.show()

    max_value_4 = np.max(y_f_amplitud)
    print('El valor maximo del array es:', max_value_4)
    frecuencia_4 = x_f[np.where(y_f_amplitud == max(y_f_amplitud))]
    print('La frecuencia registrada es de:',frecuencia_4[0])
    time.sleep(0.5)
    
    '''
    F = np.loadtxt('acelerometro_105.txt')
    N = F.size
    T = 1.0 / 200.0
    y_f = np.fft.fft(F)
    x_f = np.linspace(0.0, 1.0/(2.0*T), N//2)
    y_f_amplitud = 2.0/N * np.abs(y_f[:N//2])

    max_value_5 = np.max(y_f_amplitud)
    print('El valor maximo del array es:', max_value_5)
    frecuencia_5 = x_f[np.where(y_f_amplitud == max(y_f_amplitud))]
    print('La frecuencia registrada es de:',frecuencia_5[0])
    time.sleep(0.5)
    '''
    '''
    F = np.loadtxt('acelerometro_106.txt')
    N = F.size
    T = 1.0 / 200.0
    y_f = np.fft.fft(F)
    x_f = np.linspace(0.0, 1.0/(2.0*T), N//2)
    y_f_amplitud = 2.0/N * np.abs(y_f[:N//2])

    max_value_6 = np.max(y_f_amplitud)
    print('El valor maximo del array es:', max_value_6)
    frecuencia_6 = x_f[np.where(y_f_amplitud == max(y_f_amplitud))]
    print('La frecuencia registrada es de:',frecuencia_6[0])
    time.sleep(0.5)
    '''
    
    F = np.loadtxt('acelerometro_107.txt')
    N = F.size
    #T = 1.0 / 60.0
    T=(base_temp_2-base_temp)/800
    y_f = np.fft.fft(F)
    x_f = np.linspace(0.0, 1.0/(2.0*T), N//2)
    y_f_amplitud = 2.0/N * np.abs(y_f[:N//2])
    
    #plt.plot(x_f, y_f_amplitud)
    #plt.show()

    max_value_7 = np.max(y_f_amplitud)
    print('El valor maximo del array es:', max_value_7)
    frecuencia_7 = x_f[np.where(y_f_amplitud == max(y_f_amplitud))]
    print('La frecuencia registrada es de:',frecuencia_7[0])
    time.sleep(0.5)
    
    '''
    F = np.loadtxt('acelerometro_108.txt')
    N = F.size
    T = 1.0 / 200.0
    y_f = np.fft.fft(F)
    x_f = np.linspace(0.0, 1.0/(2.0*T), N//2)
    y_f_amplitud = 2.0/N * np.abs(y_f[:N//2])

    max_value_8 = np.max(y_f_amplitud)
    print('El valor maximo del array es:', max_value_8)
    frecuencia_8 = x_f[np.where(y_f_amplitud == max(y_f_amplitud))]
    print('La frecuencia registrada es de:',frecuencia_8[0])
    time.sleep(0.5)
    '''
    '''
    F = np.loadtxt('acelerometro_109.txt')
    N = F.size
    T = 1.0 / 200.0
    y_f = np.fft.fft(F)
    x_f = np.linspace(0.0, 1.0/(2.0*T), N//2)
    y_f_amplitud = 2.0/N * np.abs(y_f[:N//2])

    max_value_9 = np.max(y_f_amplitud)
    print('El valor maximo del array es:', max_value_9)
    frecuencia_9 = x_f[np.where(y_f_amplitud == max(y_f_amplitud))]
    print('La frecuencia registrada es de:',frecuencia_9[0])
    time.sleep(0.5)
    '''
    
    temperatura1 = sensor1.get_temp()
    temperatura2 = sensor2.get_temp()
    
    client1= paho.Client("control1")                           #create client object
    client1.on_publish = on_publish                          #assign function to callback
    client1.connect(broker,port)                                 #establish connection
    
    dict = [{"sensor":"Sensor1", "temperatura": temperatura1, "frecuencia": frecuencia_1[0], "amplitud": max_value_1},
            {"sensor":"Sensor2", "temperatura": 0,            "frecuencia": frecuencia_4[0], "amplitud": max_value_4},
            {"sensor":"Sensor3", "temperatura": temperatura2, "frecuencia": frecuencia_7[0], "amplitud": max_value_7}]
    s=pickle.dumps(dict)
    #print(s)
    d=pickle.loads(s)
    print(d)
    
    ret= client1.publish("vibraciones", json.dumps(d))
    
    #frecuenciahz = np.append(frecuenciahz, frecuencia_1[0], frecuencia_4[0], frecuencia_7[0])
    frecuenciahz = np.append(frecuenciahz, frecuencia_1[0])
    np.savetxt('frecuencias.txt', frecuenciahz, fmt = '%.4e')
    time.sleep(5)