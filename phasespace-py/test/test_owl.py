import os
import sys
import owl

if __name__ == "__main__":
    PHASESPACE_IP = os.environ["PHASESPACE_IP"]
    
    # opens a socket and configures the communication channels to pass data between the OWL server and client; this
    # function will block until there is a connection or an error; returns the passed flags if OK
    if (owl.init(PHASESPACE_IP, 0) < 0):
        print("Can't initialize the communication with OWL server: {}".format(owl.getError()))
        owl.done()
        sys.exit()

    # initializes a point tracker:
    #  - CREATE: tells the system to create a tracker
    #  - POINT_TRACKER: specifies the creation of a point tracker
    tracker = 0
    owl.trackeri(tracker, owl.CREATE, owl.POINT_TRACKER);

    # creates the marker structures, each with the proper id:
    # - MARKER Macro: builds a marker id out of a tracker id and marker index
    # - SET_LED: the following 'i' is an integer representing the LED ID of the marker
    init_marker_count = 72
    markers = [owl.Marker()] * init_marker_count
    for i in range(init_marker_count):
        owl.markeri(owl.MARKER(tracker, i), owl.SET_LED, i);

    # checking the status will block until all commands are processed and any errors are sent to the client
    if (not owl.getStatus()):
        print("Initialization generic error: {}".format(owl.getError()))
        owl.done()
        sys.exit()
    
    # enables the tracker (it has to be disabled when the markers have to be added)
    owl.tracker(tracker, owl.ENABLE)
    
    # report all values in meters rather than millimeters
    owl.scale(0.001)
    
    # sets frequency with default maximum value (OWL_MAX_FREQUENCY = 480 Hz):
    # - FREQUENCY: specifies the rate at which the server streams data
    owl.setFloat(owl.FREQUENCY, owl.MAX_FREQUENCY);
    # enables the streaming of data
    owl.setInteger(owl.STREAMING, owl.ENABLE);
    
    num_readings = 0
    while (num_readings < 100):
        # queries the server for new markers data and returns the number of current active markers (0 means old data)
        num_markers = owl.getMarkers((owl.Marker*len(markers))(*markers), init_marker_count);
        if (owl.getError() != owl.NO_ERROR):
            print("Error while reading markers' positions: {}".format(owl.getError()))
            owl.done()
            sys.exit()
        
        # waits for available data
        if (num_markers == 0):
            continue
        
        num_readings += 1
        
        print("Found {} markers.".format(num_markers))
        for i in range(num_markers):
#            if (markers[i].cond > 0):
                print("Marker {} = ({}, {}, {}) (cond = {})".format(i, markers[i].x, markers[i].y, markers[i].z, markers[i].cond))
    
    owl.done()
