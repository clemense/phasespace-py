import ctypes

lib = ctypes.CDLL('libowlsock.so')


### the different structs

class Marker(ctypes.Structure):
    _fields_ = [("id", ctypes.c_int),
                ("frame", ctypes.c_int),
                ("x", ctypes.c_float),
                ("y", ctypes.c_float),
                ("z", ctypes.c_float),
                ("cond", ctypes.c_float),
                ("flag", ctypes.c_uint)]

class Rigid(ctypes.Structure):
    _fields_ = [("id", ctypes.c_int),
                ("frame", ctypes.c_int),
                ("pose", ctypes.c_float * 7),
                ("cond", ctypes.c_float),
                ("flag", ctypes.c_uint)]

class Camera(ctypes.Structure):
    _fields_ = [("id", ctypes.c_int),
                ("pose", ctypes.c_float * 7),
                ("cond", ctypes.c_float),
                ("flag", ctypes.c_uint)]

class Event(ctypes.Structure):
    _fields_ = [("type", ctypes.c_int),
                ("frame", ctypes.c_int)]


### Constants

MAX_FREQUENCY       = 960.0

# Errors
NO_ERROR            = 0x0
INVALID_VALUE       = 0x0020
INVALID_ENUM        = 0x0021
INVALID_OPERATION   = 0x0022

# Common Events
DONE                = 0x0002

# Common flags
CREATE              = 0x0100
DESTROY             = 0x0101
ENABLE              = 0x0102
DISABLE             = 0x0103

# Init flags
SLAVE               = 0x0001  # socket only
FILE                = 0x0002  # socket only
ASYNC               = 0x0008  # socket only
POSTPROCESS         = 0x0010
MODE1               = 0x0100
MODE2               = 0x0200
MODE3               = 0x0300
MODE4               = 0x0400
LASER               = 0x0A00
CALIB               = 0x0C00
DIAGNOSTIC          = 0x0D00
CALIBPLANAR         = 0x0F00

# Sets
FREQUENCY           = 0x0200
STREAMING           = 0x0201  # socket only
INTERPOLATION       = 0x0202
BROADCAST           = 0x0203  # socket only
EVENTS              = 0x020F  # socket only
BUTTONS             = 0x0210
MARKERS             = 0x0211
RIGIDS              = 0x0212
COMMDATA            = 0x0220
TIMESTAMP           = 0x0221
PLANES              = 0x02A0
DETECTORS           = 0x02A1
IMAGES              = 0x02A2

CAMERAS             = 0x02A4

FRAME_BUFFER_SIZE   = 0x02B0  # socket only

MARKER_STATS        = 0x02D0
CAMERA_STATS        = 0x02D1
MARKER_COVARIANCE   = 0x02D5

HW_CONFIG           = 0x02F0

TRANSFORM           = 0xC200  # camera transformation

# Trackers
POINT_TRACKER       = 0x0300
RIGID_TRACKER       = 0x0301

# planar tracker (may be temporary)
PLANAR_TRACKER      = 0x030A

SET_FILTER          = 0x0310

# undocumented freatures
# use at your own risk
FEATURE0            = 0x03F0 # optical
FEATURE1            = 0x03F1 # offsets
FEATURE2            = 0x03F2 # projection
FEATURE3            = 0x03F3 # predicted
FEATURE4            = 0x03F4 # valid min
FEATURE5            = 0x03F5 # query min
FEATURE6            = 0x03F6 # storedepth
FEATURE7            = 0x03F7 # 
FEATURE8            = 0x03F8 # rejection
FEATURE9            = 0x03F9 # filtering
FEATURE10           = 0x03FA # window size
FEATURE11           = 0x03FB # LS cutoff
FEATURE12           = 0x03FC # off-fill
FEATURE_LAST        = 0x03FD # last feature

# calibration only
CALIB_TRACKER       = 0x0C01
CALIB_RESET         = 0x0C10
CALIB_LOAD          = 0x0C11
CALIB_SAVE          = 0x0C12
CALIBRATE           = 0x0C13
RECALIBRATE         = 0x0C14
CAPTURE_RESET       = 0x0C20
CAPTURE_START       = 0x0C21
CAPTURE_STOP        = 0x0C22
CALIB_ACTIVE        = 0x0C30

# planar calib tracker (may be temporary)
CALIBPL_TRACKER     = 0x0CA1

# Markers
SET_LED             = 0x0400
SET_POSITION        = 0x0401
CLEAR_MARKER        = 0x0402

# Gets 
VERSION             = 0x0500
FRAME_NUMBER        = 0x0510
STATUS_STRING       = 0x0520
CUSTOM_STRING       = 0x05F0

# calibration only
CALIB_STATUS        = 0x0C51
CALIB_ERROR         = 0x0C52



### Macros

#define MARKER(tracker, index)  (((tracker)<<12)|(index))
def MARKER(tracker, index):
	return (tracker << 12) | index

#define INDEX(id)   ((id)&0x0fff)
def INDEX(id):
	return id & 0x0fff

#define TRACKER(id) ((id)>>12)
def TRACKER(id):
	return id >> 12



### initialization 

# OWLAPI int owlInit(CTX const char *server, int flags);
init = lib.owlInit
init.restype = ctypes.c_int
init.argtypes = [ctypes.c_char_p, ctypes.c_int]

# OWLAPI void owlDone(CTXVOID);
done = lib.owlDone

### client -> server 

# OWLAPI void owlSetFloat(CTX OWLenum pname, float param);
setFloat = lib.owlSetFloat
setFloat.argtypes = [ctypes.c_uint, ctypes.c_float]

# OWLAPI void owlSetInteger(CTX OWLenum pname, int param);
setInteger = lib.owlSetInteger
setInteger.argtypes = [ctypes.c_uint, ctypes.c_int]

# OWLAPI void owlSetFloatv(CTX OWLenum pname, const float *param);
setFloatv = lib.owlSetFloatv
setFloatv.argtypes = [ctypes.c_uint, ctypes.POINTER(ctypes.c_float)]

# OWLAPI void owlSetIntegerv(CTX OWLenum pname, const int *param);
setIntegerv = lib.owlSetIntegerv
setIntegerv.argtypes = [ctypes.c_uint, ctypes.POINTER(ctypes.c_int)]

# OWLAPI void owlSetString(CTX OWLenum pname, const char *str);
setString = lib.owlSetString
setString.argtypes = [ctypes.c_uint, ctypes.c_char_p]

# 'tracker' is the tracker id
# OWLAPI void owlTracker(CTX int tracker, OWLenum pname);
tracker = lib.owlTracker
tracker.argtypes = [ctypes.c_int, ctypes.c_uint]

# OWLAPI void owlTrackerf(CTX int tracker, OWLenum pname, float param);
trackerf = lib.owlTrackerf
trackerf.argtypes = [ctypes.c_int, ctypes.c_uint, ctypes.c_float]

# OWLAPI void owlTrackeri(CTX int tracker, OWLenum pname, int param);
trackeri = lib.owlTrackeri
trackeri.argtypes = [ctypes.c_int, ctypes.c_uint, ctypes.c_int]

# OWLAPI void owlTrackerfv(CTX int tracker, OWLenum pname, const float *param);
trackerfv = lib.owlTrackerfv
trackerfv.argtypes = [ctypes.c_int, ctypes.c_uint, ctypes.POINTER(ctypes.c_float)]

# OWLAPI void owlTrackeriv(CTX int tracker, OWLenum pname, const int *param);
trackeriv = lib.owlTrackeriv
trackeriv.argtypes = [ctypes.c_int, ctypes.c_uint, ctypes.POINTER(ctypes.c_int)]

# 'marker' is MARKER(tracker, index)
# OWLAPI void owlMarker(CTX int marker, OWLenum pname);
marker = lib.owlMarker
marker.argtypes = [ctypes.c_int, ctypes.c_uint]

# OWLAPI void owlMarkerf(CTX int marker, OWLenum pname, float param);
markerf = lib.owlMarkerf
markerf.argtypes = [ctypes.c_int, ctypes.c_uint, ctypes.c_float]

# OWLAPI void owlMarkeri(CTX int marker, OWLenum pname, int param);
markeri = lib.owlMarkeri
markeri.argtypes = [ctypes.c_int, ctypes.c_uint]

# OWLAPI void owlMarkerfv(CTX int marker, OWLenum pname, const float *param);
markerfv = lib.owlMarkerfv
markerfv.argtypes = [ctypes.c_int, ctypes.c_uint, ctypes.POINTER(ctypes.c_float)]

# OWLAPI void owlMarkeriv(CTX int marker, OWLenum pname, const int *param);
markeriv = lib.owlTrackeriv
markeriv.argtypes = [ctypes.c_int, ctypes.c_uint, ctypes.POINTER(ctypes.c_int)]


### client

# OWLAPI void owlScale(CTX float scale);
scale = lib.owlScale
scale.argtypes = [ctypes.c_float]

# pose: pos, rot -- [x y z], [s x y z]
# OWLAPI void owlLoadPose(CTX const float *pose);
loadPose = lib.owlLoadPose
loadPose.argtypes = [ctypes.POINTER(ctypes.c_float)]


### server -> client

# OWLAPI int owlGetStatus(CTXVOID);
getStatus = lib.owlGetStatus
getStatus.restype = ctypes.c_int

# OWLAPI int owlGetError(CTXVOID);
getError = lib.owlGetError
getError.restype = ctypes.c_int

# OWLAPI OWLEvent owlPeekEvent(CTXVOID);
peekEvent = lib.owlPeekEvent
peekEvent.restype = Event

# OWLAPI OWLEvent owlGetEvent(CTXVOID);
getEvent = lib.owlGetEvent
getEvent.restype = Event

# OWLAPI int owlGetMarkers(CTX OWLMarker *markers, uint_t count);
getMarkers = lib.owlGetMarkers
getMarkers.restype = ctypes.c_int
getMarkers.argtypes = [ctypes.POINTER(Marker), ctypes.c_uint]

# OWLAPI int owlGetRigids(CTX OWLRigid *rigid, uint_t count);
getRigids = lib.owlGetRigids
getRigids.restype = ctypes.c_int
getRigids.argtypes = [ctypes.POINTER(Rigid), ctypes.c_uint]

# OWLAPI int owlGetCameras(CTX OWLCamera *cameras, uint_t count);
getCameras = lib.owlGetCameras
getCameras.restype = ctypes.c_int
getCameras.argtypes = [ctypes.POINTER(Camera), ctypes.c_uint]

# OWLAPI int owlGetFloatv(CTX OWLenum pname, float *param);
getFloatv = lib.owlGetFloatv
getFloatv.restype = ctypes.c_int
getFloatv.argtypes = [ctypes.c_uint, ctypes.POINTER(ctypes.c_float)]

# OWLAPI int owlGetIntegerv(CTX OWLenum pname, int *param);
getIntegerv = lib.owlGetIntegerv
getIntegerv.restype = ctypes.c_int
getIntegerv.argtypes = [ctypes.c_uint, ctypes.POINTER(ctypes.c_int)]

# OWLAPI int owlGetString(CTX OWLenum pname, char *str);
getString = lib.owlGetString
getString.restype = ctypes.c_int
getString.argtypes = [ctypes.c_uint, ctypes.c_char_p]
