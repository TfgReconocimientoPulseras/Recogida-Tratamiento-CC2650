#
# TI SimpleLink SensorTag 2016
# Date: 2016 10 17
#
# Sensor: Gyro, Accelerometer and Magnetometer
# Values: 9 bytes x, y, z for each sensor
# Note: Sensor values have not been validated
#
import struct
import sys
import traceback
import logging
import time
import datetime
import pandas as pd
import argparse
import ProcesarDatos


from bluepy.btle import UUID, Peripheral, BTLEException

def TI_UUID(val):
    return UUID("%08X-0451-4000-b000-000000000000" % (0xF0000000 + val))

def obtener_datos_sensor(nombre, tiempo, mac, archivos, actividad):
    logging.basicConfig(level=logging.INFO, format='%(levelname)-6s %(asctime)-18s %(message)s', datefmt='%d-%m-%Y %H:%M:%S')

    config_uuid = TI_UUID(0xAA82)
    data_uuid = TI_UUID(0xAA81)
    nombre_actividad = ""

    # Bit settings to turn on individual movement sensors
    # bits 0 - 2: Gyro x, y z
    # bits 3 - 5: Accelerometer x, y, z
    # bit: 6: Magnetometer turns on X, y , z with one bit

    # gyroOn = 0x0700
    # accOn = 0x3800
    # magOn = 0xC001

    # sensorOnVal = gyroOn | magOn | accOn
    sensorOnVal = 0x7F02

    sensorOn = struct.pack("BB", (sensorOnVal >> 8) & 0xFF, sensorOnVal & 0xFF) #BB dos integers
    sensorOff = struct.pack("BB", 0x00, 0x00)

    try:
        logging.info("Trying to connect to: %s", mac)
        # print "Info, trying to connect to:", sys.argv[1]
        p = Peripheral(mac)

    except BTLEException:
        logging.error("Unable to connect!")
        # print "Fatal, unable to connect!"

    except:
        logging.error("Unexpected error!")
        # print "Fatal, unexpected error!"
        traceback.print_exc()
        raise

    else:

        try:
            # print "Info, connected and turning sensor on!"
            print("Nombre: %s" %nombre)
            logging.info("Connected and turning sensor ON!")
            ch = p.getCharacteristics(uuid=config_uuid)[0]
            ch.write(sensorOn, withResponse=True)

            # print "Info, reading values!"
            logging.info("Reading values")
            ch = p.getCharacteristics(uuid=data_uuid)[0]


            #GESTION DE DATOS CON PANDAS##########################################################################################
            datos = pd.DataFrame(columns=['timestamp', 'gyro-alpha', 'gyro-beta', 'gyro-gamma', 'accel-x', 'accel-y', 'accel-z'])
            ######################################################################################################################

            #GESTION DEL TIPO DE LA ACTIVIDAD SEGUN EL VALOR DEL PARAMETRO RECIBIDO actividad#####################################
            if int(actividad) == 1:
                nombre_actividad = "ANDAR"
            elif int(actividad) == 2:
                nombre_actividad = "TROTAR"
            elif int(actividad) == 3:
                nombre_actividad = "BARRER"
            elif int(actividad) == 4:
                nombre_actividad = "DEPIE"
            elif int(actividad) == 5:
                nombre_actividad = "SENTADO"
            elif int(actividad) == 6:
                nombre_actividad = "SUBIRESCALERAS"
            elif int(actividad) == 7:
                nombre_actividad = "BAJARESCALERAS"
            else:
                print("Actividad no registrada en el sistema")
                quit()
            ######################################################################################################################

            print("timestamp;gyro-alpha;gyro-beta;gyro-gamma;accel-x;accel-y;accel-z")
            tiempo_inicio = round((datetime.datetime.utcnow() - datetime.datetime(1970, 1, 1)).total_seconds()* 1000)
            num_archivo = 0
            for i in range(0, 50000):
                rawVals = ch.read()
                #print "Raw:",
                for rawVal in rawVals:
                    temp = ord(rawVal)
                    #print "%2.2x" % temp,
                #print

                # Movement data: 9 bytes made up of x, y and z for Gyro, Accelerometer,
                # and Magnetometer.  Raw values must be divided by scale
                (gyroX, gyroY, gyroZ, accX, accY, accZ, magX, magY, magZ) = struct.unpack('<hhhhhhhhh', rawVals)

                #scale = 128.0
                #print "Gyro - x: %2.6f, y: %2.6f, z: %2.6f" % (gyroX / scale, gyroY / scale, gyroZ / scale)

                #scale = 4096.0
                #print "Acc - x: %2.6f, y: %2.6f, z: %2.6f" % (accX / scale, accY / scale, accZ / scale)

                #scale = (32768.0 / 4912.0)
                #print "Mag - x: %2.6f, y: %2.6f, z: %2.6f" % (magX / scale, magY / scale, magZ / scale)*/

                timestamp = round((datetime.datetime.utcnow() - datetime.datetime(1970, 1, 1)).total_seconds()* 1000)

                #print("%f;%f;%f;%f;%f;%f" % (timestamp, gyroX, gyroY, gyroZ, accX, accY, accZ))
                scale_accel = 4096.0
                scale_gyro = 128.0
                print "%13.0f;%.14f;%.14f;%.14f;%.14f;%.14f;%.14f" %(timestamp, gyroX/scale_gyro, gyroY/scale_gyro, gyroZ/scale_gyro, accX/scale_accel, accY/scale_accel, accZ/scale_accel)
                #datos.loc[i] = ["%13.0f;%.14f;%.14f;%.14f;%.14f;%.14f;%.14f" %(timestamp, gyroX/scale_gyro, gyroY/scale_gyro, gyroZ/scale_gyro, accX/scale_accel, accY/scale_accel, accZ/scale_accel)]
                datos.loc[i] = ['{0:13.0f}'.format(timestamp), gyroX/scale_gyro, gyroY/scale_gyro, gyroZ/scale_gyro, accX/scale_accel, accY/scale_accel, accZ/scale_accel]
                print (timestamp - tiempo_inicio)
                print ("Vuelta: ", i)
                print ("Numero archivos creados: ", num_archivo)
                print ("Archivos crear: ", archivos)
                if((timestamp - tiempo_inicio ) > ((int(tiempo) * 1000))): #Pasamos tiempo a ms
                    num_archivo = num_archivo + 1
                    datos.to_csv("Datos/%s-%s-%d.csv" %(nombre, nombre_actividad, num_archivo), ';', index=False)
                    tiempo_inicio = round((datetime.datetime.utcnow() - datetime.datetime(1970, 1, 1)).total_seconds()* 1000)
                    datos = pd.DataFrame(columns=['timestamp', 'gyro-alpha', 'gyro-beta', 'gyro-gamma', 'accel-x', 'accel-y', 'accel-z'])

                    if(num_archivo == int(archivos)):
                        break;
                        
            # print "Info, turning sensor off!"
            logging.info("Turning sensor OFF")
            ch = p.getCharacteristics(uuid=config_uuid)[0]
            ch.write(sensorOff, withResponse=True)

            ProcesarDatos.getStatisticsValues(('%s-%s' %(nombre, nombre_actividad)), int(archivos))

        except:
            # print "Fatal, unexpected error!"
            logging.error("Unexpected error!")
            traceback.print_exc()
            raise

        finally:
            # print "Info, disconnecting!"
            logging.info("Disconnecting...")
            p.disconnect()

    finally:
        quit()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Extract features from inputFile and save them in outputFile')

    parser.add_argument("m",
                        help="MAC del dispositivo")
    parser.add_argument("n",
                        help="Nombre del usuario")
    parser.add_argument("a",
                        help="Actividad a realizar")
    parser.add_argument("-t", "--t", help="Tiempo en cada uno de los ficheros. Por defecto, 30s",
                    default=30)
    parser.add_argument("-f", "--f", help="Numero de ficheros que se van a generar", default=1)
    args = parser.parse_args()

    obtener_datos_sensor(args.n, args.t, args.m, args.f, args.a)