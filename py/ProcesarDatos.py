import pandas as pd
import argparse

def getStatisticsValues(nombre, numeroFicheros,time=1, overlap=500):
    dfOut = pd.DataFrame()
    
    for i in range(0, int(numeroFicheros)):
        df = pd.read_csv("%s-%d.csv" %(nombre, i+1), sep=';', index_col=0, error_bad_lines=False)
        dfConjunta = pd.DataFrame();
        df.index = pd.to_datetime(df.index.values, unit='ms')
        
        dfResampleMean = df.resample('%dL' %(overlap)).mean()
        dfRollingMean = dfResampleMean.rolling('%ds' %(time)).mean()
        dfRollingMean.columns = ['avg_gyro-alpha', 'avg_gyro-beta', 'avg_gyro-gamma', 'avg_ax', 'avg_ay', 'avg_az']

        dfResampleMin = df.resample('%dL' %(overlap)).min()
        dfRollingMin = dfResampleMin.rolling('%ds' %(time)).min()
        dfRollingMin.columns = ['min_gyro-alpha', 'min_gyro-beta', 'min_gyro-gamma', 'min_ax', 'min_ay', 'min_az']
        
        dfResampleMax = df.resample('%dL' %(overlap)).max()
        dfRollingMax = dfResampleMax.rolling('%ds' %(time)).max()
        dfRollingMax.columns = ['max_gyro-alpha', 'max_gyro-beta', 'max_gyro-gamma', 'max_ax', 'max_ay', 'max_az']

        if(i > 0):
            dfConjunta = dfRollingMean.T.append(dfRollingMin.T).append(dfRollingMax.T)
            dfConjunta = dfConjunta.T
            dfOut = pd.concat([dfOut, dfConjunta])
        else:
            dfOut = dfRollingMean.T.append(dfRollingMin.T).append(dfRollingMax.T)
            dfOut = dfOut.T
        
    
    dfOut.to_csv("%s-procesado.csv" %(nombre), ';')

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
