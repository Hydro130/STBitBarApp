# -*- coding: utf-8 -*-
import sys
import json
import subprocess
from subprocess import check_output

##########################################################################################
## USER INPUT ############################################################################
## Enter your SmartApp URL and Secret below ##############################################
##########################################################################################

smartAppURL = "https://graph.api.smartthings.com/api/smartapps/installations/[Your SmartAppID]"
secret = "Your Secret Goes Here"

# Use images for switch status' (green/red dot) instead of emojis
useImages = True

##########################################################################################
## END USER INPUT ########################################################################
##########################################################################################


#Set URLs
statusURL = smartAppURL + "GetStatus/"
switchURL = smartAppURL + "ToggleSwitch/?id="
levelURL =  smartAppURL + "SetLevel/?id="

# Set the callback script for switch/level commands from parameters
callbackScript = sys.argv[1]

# Make the call the to the API and retrive JSON data
try:
   output = check_output(['curl', '-s', statusURL, '-H', 'Authorization: Bearer ' + secret])                     
except subprocess.CalledProcessError as grepexc:                                                                                                   
    print "No Connection"
    print "---"
    print "Please check connection and try again"
    print "Debug information: Error code ",grepexc.returncode, grepexc.output
    raise SystemExit(0)

# Parse the JSON data
j = json.loads(output)

# Get the sensor arrays from the JSON data
temps =       j['Temp Sensors']
contacts =    j['Contact Sensors']
switches =    j['Switches']
mainDisplay = j['MainDisplay']

# Print the main display
print mainDisplay[0]['name'],':',mainDisplay[0]['value']

# Find the max length sensor so values are lined up correctly
maxLength = 0
for sensor in temps:
	if len(sensor['name']) > maxLength:
		maxLength = len(sensor['name'])
		
for sensor in contacts:
	if len(sensor['name']) > maxLength:
		maxLength = len(sensor['name'])	
		
for sensor in switches:
	if len(sensor['name']) > maxLength:
		maxLength = len(sensor['name'])	
# Increment maxLength by one since contact sensor icon needs to be pulled back a little
maxLength += 1

# Output the seperation '---' between status bar items and menu items 
print '---'

# Begin outputting sensor data

# Output Temp Sensors
if len(temps) > 0: print "Temp Sensors|font=Helvetica-Bold color=black size=15"
colorSwitch = False
for sensor in temps:
	currentLength = len(sensor['name'])
	extraLength = maxLength - currentLength
	whiteSpace = ''
	for x in range(0, extraLength): whiteSpace += ' '
	colorText = ''
	currentValue = sensor['value']
	if type(currentValue) is float:
		currentValue = int(currentValue)
		
	if colorSwitch == True: colorText = 'color=#333333'
	if colorSwitch == False: colorText = 'color=#666666'
	print sensor['name'], whiteSpace, currentValue, '|font=Menlo', colorText
	colorSwitch = not colorSwitch	

#Output Contact Sensors	
if len(contacts) > 0: print "Contact Sensors|font=Helvetica-Bold color=black"
for sensor in contacts:
	currentLength = len(sensor['name'])
	extraLength = maxLength - currentLength
	whiteSpace = ''
	for x in range(0, extraLength - 1): whiteSpace += ' '
	sym = ''
	if sensor['value'] == 'closed':
		sym = '⇢⇠'
	else:
		sym = '⇠⇢'
	if colorSwitch == True: colorText = 'color=#333333'
	if colorSwitch == False: colorText = 'color=#666666'
	print sensor['name'], whiteSpace, sym , '|font=Menlo', colorText
	colorSwitch = not colorSwitch
	
# Set base64 images for status green/red
greenImage = "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"
redImage = "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"

#Output Switches	
if len(switches) > 0: print "Switches|font=Helvetica-Bold color=black"
for sensor in switches:
	currentLength = len(sensor['name'])
	extraLength = maxLength - currentLength
	whiteSpace = ''
	img = ''
	for x in range(0, extraLength): whiteSpace += ' '
	if sensor['value'] == 'on':
		sym = '🔛'
		img = greenImage
	else:
		sym = '🔴'
		img = redImage
	currentSwitchURL = switchURL + sensor['id']
	if useImages is True:
		print sensor['name'], '|font=Menlo bash=',callbackScript,' param1=request param2=',currentSwitchURL,' param3=',secret,' terminal=false refresh=true image=',img
	else:
		print sensor['name'], whiteSpace, sym , '|font=Menlo bash=',callbackScript,' param1=request param2=',currentSwitchURL,' param3=',secret,' terminal=false refresh=true'
	if sensor['isDimmer'] is True:
		print '-- Set Dimmer Level|size=9'
		currentLevel = 10
		while True:
			currentLevelURL = levelURL + sensor['id'] + '&level=' + str(currentLevel)
			print '-- ',currentLevel,'%| bash=',callbackScript,' param1=request param2=',currentLevelURL,' param3=',secret,' terminal=false refresh=true'
			if currentLevel is 100:
				break
			currentLevel += 10