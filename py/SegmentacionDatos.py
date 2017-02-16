
# coding: utf-8

# In[8]:

import pandas as pd
import argparse


# In[16]:

def getStatisticsValues(inputFile, numArchivos, time=1, overlap=500):
  
    dfVentana = pd.DataFrame()
    
    for i in range(numArchivos):
        dfVentanaAux = pd.DataFrame()
    
        df = pd.read_csv("%s-%d.csv" %(inputFile, i+1), sep=';', index_col=0, error_bad_lines=False)

        df.index = pd.to_datetime(df.index.values, unit='ms')

        datosMedia = df.resample('%dL' %(overlap)).mean()
        datosMinimo = df.resample('%dL'%(overlap)).min()
        datosMaximo = df.resample('%dL' %(overlap)).max()
        datosDesviacion = df.resample('%dL' %(overlap)).std()

        datosMedia = datosMedia.rolling('%ds' %(time)).mean()
        datosMinimo = datosMinimo.rolling('%ds' %(time)).min()
        datosMaximo = datosMaximo.rolling('%ds' %(time)).max()
        datosDesviacion = datosDesviacion.rolling('%ds' %(time)).std()

        dfVentanaAux = dfVentanaAux.append(datosMedia)
        dfVentanaAux = dfVentanaAux.append(datosMinimo)        
        dfVentanaAux = dfVentanaAux.append(datosMaximo)
        dfVentanaAux = dfVentanaAux.append(datosDesviacion)
        
        dfVentanaAux = dfVentanaAux.T  # Traspuesta para cambiar los nombres a las columnas
        dfVentanaAux.columns = ['avg_gyro-alpha', 'avg_gyro-beta', 'avg_gyro-gamma', 'avg_ax', 'avg_ay', 'avg_az',
                        'min_gyro-alpha', 'min_gyro-beta', 'min_gyro-gamma', 'min_ax', 'min_ay', 'min_az',
                        'max_gyro-alpha', 'max_gyro-beta', 'max_gyro-gamma', 'max_ax', 'max_ay', 'max_az',
                        'std_gyro-alpha', 'std_gyro-beta', 'std_gyro-gamma', 'std_ax', 'std_ay', 'std_az']  # Renombrado de columnas
        dfVentana = dfVentana.append(dfVentanaAux)
        
    dfVentana.T.to_csv("%s.csv" %(inputFile), ';')


# In[17]:

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Extract features from inputFile and save them in outputFile')

    parser.add_argument("f",
                        help="Nombre del archivo")
    parser.add_argument("n",
                        help="Output file")
    parser.add_argument("-t", "--time", help="Time of window, i.e.= 1 second",
                    default=1)
    parser.add_argument("-p", "--perc", help="overlap, i.e. = 0.5 -> 50 Overlap",
                    default=0.5)
    args = parser.parse_args()
    #print args.i
    #print args.o
    #print args.time
    #print args.perc
    getStatisticsValues(args.f, args.n, args.time, args.perc)


# In[17]:

getStatisticsValues("Iban_andando", 5, 1, 500)


# In[5]:

pd.__version__


# In[ ]:



