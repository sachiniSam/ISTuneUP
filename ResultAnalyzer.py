import pandas as pd
import numpy as np

class ResultAnaylzer:

    global optType

    @staticmethod
    # Step 2. Import the dataset
    def importResultData():
        global df
        df = pd.read_csv('overallResult.csv')
        return df

    @staticmethod
    def importConfigData():
        # read the configuration file
        global dfConf
        dfConf = pd.read_csv('DeployementConfigs/confData.conf', sep="=", header=None)
        return dfConf

    #read the multioptimized values
    @staticmethod
    def importOptimizedData():
        # read the configuration file
        global optiData
        optiData = pd.read_csv('multiobjVals.txt', sep="=", header=None)
        return optiData

    @staticmethod
    def getTargetMetric():
        configs = ResultAnaylzer.importConfigData()
        if configs[configs[0] == 'optimizationType'][1].item() == 'single':
            definedTarget = configs[configs[0] == 'targetMetric'][1].item()
        else:
            definedTarget = configs[configs[0] == 'targetMetric1'][1].item()
        return definedTarget

    @staticmethod
    def getTargetMetric2():
        configs = ResultAnaylzer.importConfigData()
        definedTarget2 = configs[configs[0] == 'targetMetric2'][1].item()
        return definedTarget2

    

    @staticmethod
    def getCategoryRow(resultData,metric):
        categoryRow = resultData.loc[resultData[metric].idxmin()]
        return categoryRow
    

    @staticmethod
    def analyseCategory():
        global rowTrans
        global rowData
        global optType
        configs = ResultAnaylzer.importConfigData()
        resultData = ResultAnaylzer.importResultData()
        if configs[configs[0] == 'optimizationType'][1].item() == 'single':
            optType = 'true'
            #rowData = df.loc[[df['99%_Line'].idxmin()]]
            rowData = ResultAnaylzer.getCategoryRow(resultData,"99%_Line")
            #rowData = resultData.loc[resultData['99%_Line'].idxmin()]
            rowTrans = rowData.T.reset_index()
            rowTrans.columns = ['parameters','values']

    
        else:
            optType = 'false'
            #read objective data from saved file
            multiD = ResultAnaylzer.importOptimizedData()
            resultData = ResultAnaylzer.importResultData()
            #capture the optimization metric
            tarOne = ResultAnaylzer.getTargetMetric()
            tarTwo = ResultAnaylzer.getTargetMetric2()

            # optimization metric values captured from the 
            tarOpt1 = multiD[multiD[0] == tarOne][1].item()
            tarOpt2 = multiD[multiD[0] == tarTwo][1].item()

            rowData = resultData.loc[(resultData[tarOne] == tarOpt1) & (resultData[tarTwo] == tarOpt2)]
            rowTrans = rowData.T.reset_index()
            rowTrans.columns = ['parameters','values']

        return rowTrans

    
    @staticmethod
    def getDefault(metric):
        resultData = ResultAnaylzer.importResultData()
        defaultMetric = resultData[metric].iloc[0]
        return defaultMetric

    @staticmethod
    def getOptimized(metric):
        global optType
        resultData = ResultAnaylzer.importResultData()
        if optType == 'true':
            optimizedValue =  ResultAnaylzer.getCategoryRow(resultData, ResultAnaylzer.getTargetMetric())[metric]
        else:
            optimizedValue =  ResultAnaylzer.getMultiObjOptimized(metric)
        
        return optimizedValue

    @staticmethod
    def getMultiObjOptimized(metric):
        resultData = ResultAnaylzer.importResultData()
        multiD = ResultAnaylzer.importOptimizedData()
        #capture the optimization metric
        tarOne = ResultAnaylzer.getTargetMetric()
        tarTwo = ResultAnaylzer.getTargetMetric2()

        # optimization metric values captured from the 
        tarOpt1 = multiD[multiD[0] == tarOne][1].item()
        tarOpt2 = multiD[multiD[0] == tarTwo][1].item()

        multiObjVal = resultData.loc[(resultData[tarOne] == tarOpt1) & (resultData[tarTwo] == tarOpt2)][metric]
        return multiObjVal


    @staticmethod
    def latencyImprovement():
        global optType
        #get the default optimization result
        defaultLatency = ResultAnaylzer.getDefault("99%_Line")
        optimizedVal = ResultAnaylzer.getOptimized("99%_Line")
        improvement = round(-1*(float(float(optimizedVal - defaultLatency)/defaultLatency )*100),2)
        return improvement

    @staticmethod
    def averageImprovement():
        #get the default optimization result
        defaultAverage = ResultAnaylzer.getDefault("Average")
        optimizedVal = ResultAnaylzer.getOptimized("Average")
        improvement = round(-1*(float(float(optimizedVal - defaultAverage)/defaultAverage )*100),2)
        return improvement

    @staticmethod
    def throughputImprovement():
        #get the default optimization result
        defaultThroughput = ResultAnaylzer.getDefault("Throughput")
        optimizedVal = ResultAnaylzer.getOptimized("Throughput")
        improvement = round((float(float(optimizedVal - defaultThroughput)/defaultThroughput )*100),2)
        return improvement

    @staticmethod
    def performanceImprovement():
        #get the default optimization result
        defaultVal = ResultAnaylzer.getDefault("99%_Line")
        optimizedVal = ResultAnaylzer.getOptimized("99%_Line")
        improvement = round((float(float(defaultVal - optimizedVal)/optimizedVal )*100),2)
        return improvement

    @staticmethod
    def improvementByFactor():
        #get the default optimization result
        defaultVal = ResultAnaylzer.getDefault("99%_Line")
        optimizedVal = ResultAnaylzer.getOptimized("99%_Line")
        improvement = round((float(defaultVal)/float(optimizedVal)),2)
        return improvement

    

