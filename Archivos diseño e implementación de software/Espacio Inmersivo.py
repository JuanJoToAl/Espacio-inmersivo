# platform: micropython-esp32
# send: wifi
# ip_mpy: 192.168.4.1
# serialport: 
# filename: main.py

from machine import Pin
from machine import ADC
from time import sleep
from hcsr04 import HCSR04

# Configuración del sensor ultrasónico (HCSR04)
# - trigger_pin: Pin de salida para enviar el pulso ultrasónico.
# - echo_pin: Pin de entrada para recibir el eco del pulso.
# - echo_timeout_us: Tiempo máximo para esperar el eco (en microsegundos).
sensor = HCSR04(trigger_pin=5, echo_pin=18, echo_timeout_us=30000)

# Configuración de pines para controlar el puente H L293D
# - en: Habilita el puente H (activar/desactivar el motor).
# - tran1 y tran2: Controlan la dirección del motor.
en = Pin(13, Pin.OUT)
tran1 = Pin(22, Pin.OUT)
tran2 = Pin(23, Pin.OUT)

# Configuración del pin para controlar una luz (LED)
luz = Pin(2, Pin.OUT)

# Función para medir la distancia con el sensor ultrasónico
def distancia():
    distance = sensor.distance_cm()  # Obtiene la distancia en centímetros
    return distance

# Función para mover el motor hacia adelante
def adelante(en, tran1, tran2):
    en.value(1)   # Habilita el puente H
    tran1.value(1)  # Activa el pin 1 del puente H
    tran2.value(0)  # Desactiva el pin 2 del puente H

# Función para mover el motor hacia atrás
def atras(en, tran1, tran2):
    en.value(1)   # Habilita el puente H
    tran1.value(0)  # Desactiva el pin 1 del puente H
    tran2.value(1)  # Activa el pin 2 del puente H

# Función para detener el motor
def quieto(en, tran1, tran2):
    en.value(1)   # Habilita el puente H
    tran1.value(0)  # Desactiva ambos pines del puente H
    tran2.value(0)

# Bucle principal del programa
while True:
    # Medir la distancia con el sensor ultrasónico
    distanciasaurio = distancia()
    print("Distancia: {:.2f} cm".format(distanciasaurio))

    # Si el objeto está a menos de 5 cm, activar el motor y la luz
    if distanciasaurio > 0 and distanciasaurio < 5:
        luz.value(1)  # Encender la luz
        adelante(en, tran1, tran2)  # Mover el motor hacia adelante
        sleep(5)  # Esperar 5 segundos
        quieto(en, tran1, tran2)  # Detener el motor
        sleep(1)  # Esperar 1 segundo
        atras(en, tran1, tran2)  # Mover el motor hacia atrás
        sleep(5)  # Esperar 5 segundos
    else:
        # Si no hay objeto cerca, apagar la luz y detener el motor
        luz.value(0)  # Apagar la luz
        quieto(en, tran1, tran2)  # Detener el motor

    sleep(5)  # Esperar 5 segundos antes de repetir el bucle