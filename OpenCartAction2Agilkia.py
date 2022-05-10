'''
Created on May 28th 2021
This script takes a txt file, storing a log of the e-shop
and generates an agilkia json file and several statistics about the input file.
The traces of the output file are grouped according to the sessionIDs of the input file.
If its argument is a directory, it processes all .txt files of the directory.
The resulting file is stored in the same directory as the input file. It 
has the suffix ".AgilkiaTraces.json"

Example:

OpenCartAction2Agilkia.py traces\20210315_OpenCartAction.txt

@author: ledru
License: MIT
'''
import os
import sys
from pathlib import Path
import agilkia
import json
from datetime import  datetime

def main():
    
   dir2Xplore=GetFile2Xplore()
   Convert_dir2jsonFiles(dir2Xplore)

#Returns the first argument or '.' if the first argument is missing
def GetFile2Xplore():
    result = "."
    if (len(sys.argv) > 1) :
        result = sys.argv[1]
    return result

# Returns a list of  Files, with suffix as their suffix, located at filePath
# filePath maybe a directory or a file
# suffix is usually of the form ".abc"
def GetListOfSuffixFiles(filePath,suffix):
    if os.path.isfile(filePath)  and filePath.endswith(suffix):
        #The parameter corresponds to a single  file whose name ends with suffix
        result=[filePath]
    elif os.path.isdir(filePath):
        # if filePath is a directory, retrieve only the suffix files
        listOfFiles=os.listdir(filePath)
        result=[]
        for ff in listOfFiles:
            txtpath = os.path.join(filePath,ff)
            if os.path.isfile(txtpath) and ff.endswith(suffix):
                result = result+[txtpath]
    else:
        result = []
    if result==[]:
        print('No '+suffix+' file at location: '+filePath)
    return result

def Convert_dir2jsonFiles(dir2Xplore):
    for txtFile in  GetListOfSuffixFiles(dir2Xplore,".txt"):
        ProcessInputFile(txtFile)
        
def ProcessInputFile(txtFile):
    f=open(txtFile,'r')
    absDirPath = os.path.abspath(os.path.dirname(txtFile))
    (shortFileName, fileExtension) = os.path.splitext(os.path.basename(txtFile))
    outputFileName = os.path.join(absDirPath,shortFileName+".AgilkiaTraces.json") #the output file is the input file with suffix .agilkiaTraces.json
    myTrace= agilkia.Trace([])
    for line in f:
        (timestamp,jsonDict)=XtractTimeStampAndDict(line)
        evt = createEvt(timestamp,jsonDict)
        myTrace.append(evt)
    tr_set = agilkia.TraceSet([])
    tr_set.append(myTrace)
    # at this stage, the trace set stores a single trace
    # create traces based on sessionID
    traceset2 = tr_set.with_traces_grouped_by("sessionID", property=True)
    print("Statistics about file: "+outputFileName)
    data = traceset2.get_trace_data(method="action_counts")
    print(data.sum().sort_values())
    print("Number of events: "+str(len(myTrace)))
    print("Number of traces: "+str(len(traceset2.traces)))
    traceset2.save_to_json(Path(outputFileName))

        
# analyses the contents of a line of the input file and returns a dictionary and a timestamp               
def XtractTimeStampAndDict(line):                
# for each line, we extract the timeStamp and a dictionary with all other 
# parameteres of the event.
    endOfTimeStamp = line.find(' - {')
    if (endOfTimeStamp != -1):
        evtDate=line[:10]
        evtTime=line[11:endOfTimeStamp]
        if (evtTime[1] == ':') :
        #transforms time of the form H:MM:SS info 0H:MM:SS
        #it supports the case where there are milliseconds 
            evtTime = "0"+evtTime
        timestamp = datetime.fromisoformat(evtDate+" "+evtTime)
        # print(timestamp)
        jsonDictString = line[endOfTimeStamp+3:len(line)-1]
        # print(jsonDictString+"**")
        jsonDict = json.loads(jsonDictString)
    else :
        print("Invalid format! No time stamp in this line : "+line)
    return (timestamp,jsonDict)     

#returns an event build from the information in the jsonDict, and the timestamp
def createEvt(timeStamp,jsonDict) :
    action = jsonDict["function"]
    inputs = {'param' : jsonDict["data"]} 
    outputs = {'status':jsonDict["httpResponseCode"]}
    others = {
        'timestamp' : timeStamp,
        'sessionID': jsonDict["sessionID"],
        'customerID' : jsonDict["customerID"],
        'controller' : jsonDict["controller"]
        # maybe controller and customerID should be added to the inputs
        }
    evt = agilkia.Event(action, inputs, outputs, others)
    return evt
  
      
#Main program
if __name__ == '__main__' :
    main()
