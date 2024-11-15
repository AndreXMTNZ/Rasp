import RPi.GPIO as GPIO
import time
import os
import subprocess

# Configuración del GPIO
GPIO.setmode(GPIO.BCM)
PIR_PIN = 17  # Pin GPIO conectado al PIR
GPIO.setup(PIR_PIN, GPIO.IN)

# Ruta del video
video_path = "/home/pi/video.mp4"  # Cambia esta ruta a la ubicación de tu video

# Función para encender/apagar la pantalla
def power_screen(on):
    if on:
        os.system("vcgencmd display_power 1")
    else:
        os.system("vcgencmd display_power 0")

# Función para iniciar el video usando VLC
def play_video():
    global player_process
    player_process = subprocess.Popen(["cvlc", "--fullscreen", "--loop", video_path])

# Función para detener el video
def stop_video():
    global player_process
    if player_process:
        player_process.terminate()
        player_process = None

player_process = None
last_motion_time = 0

try:
    while True:
        if GPIO.input(PIR_PIN):
            print("Movimiento detectado!")
            last_motion_time = time.time()

            if player_process is None:
                play_video()
                power_screen(True)

        elif player_process is not None:
            # Verificar si han pasado 30 segundos sin detección
            if time.time() - last_motion_time > 30:
                print("Sin movimiento, pausando video y apagando pantalla")
                stop_video()
                power_screen(False)

        time.sleep(1)  # Espera 1 segundo entre cada verificación

except KeyboardInterrupt:
    print("Saliendo...")
finally:
    GPIO.cleanup()
