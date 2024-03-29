#!/usr/bin/env python3

import websocket, json, argparse
import sys
#import os, time, logging

# CONSTANTS 
#
appName         = 'jellyroll'
appVersion      = 20210617.02

# EXAMPLES FROM API DOCS
#getPatternFileData = '{"cmd":"toCtlrGet", "get":[["patternFileData", "Legacy", "Red Yellow Green Blue"]]}'
#setZonePattern  = '{"cmd":"toCtlrSet","runPattern":{"file":"Christmas/Christmas Tree","data":"","id":"","state":1,"zoneName":["Zone", "Zone1"]}}'
#runPattern      = '{"cmd":"toCtlrSet","runPattern":{"file":””,"data":"{\"colors\":[<int>,<int>,<int>],\"spaceBetweenPixels\":<int>,\"effectBetweenPixels\":<effect>,\"type\":<type>,\"skip\":<int>,\"numOfLeds\":<int>,\"runData\":{\"speed\":<int>,\"brightness\":<int>,\"effect\":<effect>,\"effectValue\":<int>,\"rgbAdj\":[<int>,<int>,<int>]},\"direction\":<direction>}","id":"","state":<int>,"zoneName":[<zone>,<zone>]}}'

def wsOpen(controllerURL, headers):
    #print('Attempting connection to: %s........' % controllerURL, end = '')
    websocket.enableTrace(False)
    try:
        ws = websocket.create_connection(controllerURL, header=headers)
    except Exception as e:
        print('FAILURE: Failed to open connection to controller: %s' % controllerURL)
        print(e)
        sys.exit(1)
    #print('connection esablished.')
    
    return ws

def wsClose(ws, controllerURL):
    #print('Closing connection to: %s' % controllerURL)
    try:
        ws.close()
    except Exception as e:
        print('Failed to close connection: %s' % (e))
    return

def wsSendCommand(ws, cmd):
    try:
        #print('Sending command: %s    ....' % cmd, end = '')
        ws.send(cmd)
        #print('sent')
    except Exception as e:
        print('Failed to send command: %s' % (e))
        return

    try:
        #print('Listening for response.....' , end = '')
        wsResponse = ws.recv()
        #print("response recieved: %s" % wsResponse)
    except Exception as e:
        print('Failed to receive: %s' % (e))
        return

    return wsResponse

def jsonToListPatternFoldersAndNames(jsonObject):
    dataArray = []
    for value in jsonObject["patternFileList"]:
        dataToStore = value['folders']+'/'+value['name']
        dataArray.append(dataToStore)

    return dataArray

def testfunc(ws, keys):
    
    getPatternFileList = '{"cmd": "toCtlrGet", "get": [["patternFileList"]]}'

    patternData = json.loads(wsSendCommand(ws, getPatternFileList))

    dataArray = []
    for value in patternData["patternFileList"]:
        string = ''
        for key in keys:
            string += str(value[key])+'/'
        dataArray.append(string.replace('//','/'))
    return dataArray

def addZone(ws, zoneName):
    pass

def delZone(ws, zoneName):
    pass

def getZoneNames(ws):
    print('Getting zone list from controller..')

    getZoneNames = '{"cmd": "toCtlrGet", "get": [["zones"]]}'
    zoneData = json.loads(wsSendCommand(ws, getZoneNames))

    for zone in zoneData.get('zones').keys():
        print("    {}".format(zone))
    return

def getPatternNames(ws):
    #print('Getting pattern list from controller.....')

    getPatternFileList = '{"cmd": "toCtlrGet", "get": [["patternFileList"]]}'

    patternData = json.loads(wsSendCommand(ws, getPatternFileList))

    # patternData is a dict that contains
    #   k: cmd                v: fromCtlr
    #   k: patternFileList    v: [{'folders': 'folderName', 'name': 'patternName', 'readOnly': False}, {'folders': 'folderName', 'name': 'patternName', 'readOnly': True}, ..., ]

    patternFileList = jsonToListPatternFoldersAndNames(patternData)
    patternFileList.sort()

    #for pattern in patternFileList:
    #    print(pattern)

    return patternFileList

def getPatternFileData(ws, patternFileName):
    #print('Getting data for pattern %s ' % (patternFileName))

    patternFolder,patternName = patternFileName.split('/')

    getPatternFileCmd = '{"cmd":"toCtlrGet","get":[["patternFileData", "%s","%s"]] }' % (patternFolder, patternName)
    patternFileData = json.loads(wsSendCommand(ws, getPatternFileCmd))

    #print("%s = %s" % (patternFileName, patternFileData))
    return patternFileData

def getAllPatternFileData(ws):
    #print('Getting data for *ALL* patterns )

    patternFileList = getPatternNames(ws)

    for patternFileName in patternFileList:
        _patternFolder,_patternName = patternFileName.split('/')
        if _patternName != '':
            patternFileData = ''
            patternFileData = getPatternFileData(ws, patternFileName)
            print("%s = %s" % (patternFileName, patternFileData ))

    return

def setPattern(ws, patternName):
    # {"cmd":"toCtlrSet","runPattern":{"file":"","data":"{\"colors\":[255,0,0,255,255,255,0,0,255],\"spaceBetweenPixels\":10,\"effectBetweenPixels\":\"No ColorTransform\",\"type\":\"Multi-Paint\",\"skip\":1,\"numOfLeds\":6,\"runData\":{\"speed\":15,\"brightness\":100,\"effect\":\"NoEffect\",\"effectValue\":0,\"rgbAdj\":[100,100,100]},\"direction\":\"Center\"}","id":"","state":1,"zoneName":["Zone","Zone1"]}}
    #curPatternData = getPatternFileData(ws, patternFileName)
    #
    #
    # newPaternData = swap values as appropriate
    # wsSendCommand(ws, newPatternData)
    pass

def runPattern(ws, patternName, zoneName):
    # {"cmd":"toCtlrSet","runPattern":{"file":"<folderName>/<patternName>","data":"","id":"","state":1,"zoneName":[]}}
    # most likley a clone of setZonePattern
    #
    pass

def addPattern(ws, patternName):
    pass

def delPattern(ws, patternName):
    pass

def setZoneOnOff(ws, zoneName, zoneOnOff):
    print('Turning zone %s %s' % (zoneName, zoneOnOff))

    zoneOnOffCmd = '{"cmd":"toCtlrSet","runPattern":{"file":"","data":"","id":"","state":%s,"zoneName":["%s"]}}' % (zoneOnOff, zoneName)
    zoneOnOffResult = json.loads(wsSendCommand(ws, zoneOnOffCmd))

    return zoneOnOffResult

def checkPatternName(ws, patternName):
    # need to do checking of a patternName before sending. Sending bad name locks up system.
    pass

def setZonePattern(ws, zoneName, patternName):
    # have to include  state un-quoted
    zonePatternCmd = '{"cmd":"toCtlrSet","runPattern":{"file":"%s","data":"","id":"","state":1,"zoneName":["%s"]}}' % (patternName, zoneName)
    #print('Zone command is: %s' % zonePatternCmd)
    zonePatternResult = json.loads(wsSendCommand(ws, zonePatternCmd))
    print('Zone response is: %s' % zonePatternResult)

    return zonePatternResult

def setAllZones(ws, zoneOnOffCmd, patternName):
    # do something (on/off) or set pattern to all zones
    pass


def setZoneBrightness(ws, zoneName, zoneBrightnessLevel):
    # have to get the current running pattern data
    # replace the brightness field
    # then send the pattern back

    zoneBrightnessCmd = '{"cmd":"toCtlrSet","runPattern":{"file":"%s","data":"","id":"","state":'',"zoneName":["%s"]}}' % (patternName, zoneName)
    zoneBrightnessResult = json.loads(wsSendCommand(ws, zoneBrightnessCmd))

    return zoneBrightnessResult

def main(args): 
    controllerURL   = 'ws://%s:%s/ws/' % (args.controllerIP, args.controllerPort)
    headers         = {'user-agent': '%s (%s)' % (appName, appVersion)}

    if "getZoneNames" in sys.argv:
        #print("Found getZoneNames in arguments - attempting to get list of Zones")
        ws = wsOpen(controllerURL, headers)
        zoneNames = getZoneNames(ws)
        
    elif "getPatternNames" in sys.argv:
        #print("Found getPatterns in arguments - attempting to get list of Patterns")
        ws = wsOpen(controllerURL, headers)
        patternFileList = getPatternNames(ws)
        #keys = ['folders', 'name']
        #patternFileList = testfunc(ws, keys)
        print(patternFileList)

    elif "setZoneOnOff" in sys.argv:
        #print("Found setZoneOnOff in arguments - attempting to control a zone.")
        ws = wsOpen(controllerURL, headers)
        zoneName        = args.zoneName
        zoneOnOff       = args.zoneOnOff
        setZoneOnOff(ws, zoneName, zoneOnOff)

    elif "setZonePattern" in sys.argv:
        print("Found setZonePattern in arguments - attempting to control a zone.")
        ws = wsOpen(controllerURL, headers)
        zoneName        = args.zoneName
        patternName     = args.patternName
        setZonePatternResult = setZonePattern(ws, zoneName, patternName)
        #print(setZonePatternResult)


    
    elif "getPatternFileData" in sys.argv:
        #print("Found getPatternFileData in arguments - attempting get details of a pattern file.")
        ws = wsOpen(controllerURL, headers)
        patternFileName     = args.patternName
        patternFileData     = getPatternFileData(ws, patternFileName)

    elif "getAllPatternFileData" in sys.argv:
        #print("Found getPatternFileData in arguments - attempting get details of a pattern file.")
        ws = wsOpen(controllerURL, headers)
        allPatternFileData     = getAllPatternFileData(ws)

    else:
        print("NO COMMANDS FOUND - DOING NOTHING")
        sys.exit(1)

    wsClose(ws, controllerURL)
    sys.exit(0)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='jellyroll.py: Send commands to JellyFish Lighting controller')
    parser.add_argument('-c', '--controllerIP', type=str, required=True, help='hostname or IP address of JellyFish controller')
    parser.add_argument('-p', '--controllerPort', type=str, required=False, default='9000', help='port number that controller is listening on. Typically 9000')
    parser.add_argument('-v', '--verbose', type=bool, required=False, default=False, help='enable verbose logging')

    subparsers = parser.add_subparsers(title='COMMANDS', description='List of sub commands that can be run - each has thier own required options')
    parser_setZoneOnOff = subparsers.add_parser('setZoneOnOff')
    parser_setZoneOnOff.add_argument('-z', '--zoneName', type=str, required=True, default=argparse.SUPPRESS, help='Name of Zone to control')
    parser_setZoneOnOff.add_argument('-o', '--zoneOnOff', type=str, required=False, default=argparse.SUPPRESS, help='turn Zone on (1) or off (0)')

    parser_setZonePattern = subparsers.add_parser('setZonePattern')
    parser_setZonePattern.add_argument('-z', '--zoneName', type=str, required=True, default=argparse.SUPPRESS, help='Name of Zone to control')
    parser_setZonePattern.add_argument('-t', '--patternName', type=str, required=False, default='', help='name of the pattern (format: Folder/Pattern Name)') 

    parser_getPatternFileData = subparsers.add_parser('getPatternFileData')
    parser_getPatternFileData.add_argument('-t', '--patternName', type=str, required=False, help='name of the pattern (format: Folder/Pattern Name)') 

    parser_getZone = subparsers.add_parser('getZoneNames')
    parser_getPatterns = subparsers.add_parser('getPatternNames')
    parser_getAllPatternFileData = subparsers.add_parser('getAllPatternFileData')
    


    try:
        sys.exit(main(parser.parse_args()))
    except (SystemExit, KeyboardInterrupt): 
        raise 
    except Exception as e: 
        print("Error: " + str(e))
