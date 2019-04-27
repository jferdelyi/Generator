#!/usr/bin/env python
import os
import signal
import sys

# Signal handler for ctrl+c
def signalHandler(sig, frame):
    os.system("pkill flask")
    os.system("pkill node")
    os.system("pkill 'ng serve'")
    print("App closed")
    sys.exit(0)

# Bind signal SIGINT
signal.signal(signal.SIGINT, signalHandler)

# Start server
os.system("./server.py &")

# Start client
os.system("./client.py &")

# Wait for ctrl+c
signal.pause()

