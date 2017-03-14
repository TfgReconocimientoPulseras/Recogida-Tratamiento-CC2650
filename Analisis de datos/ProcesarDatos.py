import pandas as pd
import argparse
import time
import numpy as np
from datetime import datetime
from scipy.linalg import norm


def getStatisticsValues(nombre, numeroFicheros, time1=1, overlap=500):
    dfOut = pd.DataFrame()
    
    dfRollingMean = pd.DataFrame(columns=['avg_gyro-alpha', 'avg_gyro-beta', 'avg_gyro-gamma', 'avg_ax', 'avg_ay', 'avg_az']);

    dfRollingMin = pd.DataFrame(columns=['min_gyro-alpha', 'min_gyro-beta', 'min_gyro-gamma', 'min_ax', 'min_ay', 'min_az']);
        
    dfRollingMax = pd.DataFrame(columns=['max_gyro-alpha', 'max_gyro-beta', 'max_gyro-gamma', 'max_ax', 'max_ay', 'max_az']);
    
    dfRollingVar = pd.DataFrame(columns=['var_gyro-alpha', 'var_gyro-beta', 'var_gyro-gamma', 'var_ax', 'var_ay', 'var_az']);
    
    dfRollingFft = pd.DataFrame(columns=['fft_gyro-alpha', 'fft_gyro-beta', 'fft_gyro-gamma', 'fft_ax', 'fft_ay', 'fft_az']);
    
    dfRollingStd = pd.DataFrame(columns=['std_gyro-alpha', 'std_gyro-beta', 'std_gyro-gamma', 'std_ax', 'std_ay', 'std_az']);
    
    dfRollingCor = pd.DataFrame(columns=['cor_gyro-alpha', 'cor_gyro-beta', 'cor_gyro-gamma', 'cor_ax', 'cor_ay', 'cor_az']);
    
    dfRollingIrq = pd.DataFrame(columns=['irq_gyro-alpha', 'irq_gyro-beta', 'irq_gyro-gamma', 'irq_ax', 'irq_ay', 'irq_az']);
    
    dfRollingMg = pd.DataFrame(columns=['mg_gyro-alpha', 'mg_gyro-beta', 'mg_gyro-gamma', 'mg_ax', 'mg_ay', 'mg_az']);
    
    dfRollingCov = pd.DataFrame(columns=['cov_gyro-alpha', 'cov_gyro-beta', 'cov_gyro-gamma', 'cov_ax', 'cov_ay', 'cov_az']);
    
    dfRollingMed = pd.DataFrame(columns=['med_gyro-alpha', 'med_gyro-beta', 'med_gyro-gamma', 'med_ax', 'med_ay', 'med_az']);
    
    dfOut = dfRollingMean.T.append(dfRollingVar.T).append(dfRollingStd.T)
    #dfOut = dfRollingCov.T
    dfOut = dfOut.T    
    
    for i in range(0, int (numeroFicheros)):
        df = pd.read_csv("Datos\%s-%d.csv" %(nombre, i+1), sep=';', index_col=0, error_bad_lines=False)
        dfConjunta = pd.DataFrame();
        df.index = pd.to_datetime(df.index.values, unit='ms')
        
        dfResampleMean = df.resample('%dL' %(overlap)).mean()
        dfRollingMean = dfResampleMean.rolling('%ds' %(time1)).mean()
        dfRollingMean.columns = ['avg_gyro-alpha', 'avg_gyro-beta', 'avg_gyro-gamma', 'avg_ax', 'avg_ay', 'avg_az']

        dfResampleMin = df.resample('%dL' %(overlap)).min()
        dfRollingMin = dfResampleMin.rolling('%ds' %(time1)).min()
        dfRollingMin.columns = ['min_gyro-alpha', 'min_gyro-beta', 'min_gyro-gamma', 'min_ax', 'min_ay', 'min_az']
        
        dfResampleMax = df.resample('%dL' %(overlap)).max()
        dfRollingMax = dfResampleMax.rolling('%ds' %(time1)).max()
        dfRollingMax.columns = ['max_gyro-alpha', 'max_gyro-beta', 'max_gyro-gamma', 'max_ax', 'max_ay', 'max_az']
        
        dfResampleVar = df.resample('%dL' %(overlap)).var()
        dfRollingVar = dfResampleVar.rolling('%ds' %(time1)).var()
        dfRollingVar.columns = ['var_gyro-alpha', 'var_gyro-beta', 'var_gyro-gamma', 'var_ax', 'var_ay', 'var_az']
#        
#        dfResampleFft = df.resample('%dL' %(overlap)).apply(np.fft)
#        dfRollingFft = dfResampleFft.rolling('%ds' %(time1)).apply(np.fft)
#        dfRollingFft.columns = ['fft_gyro-alpha', 'fft_gyro-beta', 'fft_gyro-gamma', 'fft_ax', 'fft_ay', 'fft_az']
        
        dfResampleStd = df.resample('%dL' %(overlap)).std()
        dfRollingStd = dfResampleStd.rolling('%ds' %(time1)).std()
        dfRollingStd.columns = ['std_gyro-alpha', 'std_gyro-beta', 'std_gyro-gamma', 'std_ax', 'std_ay', 'std_az']
        
#        dfResampleCor = df.resample('%dL' %(overlap)).corr().mean()
#        dfRollingCor = dfResampleCor.rolling('%ds' %(time1)).corr()
#        dfRollingCor.columns = ['cor_gyro-alpha', 'cor_gyro-beta', 'cor_gyro-gamma', 'cor_ax', 'cor_ay', 'cor_az']
        
#        dfResampleIrq = df.resample('%dL' %(overlap)).quantile(0.75)
#        dfRollingIrq = dfResampleIrq.rolling('%ds' %(time1)).quantile(0.75)
#        dfRollingIrq.columns = ['irq_gyro-alpha', 'irq_gyro-beta', 'irq_gyro-gamma', 'irq_ax', 'irq_ay', 'irq_az']
                
#        dfResampleMg = df.resample('%dL' %(overlap)).apply(norm())
#        dfRollingMg = dfResampleMg.rolling('%ds' %(time1)).apply(norm())
#        dfRollingMg.columns = ['mg_gyro-alpha', 'mg_gyro-beta', 'mg_gyro-gamma', 'mg_ax', 'mg_ay', 'mg_az']
        
#        dfResampleCov = df.resample('%dL' %(overlap)).cov()
#        dfRollingCov = dfResampleCov.rolling('%ds' %(time1)).cov()
#        dfRollingCov.columns = ['cov_gyro-alpha', 'cov_gyro-beta', 'cov_gyro-gamma', 'cov_ax', 'cov_ay', 'cov_az']
#        
        dfResampleMed = df.resample('%dL' %(overlap)).median()
        dfRollingMed = dfResampleMed.rolling('%ds' %(time1)).median()
        dfRollingMed.columns = ['med_gyro-alpha', 'med_gyro-beta', 'med_gyro-gamma', 'med_ax', 'med_ay', 'med_az']
        
        

        dfConjunta = dfRollingMean.T.append(dfRollingVar.T).append(dfRollingStd.T)
        # dfConjunta = dfRollingCov.T
        dfConjunta = dfConjunta.T
        dfOut = pd.concat([dfOut, dfConjunta])
        
    fecha = datetime.now().microsecond

    dfOut.to_csv("prueba/%s-procesado-%s.csv" %(nombre, fecha), ';')

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Extract features from inputFile and save them in outputFile')

    parser.add_argument("i",
                        help="File/s to be analyzed")
    parser.add_argument("n",
                        help="Number of files")
    parser.add_argument("-t", "--time", help="Time of window, i.e.= 1 second",
                    default=1)
    parser.add_argument("-o", "--overlap", help="overlap || 500ms -> 50.00perc verlap",
                    default=500)
    args = parser.parse_args()

    getStatisticsValues(args.i, args.n, args.time, args.overlap)
