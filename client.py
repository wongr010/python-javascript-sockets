
#bitalino device simulator, simulates EMG sensor data that is sent to server which is forwarded to client.js for assessment
import sys
from twisted.internet import reactor
import random
from autobahn.twisted.websocket import WebSocketClientFactory, \
    WebSocketClientProtocol, \
    connectWS

import BITalino  # BITalino API
import numpy

def grab_EMG_ACC_data(device, reps, data):
	    """
	    # call the BITalino API
	    device = BITalino.BITalino()

	    import time

	    macAddress = "20:17:09:18:47:36"
	    SamplingRate = 1000
	    nFrames = 100  # number of samples to read
	    threshold = 500  # threshold defined to turn the led on
	    acquisitionTime = 20  # seconds

	    # connect do BITalino device
	    device.open(macAddress, SamplingRate=SamplingRate)
	    time.sleep(1)
	    """

	    # start acquisition on analog channel 0 (EMG) and channel 4 (ACC)
	    # device.start([0, 4])
	    
	    acquireLoop = 0
	    nFrames = 300  # number of samples to read
	    #while (acquireLoop != (acquisitionTime * SamplingRate)):
	    while (acquireLoop < reps):
	        # read samples
	        dataAcquired = device.read(nFrames)
	        # get EMG signal, ACC signal (nFrames samples)
	        EMG = dataAcquired[5, :]
	        ACC = dataAcquired[6, :]

	        # center the EMG/ACC signal baseline at zero, by subtracting its mean
	        # calculate the mean value of the absolute of the EMG/ACC signal
	        ECGvalue = numpy.mean(abs(EMG - numpy.mean(EMG)))
	        ACCvalue = numpy.mean(abs(ACC - numpy.mean(ACC)))

	        #print "ECGvalue: ", ECGvalue
	        #print "ACCvalue: ", ACCvalue

	        # put data into matrix
	        data[0][acquireLoop] = ECGvalue
	        data[1][acquireLoop] = ACCvalue

	        """
	        if value >= threshold:
	            # turn digital ports on
	            # device.trigger([1, 1, 1, 1])
	            # turn LED on [1,0,0,0], BUZ on [0,1,0,0]
	            LEDoutput = [1,0,0,0]
	            BUZoutput = [0,1,0,0]
	            device.trigger (LEDoutput)
	        else:
	            # turn digital ports off
	            device.trigger([0, 0, 0, 0])
	            """
	        #acquireLoop += nFrames
	        acquireLoop += 1

	    # stop acquisition
	    # device.stop()
	    # # diconnect device
	    # device.close()
	    


class BroadcastClientProtocol(WebSocketClientProtocol):

    """
    Simple client that connects to a WebSocket server, send a HELLO
    message every 2 seconds and print everything it receives.
    """

    def sendHello(self):
        reps = 1
    # Creates a list containing [reps] lists, each of [2] items, all set to 0
        w, h = reps, 2;
        data = [[0 for x in range(w)] for y in range(h)]
        grab_EMG_ACC_data(device, reps, data)
        print"EMG data: "
        print data[0]
        #ACC data
        print "\n ACC data: "
        print data[1]
        print "\n"
        emg_str=str(data[0][0])
        acc_str=str(data[1][0])
        self.sendMessage(emg_str.encode('utf8'))
        self.sendMessage(acc_str.encode('utf8'))
        reactor.callLater(2, self.sendHello)

    def onOpen(self):
        self.sendHello()

    def onMessage(self, payload, isBinary):
        if not isBinary:
            print"Text message received: {}".format(payload.decode('utf8'))


if __name__ == '__main__':

    if len(sys.argv) < 2:
        print"Need the WebSocket server address, i.e. ws://127.0.0.1:9000"
        sys.exit(1)

    device = BITalino.BITalino()

    #import time

    macAddress = "20:17:09:18:47:36"
    # macAddress = "00:12:12:31:11:04"
    SamplingRate = 1000
    #nSamples = 5000

    # Connect to bluetooth device and set Sampling Rate
    print "connecting..."
    device.open(macAddress, SamplingRate=SamplingRate)
    print "connected!"

    factory = WebSocketClientFactory(sys.argv[1])
    factory.protocol = BroadcastClientProtocol
    connectWS(factory)
    device.start([0, 4])
    reactor.run()