import subprocess
import sys

"""ReadCIDTone.py
a wrapper around minimodem with binary output turned on
to process demodulated CID bytes

an alternative since minimodem's callerid sdmf demodulation is not working for me
on files which have more than one callerid data burst in them, or on some other occasions for some reason
but it is demodulating the bytes themselves perfectly in Bell Type 202

based on specs provided at https://hkn.eecs.berkeley.edu/~drake/callsense/callerid.html
"""

class MessageType:
	MDMF = 128
	SDMF = 4

class MDMFParamTypes:
	DT = 1 #date/time
	number = 2 #phone number
	name = 7
	
class CIDLogger:
	byteStrings = []
	binaryPlacement = [1,2,4,8,16,32,64,128] #numbers are processed in the order they are defined.
						 #i.e, in the provided link, numbers are opposite order, reverse if this is case
	startBytes = [128, #MDMF format
		      4]  #SDMF format
	messageType = None
	startByteEncountered = False
	pType = None
	pCount = None
	pTypeCounter = 1
	byteStr = ''
	outputStr = ''
	dt = ''
	number = ''
	name = ''
	processed = []
	msgLen = None
	msgCounter = 0
	def __init__(self,
		     output):
		self.byteStrings = output.splitlines()
		self.ProcessData()
		self.PresentData()
	def BinStrToAsciiCode(self,
			      binStr):
		curPlace = 1
		num = 0
		for a in binStr:
			if a == '1':
				num += self.binaryPlacement[curPlace - 1]
			curPlace += 1
		return num  
	def formatDT(self,
		     dt):
		if len(dt) == 9:
			hr = int(dt[5:7])
			ampm = 'AM'
			if hr >= 13:
			      hr -= 12
			      ampm = 'PM'
			if hr <= 0:
			      return 'N/A'
			r = '%s/%s @ Time %s' + ampm
			return r % (dt[:3], dt[2:3], str(hr) + ':' + dt[7:9])
		else:
			return 'N/A'
	def ProcessData(self):
		for a in self.byteStrings:
			b = self.BinStrToAsciiCode(a)
			if not self.startByteEncountered:
				if b in self.startBytes:
				      self.startByteEncountered = True
				      self.messageType = b
				      self.messageCounter = 0
			elif self.messageType == MessageType.MDMF:
				if self.msgLen is None:
				      self.msgLen = b
				elif self.pType is None:
				      self.pType = b
				elif self.pCount is None:
				      self.pCount =  b
				if self.pType == MDMFParamTypes.DT:
				      if self.pTypeCounter <= self.pCount:
					      self.dt = self.dt + unichr(b)
					      self.pTypeCounter += 1
				      else:
					      self.pTypeCounter = 0
					      self.pType = b
					      self.pCount = None
				elif self.pType == MDMFParamTypes.number:
				      if self.pTypeCounter <= self.pCount:
					      self.number = self.number + unichr(b)
					      self.pTypeCounter += 1
				      else:
					      self.pTypeCounter = 0
					      self.pType = b
					      self.pCount = None
				elif self.pType == MDMFParamTypes.name:
				      if self.pTypeCounter <= self.pCount:
					      self.name = self.name + unichr(b)
					      self.pTypeCounter += 1
				if self.messageCounter == self.msgLen:      
					      self.checkSum = b
					      if not self.name:
						    self.name = 'N/A'
					      if not self.number:
						    self.number = 'N/A'
					      if not self.dt:
						    self.dt = 'N/A'
					      self.processed.append([self.formatDT(self.dt),self.name,self.number])
					      self.pTypeCounter = 0
					      self.dt = ''
					      self.name = ''
					      self.number = ''
					      self.pType = None
					      self.pCount = None
					      self.startByteEncountered = False
					      self.msgLen = None
					      self.messageCounter = 0
				self.messageCounter += 1
			elif self.messageType == MessageType.SDMF:
				if self.msgLen is None:
				      self.msgLen = b
				      self.pTypeCounter = 0
				else:
				      if self.pTypeCounter <= 8:#length of SDMF date
					      self.dt = self.dt + unichr(b)
				      elif self.pTypeCounter <= self.msgLen:
					      self.number = self.number + unichr(b)
				      else:
					      self.processed.append([self.formatDT(self.dt), 'N/A', self.number])
				self.pTypeCounter += 1
	def PresentData(self):
		for a in self.processed:
			print 'Date:', str(a[0])
			print 'name:', str(a[1]) 
			print 'number:', str(a[2]) 
			print '-----------------------------' 
			print ''
if __name__ == "__main__":
	if len(sys.argv) == 2:
		p = subprocess.Popen(['minimodem',
				      '--rx',
				      '--binary-output',
				      '1200',
				      '--ascii',
				      '-f',
				      sys.argv[1]], 
				      stderr= subprocess.PIPE,
				      stdout = subprocess.PIPE)
		out = p.communicate()[0]
		CIDLogger(out)

