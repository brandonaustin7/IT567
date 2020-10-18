import sys
import argparse
import socket
import subprocess
from datetime import datetime
import fpdf
import pyfiglet

#Clear Screen
subprocess.call('clear', shell=True)


#Do cool intro thing
banner = pyfiglet.figlet_format("THE BEST PORT SCANNER")
print(banner)


#Create the PDF
pdf = fpdf.FPDF(format='letter')
pdf.add_page()
pdf.set_font("Arial", size=14)


#start the while loop
keepGoing = 'y'
while keepGoing == 'y':

#This gets the host ip address
	ipAddress = input("Enter the IP Address you would like to scan: ")
	serverIpAddress = socket.gethostbyname(ipAddress)
	print('You have chosen to scan ' + ipAddress + '\n')

#This is where you choose the ports
	lowPort = int(input("What is the lowest number port you would like to scan: "))
	highPort = int(input("What is the highest number port you would like to scan: "))
	theStartTime = datetime.now() #time starts to see how long it takes
	print ("Now scanning port ranges ",lowPort, "to ", highPort, '\n')
	print ("Here are the TCP Ports:")
	pdf.write(5,"The host is " + ipAddress)
	pdf.write(5,"\nThe port range is " + str(lowPort) + " - " + str(highPort) + "\n")
	pdf.write(5,"\nThese are the open TCP ports:")
#This is where the actual scanning starts
	try:
		for port in range(lowPort,highPort):
			theSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
			result = theSocket.connect_ex((serverIpAddress, port))
			if result == 0:
				print ("Port {}:		Open".format(port))
				pdf.write(5,"\nPort {}: 		Open".format(port))
			theSocket.close()
	except KeyboardInterrupt:
		print ("\nYou have canceled the port scanning")
		sys.exit()
	except socket.gaierror:
		print ("\nCan't resolve hostname.  Quitting Program")
		sys.exit()
	except socket.error:
		print ("\nCan't connect to server")
		sys.exit()

#Try to do TCP
	wantUDP = input("\nDo you want to scan for those UDP ports as well y/n?: ")
	if wantUDP == 'y':
		print ("\nHere are the UDP Ports:")
		pdf.write(5,"\n\nThese are the open UDP Ports:")
		try:
			for portTCP in range(lowPort,highPort):
				TCPSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
				TCPResult = TCPSocket.connect_ex((serverIpAddress, portTCP))
				if TCPResult == 0:
					print ("Port {}:		Open".format(portTCP))
					pdf.write(5,"\nPort {}: 		Open".format(portTCP))
		except KeyboardInterrupt:
			print ("\nYou have canceled the port scanning")
			sys.exit()
#This is where we print the time
	pdf.write(5,"\n\n\n---------------------------------------------\n\n")
	theEndTime = datetime.now()
	timeToScan = theEndTime - theStartTime
	print ("\nScanning complete.  This took the program", timeToScan)
	keepGoing = input("\nWould you like to scan another host y/n?: ")

print ("\nThanks for using this program.  Have a great day!")
pdf.write(5,"Thanks for using this program.  Have a great day!")
pdf.output("myResults.pdf")
