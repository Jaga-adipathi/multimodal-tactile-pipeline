import ctypes
import os
import time
import socket
# Please kindly modify the IP and Port
UDP_IP = "12x.x.x.x"
UDP_PORT = 5xxx
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
# Add the path
current_folder = os.path.dirname(os.path.abspath(__file__))
DLL_PATH = os.path.join(current_folder, "fglove.dll")
fglove = ctypes.CDLL(DLL_PATH, winmode=0)

fdOpen = getattr(fglove, "?fdOpen@@YAPAUfdGlove@@PAD@Z")
fdGetSensorScaledAll = getattr(fglove, "?fdGetSensorScaledAll@@YAXPAUfdGlove@@PAM@Z")
fdOpen.restype = ctypes.c_void_p
fdGetSensorScaledAll.argtypes = [ctypes.c_void_p, ctypes.POINTER(ctypes.c_float)]

pGlove = None
for port in [b"USB0", b"USB1", b"USB2", b"COM3", b"COM4"]:
    pGlove = fdOpen(port)
    if pGlove: 
        print(f"[SUCCESS] 5DT Glove connected on {port.decode()}")
        break

glove_data = (ctypes.c_float * 14)()

print(f"Transmitting 5DT Finger Data to Port {UDP_PORT}...")
try:
    while True:
        if pGlove:
            fdGetSensorScaledAll(pGlove, glove_data)
            msg = f"{glove_data[0]:.3f},{glove_data[3]:.3f},{glove_data[6]:.3f},{glove_data[9]:.3f},{glove_data[12]:.3f}"
            sock.sendto(msg.encode(), (UDP_IP, UDP_PORT))
        time.sleep(0.02)
except KeyboardInterrupt:
    pass
finally:
    if pGlove: getattr(fglove, "?fdClose@@YAHPAUfdGlove@@@Z")(pGlove)
